import os
import sys
import json
from playwright.sync_api import Playwright, sync_playwright, expect

LOGIN_URL = "https://www.chess.com/login_and_go?returnUrl=https://www.chess.com/"
FINISH = ".tab-review-start-review-wrapper"
SUMMARY = os.getenv('GITHUB_STEP_SUMMARY')

failed = 0
status = []

with open('bots.json', 'r') as file:
    BOTS = json.load(file)

def run(playwright: Playwright, i) -> None:
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
        page.wait_for_selector(FINISH, timeout=5000)
        #print(f"::notice::BOT {n} successfully reviewed")
        status.append(f"| BOT {n} | ✅ |\n")
    except:
        #print(f"::error::BOT {n} failed to review")
        status.append(f"| BOT {n} | ❌ |\n")
        failed = 1

    # ---------------------
    context.close()
    browser.close()


for i in range(len(BOTS)):
    with sync_playwright() as playwright:
        run(playwright, i)

with open(SUMMARY, 'w') as summary:
    summary.write("# SUMMARY\n\n")
    summary.write("| BOT N | STATUS |\n")
    summary.write("|:-:|:-:|\n")
    summary.writelines(status)

sys.exit(failed)