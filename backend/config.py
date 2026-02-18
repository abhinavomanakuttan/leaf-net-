import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
HF_VISION_MODEL = os.getenv(
    "HF_VISION_MODEL",
    "ozair23/mobilenet_v2_1.0_224-finetuned-plantdisease",
)
