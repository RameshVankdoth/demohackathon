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


# Define comment syntax
def get_comment(file):
    if file.endswith((".py", ".sql", ".yml")) or "dockerfile" in file.lower():
        return "#"
    elif file.endswith((".log", ".txt")):
        return "//"
    elif file.endswith(".md"):
        return "<!--", "-->"
    else:
        return "#"


# Generate 100 random dates between Aug 1, 2024 and Feb 28, 2025
def generate_random_dates(n):
    start = datetime(2024, 8, 1)
    end = datetime(2025, 2, 28)
    return sorted(
        [
            start + timedelta(days=random.randint(0, (end - start).days))
            for _ in range(n)
        ]
    )


# Get 100 commits across the files
random_dates = generate_random_dates(100)

for date in random_dates:
    file = random.choice(files)
    if not os.path.exists(file):
        print(f"❌ File not found: {file}")
        continue

    comment = get_comment(file)
    formatted_date = date.strftime("%Y-%m-%d")

    try:
        with open(file, "a", encoding="utf-8", errors="ignore") as f:
            if isinstance(comment, tuple):
                f.write(
                    f"\n{comment[0]} file updated at {formatted_date} {comment[1]}\n"
                )
            else:
                f.write(f"\n{comment} file updated at {formatted_date}\n")

        subprocess.run(["git", "add", file])

        # Set fake dates for Git
        env = os.environ.copy()
        iso = f"{formatted_date}T10:00:00"
        env["GIT_AUTHOR_DATE"] = iso
        env["GIT_COMMITTER_DATE"] = iso

        msg = f"file updated at {formatted_date}"
        subprocess.run(["git", "commit", "-m", msg], env=env)

    except Exception as e:
        print(f"⚠️ Error updating {file}: {e}")

print("\n✅ 100 commits generated. Push using:\n   git push -u origin main")

# file updated at 2024-08-05
