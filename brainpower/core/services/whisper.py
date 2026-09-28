from faster_whisper import WhisperModel
from core.services.essay_editor import EssayEditor
import librosa
from statistics import mean

#Load Model
model = WhisperModel(
    model_size_or_path="medium",
    device="cuda", 
    compute_type="int8_float16",
    cpu_threads=16,
)

def transcribe_audio(file_path):
  
    #Load audio file and set sample rate
    audio, rate = librosa.load(file_path, sr=16000)
    
    #Get length of audio
    duration = librosa.get_duration(y=audio, sr=rate)
    segments, info = model.transcribe(
        audio, 
        language='en',
        beam_size=2,
        vad_filter=True 
    )
    avg_logprob_threshold = info.transcription_options.log_prob_threshold
    compression_ratio_threshold = info.transcription_options.compression_ratio_threshold

    #Convert segments to list as it is a generator
    segments = list(segments)
    
    #Assemble transcription
    whisper_output = " ".join([segment.text for segment in segments])

    #Whisper internal metrics
    avg_logprob = mean(segment.avg_logprob for segment in segments)
    compression_ratio = mean(segment.compression_ratio for segment in segments)

    #Convert to EssayEditor Object for normalisation
    whisper_output = EssayEditor(whisper_output)
    

    #Transcription Quality Gate based on Whisper's transcription confidence
    scoring_method  = ("Manual" if avg_logprob < avg_logprob_threshold
                        or compression_ratio > compression_ratio_threshold else "Automated")       
    
    #Store the details of the transcription 
    transcription = {
        "Avg_logprob":avg_logprob,
        "Compression_Ratio":compression_ratio,
        "Output": whisper_output,  
        "Scoring_Method": scoring_method
    }
    
    return transcription