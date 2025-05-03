import re
from playwright.sync_api import Playwright, sync_playwright, expect
import os

bot_username = os.getenv("USERNAME")
bot_password = os.getenv("PASSWORD")
index = int(os.getenv("BOT_NUMBER"))

LOGIN_URL = "https://www.chess.com/login_and_go?returnUrl=https://www.chess.com/"
FINISH = ".tab-review-start-review-wrapper"

with open("urls.txt", 'r') as file:
    lines = file.readlines()
    if 1 <= index <= len(lines):
        review_url = lines[ index - 1].strip()

def run(playwright: Playwright) -> None:
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
        print(f"Successfully reviewed")
    except:
        print(f"Failed to review")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)