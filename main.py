import asyncio
import random
from playwright.async_api import async_playwright

USERNAME = "nalinnishant.dev@gmail.com"
PASSWORD = "xxx"
descriptions = [
    "Software Engineer with expertise in Java, Spring Boot, Microservices, AWS, SQL, REST APIs, and System Design.",
    "Backend Developer skilled in Java, Hibernate, Spring MVC, Kafka, Docker, and Application Development.",
    "Fullstack Developer with experience in Java, React.js, HTML, CSS, SQL, and Microservices Architecture.",
    "Experienced Software Engineer proficient in Data Structures, Algorithms, C++, Java, Debugging, and Project Execution.",
    "Developer with hands-on skills in Java, Spring Boot, API Integration, AWS, HLD, and Fullstack Development."
]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # keep false for now
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113 Safari/537.36",
            locale="en-US",
            viewport={"width": 1280, "height": 800},
            java_script_enabled=True
        )
        page = await context.new_page()

        # Hide automation fingerprint
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        await page.goto("https://www.naukri.com/nlogin/login", wait_until="networkidle")

        await page.screenshot(path="debug.png")
        await page.fill("#usernameField", USERNAME)
        await page.fill("#passwordField", PASSWORD)
        await page.click("button[type='submit']")

        await page.wait_for_timeout(5000)

        # Go to profile
        await page.goto("https://www.naukri.com/mnjuser/profile", wait_until="networkidle")

        # Wait for page to load
        await page.wait_for_timeout(5000)

        # Optionally update mobile number
        try:
            await page.click("//*[@id='lazyResumeHead']/div/div/div[1]/span[2]")
            #//*[@id="resumeHeadlineTxt"]
            await page.fill("//*[@id='resumeHeadlineTxt']", random.choice(descriptions))
            #/html/body/div[6]/div[8]/div[2]/form/div[3]/div/button
            await page.click("//button[@class='btn-dark-ot' and text()='Save']")
        except:
            pass

        await page.wait_for_timeout(5000)
        # Upload Resume (Assuming file input is present)
        await page.set_input_files("#attachCV", "Resume_SDE_Nalin.pdf")

        await page.wait_for_timeout(5000)

        print("Resume updated successfully.")

        await browser.close()


asyncio.run(main())
