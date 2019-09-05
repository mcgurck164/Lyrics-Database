# -*- coding: utf-8 -*-

from Settings import Settings

if __name__ == "__main__":
    settings = Settings()
    settings.set(section="Misc", key="db_name", value="\\songs.db")