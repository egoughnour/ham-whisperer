# Ham Whisperer
<img alt="very smoked ham" src="image_generation/images/smoked_ham.png" width="256" height="256" />
Stitch together audio (and/or video) from multiple sources, word-by-word.
Thus you can match the audio or video of your choice to some arbitrary clips.
Assume your clips include the words in your video's transcript as a subset of their collective transcripts.


Ham Whisperer uses `openai-whisper` and keeps tabs on the output data to allow you to splice everything back together.

Not intent on burying the lead, we present for your judgment an outtake from a generated file. _P.S.: the embedded audio player may be muted by default_

https://user-images.githubusercontent.com/457471/229022961-a2bfb099-2931-4bbf-b0e5-4b7639ed6f2e.mp4

With the transcript generated, Ham Whisperer is able to track some fairly useful data for you. 

- the source and destination timestamps
- the occurrence order
- the overall phrase to be reproduced, for each line of dialog
- the disparity in length (that is, elapsed time) and
- the probability estimate of an actual occurrence (rather than a false positive) 


For example, you may want to find a video clip in which Rick Moranis or Ellen Greene sing the word "Seymour".
Suppose again for some reason you can't find voice acting in _22 Short Films About Springfield_ to compare to their vocal qualities.
You do remember _Suddenly Seymour_ though.

Then Ham Whisperer can help you and Gary Chalmers to excoriate Skinner much more soulfully than you might otherwise.

There is also a **moderately complete walkthrough of my programmatic image generation and editing workflow** (since I had to create assets anyway).
You can [find it here](image_generation/image_workflow.md) with source included.
You might as well spin up a virtual environment and try it from your git checkout since it's housed in this repository anyhow.

### _What started out as an LLM's fever dream of Audrey paradoxically comforted by Seymour's arson and confabulation_
![image](image_generation/images/suddenly_seymour.jpeg)



# Quick Start

1. Clone the repo in git
   ```bash
   git clone https://github.com/egoughnour/ham-whisperer.git
   ```
2. Create a virtual environment. (Python 3.10 or lower will keep `whisper` happy.)
    ```bash
    brew install python@3.10
    python3.10 -m venv virtualenv
    ```
3. Activate the environment
   ```bash
   source virtualenv/bin/activate
   ```
Note the command line arguments.

    usage: run_this.py [-h] [-p PROMPT_FILE] [-w WHISPER_MODEL] [-o OTHER_AUDIO_FILE]
                   input_audio output_path [search_path]

4. Install python dependencies
   ```bash
   pip install -r requirements.txt
   ```
5. Install the application `ffmpeg` (this may not be necessary, depending on whether `moviepy` can install this dependency--which it is claimed to do).
    ```bash
    brew install ffmpeg
    ```
6. Run something like the following to extract the transcription data from an audio or video clip.
   ```bash
   python ./run_this.py apollo.mp3 apollo.json
   ```
7. If you find the transcription is lacking, you can either change to a [larger model in whisper](https://github.com/openai/whisper#available-models-and-languages) using the `-w` argument --which will take significantly more time to process--or simply write out a prompt file.
 Enter token sequences you expect the decoder to hear, one per line, into a text file.  For example in _Suddenly Seymour_, the word _Seymour_ was consistently separated into _see_ _more_ . Unsurprisingly _Seymour's_ became _see more as_.  Compounding this problem was _wash off your mascara_ -- which became a single four syllable word.
This requires a prompt file like so:
 ```text
 Wash off your mascara
 Seymour
 ```
Save it as, say, `whisper_input_prompt.txt` then, to continue with the example, we would use the `-p` argument.
```bash
python ./run_this.py sud_seymour.mp4 sud_seymour.json -p whisper_input_prompt.txt
```
8. Now you have the data necessary, but the merge has not been executed.  When calling with the `-o` argument and passing a total of two files containing audio streams and two JSON files, the best matches are automatically chosen.  Currently this is limited to one source and one target file.

```bash
python ./run_this.py full_steam.wav full_ham.json sud_seymour.json -o sud_seymour.mp4
```

The above command will output the merged file into `masterpiece.wav'

This is what the last 23 seconds of that little slice of heaven might sound like:




