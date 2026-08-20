import os
import sys
import json
import argparse
import urllib.request
import urllib.error

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

def load_env():
    """Load GEMINI_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY, etc. from .env if present."""
    env_paths = [".env", "../.env", "../../.env", os.path.expanduser("~/.env")]
    for path in env_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip('"').strip("'")
                        if k not in os.environ:
                            os.environ[k] = v

def call_gemini(prompt: str, api_key: str) -> str:
    """Call Google Gemini API (gemini-1.5-flash or gemini-2.0-flash)."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 4096
        }
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        return res["candidates"][0]["content"]["parts"][0]["text"]

def call_ollama(prompt: str, model: str = "llama3") -> str:
    """Call local offline Ollama instance."""
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.3}
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        return res.get("response", "")

def call_openai(prompt: str, api_key: str, model: str = "gpt-4o-mini") -> str:
    """Call OpenAI compatible API."""
    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an expert ATS (Applicant Tracking System) optimizer and career consultant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        return res["choices"][0]["message"]["content"]

def optimize_resume(master_resume: str, job_description: str, provider: str = "gemini", model_name: str = None) -> str:
    load_env()
    
    prompt = f"""
You are an expert ATS (Applicant Tracking System) optimization algorithm and executive tech resume consultant.
Your objective is to tailor the candidate's Master Resume to achieve an estimated 95%+ ATS match score for the provided Job Description, while preserving 100% factual integrity.

=== MASTER RESUME DATA ===
{master_resume}

=== TARGET JOB DESCRIPTION ===
{job_description}

=== INSTRUCTIONS ===
1. Analyze the Job Description for core keywords, tech stack, soft skills, and exact phrasing preferred by modern ATS parsers (Workday, Greenhouse, Lever, Taleo).
2. Restructure the Master Resume experience bullet points to lead with strong action verbs and directly reflect the required competencies.
3. STRICT RULE: Do not invent false companies, educational degrees, or titles. All dates, positions, and company history must remain factually true to the Master Resume.
4. Add an ATS Executive Telemetry Header at the top formatted as:
   ```markdown
   # 📊 ATS Optimization Report
   - **Target Role:** [Title extracted from JD]
   - **Estimated Match Score:** [e.g. 96/100]
   - **Primary Keywords Emphasized:** [Comma-separated key skills]
   - **Strategic Revisions:** [2-3 bullet points detailing modifications]
   ---
   ```
5. Followed by the complete, fully tailored Markdown resume ready for submission.
"""

    if provider == "gemini":
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set. Get a free key at https://aistudio.google.com/")
        return call_gemini(prompt, api_key)
        
    elif provider == "ollama":
        model = model_name or "llama3"
        return call_ollama(prompt, model)
        
    elif provider == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")
        model = model_name or "gpt-4o-mini"
        return call_openai(prompt, api_key, model)
        
    else:
        raise ValueError(f"Unsupported provider: {provider}. Supported: gemini, ollama, openai")

def main():
    parser = argparse.ArgumentParser(description="ATS Resume Optimizer — Tailor your master resume to job descriptions with 95%+ ATS score.")
    parser.add_argument("--resume", "-r", required=True, help="Path to your master resume file (Markdown or text)")
    parser.add_argument("--job", "-j", required=True, help="Path to target job description file")
    parser.add_argument("--output", "-o", default="tailored_resume.md", help="Output file path (default: tailored_resume.md)")
    parser.add_argument("--provider", "-p", default="gemini", choices=["gemini", "ollama", "openai"], help="LLM Provider (default: gemini)")
    parser.add_argument("--model", "-m", help="Specific model name (e.g. llama3, deepseek-r1, gpt-4o-mini)")
    
    args = parser.parse_args()

    if not os.path.exists(args.resume):
        print(f"Error: Resume file not found at '{args.resume}'")
        sys.exit(1)

    if not os.path.exists(args.job):
        print(f"Error: Job description file not found at '{args.job}'")
        sys.exit(1)

    with open(args.resume, "r", encoding="utf-8") as f:
        master_resume = f.read()

    with open(args.job, "r", encoding="utf-8") as f:
        job_desc = f.read()

    print(f"⚡ Optimizing resume against job description via [{args.provider.upper()}]...")
    try:
        tailored = optimize_resume(master_resume, job_desc, provider=args.provider, model_name=args.model)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(tailored)
        print(f"✅ Success! Tailored resume with ATS telemetry report saved to: {args.output}")
    except Exception as e:
        print(f"❌ Error during optimization: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
