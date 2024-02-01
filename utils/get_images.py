import itertools
from bs4 import BeautifulSoup
import requests
import concurrent.futures
from functools import lru_cache

url = "https://ludomancien.com"  # Replace with the URL of the web page you want to scrape
main_response = requests.get(url)
soup = BeautifulSoup(main_response.text, "html.parser")
counter = itertools.count()
image_tags = soup.find_all("img")
image_urls = [img["src"] for img in image_tags]

@lru_cache(maxsize=100)  # Caches responses. Adjust maxsize as needed.
def get_content(url):
    return requests.get(url).content

# Using ThreadPoolExecutor to download images concurrently
with concurrent.futures.ThreadPoolExecutor() as executor:   
    for i, content in zip(image_urls, executor.map(get_content, image_urls)):
        filename = f"image_{next(counter)}.jpg"
        with open(filename, 'wb') as file:
            file.write(content)
