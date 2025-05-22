from fastapi import FastAPI
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from proxy_plugin import create_proxy_extension
import time

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Job scraper is live!"}

@app.get("/scrape")
def scrape_jobs():
    # Proxy credentials
    proxy_host = "geo.iproyal.com"
    proxy_port = "12321"
    proxy_user = "6Bk04u9eWn8IH8Ug"
    proxy_pass = "rOQtoGgpyHhSDEn3"

    # Create extension
    plugin_path = create_proxy_extension(proxy_host, proxy_port, proxy_user, proxy_pass)

    # Start browser
    driver = Driver(uc=True, extension_dir=plugin_path)
    url = "https://ca.indeed.com/jobs?q=software+engineer&l=toronto%2C+on"
    driver.uc_open_with_reconnect(url, 10)

    time.sleep(5)
    try:
        driver.uc_gui_click_captcha()
    except Exception:
        pass

    time.sleep(5)

    jobs = []
    job_cards = driver.find_elements(By.CLASS_NAME, "job_seen_beacon")
    for card in job_cards[:10]:
        try:
            title = card.find_element(By.CSS_SELECTOR, "h2.jobTitle span").text.strip()
            company = card.find_element(By.CSS_SELECTOR, "[data-testid='company-name']").text.strip()
            location = card.find_element(By.CSS_SELECTOR, "[data-testid='text-location']").text.strip()
            jobs.append({"title": title, "company": company, "location": location})
        except:
            continue

    driver.quit()
    return {"count": len(jobs), "jobs": jobs}
