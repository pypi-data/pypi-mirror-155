from transformers import AutoModelForCTC, AutoProcessor
import torch
import librosa
import pyctcdecode

def transcription(audio_path, model, processor):
	
	# load audio
	speech, rate = librosa.load(audio_path,sr=16000)

	inputs = processor(speech, sampling_rate=16_000, return_tensors="pt", padding=True)

	with torch.no_grad():
  		logits = model(inputs.input_values, attention_mask=inputs.attention_mask).logits

	pred = processor.batch_decode(logits.numpy()).text
	
	print(pred)
	
	return
