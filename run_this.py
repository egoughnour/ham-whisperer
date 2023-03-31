from argparse import ArgumentParser
from pathlib import Path
from typing import List
import speech_to_text
import start_compose
import pathlib


def is_existing_json(path: str | Path) -> bool:
    if type(path) is Path:
        path_to_check = path.resolve()
    else:
        path_to_check = pathlib.Path(path).resolve()
    return path_to_check.exists() and path_to_check.is_file()

def read_prompt_file(prompt_path: Path) -> List[str]:
    with open(prompt_path) as f:
        return f.readlines()

def process(input_audio, output_path, search_path, prompt_file, whisper_model, other_audio_file):
    match_count = None
    if prompt_file:
        listen_for = read_prompt_file(prompt_path=prompt_file)
    else:
        listen_for = None
    """  input_audio='full_steam.wav'
    output_path='full_ham.json'
    search_path='lsoh_sseymour_timestamps.json' 
    listen_for = ['Albany', 'Utica', 'Aurora borealis', 'Seymour', 'Superintendent', 'Chalmers']"""
    if not is_existing_json(output_path):
        speech_to_text.transcribe_to_json(output_path=(output_path_string := str(output_path.resolve())), input_path=str(input_audio.resolve()), suggested_phrases=listen_for, whisper_model=whisper_model)
    if search_path:
        output_path_string = str(output_path.resolve())
        match_count, matches = start_compose.get_matches_from_json(output_path_string, str(search_path.resolve()), str(input_audio.resolve()), str(other_audio_file.resolve()) if other_audio_file is not None else None)
    if match_count is not None:
        print(f'Match count is: {match_count}')

def main():
    parser = ArgumentParser()
    parser.add_argument('input_audio', type=Path, help='path to an audio file that will be transcribed')
    parser.add_argument('output_path', type=Path, help='path to a JSON file to store the transcription data.  If it exists, transcription is assumed complete.')
    parser.add_argument('search_path', nargs='?',type=Path, default=None, help='path to another JSON file. This file contains the transcription data for an audio or video source to search, matching against the first (word by word).')
    parser.add_argument('-p','--prompt-file', type=Path, help='the path to a file containing hints for difficult to decode words or phrases.  The phrases or word should simply be listed one per line without punctuation.')
    parser.add_argument('-w','--whisper-model', type=str, default='medium', help='The model to use for whisper.')
    parser.add_argument('-o', '--other-audio-file', type=Path, default=None, help='the path to an other audio file. Namely the audio file corresponding to the source of the JSON file on the search path.')
    args = parser.parse_args()
    process(**vars(args))

if __name__ == '__main__':
    main()