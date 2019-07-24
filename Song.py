# -*- coding: utf-8 -*-

class Song():
    def __init__(self, artist, record, year, song_title, lyrics, link_to_lyrics):
        self.artist = artist
        self.record = record
        self.year = year
        self.song_title = song_title
        self.lyrics = lyrics
        self.link_to_lyrics = link_to_lyrics
        
    def __len__(self):
        return len(self.lyrics)
    
    def __eq__(self, other_song):
        same = (self.artist == other_song.artist) and \
               (self.record == other_song.record) and \
               (self.song_title == other_song.song_title)
        return same
        
    @property
    def artist(self):
        return self.__artist
    
    @artist.setter
    def artist(self, var):
        self.__artist = var
                
    @property
    def record(self):
        return self.__record
    
    @record.setter
    def record(self, var):
        self.__record = var
                
    @property
    def year(self):
        return self.__year
    
    @year.setter
    def year(self, var):
        self.__year = var
                
    @property
    def song_title(self):
        return self.__song_title
    
    @song_title.setter
    def song_title(self, var):
        self.__song_title = var
                
    @property
    def lyrics(self):
        return self.__lyrics
    
    @lyrics.setter
    def lyrics(self, var):
        self.__lyrics = var
                
    @property
    def link_to_lyrics(self):
        return self.__link_to_lyrics
    
    @link_to_lyrics.setter
    def link_to_lyrics(self, var):
        self.__link_to_lyrics = var