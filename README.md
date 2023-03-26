# Ham Whisperer
Stitch together audio (and/or video) from multiple sources, word-by-word.
Thus you can match the audio or video of your choice to some arbitrary clips.
Assume your clips include the words in your video's transcript as a subset of their collective transcripts.

Ham Whisperer uses `openai-whisper` and keeps tabs on the output data to allow you to splice everything back together.

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
4. Install the application `ffmpeg`
    ```bash
    brew install ffmpeg
    ```
5. Install python dependencies
   ```bash
   pip install -r requirements.txt
   ```
6. Update `run_this.py` to reflect the .wav and JSON files you wish to process.
7. Execute within your virtual environment.  This may take a short while depending on the model you select and whether you have a GPU. The default model is medium.
   ```bash
   python run_this.py
   ```
8. (_Work In Progress_) iterate over the transcript and timestamp data to select the clips you want.


Remove valid matches word-by-word and add more source audio until the full source transcript is accounted for. 

