import speech_to_text

input_audio='full_steam.wav'
output_path='full_ham.json'
listen_for = ['Albany', 'Utica', 'Aurora borealis', 'Seymour', 'Superintendent', 'Chalmers']
speech_to_text.transcribe_to_json(output_path=output_path, input_path=input_audio, suggested_phrases=listen_for)
