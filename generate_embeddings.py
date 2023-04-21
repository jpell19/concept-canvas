import torch
from diffusers import StableDiffusionInstructPix2PixPipeline, EulerAncestralDiscreteScheduler
from sklearn.decomposition import PCA
import pandas as pd

model_id = "timbrooks/instruct-pix2pix"
pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(model_id, torch_dtype=torch.float16, revision="fp16", safety_checker=None)
device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
pipe.to(device)
pipe.enable_attention_slicing()

text_encoder = pipe.text_encoder.to(device)
tokenizer = pipe.tokenizer

positve_root, negative_root = "make his face more", "make his face less"

root_word = "smug"

root_sentence = f'{positve_root} {root_word}'

synonyms  = [
    "amused", "excited", "victorious" ,"surprised",
    "proud", "cocky", "confident", "awestruck"
]

antonyms = ["humble", "modest", "timid", "grateful", "diffident"]

synonym_senetences = [f'{positve_root} {synonym}' for synonym in synonyms]

antonym_senetences = [f'{negative_root} {antonym}' for antonym in antonyms]

words = [root_word] + synonyms #+ antonyms

prompts = [root_sentence] + synonym_senetences #+ antonym_senetences

text_inputs = tokenizer(
                prompts,
                padding="max_length",
                max_length=tokenizer.model_max_length,
                truncation=True,
                return_tensors="pt",
            )

text_input_ids = text_inputs.input_ids

prompt_embeds = text_encoder(text_input_ids.to(device))

concepts = prompt_embeds.pooler_output.cpu().detach().numpy()

pca = PCA(n_components=4) 
pca.fit(concepts) 
concepts_reduced = pca.transform(concepts)

df = pd.DataFrame(concepts_reduced)
df['prompt'] = prompts
df['word'] = words

df.rename(columns={0: "x", 1: "y", 2: "z", 3: "color"}, inplace=True)

df.index.name='idx'

df.to_csv('concepts_reduced.csv')