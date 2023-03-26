import os
import openai
import requests
from PIL import Image
from dotenv import load_dotenv

def main():
    
    # Load API key from .env file
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    #TODO pull these from an ArgumentParser: prompt, source_file, alpha_file, img_side_length, output_file

    # Define the parameters for the create_edit function
    prompt = "woman pointing in shock in upscale dining room without roof under aurora borealis"
    source_file = "input_to_correct.png"
    alpha_file = "mask.png"
    count = 1
    img_side_length = 512
    dims = f'{img_side_length}x{img_side_length}'
    output_file = "generated_image.jpg"

    # Call the create_edit function
    with open(source_file, "rb") as source_file:
        with open(alpha_file, "rb") as alpha_file:
            response = openai.Image.create_edit(
                image=source_file,
                mask=alpha_file,
                n=count,
                size=dims,
            )

    # Get the URL of the generated image from the response
    output_url = response["output_url"]

    # Download and display the generated image
    img_data = requests.get(output_url).content
    with open(output_file, "wb") as handler:
        handler.write(img_data)
        generated_image = Image.open(output_file)
        generated_image.show()

if __name__ == '__main__':
    main()