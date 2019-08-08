# -*- coding: utf-8 -*-

import requests
import bs4
import re

def __get_html(url):
    """
    Returns the HTML contents of the specified URL as string.

    Args:
        url: HTML URL as string, 
             e.g. "https://www.azlyrics.com/g/gaslightanthem.html"
    
    Returns:
        string
    
    Raises:
        -
    """
    res = requests.get(url)
    res.encoding = 'utf-8'
    res.raise_for_status()
    return res.text

def __get_discography(html):
    """
    Parses the given html string for tags with a CSS class attribute
    named 'album' and returns a list of all found tags

    Args:
        html: HTML page content as string, 
    
    Returns:
        list of elements of class bs4.element.Tag
    
    Raises:
        -
    """
    soup = bs4.BeautifulSoup(html, features="lxml")
    albums = soup.select("#listAlbum .album") # returns a list of bs4.element.Tag
    albums = [a.getText() for a in albums]
    return albums

def __find_album_position(html, album_name):
    album_name = album_name.replace("&", "&amp;")
    album_name = album_name.replace(' "', ' <b>"')
    album_name = album_name.replace('" ', '"</b> ')
        # album: <b>"Sink Or Swim"</b> (2007)    
    return html.find(album_name)

def transform_to_album_class(albums, html, artist):
    out = []
    for a in albums:
        title, year = extract_title_and_year(a)
        pos = __find_album_position(html, title)
        album = __Album(title=title, year=year, artist=artist, pos_in_html=pos)
        out.append(album)
    return out

def extract_title_and_year(album):
    if "other songs" in album:
        title = "other songs"
        year = 0
    else:
        title = re.findall('\"([A-Za-z0-9ñ \'"&\/]+)\"', album)[0]
        year = re.findall('\(([0-9]{4})\)', album)[0]
    return title, year

class __Album():
    def __init__(self, title, year=None, artist=None, pos_in_html=None):
        self.title       = title
        self.year        = year
        self.artist      = artist
        self.pos_in_html = pos_in_html
    
    @property
    def title(self):
        return self.__title
    
    @title.setter
    def title(self, var):
        self.__title = var

    @property
    def year(self):
        return self.__year
    
    @year.setter
    def year(self, var):
        self.__year = var
        
    @property
    def artist(self):
        return self.__artist
    
    @artist.setter
    def artist(self, var):
        self.__artist = var
        
    @property
    def pos_in_html(self):
        return self.__pos_in_html
    
    @pos_in_html.setter
    def pos_in_html(self, var):
        self.__pos_in_html = var

def main():
    ARTIST = "The Gaslight Anthem"
    URL = "https://www.azlyrics.com/g/gaslightanthem.html"
    html = __get_html(URL)
    albums = __get_discography(html)
    albums = transform_to_album_class(albums, html, ARTIST)
    
    print(albums[1].title)

if __name__ == "__main__":
    main()