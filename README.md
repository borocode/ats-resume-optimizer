# 📄 ATS Resume Optimizer & Career Pipeline

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![AI Providers](https://img.shields.io/badge/AI_Providers-Gemini_|_Ollama_|_OpenAI-orange.svg)](#supported-ai-providers)

An automated, privacy-first **Applicant Tracking System (ATS) Resume Optimizer** and career pipeline CLI.

Tailor your Master Resume against any job description to achieve a **95%+ ATS match score** while strictly maintaining 100% factual integrity (no hallucinated companies, degrees, or false experience).

---

## ⚡ Features

* 🎯 **95%+ ATS Keyword Optimization:** Automatically scans job descriptions for high-weight keywords, required tech stacks, and domain skills, realigning your experience bullet points to pass recruiter filters (Workday, Greenhouse, Lever, Taleo).
* 📊 **ATS Telemetry Report:** Every run generates an executive summary showing estimated match score (0–100%), keywords emphasized, and strategic revisions made.
* 🔒 **100% Privacy & Zero Lock-In:** Runs locally on your machine.
* 🤖 **Multi-Model / BYOK Support:**
  * **Google Gemini** (Free Tier default — 15 RPM free from [Google AI Studio](https://aistudio.google.com/))
  * **Ollama** (100% offline, local, private — `llama3`, `deepseek-r1`, `qwen2.5`)
  * **OpenAI / Claude / Groq** (Standard API key fallback)
* 📧 **Automated Follow-Up Generator:** Generates high-conversion, professional follow-up emails tailored to the hiring team and logs submission timelines.

---

## 🚀 Quickstart

### 1. Clone & Install
```bash
git clone https://github.com/borocode/ats-resume-optimizer.git
cd ats-resume-optimizer
```

### 2. Configure Your API Key (Optional for Local Ollama)
Create a `.env` file in the project root:
```env
# Free API key from https://aistudio.google.com/
GEMINI_API_KEY=your_gemini_api_key_here

# Or OpenAI / Anthropic (if using those providers)
OPENAI_API_KEY=your_openai_key_here
```

### 3. Optimize Your Resume
```bash
# Using Google Gemini (Default / Free tier)
python optimizer.py --resume my_master_resume.md --job target_job_description.txt --output tailored_resume.md

# Using 100% Offline Local Ollama (Zero API keys required)
python optimizer.py --resume my_master_resume.md --job target_job_description.txt --provider ollama --model llama3

# Using OpenAI GPT-4o-mini
python optimizer.py --resume my_master_resume.md --job target_job_description.txt --provider openai
```

### 4. Generate Follow-Up Email & Log Application
```bash
python followup.py --company "NovaSync Digital Labs" --role "QA Analyst" --name "Rishad Haque" --email "rishad@boroghor.com" --log
```

---

## 📋 Example ATS Telemetry Report

Each generated resume begins with a detailed breakdown:

```markdown
# 📊 ATS Optimization Report

- **Target Role:** QA Analyst / Automation Specialist (NovaSync Digital Labs)
- **Estimated Match Score:** 98/100
- **Keywords Added / Emphasized:** Test Lifecycle, Test Case Design & Execution, Defect Logging, JIRA, Regression Testing, Functional Testing, Smoke Testing, Agile/Scrum Sprints, Traceability Matrices, API Testing, Postman, Linux CLI, Git CI/CD, SQL Data Integrity.
- **Strategic Revisions:** 
  - Restructured bullet points to emphasize sole QA pipeline ownership and zero-defect healthcare software releases.
  - Aligned technical skills hierarchy with NovaSync's required stack (Postman, Linux CLI, Git, JIRA).
  - Preserved all sovereign systems projects (Bitcoin/Lightning node operations and FFmpeg streaming suites) as real-world proof of self-directed technical execution.
```

Explore full sample files in [`examples/`](examples/):
- [`examples/master_resume.md`](examples/master_resume.md) — Comprehensive Master Resume template.
- [`examples/jobs/qa_automation_analyst.txt`](examples/jobs/qa_automation_analyst.txt) — Sample target job description.
- [`examples/outputs/tailored_qa_analyst.md`](examples/outputs/tailored_qa_analyst.md) — Tailored output with 98% match.

---

## 🛠️ CLI Options

```text
usage: optimizer.py [-h] --resume RESUME --job JOB [--output OUTPUT] [--provider {gemini,ollama,openai}] [--model MODEL]

options:
  -h, --help            show this help message and exit
  --resume RESUME, -r RESUME
                        Path to your master resume file (Markdown or text)
  --job JOB, -j JOB     Path to target job description file
  --output OUTPUT, -o OUTPUT
                        Output file path (default: tailored_resume.md)
  --provider {gemini,ollama,openai}, -p {gemini,ollama,openai}
                        LLM Provider (default: gemini)
  --model MODEL, -m MODEL
                        Specific model name (e.g. llama3, deepseek-r1, gpt-4o-mini)
```

---

## 📜 License

MIT License. Crafted with sovereignty by [Boro Code](https://github.com/borocode) / [boroghor.com](https://boroghor.com).
