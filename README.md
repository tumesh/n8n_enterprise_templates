# n8n_enterprise_templates
AI Automation Repository 
# Unified n8n Workflow Templates Collection

![n8n Version](https://img.shields.io/badge/n8n-latest-orange?logo=n8n)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-consolidated-blue)

## 📖 Overview

This repository serves as a **consolidated master collection** of n8n workflow templates. It aggregates, de-duplicates, and categorizes workflows from over 10 different open-source collections, providing a single source of truth for automation enthusiasts.

Whether you are looking to automate social media, manage DevOps pipelines, or integrate AI agents, you will find a starter template here.

## 📂 Directory Structure

The workflows are organized by **Category** rather than by source.

| Category | Description |
| :--- | :--- |
| **`/ai`** | LLM chains, OpenAI/ChatGPT integrations, Stable Diffusion, and Vector Store automations. |
| **`/marketing`** | Email marketing, Social Media posting, Lead generation, and SEO tools. |
| **`/devops`** | Server monitoring, Docker management, Git webhooks, and CI/CD pipelines. |
| **`/productivity`** | Notion syncs, Slack/Telegram bots, Task management, and Calendar automations. |
| **`/finance`** | Crypto tracking, Stripe invoicing, and Budget management. |
| **`/uncategorized`** | General utilities, web scrapers, and experimental workflows. |

## 🚀 How to Use These Templates

1.  **Find a Template:** Navigate to the relevant folder (e.g., `/workflows/productivity/slack-daily-standup.json`).
2.  **Copy JSON:** Open the `.json` file and copy the raw content to your clipboard.
3.  **Import to n8n:**
    * Open your n8n editor.
    * Click simply on the canvas and press `Ctrl + V` (or `Cmd + V`).
    * *Alternatively:* Click the **menu** (top right) → **Import from...** → **File**.
4.  **Configure Credentials:** Double-click the nodes that have red warning signs and add your own API credentials.

## 🤝 Credits & Sources

This repository is a consolidation of the amazing work done by the n8n community. Huge thanks and attribution to the original curators:

* **@Salheen10** & **@ritik-prog** (Massive 5000+ collections)
* **@devlikeapro** (Waha integration templates)
* **@lucaswalter** (AI-specific automations)
* **@jz-clln**, **@Danitilahun**, **@creativetimofficial**, **@Marvomatic**, **@wassupjay**, **@enescingoz**

## ⚠️ Disclaimer

* **Review before running:** Always review the nodes in a template before executing. Some templates may require specific n8n versions or community nodes.
* **Credentials:** Never commit your `credentials` or API keys to this repository.

## 📄 License

This compilation is distributed under the MIT License. Individual templates retain the licensing of their original creators/repositories.
