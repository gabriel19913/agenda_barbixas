import asyncio
from playwright.async_api import async_playwright, TimeoutError
import time

def clean_text(text):
    return text.replace("\t", "").replace("\n\n\n\n", " ").replace("\n\n\n", "").strip()

async def get_agenda(playwright):
    url = "https://barbixas.com.br"
    chromium = playwright.chromium
    browser = await chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()
    await page.set_viewport_size({"width": 1920, "height": 1080})
    await page.goto(url)
    time.sleep(2)
    # await page.locator("//span[@class='elementor-button-text']").click()
    # try:
        # while True:
    try:
        while await page.get_by_text("Carregar mais").is_visible():
            await page.locator("text=Carregar mais").click(timeout=30000, force=True)
            await asyncio.sleep(1)
    except TimeoutError:
        pass
    print("TA FORAAAAA")
    dates = page.locator("//div[@class='elementor-column elementor-col-33 elementor-top-column elementor-element elementor-element-325dcc9']")
    shows = page.locator("//div[@class='elementor-column elementor-col-33 elementor-top-column elementor-element elementor-element-ccc2430']")
    links = page.locator("//a[@class='elementor-button elementor-button-link elementor-size-sm elementor-animation-shrink']")
    count = await dates.count()
    list_dates = []
    list_shows = []
    list_shows_clean = []
    list_links = []
    for i in range(count):
        element = dates.nth(i)
        text_content = await element.text_content()
        text_content = clean_text(text_content)
        text_content_list = text_content.split(" ")
        text_content_list[-1] = f"({text_content_list[-1]})"
        date_string = " ".join(text_content_list)
        list_dates.append(date_string)
        
        show = shows.nth(i)
        text_content_shows = await show.text_content()
        text_content_shows = clean_text(text_content_shows)
        list_shows.append(text_content_shows)
        
        link = links.nth(i)
        text_content_link = await link.get_attribute('href')
        list_links.append(text_content_link)
        
    for item in list_shows:
        clean_item = item.replace("/*! elementor - v3.22.0 - 16-06-2024 */\n.elementor-heading-title{padding:0;margin:0;line-height:1}.elementor-widget-heading .elementor-heading-title[class*=elementor-size-]>a{color:inherit;font-size:inherit;line-height:inherit}.elementor-widget-heading .elementor-heading-title.elementor-size-small{font-size:15px}.elementor-widget-heading .elementor-heading-title.elementor-size-medium{font-size:19px}.elementor-widget-heading .elementor-heading-title.elementor-size-large{font-size:29px}.elementor-widget-heading .elementor-heading-title.elementor-size-xl{font-size:39px}.elementor-widget-heading .elementor-heading-title.elementor-size-xxl{font-size:59px}", "")
        list_shows_clean.append(clean_item)
    # shows = page.locator("//div[@class='elementor-column elementor-col-33 elementor-top-column elementor-element elementor-element-ccc2430']")
    print(list_links)
    time.sleep(200000)
    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await get_agenda(playwright)

asyncio.run(main())
