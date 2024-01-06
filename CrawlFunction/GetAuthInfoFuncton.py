from configparser import ConfigParser
import os.path as path

## Function to parse Authorization from .ini files
## Parameters: 
#   filename: path of .ini file 
#   section: header of config you want to get which is displayed in square bracket /[]/

def ReadConfigFile(filename:str, section:str):
    
    try:
        text_file_path = path.dirname(path.abspath(__file__)) + '/' + filename
    except:
        raise "Failed to get path of config file."
    
    parser = ConfigParser()
    parser.read(text_file_path)    
    config_info = {}
    
    if parser.has_section(section=section):
        params = parser.items(section=section)
        for param in params:
            config_info[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, text_file_path))        
    
    return config_info

