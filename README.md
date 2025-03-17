# AudioMind -


## Overview
AudioMind is a powerful web application that transcribes audio content and provides various text analysis features. It supports both audio file uploads and live recording, with automatic language detection and processing. 😂

[demo graduation_project.webm](https://github.com/user-attachments/assets/7731e412-21e2-488a-8f4d-20ab2fac7eb7)

# Mobile App ~~for~~ `Web` Scroll Down 
![image](https://github.com/user-attachments/assets/d6eb5ebf-6ae2-487f-ab22-cb594b2ff060)

# Demo



## Features
- 🎤 Audio Input Methods:
  - File upload (supports multiple audio formats)
  - Live recording through browser

- 📝 Core Functionalities:
  - Speech-to-text transcription with language detection
  - Automated text summarization
  - Title generation
  - Entity highlighting and recognition
  - Automatic translation (Arabic ↔ English)

- 🔍 Entity Recognition Categories:
  - Basic: person, organization, location, date, event
  - Academic: university, degree, course, thesis
  - Business: company, currency, economic indicators
  - Medical: disease, treatment, medication
  - And many more...

# Technical Stack
- Backend:
  - Flask (Python web framework)
  - Whisper Large V3 (Speech recognition) ` Fine_Tuing_on the Blowe Data and code for train on my privte `
  - Mistral AI (Text summarization)   ~~Fine_Tuing_on the Blowe Data and code for train on my privte~~
  - GLiNER (Entity recognition)  ~~Fine_Tuing_on the Blowe Data and code for train on my privte~~
  - Google Translate API         ~~Fine_Tuing_on the Blowe Data and code for train on my privte~~

- Frontend:
  - Bootstrap 5
  - Vanilla JavaScript
  - HTML5 Audio API

# Usage
- Upload or Record Audio

- Use the file upload button or
- Click "Start Recording" for live input
- Transcribe

- Click "Transcribe File" for uploaded audio or
- Click "Transcribe Recording" for recorded audio
Process Text

- Get Title: Generates a concise title
- Summarize: Creates a summary of the content
- Highlight: Identifies and highlights key entities
- Translate: Automatically translates between Arabic and English

![image](https://github.com/user-attachments/assets/7cd27576-92f5-4444-8fa3-6cbf876dd7a4)
  
## Project Structure  

```bash
audio/
│
├── app.py              # Main Flask application
├── Audio.py            # Speech recognition setup
├── translator.py       # Translation functions
├── sumerizer.py        # Text summarization
├── highliter.py        # Entity recognition
│
├── static/
│   ├── audio/         # Stored audio files
│   └── css/
│       └── style.css  # Custom styling
│
├── templates/
│   ├── base.html      # Base template
│   └── index.html     # Main application page
│
└── uploads/           # Temporary file storage
```
   

# Technical Notes
- Supports both Arabic and English audio input
- Automatic language detection for optimal processing
- Real-time audio processing and playback
- Entity highlighting with multiple category support

# Data Used for Fine-Tuning  

![images for clarify](https://github.com/user-attachments/assets/84d9561a-ab62-4469-8662-b03dbbdd1e30)  

![mages for clarify](https://github.com/user-attachments/assets/6856b6f0-179c-46cf-9692-2295c114764f)  

[FineWeb-2 Dataset on Hugging Face](https://huggingface.co/datasets/HuggingFaceFW/fineweb-2/tree/main)  

# Web 
![image](https://github.com/user-attachments/assets/ac095562-4865-41a7-aada-129946a20f99)

## Installation Guide

### Clone the Repository  
Run the following command to clone the project:  

```bash
git clone https://github.com/AhemdMahmoud/AudioMind.git
```
```bash
cd AudioMind
pip install -r requirements.txt
```
```bash

python .\app.py
```

 

# Authors
## Team Z 😘😂![MuaKissGIF](https://github.com/user-attachments/assets/57a0863a-4d7a-4050-983a-45a9347b8dc3)

# thanks for all my team ,Dr

![SoExcited~GIF (2)](https://github.com/user-attachments/assets/4a861fb1-789c-4356-a50f-ae2ab8b7261e)


