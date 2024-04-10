"""
Module to access the config INI file
and decode the encrypted passwords
"""

# configurations
import base64
import configparser


CONFIGFILE = "../env/secrets.ini"
# print(CONFIGFILE)


def decoder(section, item="password", configfile=CONFIGFILE):
    """
    Function to decode the passwords in the config file
    """
    parser = configparser.ConfigParser()

    parser.read(configfile)
    return base64.b64decode(bytes(parser[section][item], "ascii")).decode()
