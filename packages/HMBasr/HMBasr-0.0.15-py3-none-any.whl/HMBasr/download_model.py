from transformers import Wav2Vec2ForCTC, Wav2Vec2ProcessorWithLM

my_model_id = "loulely/XLSR_300M_Fine_Tuning_FR_2"

# load model and processor
my_model = Wav2Vec2ForCTC.from_pretrained(my_model_id)
my_processor = Wav2Vec2ProcessorWithLM.from_pretrained(my_model_id)


my_model.save_pretrained(save_directory="./")
my_processor.save_pretrained(save_directory="./")