# -*- coding: utf-8 -*-

import requests
import bs4
import pandas as pd
import os

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

def get_albums(soup):
    albums = soup.find_all("div", class_="album-holder albums-list")
    df = pd.DataFrame()
    for album in albums:
        title = album.find("h3").getText()
        year = album.find("ul", class_="albumlist").find("li").getText()[:4]
        link = album.find("a").get_attribute_list("href")[0]
        series = pd.Series({"Title": title, "Year": year, "Link": link})
        df = df.append(series, ignore_index=True)
    return df.sort_values(by="Year")

def get_songs(albums):
    df = pd.DataFrame()
    for _, row in albums.iterrows():
        link = row["Link"]
        html = get_html(link)
        soup = bs4.BeautifulSoup(html, "lxml")
        songs = soup.find("table").find_all("a")
        song_idx = 0
        for song in songs:
            song_idx += 1
            link = song.get_attribute_list("href")[0]
            title = song.getText()
            series = pd.Series({"Title": title, 
                                "Link":  link,
                                "Album": row["Title"],
                                "Year":  row["Year"],
                                "Index": song_idx})
            df = df.append(series, ignore_index=True)
    return df

def get_lyrics(link_to_song):
    html = get_html(link_to_song)
    soup = bs4.BeautifulSoup(html, "lxml")
    lyrics = soup.find("div", class_="holder lyric-box").getText().strip()
    end = lyrics.find("Edit Lyrics")
    return lyrics[:end]

def crawl():
    ARTIST = "The Gaslight Anthem"
    BASE_URL = "https://songmeanings.com/"
    ARTIST_URL = BASE_URL + "artist/view/discography/137438979128/"
    html = get_html(ARTIST_URL)
    soup = bs4.BeautifulSoup(html, "lxml")
    albums = get_albums(soup)
    albums["Link"] = BASE_URL[:-1] + albums["Link"]
    print("Albums downloaded")
    songs = get_songs(albums)
    songs["Link"] = "https:" + songs["Link"]
    songs["Artist"] = ARTIST
    songs["Lyrics"] = songs["Link"].apply(get_lyrics)
    songs.to_csv(os.getcwd()+"//songs.csv", index=False)

if __name__ == "__main__":
    crawl()