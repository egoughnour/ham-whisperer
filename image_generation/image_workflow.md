# Steps

## Image Prep

1. Create or generate some raw images to use as input.
2. Save these to `image_generation/raw_inputs` .
3. Find the parts that are not OK as-is.
3. Mask these out. Specifically
     - export to PNG ensuring the output file is square.
         - name the file `input_to_correct.png` , saving it within the `image_generation` directory 
     - copy the exported PNG, and open in a graphics editor.
         - _A word to the uninitiated:_ you might install [GIMP][download]. (It's great! It can help with the preceding steps also. [More details][gimphelp])
     - Open the copied PNG as an image or layer.  
     - Delete to transparency in areas where the input image needs to be updated. (Alpha channel should be a mask of good vs bad.)
     - export the mask  as PNG, again saving in the `image_generation` directory.
         - name the file `mask.png`

## Using OpenAI

1. Sign up for an API Key from OpenAI if you don't already have one.
2. Save this API key in the `.env` file under the `image_generation` directory.
     - You can edit the file `dotenv_template.txt`, save and rename it to `.env`, which is in the .gitignore. (By default the `.env` file can't and won't be part of your next Pull Request--not unless you include it on purpose).
      - DO NOT COMMIT CHANGES TO `dotenv_template.txt` !  
      - In `.env` replace `YOUR_API_KEY` with the API key from OpenAI, then save the file.

## Virtual Environment Setup

1. From your IDE (within the terminal) or in the shell, deactivate the current virtual environment if any has already been activated in the project directory.
    ```bash
    deactivate
    ```
2. Change directory to the `image_generation` directory
    ```bash
    pushd image_generation
    ```
3. Create an image-specific virtual environment
    ```bash
    python3 -m venv imagevenv
    ```
4. Activate the virtual environment.
    ```bash
    source imagevenv/bin/activate
    ```
     - Your prompt should now be prefixed with `(imagevenv)`.
5. Restore dependencies from `requirements.txt`
    ```bash
    pip install -r requirements.txt
    ``` 



## More Details: How to Carry out the Editing Steps in GIMP
 - Any compatible file can be opened as a new image or pasted as a layer in GIMP.
 - To erase:
     -  select the freehand erase tool (eraser icon).
     - adjust the tool size so that you can balance out speed and accuracy of erasure.
     - verify (in the tool settings panel) that your eraser will erase to transparency rather than the background color.
     - The tool size to select will depend on your image size and the level of detail near the region to be corrected.
     - Click and drag to remove the unwanted image parts.
     - Export as png.
 - Any data can be exported as an image in whatever format you want.
     - when exporting the mask as PNG, make sure to preserve (alpha/pixel transparency) in the pop-up dialog.
 - GIMP saves your history as a non-image XCF file, but includes image (and other) data for every step.  (Implementation detail--I'm not sure if this is stored as deltas or what.)
 - Crop the image to square:
     - Open the rectangle selection tool.
     - In the tool details pane, lock the aspect ratio at 1:1.
     - Click and drag to select the square area of the image you will keep.
     - In the image drop down menu, select crop image to selection.


[download]: https://www.gimp.org/downloads/
[gimphelp]: #more-details-how-to-carry-out-the-editing-steps-in-gimp



