from configparser import ConfigParser
from os.path import isfile

FILE_NAME_SETTINGS = "config.ini"

class Settings():
    def __init__(self):
        exists = isfile(FILE_NAME_SETTINGS)
        self.config = ConfigParser()
        self.config.read(FILE_NAME_SETTINGS)
        if not exists:
            self._setup()
            
    def _setup(self):
        self.config.add_section("main")
        self.set("main", key="db_name", value="\\songs.db")
    
    def set(self, section, key, value):
        """
        Add/Edit a settings parameter

        Args:
            section: (String)
            key:     (String)
            value 
        Returns:
            -
        Raises:
            -
        """
        self.config.set(section, key, value)
        with open(FILE_NAME_SETTINGS, 'w') as f:
            self.config.write(f)
    
    def get(self, section, key):
        """
        Get a parameter value

        Args:
            section: (String)
            key:     (String)
        Returns:
            parameter value
        Raises:
            -
        """
        return self.config.get(section, key)