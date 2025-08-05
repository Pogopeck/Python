import os
import asyncio
import re
from dotenv import load_dotenv
from playwright.async_api import async_playwright

# Load environment variables from .env file
load_dotenv()
sname = os.getenv("IT_NAME")
spass = os.getenv("PRD_PASS")
dsfurl = os.getenv("PRD_URL")

async def main():
    edge_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
    combined_cert_path = "D:\\Chandan\\combined_certificates.crt"  # Not used in this script but kept for reference

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=edge_path,
            headless=False
        )
        context = await browser.new_context(locale='en-US')
        page = await context.new_page()

        # Navigate to DSF URL
        await page.goto(dsfurl)

        # Login flow
        await page.get_by_role("link", name="Login with SSO").click()
        await page.get_by_role("textbox", name="Enter your email, phone, or").click()
        await page.get_by_role("textbox", name="Enter your email, phone, or").fill(sname)
        await page.get_by_role("button", name="Next").click()
        await page.get_by_role("textbox", name="Enter the password for").click()
        await page.get_by_role("textbox", name="Enter the password for").fill(spass)
        await page.get_by_role("button", name="Sign in").click()
        await page.get_by_role("button", name="No").click()

        # Handle popup window
        async with page.expect_popup() as page1_info:
            await page.get_by_role("button", name="Click to trigger the search").click()
        page1 = await page1_info.value

        # Interact with popup page
        locator = page1.locator('[data-test-id="202006091432210525478"] [data-test-id="2016122110475608391271"]')
        await locator.click()
        await locator.fill("dsf-*")
        await locator.press("Enter")

        # Wait for the page to load results
        await page.wait_for_timeout(5000)

        import re
        import logging

        try:
            # Locate the element containing the result count text
            result_text_locator = page.locator("text=/\\d+ results/").first

            # Wait for it to be visible
            await result_text_locator.wait_for(state="visible", timeout=30000)

            # Get the full text content
            full_text = await result_text_locator.text_content()
            logging.info(f"Found result count text: {full_text}")

            # Extract the number using regex
            match = re.search(r"(\d+)\s+results", full_text)
            if match:
                result_count = int(match.group(1))
                print(f"✅ Extracted result count: {result_count}")
            else:
                print("❌ Could not extract result count from text.")

        except Exception as e:
            logging.error(f"Error while extracting result count: {e}")
            print("❌ Failed to extract result count due to an error.")

        await page.pause()

        # Close browser
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
