import whisper
import os
import numpy as np
import torch

torch.cuda.is_available()
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("medium", device=DEVICE)
print(
    f"Model is {'multilingual' if model.is_multilingual else 'English-only'} "
    f"and has {sum(np.prod(p.shape) for p in model.parameters()):,} parameters."
)
audio = whisper.load_audio("steam_ham_audio.wav")
audio = whisper.pad_or_trim(audio)
mel = whisper.log_mel_spectrogram(audio).to(model.device)
_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")
options = whisper.DecodingOptions(language="en", without_timestamps=True, fp16=False)
result = whisper.decode(model, mel, options)
print(result.text)
result = model.transcribe("steam_ham_audio.wav", word_timestamps=True)
print(result["text"])
segment_list = [segment for segment in result['segments']]
for i, segment in enumerate(segment_list):
    start, end, whole_text, words =  (segment['start'], segment['end'], segment['text'],segment['words'])
    #TODO save to output with file.write(json.dumps())?
    for j, word in enumerate(words):
        print(f"""{j:02d}. {word['word']} [{word['start']}-{word['end']}]({word['probability']:.5f}%) """)
