import json
import numpy as np
from dataclasses import dataclass

@dataclass
class WordMatch:
    match_text: str
    percentage_time_error: float
    detected_word_reliability: float
    target: dict
    candidate: dict

matches = []
with open('target_timestamps.json') as f:
    to_match = json.load(f)
with open('lsoh_sseymour_timestamps.json') as f:
    to_search = json.load(f)
print('loaded')
search_segs = to_search['segments']
target_segs = to_match['segments']

#don't need to enumerate because the keys are indexes
for i, wanted_seg in target_segs.items():
    for j, found_seg in search_segs.items():
        i = int(i)
        j = int(j)
        words_needed = [ (s['bare_word'].strip(), s) for _,s in wanted_seg['words'].items()]
        words_available = [(s['bare_word'].strip(), s) for _,s in found_seg['words'].items()]
        #TODO normalize probabilities?
        for needed, n_data in  words_needed:
            target_time = n_data['end'] - n_data['start']
            pt = n_data['probability']
            for available, a_data in words_available:
                if needed == available:
                    candidate_time = a_data['end']-a_data['start']
                    pc = a_data['probability']
                    relative_time_mismatch = np.abs(1.0 - (candidate_time/target_time))
                    reliability = pt * pc
                    matches.append(WordMatch(needed, relative_time_mismatch, reliability, n_data, a_data))
unique_matches = set()
for match in matches:
    unique_matches.add(match.match_text)

match_count = len(unique_matches)

print(f"""Found {match_count} matches""")



