# Lab 2: API Client Integration

In this lab, you will explore the foundational API integration layer for your Gen-AI applications using **LiteLLM** and **OpenRouter**. 

**By the end of this lab, you will have a solid understanding of how to use LiteLLM to securely authenticate, handle rate limits automatically, and cache responses to save time and API costs during development.

---

## Lab Structure

This lab is contained within a single Jupyter notebook that walks through 4 key steps:

### Step 1: Environment Setup
Securely load API keys from a `.env` file using `python-dotenv`.

### Step 2: Your First API Call
Query an open-source model via OpenRouter using `litellm.completion()`.

### Step 3: Retry Logic
Use LiteLLM's built-in `num_retries` parameter to handle rate limits and transient network errors automatically.

### Step 4: Response Caching
Enable LiteLLM's built-in in-memory cache with `litellm.enable_cache(type="local")` to avoid redundant API calls during development.

---

## Setup Instructions

1. Ensure you have Python 3.10+ installed.
2. Install the required dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```
3. Copy `.env.example` to a new file named `.env`:
   ```bash
   cp .env.example .env
   ```
4. Create an OpenRouter account at [openrouter.ai](https://openrouter.ai), generate an API key, and paste it into your `.env` file.

---

## Running the Lab

Open the notebook in the root of this directory:

```
lab_02_api_client.ipynb
```
