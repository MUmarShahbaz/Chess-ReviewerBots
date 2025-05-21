import os
import sys
import json
from playwright.sync_api import Playwright, sync_playwright, expect

LOGIN_URL = "https://www.chess.com/login_and_go?returnUrl=https://www.chess.com/"
FINISH = ".tab-review-start-review-wrapper"

JOB = int(os.getenv("JOB"))
OFFSET = (JOB - 1)*5

with open('bots.json', 'r') as file:
    BOTS = json.load(file)

def run(playwright: Playwright, i, idx) -> None:
    global failed
    global status

    n = i + 1

    bot_key = list(BOTS.keys())[i]
    bot_username = BOTS[bot_key].get("user", "")
    bot_password = BOTS[bot_key].get("pass", "")

    with open("urls.txt", 'r') as file:
        lines = file.readlines()
        if 1 <= n <= len(lines):
            review_url = lines[i].strip()


    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(LOGIN_URL)
    page.get_by_role("textbox", name="Username, Phone, or Email").click()
    page.get_by_role("textbox", name="Username, Phone, or Email").fill(bot_username)
    page.get_by_role("textbox", name="Password").click()
    page.get_by_role("textbox", name="Password").fill(bot_password)
    page.get_by_role("button", name="Log In").click()
    page.goto(review_url)
    try:
        page.wait_for_selector(FINISH, timeout=10000)
        status[idx] = 0
    except:
        status[idx] = 1

    # ---------------------
    context.close()
    browser.close()




# MAIN CODE

start = OFFSET
end = min(OFFSET + 5, len(BOTS))
status = [1] * (end - start)  # Only for this chunk

for idx, bot_num in enumerate(range(start, end)):
    print(f"\tRunning BOT {bot_num + 1}")
    with sync_playwright() as playwright:
        run(playwright, bot_num, idx)
    print(f"\tBOT {bot_num + 1} status: {'Failed' if status[idx] else 'Succeeded'}\n")

# Write per-chunk summary file for artifact upload
with open(f"summary_{JOB}.txt", 'w') as summary:
    for idx, bot_num in enumerate(range(start, end)):
        summary.write(f"{bot_num + 1},{status[idx]}\n")

sys.exit(sum(status))