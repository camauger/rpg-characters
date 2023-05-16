import itertools
from bs4 import BeautifulSoup
import requests


url = "https://ludomancien.com"  # Replace with the URL of the web page you want to scrape
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
counter = itertools.count()
image_tags = soup.find_all("img")
image_urls = [img["src"] for img in image_tags]
for url in image_urls:
    response = requests.get(url)
    # Extract the image filename from the URL or use a counter to generate a unique filename
    filename = f"image_{next(counter)}.jpg" # Replace with an appropriate filename and extension
    with open(filename, "wb") as file:
        file.write(response.content)