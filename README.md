# Marketing Campaign Agent (Google ADK + Gemini + Imagen)

An AI agent that plans and produces complete marketing campaigns end-to-end using Google ADK. It analyzes the brief, generates strategy and taglines, develops a visual concept, creates a high‑quality image with Imagen, and compiles a final report.

## Overview
- Core agent: `marketing_agent.root_agent` (Gemini model orchestration + tools)
- Output: images and conversation history saved under `output/`

## 🎯 Features

This AI agent executes a systematic five‑step campaign creation process:

1. Market Strategy Development — analyzes audience, defines strategy, and identifies key messaging
2. Tagline & Slogan Generation — creates 5 compelling taglines with psychological justifications
3. Visual Concept Creation — selects the best tagline and develops detailed visual briefs
4. Image Generation — produces campaign images via Google Imagen 4 API
5. Final Campaign Report — compiles all artifacts into a comprehensive markdown deliverable

### ✨ Image Generation with Imagen
- Uses Google Imagen 4 model (`imagen-4.0-generate-preview-06-06`) via `google-genai`
- 16:9 marketing-friendly composition encouraged by the prompt
- Images saved automatically to `output/campaign_image_[timestamp].png`
- Graceful fallback with an explanatory status if generation fails

## Tech Stack
- Language: Python
- Framework/SDK: Google ADK (Agents/Tools runner)
- Models & APIs: Gemini (text reasoning), Imagen 4 (image generation) via `google-genai`
- Env management: `python-dotenv`
- Imaging: `Pillow`
- Package manager: `pip` (requirements.txt)

## Requirements
- Python 3.10+ (recommended). TODO: Verify minimum supported version for google-adk in this project.
- Google AI API key with access to the Gemini/Imagen models.

## Setup
1. Create and activate a virtual environment (Windows PowerShell):
   - py -3 -m venv .venv
   - .\.venv\Scripts\Activate.ps1
2. Install dependencies:
   - pip install -r requirements.txt
3. Configure environment variables (create a `.env` file in the project root):
   - GOOGLE_API_KEY=your_api_key_here
   - Get an API key: https://aistudio.google.com/app/apikey

## Run
- ADK Web UI (inspect/drive the agent in a browser):
  - adk web
  - Go to http://localhost:8000 in your browser

- In the UI, select the agent "marketing_agent" and provide your campaign brief.

## Scripts & Entry Points
- agent package: `marketing_agent` — exposes `root_agent` in `__init__.py`
- tools implemented in `marketing_agent/agent.py`:
  - analyze_market_strategy
  - generate_taglines
  - develop_visual_concept
  - generate_campaign_image (Imagen 4)
  - generate_campaign_report

## Environment Variables
- GOOGLE_API_KEY (required) — Google AI key used by ADK/GenAI clients

## Outputs
- Images: `output/campaign_image_*.png`
- Conversation history: `output/campaign_conversation.txt` (saved after a run)

## Tests
- No tests are included yet. TODO: Add unit tests and an end‑to‑end smoke test using the ADK runner or Web UI.

## Project Structure
```
.
├─ marketing_agent/
│  ├─ __init__.py            # Exports root_agent
│  └─ agent.py               # Agent definition + tools (strategy, taglines, visual, image, report)
├─ output/                   # Generated artifacts (images, conversation history)
├─ requirements.txt          # Python dependencies
└─ README.md
```

## Examples
Here are a few example briefs you can paste into the ADK Web UI when chatting with the agent:

- Example 1: Eco-friendly water bottle D2C launch
  - Product/Service: Reusable stainless‑steel water bottle with filter
  - Target Audience: Urban professionals 22–35 who care about sustainability and fitness
  - Key Differentiator: Keeps drinks cold 36 hours; built‑in replaceable filter
  - Expected outputs: Market strategy, 5 taglines with psychology, visual brief, an image saved to output, and a final campaign report.

- Example 2: B2B SaaS productivity platform
  - Product/Service: Team productivity suite with AI meeting notes
  - Target Audience: Mid‑size tech companies; team leads and PMs
  - Key Differentiator: One‑click summaries and action items from any meeting recording
  - Expected outputs: Strategy focused on time‑to‑value, 5 taglines, a dashboard‑style visual concept, generated image, and a final report.

- Example 3: Local bakery seasonal promotion
  - Product/Service: Autumn limited‑edition pumpkin‑spice croissant
  - Target Audience: Neighborhood foodies and coffee lovers
  - Key Differentiator: Daily fresh‑baked, locally sourced ingredients
  - Expected outputs: Neighborhood‑centric strategy, cozy fall visual concept, storefront or flat‑lay image, and a final report.


## Troubleshooting
- Missing API key:
  - Symptom: "GOOGLE_API_KEY environment variable not set" on startup
  - Fix: Create .env with `GOOGLE_API_KEY=...` or set it in your environment
- Import errors for ADK:
  - Fix: pip install google-adk==1.15.1
- Image not generated:
  - The run will still complete with a status message. Check API quotas/billing and try again, or refine the visual brief.


## Approximate Cost
- This agent uses Gemini for text reasoning and Imagen 4 for image generation. Each complete campaign typically triggers several text generations and one image render.
- Typical single run: about 3–6 text calls + 1 image.

Rough cost guidance (always verify current pricing on Google's site):
- Gemini text generations: commonly a few cents per run depending on prompt/response length. As a ballpark, expect roughly $0.02–$0.20 for short briefs and $0.20–$1.00 for long/verbose briefs.
- Imagen 4 image generation: per‑image pricing varies by model/version and region; a conservative ballpark is ~$0.02–$0.25 per image for preview/low‑res tiers. Higher quality or different tiers may cost more.

Estimated total per campaign run:
- Light usage (short brief): ~$0.05–$0.30
- Heavier usage (long brief + rich outputs): ~$0.30–$1.25

Notes:
- Prices vary by model selection, tokens used, resolution, region, volume, and Google plan. Treat these numbers as estimates only.
- Check the official pricing page for up‑to‑date details: https://ai.google.dev/pricing
- You can reduce cost by limiting max tokens, shortening briefs, or skipping image generation.
