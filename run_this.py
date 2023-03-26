import speech_to_text
import start_compose
import pathlib


def is_existing_json(path: str) -> bool:
    path_to_check = pathlib.Path(path).resolve()
    return path_to_check.exists() and path_to_check.is_file()

input_audio='full_steam.wav'
output_path='full_ham.json'
search_path='lsoh_sseymour_timestamps.json'
listen_for = ['Albany', 'Utica', 'Aurora borealis', 'Seymour', 'Superintendent', 'Chalmers']
if not is_existing_json(output_path):
    speech_to_text.transcribe_to_json(output_path=output_path, input_path=input_audio, suggested_phrases=listen_for)
match_count, matches = start_compose.get_matches_from_json(output_path, search_path)
print(f'Match count is: {match_count}')