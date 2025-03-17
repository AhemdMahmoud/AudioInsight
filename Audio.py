import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from utils import load_audio, save_transcript

# Set up device and dtype
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

def initialize_whisper():
    try:
        # Load model and processor
        model_id = "openai/whisper-large-v3-turbo"
        
        print("Loading model...")
        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
        )
        model.to(device)

        print("Loading processor...")
        processor = AutoProcessor.from_pretrained(model_id)

        return pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            torch_dtype=torch_dtype,
            device=device,
        )

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise e

# Initialize the pipeline once
pipe = initialize_whisper()