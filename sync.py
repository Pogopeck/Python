## To take a screenshot using playwright 
#launch(headless=False) is not working with codespace in line 7 e.g browser = p.chromium.launch(headless=False)
# pip install --upgrade pip 
# pip install playwright
# playwright install

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://whatmyuseragent.com/")
    page.screenshot(path="demo.png")
    browser.close()
