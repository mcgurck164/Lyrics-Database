# -*- coding: utf-8 -*-

import tkinter as tk
import os
from Database import Database

class Gui(tk.Tk):
    def __init__(self, path_db):
        tk.Tk.__init__(self)
        self.configure(bg="white")
        self.db = Database(path_db)
        self.found_songs = {}
        self.build()
        self.resizable(False, False)
        items = self.search_songs(sort_by_title=True)
        self.populate_lbx_songsfound(items)
    
    def build(self):        
        WIDTH_COLUMN = [2, 30, 5, 10, 60, 5, 2]
        
        CONFIG_DEFAULT_LABEL = {"bg":      "white",
                                "anchor":  tk.W,
                                "justify": tk.LEFT,
                                "font":    "Calibri 12 bold"}
        CONFIG_DEFAULT_ENTRY = {"bg":      "white",
                                "justify": tk.LEFT,
                                "font":    "Calibri 12"}
        CONFIG_DEFAULT_LISTBOX = {"bg":      "white",
                                 "font":    "Calibri 12"}
        
        # =====================================================================
        #   Header
        # =====================================================================
        
        # Label: Header
        self.lab_title = tk.Label(self, text="Lyrics Database".upper(), 
                                  bg="white",
                                  font="Calibri 35 bold italic")
        self.lab_title.grid(row=0, column=0, columnspan=len(WIDTH_COLUMN))
        
        # =====================================================================
        #   Column
        # =====================================================================
        COL = 0
        # Label: <SPACE>
        self.lab_space = tk.Label(self, text="",
                                   width=WIDTH_COLUMN[COL],
                                   **CONFIG_DEFAULT_LABEL)
        self.lab_space.grid(row=0, column=COL)
        
        # =====================================================================
        #   Column
        # =====================================================================
        COL += 1
        
        # Label: Artist
        self.lab_artist = tk.Label(self, text="Artist",
                                  width=WIDTH_COLUMN[COL],
                                  **CONFIG_DEFAULT_LABEL)
        self.lab_artist.grid(row=1, column=COL)
        
        # Entry: Artist
        self.artist_in = tk.StringVar()
        self.artist_in.trace_add("write", self.event_search_songs)
        self.ent_artist = tk.Entry(self, textvariable=self.artist_in,
                                   width=WIDTH_COLUMN[COL],
                                   **CONFIG_DEFAULT_ENTRY)
        self.ent_artist.grid(row=2, column=COL)
        
        # Label: Record Title
        self.lab_rectitle = tk.Label(self, text="Record Title",
                                     width=WIDTH_COLUMN[COL],
                                     **CONFIG_DEFAULT_LABEL)
        self.lab_rectitle.grid(row=3, column=COL)
        
        # Entry: Record Title
        self.rectitle_in = tk.StringVar()
        self.rectitle_in.trace_add("write", self.event_search_songs)
        self.ent_rectitle = tk.Entry(self, textvariable=self.rectitle_in,
                                   width=WIDTH_COLUMN[COL],
                                   **CONFIG_DEFAULT_ENTRY)
        self.ent_rectitle.grid(row=4, column=COL)
        
        # Label: Song Title
        self.lab_songtitle = tk.Label(self, text="Song Title",
                                      width=WIDTH_COLUMN[COL],
                                      **CONFIG_DEFAULT_LABEL)
        self.lab_songtitle.grid(row=5, column=COL)
        
        # Entry: Song Title
        self.songtitle_in = tk.StringVar()
        self.songtitle_in.trace_add("write", self.event_search_songs)
        self.ent_songtitle = tk.Entry(self, textvariable=self.songtitle_in,
                                   width=WIDTH_COLUMN[COL],
                                   **CONFIG_DEFAULT_ENTRY)
        self.ent_songtitle.grid(row=6, column=COL)
        
        # Label: <SPACE>
        self.lab_space1 = tk.Label(self, text="",
                                   width=WIDTH_COLUMN[COL],
                                   **CONFIG_DEFAULT_LABEL)
        self.lab_space1.grid(row=7, column=COL)
        
        # Label: Songs Found
        self.lab_songsfound = tk.Label(self, text="Songs Found",
                                       width=WIDTH_COLUMN[COL],
                                       **CONFIG_DEFAULT_LABEL)
        self.lab_songsfound.grid(row=8, column=COL)
        
        # Listbox: Songs Found
        self.lbx_songsfound = tk.Listbox(self,
                                         selectmode=tk.SINGLE,
                                         width=WIDTH_COLUMN[COL],
                                         **CONFIG_DEFAULT_LISTBOX)
        self.lbx_songsfound.grid(row=9, column=COL, rowspan=10)
        self.lbx_songsfound.bind("<<ListboxSelect>>", self.event_select_song)
        
        
        # Label: <SPACE>
        self.lab_space2 = tk.Label(self, text="",
                                   width=WIDTH_COLUMN[COL],
                                   **CONFIG_DEFAULT_LABEL)
        self.lab_space2.grid(row=20, column=COL)
        
        # =====================================================================
        #   Column
        # =====================================================================
        COL += 1
        
        # Scrollbar: Songs Found
        self.scb_songsfound = tk.Scrollbar(self)
        self.scb_songsfound.grid(row=9, column=COL, rowspan=10, sticky="ns")
        self.lbx_songsfound.configure(yscrollcommand=self.scb_songsfound.set)
        self.scb_songsfound.configure(command=self.lbx_songsfound.yview)
        
        # =====================================================================
        #   Column
        # =====================================================================
        COL += 1
        
        # Label: <SPACE>
        self.lab_space3 = tk.Label(self, text="",
                                   width=WIDTH_COLUMN[COL],
                                   **CONFIG_DEFAULT_LABEL)
        self.lab_space3.grid(row=1, column=COL)    
        
        # =====================================================================
        #   Column
        # =====================================================================
        COL += 1
        
        # Label: Lyrics
        self.lab_lyrics = tk.Label(self, text="<Selected Song>",
                                  width=WIDTH_COLUMN[COL],
                                  **CONFIG_DEFAULT_LABEL)
        self.lab_lyrics.grid(row=1, column=COL)
        
        # Listbox: Lyrics
        self.lbx_lyrics = tk.Listbox(self,
                                     selectmode=tk.SINGLE,
                                     width=WIDTH_COLUMN[COL],
                                     height=20,
                                     **CONFIG_DEFAULT_LISTBOX)
        self.lbx_lyrics.grid(row=2, column=COL, rowspan=17)
        
        # =====================================================================
        #   Column
        # =====================================================================
        COL += 1
        
        # Scrollbar: Songs Found
        self.scb_lyrics = tk.Scrollbar(self)
        self.scb_lyrics.grid(row=2, column=COL, rowspan=17, sticky="ns")
        self.lbx_lyrics.configure(yscrollcommand=self.scb_lyrics.set)
        self.scb_lyrics.configure(command=self.lbx_lyrics.yview)
        
        # =====================================================================
        #   Column
        # =====================================================================
        COL += 1
        # Label: <SPACE>
        self.lab_space4 = tk.Label(self, text="",
                                   width=WIDTH_COLUMN[COL],
                                   **CONFIG_DEFAULT_LABEL)
        self.lab_space4.grid(row=0, column=COL)

    def populate_lbx_songsfound(self, items):
        """
        Adds song names to 'Songs Found' listbox. Saves listbox index and
        song ID to a dictionary for use in other methods.

        Args:
            items: (List) of tuples (song_id, song_name, ...) 
        
        Returns:
            -
        
        Raises:
            -
        """
        self.lbx_songsfound.delete(0, tk.END)
        self.found_songs = dict([(idx, item[0]) 
                                for idx, item in enumerate(items)])
        for item in items:
            self.lbx_songsfound.insert(tk.END, item[1])

    def populate_lbx_lyrics(self, lyrics):
        """
        Writes lyrics of a song to 'Lyrics' listbox.

        Args:
            lyrics: (String) Lines are assumed to be separated by the substring
                    "\r\n"
        
        Returns:
            -
        
        Raises:
            -
        """
        self.lbx_lyrics.delete(0, tk.END)
        for line in lyrics.split("\r\n"):
            self.lbx_lyrics.insert(tk.END, " " + line)
    
    def search_songs(self, song_title="", record="", artist="", 
                     sort_by_title=False):
        """
        Queries database to find IDs and titles of songs matching the
        input criteria

        Args:
            song_title:    (String)
            record:        (String)
            artist:        (String)
            sort_by_title: (Boolean)
        
        Returns:
            (List) of tuples (song_id, song_name)
        
        Raises:
            -
        """
        sql = (f"SELECT id, song_title FROM Songs "
               f"WHERE (song_title LIKE '%{song_title}%') "
               f"AND (record LIKE '%{record}%') "
               f"AND (artist LIKE '%{artist}%')")
        if sort_by_title:
            sql += " ORDER BY song_title ASC"
        items = self.db.query_db(sql)
        return items
    
    def event_select_song(self, evt):
        """
        Event that fires when a song is selected from the 'Songs Found'
        listbox. Writes the selected song's lyrics to 'Lyrics' listbox.

        Args:
            evt: (Event)
        
        Returns:
            -
        
        Raises:
            -
        """
        w = evt.widget
        try:
            index = int(w.curselection()[0])
            # event occasionally fires even if it's not the listbox
            # that's clicked-on. In that case nothing should happen.
        except(IndexError):
            return
        value = w.get(index)
        song_id = self.found_songs[index]
        self.lab_lyrics.config(text=value)
        sql = f"SELECT lyrics FROM Songs WHERE id={song_id}"
        lyrics = self.db.query_db(sql)[0][0]
        self.populate_lbx_lyrics(lyrics)

    def event_search_songs(self, *args):
        """
        Event that fires when the text in any of the entry fields is changed.
        Writes all songs matching the input criteria to 'Songs Found' listbox.

        Args:
            *args: ~Not used~
        
        Returns:
            -
        
        Raises:
            -
        """
        song_title = self.ent_songtitle.get()
        record = self.ent_rectitle.get()
        artist = self.ent_artist.get()
        items = self.search_songs(song_title, record, artist)        
        self.populate_lbx_songsfound(items)
    
    def close(self):
        self.destroy()

if __name__ == "__main__":
    DB_NAME = "\\songs.db"
    gui = Gui(os.getcwd() + DB_NAME)
    gui.mainloop()