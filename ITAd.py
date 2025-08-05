import os
import asyncio
from dotenv import load_dotenv

load_dotenv()
# Access them using os.getenv
itname = os.getenv("IT_NAME")
itpass = os.getenv("IT_PASS")
dsfurl = os.getenv("DSF_URL")

from playwright.async_api import async_playwright

async def main():  # Added async here
    #os.environ["DEBUG"] = "pw:api"
    edge_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
    ##chrome_path = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    combined_cert_path = "D:\\Chandan\\combined_certificates.crt"
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=edge_path,
            headless=False
        )
        context = await browser.new_context(locale='en-US')
        page = await context.new_page()
        await page.goto(dsfurl)
        await page.get_by_role("textbox", name="User name *").click()
        await page.get_by_role("textbox", name="User name *").fill(itname)
        await page.get_by_role("textbox", name="Password *").click()
        await page.get_by_role("textbox", name="Password *").fill(itpass)
        await page.get_by_role("button", name="Log in").click()

        await page.pause()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())  # Use asyncio.run to execute the async function
