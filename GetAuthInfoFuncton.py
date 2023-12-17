from sqlalchemy import create_engine
from configparser import ConfigParser

## Function to parse Authorization from .ini files
## Parameters: 
#   filename: path of .ini file 
#   section: header of config you want to get which is displayed in square bracket /[]/

def ReadConfigFile(filename:str, section:str):
    parser = ConfigParser()
    parser.read(filename)
   
    config_info = {}
    
    if parser.has_section(section=section):
        params = parser.items(section=section)
        for param in params:
            config_info[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))        
    
    return config_info

