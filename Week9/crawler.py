import requests
from bs4 import BeautifulSoup


def extract_news_titles(query, num_pages):
    titles = []

    for page in range(num_pages):
        url = f"https://www.google.com/search?gl=us&q={query}&tbm=nws&start={page*10}&hl=en"

        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if there was an error

        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all the news title elements
        news_titles = soup.find_all("h3", class_="zBAuLc")

        # Extract the text from the news title elements
        titles.extend([title.text for title in news_titles])

    return titles


if __name__ == "__main__":
    # Example usage
    query = "TESLA"
    num_pages = 3  # Fetch news titles from 3 pages (30 titles in total)
    news_titles = extract_news_titles(query, num_pages)

    # Process the extracted news titles
    for title in news_titles:
        # Perform your desired processing on each title
        print(title)
