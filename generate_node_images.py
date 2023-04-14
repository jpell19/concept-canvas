import PIL
from pathlib import Path
import torch
from diffusers import StableDiffusionInstructPix2PixPipeline
import os

model_id = "timbrooks/instruct-pix2pix"
pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(model_id, torch_dtype=torch.float16, revision="fp16", safety_checker=None)
device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
print(device)
pipe.to(device)
pipe.enable_attention_slicing()

model = pipe.text_encoder.to(device)
input_embeddings = pipe.text_encoder.get_input_embeddings()
tokenizer = pipe.tokenizer

positve_root, negative_root = "make his face more", "make his face less"

root_word = "smug"

root_sentence = f'{positve_root} {root_word}'

synonyms = ["arrogant", "self-satisfied", "condescending", "complacent", "proud"]

antonyms = ["humble", "modest", "timid", "grateful", "diffident"]

synonym_senetences = [f'{positve_root} {synonym}' for synonym in synonyms]

antonym_senetences = [f'{negative_root} {antonym}' for antonym in antonyms]

words = [root_word] + synonyms + antonyms

prompts = [root_sentence] + synonym_senetences + antonym_senetences

image = PIL.Image.open("./david.jpeg")
image = PIL.ImageOps.exif_transpose(image)
image = image.convert("RGB")


seed = 68
generator = [torch.Generator(device=device).manual_seed(seed) for _ in range(len(prompts))]

images = [image for _ in range(len(prompts))]

#generator = torch.manual_seed(seed)
output = pipe(prompts, image=images, num_inference_steps=50, image_guidance_scale=1.05, generator=generator)

DIR_NAME="./assets"
dirpath = Path(DIR_NAME)
# create parent dir if doesn't exist
dirpath.mkdir(parents=True, exist_ok=True)

for idx, image in enumerate(output.images):
    image_name = f'{words[idx]}_{seed}.png'
    image_path = os.path.join(dirpath, image_name)
    image.save(image_path)