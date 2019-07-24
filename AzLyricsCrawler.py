# -*- coding: utf-8 -*-

import requests
import bs4

def get_discography(url):
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, features="lxml")
    albums = soup.select(".album") # returns a list of bs4.element.Tag
    
    return albums
    
def main():
    URL = "https://www.azlyrics.com/g/gaslightanthem.html"
    albums = get_discography(URL)
    print(albums[0].getText())

if __name__ == "__main__":
    main()