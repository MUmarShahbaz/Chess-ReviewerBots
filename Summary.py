import os
SUMMARY = os.getenv('GITHUB_STEP_SUMMARY')

with open('all_summaries.txt', 'r') as f:
    status = [line.strip().split(',') for line in f if line.strip()]

with open(SUMMARY, 'w', encoding='utf-8') as summary:
    summary.write("# SUMMARY\n\n")
    summary.write("| BOT N | STATUS |\n")
    summary.write("|:-:|:-:|\n")
    for bot, stat in status:
        if int(stat):
            summary.write(f"| BOT {bot} | ❌ |\n")
        else:
            summary.write(f"| BOT {bot} | ✅ |\n")

