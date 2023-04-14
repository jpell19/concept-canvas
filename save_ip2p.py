import torch
from diffusers import StableDiffusionInstructPix2PixPipeline


model_id = "timbrooks/instruct-pix2pix"
pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(model_id, torch_dtype=torch.float16, revision="fp16", safety_checker=None)
pipe.save_pretrained("ip2p_model")