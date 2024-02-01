import requests
from bs4 import BeautifulSoup

def scrape_artists(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (requests.HTTPError, requests.ConnectionError) as e:
        print(f"Failed to open {url}, Error: {str(e)}")
        return []
    except requests.Timeout as e:
        print(f"Timed out while trying to open the url {url}. Error: {str(e)}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    artist_elements = soup.find_all("div", class_="copy3")

    return [artist.get_text().strip() for artist in artist_elements]

url = "https://mpost.io/midjourney-and-dall-e-artist-styles-dump-with-examples-130-famous-ai-painting-techniques/"
artists = scrape_artists(url)
print(artists)
