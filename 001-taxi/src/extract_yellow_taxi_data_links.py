"""
Pull all the links to download NYC Yellow Taxi records
"""
import re
import requests
from bs4 import BeautifulSoup

URL = "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page"
# the link may end with one or more spaces
PATTERN = re.compile(r'https://[a-zA-Z0-9]+\.cloudfront\.net/trip-data/yellow_tripdata_\d{4}-\d{2}\.parquet\s*')


def keep_it(link):
    if link.get("href"):
        return PATTERN.match(link.get("href"))
    return False


def main():
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.find_all("a")
    for link in sorted([ link.get("href") for link in links if keep_it(link) ]):
        print(link)


if __name__ == "__main__":
    main()
