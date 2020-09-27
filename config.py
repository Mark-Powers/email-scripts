import os
from configparser import ConfigParser

config_path = "/home/mark/projects/email-scripts/config.ini"

config = ConfigParser()
if os.path.isfile(config_path):
    config.read(config_path)
else:
    if input("Config file not found, create one? (y/n)") == "y":
        config_dict = {"email": {}, "database": {}, "weather": {}, "news": {}}
        config_dict["email"]["server"] = input("Email server: ").strip()
        config_dict["email"]["port"] = input("Email port: ").strip()
        config_dict["email"]["name"] = input("Email name: ").strip()
        config_dict["email"]["user"] = input("Email username name: ").strip()
        config_dict["email"]["pass"] = input("Email password: ").strip()

        if input("Configure database? (y/n)") == "y":
            config_dict["database"]["db"] = input("DB name: ").strip()
            config_dict["database"]["user"] = input("DB user: ").strip()
            config_dict["database"]["pass"] = input("DB password: ").strip()

        if input("Configure weather? (y/n)") == "y":
            config_dict["weather"]["lat"] = input("Latitude: ").strip()
            config_dict["weather"]["long"] = input("Longitude: ").strip()

        if input("Configure century old news? (y/n)") == "y":
            print("Go to https://chroniclingamerica.loc.gov/ and find a newspaper to follow")
            print("Open the issue for that newspaper, and replace the date in the URL with %%s")
            config_dict["news"]["urls"] = input("Enter URLs formatted as described above, comma seperated: ").strip()
            config_dict["news"]["names"] = input("Enter names for each respective URL, comma seperated: ").strip()
        
    input("Press enter to save config")
    config.read_dict(config_dict)
    with open(config_path, 'w') as configfile:
        config.write(configfile)

