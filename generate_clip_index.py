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

index = faiss.IndexFlatL2(embeddings_np.shape[1])   # build the index
print(index.is_trained)
index.add(embeddings_np)                  # add vectors to the index
print(index.ntotal)

faiss.write_index(index, "clip_text.index")

tokenizer = pipe.tokenizer
smug_embedded_idx = tokenizer(
                "smug",
                padding="do_not_pad",
                max_length=tokenizer.model_max_length,
                truncation=True,
                return_tensors="pt",
            ).input_ids[0][1]

query = embeddings_np[smug_embedded_idx][np.newaxis, ...]

D, I = index.search(query, 5)

tokenizer.decode(torch.tensor(I[0]))
