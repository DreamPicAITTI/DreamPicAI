from fastapi import FastAPI, HTTPException
import os
import replicate

app = FastAPI()

# Get Replicate API key from environment variable
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

if not REPLICATE_API_TOKEN:
    raise RuntimeError("Missing REPLICATE_API_TOKEN. Set it as an environment variable.")

@app.post("/generate")
async def generate_image(data: dict):
    try:
        text_prompt = data.get("text", "").strip()
        style = data.get("style", "").strip()

        if not text_prompt:
            raise HTTPException(status_code=400, detail="Prompt is required!")

        # Combine text and style for better image generation
        final_prompt = f"{style}, {text_prompt}, highly detailed, cinematic lighting"

        # Call Replicate's Stable Diffusion model
        output = replicate.run(
            "stability-ai/stable-diffusion",
            input={"prompt": final_prompt, "width": 512, "height": 512, "num_outputs": 1}
        )

        return {"image_url": output[0]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
