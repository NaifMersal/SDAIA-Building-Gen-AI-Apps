import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Central model configuration
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")
