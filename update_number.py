#!/usr/bin/env python3
"""
Daily Notes Intelligent Commit System
Windows-compatible version with proper encoding handling
"""

import os
import sys
import random
import subprocess
import re
from datetime import datetime
from pathlib import Path

# Force UTF-8 encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configuration
USE_LLM = os.environ.get("FANCY_JOB_USE_LLM", "false").lower() == "true"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

# Realistic commit types and scopes for daily notes
COMMIT_TYPES = [
    "feat", "fix", "docs", "style", "refactor", 
    "test", "chore", "perf", "ci", "build", "revert"
]

COMMIT_SCOPES = [
    "journal", "practice", "notes", "docs", "examples",
    "algorithms", "data-structures", "python", "javascript",
    "learning", "review", "exercises", "projects"
]

COMMIT_ACTIVITIES = [
    "daily learning session",
    "practice exercise",
    "code examples",
    "algorithm practice",
    "data structures",
    "problem solving",
    "coding challenge",
    "review notes",
    "update journal",
    "add examples",
    "learning progress",
    "documentation",
    "code practice",
    "knowledge base",
    "study notes"
]

def safe_write_file(filepath, content):
    """Write file with UTF-8 encoding"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def get_llm_commit_message():
    """Generate intelligent commit message using GPT-2"""
    try:
        from transformers import pipeline, set_seed
        import torch
        
        generator = pipeline(
            'text-generation',
            model='openai-community/gpt2',
            device=-1,
            torch_dtype=torch.float32
        )
        set_seed(random.randint(1, 1000))
        
        date_str = datetime.now().strftime("%Y-%m-%d")
        day_name = datetime.now().strftime("%A")
        
        prompts = [
            f"""Generate a realistic Git commit message for a daily learning journal on {day_name}, {date_str}.
The commit should follow Conventional Commits format with a type, scope, and subject.

Examples:
- feat(journal): document Python decorators learning
- docs(practice): add solutions for array problems
- chore(notes): update daily learning log

Commit message:""",

            f"""Create a commit message for daily coding practice on {date_str}.
Focus on: algorithms, data structures, Python, or JavaScript.

Example: "feat(algorithms): implement binary search practice"

Commit message:"""
        ]
        
        prompt = random.choice(prompts)
        
        generated = generator(
            prompt,
            max_new_tokens=30,
            num_return_sequences=2,
            temperature=0.85,
            top_k=40,
            top_p=0.9,
            do_sample=True,
            pad_token_id=50256,
            repetition_penalty=1.1
        )
        
        for text in [g['generated_text'] for g in generated]:
            if prompt in text:
                commit_msg = text.split(prompt)[-1].strip()
            else:
                commit_msg = text.strip()
            
            commit_msg = clean_commit_message(commit_msg)
            
            if commit_msg and len(commit_msg) > 5:
                return f"{commit_msg} [{date_str}]"
        
        return get_fallback_message()
        
    except Exception as e:
        print(f"Warning: LLM Error: {e}")
        return get_fallback_message()

def clean_commit_message(msg):
    """Clean and format the generated commit message"""
    msg = msg.strip('"\'.,!?')
    msg = ' '.join(msg.split())
    
    patterns = [
        r'^Commit message:',
        r'^Message:',
        r'^Example:',
        r'^Format:'
    ]
    for pattern in patterns:
        msg = re.sub(pattern, '', msg, flags=re.IGNORECASE)
    
    if not re.match(r'^[a-z]+(\([a-z-]+\))?:', msg):
        commit_type = random.choice(COMMIT_TYPES)
        scope = random.choice(COMMIT_SCOPES)
        msg = f"{commit_type}({scope}): {msg}"
    
    if len(msg) > 72:
        msg = msg[:69] + "..."
    
    return msg.strip()

def get_fallback_message():
    """Generate realistic commit without LLM"""
    commit_type = random.choice(COMMIT_TYPES)
    scope = random.choice(COMMIT_SCOPES)
    activity = random.choice(COMMIT_ACTIVITIES)
    
    if random.random() < 0.3:
        day_num = datetime.now().day
        return f"{commit_type}({scope}): {activity} - day {day_num}"
    elif random.random() < 0.5:
        return f"{commit_type}({scope}): {activity}"
    else:
        return f"{commit_type}: {activity}"

def get_daily_context():
    """Get context about what to commit based on the day"""
    day = datetime.now().weekday()
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_name = day_names[day]
    
    contexts = {
        "Monday": "start of week, planning and organization",
        "Tuesday": "deep dive into topics, focused practice",
        "Wednesday": "mid-week review and consolidation",
        "Thursday": "advanced topics and challenges",
        "Friday": "week review and project work",
        "Saturday": "personal projects and exploration",
        "Sunday": "reflection and planning for next week"
    }
    
    return contexts.get(day_name, "daily learning practice")

def create_daily_content():
    """Create realistic daily content files (with proper encoding)"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    year = datetime.now().year
    month = datetime.now().month
    day_context = get_daily_context()
    
    # Create journal entry
    journal_dir = Path(f"journal/{year}/{month:02d}")
    journal_dir.mkdir(parents=True, exist_ok=True)
    
    journal_file = journal_dir / f"{date_str}.md"
    if not journal_file.exists():
        content = f"""# Daily Learning - {date_str}

## Focus
- {day_context}
- Practice: {random.choice(['Python', 'JavaScript', 'Data Structures', 'Algorithms', 'System Design'])}
- Duration: {random.randint(30, 120)} minutes

## Notes
- Completed daily practice session
- Reviewed previous concepts
- Working on new examples

## Next Steps
- Continue with learning path
- Practice more examples
- Review and consolidate

---
Generated from daily practice session #{get_number() + 1}
"""
        safe_write_file(journal_file, content)
    
    # Create practice file
    practice_dir = Path("practice")
    practice_dir.mkdir(parents=True, exist_ok=True)
    
    topic = random.choice(['Functions', 'Classes', 'Algorithms', 'Data Structures', 'File I/O'])
    practice_file = practice_dir / f"{year}-{month:02d}-{date_str}.py"
    
    if not practice_file.exists():
        content = f'''#!/usr/bin/env python3
"""
Daily Practice Session - {date_str}
Topic: {topic}
"""

def main():
    """Main practice function"""
    print("Daily Practice Session")
    print(f"Date: {date_str}")
    print("=" * 40)
    
    # Practice code goes here
    examples = [
        "def example_function():",
        "    return 'Hello, World!'",
        "",
        "class PracticeClass:",
        "    def __init__(self):",
        "        self.name = 'Daily Practice'",
        "        self.date = '{date_str}'"
    ]
    
    for line in examples:
        print(line)
    
    return True

if __name__ == "__main__":
    main()
'''
        safe_write_file(practice_file, content)

def get_number():
    """Read current number"""
    try:
        with open("number.txt", "r") as f:
            return int(f.read().strip())
    except:
        return 0

def update_number():
    """Main update function"""
    current = get_number()
    new_number = current + 1
    
    # Create daily content
    create_daily_content()
    
    # Update number
    with open("number.txt", "w") as f:
        f.write(str(new_number))
    
    print(f"Number updated: {current} -> {new_number}")
    
    # Generate commit message
    if USE_LLM:
        print("Generating intelligent commit message with LLM...")
        commit_msg = get_llm_commit_message()
    else:
        commit_msg = get_fallback_message()
    
    # Add date for uniqueness
    date_str = datetime.now().strftime("%Y-%m-%d")
    if not commit_msg.endswith(f"[{date_str}]"):
        commit_msg = f"{commit_msg} [{date_str}]"
    
    # Stage all changes
    subprocess.run(["git", "add", "."], check=False)
    
    # Commit
    result = subprocess.run(
        ["git", "commit", "-m", commit_msg],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(f"Commit created: {commit_msg}")
        return True
    else:
        print(f"Commit failed: {result.stderr}")
        return False

def git_push():
    """Push to GitHub"""
    result = subprocess.run(["git", "push"], capture_output=True, text=True)
    if result.returncode == 0:
        print("Changes pushed to GitHub successfully.")
        return True
    else:
        print("Error pushing to GitHub:")
        print(result.stderr)
        return False

def main():
    """Main execution"""
    try:
        success = update_number()
        if success:
            git_push()
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()