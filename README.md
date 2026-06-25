---
title: QueueStorm API
emoji: ⚡
colorFrom: indigo
colorTo: blue
sdk: docker
pinned: false
---

# QueueStorm API - CRM Ticket Triage

An automated, high-performance ticket triage system built with **FastAPI** and powered by **Google Gemini 2.5 Flash**. This application automatically classifies incoming customer support tickets into predefined categories (e.g., Technical Support, Billing, Account Access) and falls back to a precise keyword-matching algorithm if the LLM provider experiences network or credential issues.

---

## 🚀 Live Deployments

- **Primary (Vercel Serverless):** `https://your-vercel-project-url.vercel.app`
- **Secondary / Backup (Hugging Face Docker Space):** `https://meamir-queuestorm-api.hf.space`

---

## ⚙️ Features
- **AI-Powered Triage:** Instant text classification using the lightweight and fast Gemini 2.5 Flash model.
- **Fail-Safe Fallback:** Deterministic regex/keyword matching backup system to ensure zero-downtime routing.
- **High Concurrency:** Asynchronous request handling via ASGI/Uvicorn.
- **Automated Docs:** Self-documenting interactive API playground out of the box.

---

## 🛠️ Local Setup Instructions

If you are a judge or organizer testing this application locally, follow these steps to spin up the server in under 2 minutes.

### 1. Prerequisites
- **Python:** Version 3.9 or higher
- **Credentials:** A valid Google Gemini API Key

### 2. Installation & Environment Configuration
Clone this repository, navigate to the folder, create a virtual environment, and install dependencies:

```bash
# Clone and enter directory
git clone <your-repository-url>
cd SUSTMock

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install -r requirements.txt