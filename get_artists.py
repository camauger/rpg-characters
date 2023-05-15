import requests
from bs4 import BeautifulSoup


url = "https://mpost.io/midjourney-and-dall-e-artist-styles-dump-with-examples-130-famous-ai-painting-techniques/"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

artists = []
artist_elements = soup.find_all("div", class_="copy3")

for artist_element in artist_elements:
    artist_name = artist_element.get_text().strip()
    artists.append(artist_name)

print(artists)

