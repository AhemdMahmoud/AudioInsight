from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from utils import load_audio, save_transcript
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from gliner import GLiNER
import spacy
from langdetect import detect, detect_langs
import re
from Audio import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import torch
from Audio import pipe as transcription_pipe  # Import the initialized pipeline
from sumerizer import summarize_text  # Add this import at the top
from translator import translate_text  # Add this import at the top

# Initialize Flask app and configurations
app = Flask(__name__, 
    template_folder='templates',
    static_folder='static'
)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Add this after the Flask initialization
app.config['AUDIO_FOLDER'] = 'static/audio'
os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)

# Initialize GLiNER
highlighter = GLiNER.from_pretrained("urchade/gliner_multi-v2.1")
nlp = spacy.blank("ar")

@app.route('/')
def index():
    return render_template('index.html')

# Add this helper function after the imports
def detect_language_robustly(text):
    if not text:
        return 'en'  # default to English if no text
        
    # Clean the text
    text = re.sub(r'[0-9\s\n\r\t]+', ' ', text).strip()
    
    if not text:
        return 'en'
    
    try:
        # Get all possible languages with probabilities
        langs = detect_langs(text)
        
        # Filter out low probability detections
        reliable_langs = [lang for lang in langs if lang.prob > 0.5]
        
        if reliable_langs:
            # Check specifically for Arabic first
            for lang in reliable_langs:
                if lang.lang == 'ar' and lang.prob > 0.3:  # Lower threshold for Arabic
                    return 'ar'
            
            # Return the highest probability language
            return reliable_langs[0].lang
        
        # Fallback to basic detection
        detected = detect(text)
        return detected if detected else 'en'
        
    except Exception as e:
        print(f"Language detection error: {str(e)}")
        # If detection fails, check for Arabic characters
        if bool(re.search(r'[\u0600-\u06FF]', text)):
            return 'ar'
        return 'en'

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        # Save uploaded file for processing
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save a copy for playback (use shutil to copy the file)
        import shutil
        audio_path = os.path.join(app.config['AUDIO_FOLDER'], filename)
        
        # Save the file first
        file.save(filepath)
        # Make a copy for audio playback
        shutil.copy2(filepath, audio_path)

        # Process audio
        audio_data, sampling_rate = load_audio(filepath)
        
        # Get a longer sample for better language detection
        sample_result = transcription_pipe(
            {"raw": audio_data[:sampling_rate*10], "sampling_rate": sampling_rate},  # Use first 10 seconds
            return_timestamps=False,
            generate_kwargs={"language": None}
        )
        
        # Use robust language detection
        detected_lang = detect_language_robustly(sample_result["text"])
        print(f"Detected language (robust): {detected_lang}")  # Debug print
        
        # Map detected language to Whisper model language codes
        language_mapping = {
            'ar': 'ar',  # Arabic
            'en': 'en',  # English
            # Add more mappings as needed
        }
        
        whisper_lang = language_mapping.get(detected_lang, 'en')
        
        # Now do full transcription with detected language
        result = transcription_pipe(
            {"raw": audio_data, "sampling_rate": sampling_rate},
            return_timestamps=True,
            generate_kwargs={"language": whisper_lang}
        )
        transcript = result["text"]
        
        # Save transcript
        save_transcript(transcript)
        
        # Clean up processing file only
        if os.path.exists(filepath):
            os.remove(filepath)
        
        # Make sure the audio URL is correct
        audio_url = f'/static/audio/{filename}'
        
        print(f"Audio saved at: {audio_path}")  # Debug print
        print(f"Audio URL: {audio_url}")        # Debug print
        
        return jsonify({
            'success': True,
            'transcript': transcript,
            'audio_url': audio_url,
            'detected_language': detected_lang  # Optional: send language info to frontend
        })
    except Exception as e:
        if os.path.exists(filepath):
            os.remove(filepath)
        if os.path.exists(audio_path):
            os.remove(audio_path)
        print(f"Error: {str(e)}")  # Debug print
        return jsonify({'error': str(e)}), 500

@app.route('/summarize', methods=['POST'])
def summarize():
    text = request.json.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        title_response, text_response = summarize_text(text)
        
        return jsonify({
            'success': True,
            'title_summary': title_response.choices[0].message.content,
            'text_summary': text_response.choices[0].message.content
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/highlight', methods=['POST'])
def highlight():
    text = request.json.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        labels = [
  "person", "organization", "location", "date", "event", "award", "teams",  
  "competitions", "percent", "Time", "currency", "Fac", "quantity", "UNIT",  
  "law", "DATE", "Product", "Work of Art", "Language", "Nationality",  
  "Email", "URL", "Phone Number", "Measurement", "Gene", "Chemical", "Sport",  

#   // **Education-related entities**
  "University", "Degree", "Course", "GPA", "Scholarship", "Thesis", "Academic Paper",  

#   // **Economics-related entities**
  "Stock", "Market Index", "Inflation Rate", "GDP", "Trade Agreement",  
  "Company Revenue", "Economic Indicator", "Tax Policy",  

#   // **Medical-related entities**
  "Disease", "Symptom", "Medication", "Treatment", "Medical Procedure",  
  "Hospital", "Doctor", "Patient", "Vaccine", "Medical Device",  

#   // **Additional useful entities**
  "Technology", "Software", "Algorithm", "Patent", "Job Title",  
  "Political Party", "Government Policy", "Climate Metric", "Scientific Term"
]
        entities = highlighter.predict_entities(text, labels)
        
        # Make sure entities have start and end positions
        for entity in entities:
            if 'start' not in entity:
                # Find position in original text if not provided
                entity['start'] = text.find(entity['text'])
                entity['end'] = entity['start'] + len(entity['text'])
        
        return jsonify({
            'success': True,
            'entities': entities
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/translate', methods=['POST'])
def translate():
    text = request.json.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        translated = translate_text(text)
        if translated:
            return jsonify({
                'success': True,
                'translated_text': translated,
                'original_text': text
            })
        else:
            return jsonify({'error': 'Translation failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
