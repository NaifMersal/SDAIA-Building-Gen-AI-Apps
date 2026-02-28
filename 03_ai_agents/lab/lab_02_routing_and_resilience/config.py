import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Central model configuration
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")
EMBEDDING_MODEL = "text-embedding-3-small"
