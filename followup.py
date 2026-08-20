import os
import sys
import argparse
from datetime import datetime

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

def generate_followup(company_name: str, role_title: str, candidate_name: str, email: str, phone: str = "") -> str:
    """Generate a clean, high-conversion follow-up outreach email draft."""
    return f"""======================================================================
📧 OUTREACH DRAFT: {company_name.upper()} ({role_title})
======================================================================
Subject: Application Follow-Up — {role_title} — {candidate_name}

Hi {company_name} Hiring Team,

I hope your week is going well.

I recently submitted my application for the {role_title} role at {company_name}. 
Given my background in technical systems analysis, QA automation, and infrastructure resilience, I wanted to reiterate my strong enthusiasm for joining your team.

Please let me know if you need any additional portfolio examples, technical writeups, or documentation from my end.

Best regards,

{candidate_name}
{email}{f' | {phone}' if phone else ''}
======================================================================
"""

def main():
    parser = argparse.ArgumentParser(description="Automated Career Follow-Up Draft Generator")
    parser.add_argument("--company", "-c", required=True, help="Target company name (e.g. Acme Corp)")
    parser.add_argument("--role", "-r", default="Technical Analyst / QA Engineer", help="Role title applied for")
    parser.add_argument("--name", "-n", default="Rishad Haque", help="Candidate full name")
    parser.add_argument("--email", "-e", default="rishad@rishadhaque.com", help="Candidate contact email")
    parser.add_argument("--phone", "-p", default="", help="Candidate contact phone (optional)")
    parser.add_argument("--log", "-l", action="store_true", help="Log application submission to applications_log.txt")
    
    args = parser.parse_args()
    
    draft = generate_followup(args.company, args.role, args.name, args.email, args.phone)
    print(draft)
    
    if args.log:
        log_line = f"[{datetime.now().isoformat()}] COMPANY={args.company} | ROLE={args.role} | STATUS=SUBMITTED\n"
        with open("applications_log.txt", "a", encoding="utf-8") as f:
            f.write(log_line)
        print("📁 Logged submission event to 'applications_log.txt'")

if __name__ == "__main__":
    main()
