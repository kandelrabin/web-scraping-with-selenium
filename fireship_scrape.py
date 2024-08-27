from selenium import webdriver
from time import sleep
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


ENDPOINT = "https://www.youtube.com/@Fireship/videos"
videos_data = []

driver = webdriver.Chrome()
driver.get(ENDPOINT)
sleep(3)

html = driver.find_element(By.TAG_NAME, 'html')
for i in range(4):
    html.send_keys(Keys.END)

    # Wait for the page to fully render.
    sleep(3)

video_elements = driver.find_elements(By.TAG_NAME, 'ytd-rich-grid-media')

for video in video_elements:
    container = video.find_element(By.XPATH, './/div[@id="dismissible"]')
    url = container.find_element(By.XPATH, './/a[@id="video-title-link"]').get_attribute('href')
    duration = container.find_element(By.XPATH, './/div[@id="time-status"]/span').get_attribute('aria-label')
    title = container.find_element(By.XPATH, './/h3/a/yt-formatted-string').text
    metadata = container.find_elements(By.CSS_SELECTOR, 'span.inline-metadata-item')
    views = metadata[0].text
    uploaded = metadata[1].text
    videos_data.append(
        {
            "url": url,
            "duration":  duration,
            "title" : title,
            "views": views,
            "uploaded" : uploaded
        }
    )

driver.close()

with open('fireship.json', 'w') as f:
    json.dump(videos_data, f, ensure_ascii=False)