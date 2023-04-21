import torch
from diffusers import StableDiffusionInstructPix2PixPipeline
import numpy as np
import faiss

model_id = "timbrooks/instruct-pix2pix"
pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(model_id, torch_dtype=torch.float16, revision="fp16", safety_checker=None)
device = "cpu"
pipe.to(device)
pipe.enable_attention_slicing()

input_embeddings = pipe.text_encoder.get_input_embeddings()

embeddings_np = input_embeddings(torch.LongTensor([i for i in range(input_embeddings.num_embeddings)])).detach().numpy()

#cleanup some strange tokens
embeddings_np = embeddings_np[513:49408]

tokens = [tokenizer.decode(torch.tensor(i)) for i in range(513, 49408)]

index = faiss.IndexFlatL2(embeddings_np.shape[1])   # build the index
print(index.is_trained)
index.add(embeddings_np)                  # add vectors to the index
print(index.ntotal)

faiss.write_index(index, "clip_text.index")

tokenizer = pipe.tokenizer
prompt = "happy"

smug_embedded_idx = [idx for idx, token in enumerate(tokens) if token == prompt]

query = embeddings_np[smug_embedded_idx[0]][np.newaxis, ...]

D, I = index.search(query, 5)

#tokenizer.decode(torch.tensor(I[0]))

related_idxs = I[0].tolist()

related_tokes = [tokens[i] for i in related_idxs]