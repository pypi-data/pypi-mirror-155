from transformers import AutoModelForCTC, AutoProcessor
import torch
import librosa
import pyctcdecode

def transcription(audio_path):

	# my_model_id = "loulely/XLSR_300M_Fine_Tuning_FR_2"
	my_model_id = "./my_model"

	# load model and processor
	my_model = AutoModelForCTC.from_pretrained(my_model_id)
	my_processor = AutoProcessor.from_pretrained(my_model_id)
	
	# load audio
	speech, rate = librosa.load(audio_path,sr=16000)

	inputs = my_processor(speech, sampling_rate=16_000, return_tensors="pt", padding=True)

	with torch.no_grad():
  		logits = my_model(inputs.input_values, attention_mask=inputs.attention_mask).logits

	pred = my_processor.batch_decode(logits.numpy()).text
	
	print(pred)
	
	return
