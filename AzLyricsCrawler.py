# -*- coding: utf-8 -*-

import requests
import bs4
import re
import pandas as pd

def get_html(url):
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

def find_album_position(html, album_name):
    album_name = album_name.replace("&", "&amp;")
    album_name = album_name.replace(' "', ' <b>"')
    album_name = album_name.replace('" ', '"</b> ')
        # album: <b>"Sink Or Swim"</b> (2007)    
    return html.find(album_name)

def find_song_position(html, song):
    song = song.replace("&", "&amp;")
    song = song + "</a>"
        # song: The '59 Sound</a>
    return html.find(song)

def extract_title_and_year(album):
    album = album.getText()
    if "other songs" in album:
        title = "other songs"
        year = 0
    else:
        title = re.findall('\"([A-Za-z0-9ñ \'"&\/]+)\"', album)[0]
        year = re.findall('\(([0-9]{4})\)', album)[0]
    return title, year

def get_albums(soup):
    albums = soup.select("#listAlbum .album")
    df = pd.DataFrame()
    for album in albums:
        title, year = extract_title_and_year(album)
        pos = find_album_position(str(soup), album.getText())
        series = pd.Series({"Title": title, "Year": year, "Position": pos})
        df = df.append(series, ignore_index=True)
    return df.sort_values("Position")

def find_album(song_position, albums):
    albums.sort_values("Position", ascending=False, inplace=True)
    
    for index, row in albums.iterrows():
        if song_position > row["Position"]:
            return row["Title"]
    return None    

def get_songs(soup, albums, artist):
    songs = soup.select("#listAlbum a")
    df = pd.DataFrame()
    for song in songs:
        link = song.get_attribute_list("href")[0]
        song = song.getText()
        pos = find_song_position(str(soup), song)
        series = pd.Series({"SongTitle": song, 
                            "Position":  pos, 
                            "Link":      link})
        df = df.append(series, ignore_index=True)
    df["Album"] = df["Position"].apply(lambda x: find_album(x, albums))
    df["Artist"] = artist
    return df.drop("Position", axis=1)

def get_lyrics(url):
    START_STRING = ("<!-- Usage of azlyrics.com content by any third-party " 
                    "lyrics provider is prohibited by our licensing agreement. "
                    "Sorry about that. -->")
    END_STRING = "</div>"
    lyrics = get_html(url)
    start = lyrics.find(START_STRING) + len(START_STRING)
    lyrics = lyrics[start:]
    end = lyrics.find(END_STRING)
    lyrics = lyrics[:end]
    return lyrics

def main():
    ARTIST = "The Gaslight Anthem"
    BASE_URL = "https://www.azlyrics.com/"
    ARTIST_URL = BASE_URL + "g/gaslightanthem.html"
    html = get_html(ARTIST_URL)
    soup = bs4.BeautifulSoup(html, "lxml")
    albums = get_albums(soup)
    songs = get_songs(soup, albums, ARTIST)
    songs["Link"] = songs["Link"].apply(lambda x: x.replace("../", BASE_URL))
    songs["Lyrics"] = songs["Link"].apply(get_lyrics)
    print(songs.head())

if __name__ == "__main__":
    main()