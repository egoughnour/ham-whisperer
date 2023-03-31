import json
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple
from moviepy import *
from moviepy.editor import *

@dataclass
class WordMatch:
    match_text: str
    percentage_time_error: float
    detected_word_reliability: float
    target: dict
    candidate: dict
    clip_index: int

def get_matches_from_json(file_to_match:str, file_to_search:str, input_audio_file:str, other_audio_file:str) -> Tuple[int, List[WordMatch]]:
    matches = []
    with open(file_to_match) as f:
        to_match = json.load(f)
    with open(file_to_search) as f:
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
                        relative_time_mismatch = np.abs(1.0 - (candidate_time/target_time)) if ((target_time > 0) and (candidate_time > 0))  else -1
                        reliability = pt * pc
                        matches.append(WordMatch(needed, relative_time_mismatch, reliability, n_data, a_data, -1))
    unique_matches = set()
    for match in matches:
        unique_matches.add(match.match_text)

    match_count = len(unique_matches)

    best_matches = []
    for unique_text in unique_matches:
        related_matches = [m for m in  matches if m.match_text == unique_text]
        best_match = max(related_matches, key=lambda x: x.detected_word_reliability)
        best_matches.append(best_match)

    sub_clips = []
   
    if  other_audio_file is not None:
        original_clip = AudioFileClip(input_audio_file)
        clip = AudioFileClip(other_audio_file)

        for i, bm in enumerate(best_matches):
            sub_clip = clip.subclip(bm.candidate["start"], bm.candidate["end"])
            sub_clips.append(sub_clip)
            bm.clip_index = len(sub_clips)-1

        clips_to_concat = []
        hits = 0
        misses = 0
        matches_for_clipword = [fw.target for fw in best_matches]
        for i, seg in target_segs.items():
            target_time = seg['end'] - seg['start']
            if (target_time == 0) or (not seg['text']) or (not seg['words']):
                continue
            for j, clip_word in seg['words'].items():
                if clip_word in matches_for_clipword:
                    hits += 1    
                    word_match_index = matches_for_clipword.index(clip_word)
                    match_for_this_word = best_matches[word_match_index]
                    clips_to_concat.append(sub_clips[match_for_this_word.clip_index].copy())
                else:
                    misses += 1
                    clips_to_concat.append(original_clip.subclip(clip_word['start'], clip_word['end']))
        #TODO fix condition here assert(len(clips_to_concat) == len())

        print(f'misses: {misses}')
        print(f'hits: {hits}')

        patchwork = concatenate_audioclips(clips_to_concat) 
        patchwork.write_audiofile('masterpiece.wav')




    print(f"""Found {match_count} matches""")
    return match_count, matches



