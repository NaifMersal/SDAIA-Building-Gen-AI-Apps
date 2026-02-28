import os
from dotenv import load_dotenv

load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")
EMBEDDING_MODEL = "text-embedding-3-small"
