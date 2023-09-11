<br>

<h2 align="center">A demo "Concept Canvas" that allows a user to explore similar concepts to fine-tune stable diffusion generated images</h2>

<div align="center">

https://user-images.githubusercontent.com/24516535/266800675-5f368fbb-c28c-4090-9d8d-118f244d72c5.mp4

</div>

---

#### Overview

This is a demo where a user adjusts an image of the statue of David to try and capture his facial expression after his iconic victory over Goliath.  The main goal is to provide a tool that allows the user to try an initial prompt to edit the input image, and then to explore and combine similar concepts in the CLIP embedding space to tailor the embedding that is fed to the U-Net model to best meet the user's intent.
  
#### Interface 

The upper left 3D interactive scatter plot represents the concept canvas consisting of PCA reduced (768-dimensional CLIP embeddings reduced to graph nodes in 4 dimensions -> 3d space + color) synonyms for "smug."  I focus on swapping different variations of this word because it is the adjective describing the object (David's face) from the original prompt.  Because words are subjective, redundant, and context sensitive, the similar synonym nodes in the concept canvas help to provide different directions in the embedding space to help distinguish the user's precise intent somewhere within this cluster of similar concepts.  To start, I just consider pairwise relationships between synonyms, but combinations of multiple synonyms and antonyms are possible as well.  The image on the upper right depicts the resulting image from any combination of prompt synonyms.  The bottom portion of the interface provides a slider (with reference images) to provide the user with a knob to combine different proportions of the synonymous concepts.  Consider two points in the prompt embedding space (e.g., "Make his face more smug" and "Make his face more excited") - if we move the slider to 50%, this represents the point in the embedding space halfway between the points representing those two concepts.  Thus, the user can leverage this interface to explore and blend different similar concepts to define their own embeddings that generate images that more closely resemble the images from their imagination.