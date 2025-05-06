import os
import sys
import json
import time
from playwright.sync_api import Playwright, sync_playwright, expect

LOGIN_URL = "https://www.chess.com/login_and_go?returnUrl=https://www.chess.com/"
FINISH = ".tab-review-start-review-wrapper"
SUMMARY = os.getenv('GITHUB_STEP_SUMMARY')

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
        page.wait_for_selector(FINISH, timeout=10000)
        status[i] = 0
    except:
        status[i] = 1

    # ---------------------
    context.close()
    browser.close()




# MAIN CODE

status = [1] * len(BOTS) # 1 means failed
iteration_counter = 1

# Iterative Solver
while sum(status) > 0 and iteration_counter <= 3:
    print(f"\nIteration {iteration_counter}:")
    for bot_num in range(len(status)):
        if status[bot_num]:
            print(f"\tRunning BOT {bot_num + 1}")
            with sync_playwright() as playwright:
                run(playwright, bot_num)
            print(f"\tBOT {bot_num + 1} status: { "Failed" if status[bot_num] else "Succeeded" }\n")
    iteration_counter = iteration_counter + 1
    time.sleep(10)


with open(SUMMARY, 'w') as summary:
    summary.write("# SUMMARY\n\n")
    summary.write("| BOT N | STATUS |\n")
    summary.write("|:-:|:-:|\n")
    for i in range(len(status)):
        if status[i]:
            summary.write(f"| BOT {i + 1} | ❌ |\n")
        else:
            summary.write(f"| BOT {i + 1} | ✅ |\n") 

sys.exit(sum(status))
