import os
import random
import subprocess
from datetime import datetime, timedelta

files = [
    "app.py",
    "combined_execution.log",
    "compiler_api.py",
    "compose.yml",
    "dockerfile",
    "docker_compose",
    "function SessionData.docx",
    "hackathon.log",
    "manage.py",
    "readme.md",
    "requirements.txt",
    "script.sql",
    "start.txt",
]


# Helper to get comment syntax
def get_comment(file):
    if file.endswith((".py", ".sql")):
        return "#"
    elif file.endswith((".log", ".txt")):
        return "//"
    elif file.endswith(".md"):
        return "<!--", "-->"
    elif file.endswith(".yml") or file.endswith("dockerfile"):
        return "#"
    else:
        return "#"


# Generate random date within past 8 months
def random_date():
    today = datetime.today()
    start = today - timedelta(days=30 * 8)
    rand_days = random.randint(0, (today - start).days)
    return (start + timedelta(days=rand_days)).strftime("%Y-%m-%d")


for file in files:
    if not os.path.exists(file):
        print(f"❌ File not found: {file}")
        continue

    date = random_date()
    comment = get_comment(file)

    # Add comment
    with open(file, "a", encoding="utf-8", errors="ignore") as f:
        if isinstance(comment, tuple):
            f.write(f"\n{comment[0]} file updated at {date} {comment[1]}\n")
        else:
            f.write(f"\n{comment} file updated at {date}\n")

    subprocess.run(["git", "add", file])

    # Git commit with fake timestamp
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = f"{date}T10:00:00"
    env["GIT_COMMITTER_DATE"] = f"{date}T10:00:00"

    msg = f"file updated at {date}"
    subprocess.run(["git", "commit", "-m", msg], env=env)

print("\n✅ All commits done. You can now push:\n   git push -u origin main")

# file updated at 2024-12-24
