import librosa
import numpy as np
from datetime import datetime
import os

def load_audio(file_path, target_sr=16000):
    """Load and preprocess audio file"""
    try:
        # Load audio file
        audio, sr = librosa.load(file_path, sr=target_sr)
        
        # Convert to mono if stereo
        if len(audio.shape) > 1:
            audio = audio.mean(axis=1)
        
        # Normalize audio
        audio = audio / np.max(np.abs(audio))
        
        return audio, target_sr
    
    except Exception as e:
        raise Exception(f"Error loading audio file: {str(e)}")

def save_transcript(text, output_dir="transcripts"):
    """Save transcript to a file with timestamp"""
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"transcript_{timestamp}.txt"
        filepath = os.path.join(output_dir, filename)
        
        # Write transcript to file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text)
            
        return filepath
        
    except Exception as e:
        raise Exception(f"Error saving transcript: {str(e)}")
