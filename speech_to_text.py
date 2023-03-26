import whisper
import os
import numpy as np
import torch
from string import punctuation
import json
from pathlib import Path
from typing import List

def transcribe_to_json(output_path: str, input_path: str, suggested_phrases: List[str], whisper_model: str="medium"):
    torch.cuda.is_available()
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model(whisper_model, device=DEVICE)
    print(
        f"Model is {'multilingual' if model.is_multilingual else 'English-only'} "
        f"and has {sum(np.prod(p.shape) for p in model.parameters()):,} parameters."
    )
    audio = whisper.load_audio(input_path)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")
    options = whisper.DecodingOptions(language="en", without_timestamps=True, fp16=False)
    result = whisper.decode(model, mel, options)
    print(result.text)
    if suggested_phrases:
        model_prompt = ' '.join(suggested_phrases)
        print(f"""Using prompt '{model_prompt}'.""")
        result = model.transcribe(input_path, word_timestamps=True, initial_prompt=model_prompt)
    else:
        print('Not passing any prompts to the whisper model')
        result = model.transcribe(input_path, word_timestamps=True)
    print(result["text"])
    segment_list = [segment for segment in result['segments']]
    segment_dict = {'segments':{}}
    for i, segment in enumerate(segment_list):
        start, end, whole_text, words =  (segment['start'], segment['end'], segment['text'],segment['words'])
        segment_data = {'start':start, 'end':end, 'text':whole_text, 'words':{}}
        for j, word in enumerate(words):
            print(f"""{j:02d}. {word['word']} [{word['start']}-{word['end']}]({word['probability']:.5f}%) """)
            word_data = {'word':word['word'], 'bare_word':word['word'].strip(punctuation).lower(), 'start':word['start'], 'end':word['end'], 'probability':word['probability']}
            segment_data['words'][j] = word_data
        segment_dict['segments'][i] = segment_data
    json_value = json.dumps(segment_dict, ensure_ascii=False, indent=4)
    with open(output_path, 'w') as f:
        f.write(json_value)
    output_path_to_check = Path(output_path).resolve()
    if not (output_path_to_check.exists() and output_path_to_check.is_file()):
        print(f'file {output_path} was not written')
    else:
        print(f'audio script with timestamps has been saved to: {output_path}')