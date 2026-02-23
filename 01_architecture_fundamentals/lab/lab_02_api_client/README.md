# Lab 2: API Client Integration

In this lab, you will build the foundational API integration layer for your Gen-AI applications using **LiteLLM** and **OpenRouter**. 

By the end of this lab, you will have a production-ready API client that can securely authenticate, handle rate limits, and implement local caching to save time and API costs during development.

---

## Lab Structure

This lab is divided into five steps. You will work primarily in the `starter/` directory. If you get stuck, reference the `solutions/` directory.

### Step 1: Environment Setup
Learn how to securely manage API keys using environment variables. You will inspect how tokens are loaded from a `.env` file instead of being hardcoded into scripts.

### Step 2: Your First API Call
Write a basic script to query an open-source model via OpenRouter using the `litellm` library.

### Step 3: Handling Errors (Rate Limits)
Implement exponential backoff to gracefully handle `RateLimitError` when you exceed your free tier limits.

### Step 4: Building a Reusable Client
Wrap your API logic into a reusable `LiteLLMClient` class that you can import into future projects.

### Step 5: Caching Responses
Extend your client to cache API responses locally. This is a critical skill for development: it allows you to iterate on your application logic without repeatedly waiting for, or paying for, the same expensive API calls.

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

## Running the Code

Navigate to the `starter/` directory and run the scripts as you complete them:

```bash
python hello_litellm.py
python litellm_client.py
python cached_client.py
```
