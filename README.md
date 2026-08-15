

# Generate Images with AI — Azure AI Vision Lab

A hands-on exercise using **Microsoft Foundry** and the **Azure OpenAI SDK** to build a Python client application that generates images from text prompts using a `gpt-image` model.

> Based on: [Develop computer vision solutions in Azure — Exercise 02: Generate images with AI](https://microsoftlearning.github.io/mslearn-ai-vision/Instructions/Exercises/02-generate-image.html)

---

## Overview

This lab walks through deploying an image-generation model in Microsoft Foundry, testing it in the playground, and then building a simple Python console app that sends prompts to the model via the OpenAI SDK and saves the generated images locally.

---

## Prerequisites

- An active [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Python 3.13+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/install/)
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli?view=azure-cli-latest)

---

## Setup & Installation

1. **Create a Microsoft Foundry project**
   - Sign in at [ai.azure.com](https://ai.azure.com)
   - Enable **New Foundry**, create a project, and note the **Azure OpenAI endpoint** for later.

2. **Deploy an image model**
   - In the Foundry model catalog, search for and deploy `gpt-image-2` using default settings.
   - Note the deployment name (defaults to `gpt-image-2`).

3. **Test in the playground**
   - Try prompts like `A robot eating spaghetti`, then iterate with follow-ups (e.g. `Show the robot in a restaurant`).

4. **Clone the starter repo**
   ```bash
   git clone https://github.com/microsoftlearning/mslearn-ai-vision
   ```
   Open the `/labfiles/image-client/python` folder in VS Code.

5. **Configure the app**
   - Update `.env` with your **Azure OpenAI endpoint** (not the project endpoint) and model deployment name.

6. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## How to Run

1. Sign in to Azure:
   ```bash
   az login
   ```
2. Run the client:
   ```bash
   python image-client.py
   ```
3. Enter an image prompt when asked (e.g. `Create an image of a robot eating pizza`).
4. Generated images save to the `images/` folder as `.png` files.
5. Type `quit` to exit. Note: this simple version has no conversation memory — each prompt is treated independently.

**Clean up:** delete the Azure resource group afterward to avoid ongoing costs.

---

## Key Code Concepts

- **Authentication** — uses `DefaultAzureCredential` with a bearer token provider (via `azure.identity`) instead of static API keys, scoped to `cognitiveservices.azure.com`.
- **Client initialization** — the `OpenAI` SDK client is pointed at the Azure OpenAI endpoint with the token provider as the API key.
- **Image generation call** — `client.images.generate(model=..., prompt=..., n=1)` returns a base64-encoded image (`b64_json`), which is decoded and written to disk.

```python
img = client.images.generate(
    model=model_deployment,
    prompt=input_text,
    n=1
)
image_data = json.loads(img.model_dump_json())["data"][0].get("b64_json")
image_data_in_bytes = base64.b64decode(image_data)
```

---

## What I Learned

- How to provision and deploy a generative image model (`gpt-image-2`) through Microsoft Foundry, separate from a chat/completion model.
- The distinction between a **Foundry project endpoint** and an **Azure OpenAI endpoint** — and why the app specifically needs the latter.
- How to authenticate to Azure AI services using `DefaultAzureCredential` and a bearer token provider, rather than hardcoding API keys — a more production-appropriate pattern.
- How the OpenAI SDK abstracts image generation into a single `images.generate()` call, and how to handle its base64 image response.
- The basic lifecycle of a minimal AI client app: configure → authenticate → call model → handle response → persist output.

---

## How This Fits My AI Engineering Learning Path

This exercise builds directly on the core AI engineering skill set I've been developing:

- **Multi-modal AI exposure** — complements prior work with text-based LLMs (chat, RAG) by covering image generation, broadening my hands-on experience across modalities.
- **Cloud AI deployment** — reinforces Microsoft Foundry/Azure AI patterns (model deployment, endpoints, credential-based auth) that are core to the Azure AI-103 certification I'm preparing for.
- **Production-minded habits** — using `DefaultAzureCredential` instead of API keys, and separating configuration (`.env`) from code, reflects practices I want to carry into real AI product work.
- **Foundational building block for agentic systems** — image generation is a tool an AI agent can call; understanding how to wire up and authenticate a single model API is a stepping stone toward building multi-tool, multi-modal agents.