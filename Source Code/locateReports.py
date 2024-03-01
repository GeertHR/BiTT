import os
from datetime import datetime
import os.path
from os import path
import glob
from init import exclude_files, include_domain
import logger

# Function to locate reports based on file extension, root directory, and LGX folder
def locateReports(file_extension, root_dir, lgx_folder, settings_path):
    """
    Locates report files based on specified criteria.
    
    Args:
        file_extension (str): The extension of the files to search for.
        root_dir (str): The root directory to search for report files.
        lgx_folder (str): The subfolder containing LGX files within each domain directory.
        settings_path (str): The path to settings files within each domain directory.
        
    Returns:
        tuple: A tuple containing two dictionaries:
            - lgx_dir: A dictionary with domain names as keys and lists of corresponding LGX file paths as values.
            - settingslist: A dictionary with domain names as keys and paths to their settings files as values.
    """
    
    settingslist = {}

    lgx_dir = {}  # Dictionary to store directory and corresponding files
    
    for dir in os.listdir(root_dir):
        # Check if the domain is in include_domain list
        if include_domain == []:
            pass
        elif (dir in include_domain) == False:
            logger.logger.info("Domain: "+dir+" :skipped")
            continue
        
        dir_files = []  # List to store files in the directory
        dirpath = os.path.join(root_dir, dir)
        
        if os.path.isdir(dirpath):
            files_count = 0

            lgx_loc = os.path.join(dirpath, lgx_folder) #create path with lgx files

            settings_loc = os.path.normpath(os.path.join(dirpath, settings_path)) #create path with settings files

            if os.path.exists(settings_loc) and settingslist.get(dir) is None:
                settingslist[dir] = settings_loc
                logger.logger.info("SettingsFile: " + settings_loc)

            if os.path.exists(lgx_loc):
                # Search the domain for LGX files with the given extension
                for file in glob.glob((os.path.join(lgx_loc, file_extension))):
                    if dir in exclude_files:
                        if ((file.split("\\")[-1]) in exclude_files[dir]) == True:
                            continue
                    now = datetime.now()
                    current_time = str(now.strftime("%d/%m/%Y %H:%M:%S"))
                    
                    if files_count == 0:
                        logger.logger.info(current_time + " - File: " + file)
                    else:
                        logger.logger.info(current_time + " - File: ...\\" + file.split("\\")[-1])
                    
                    dir_files.append(file)
                    files_count += 1
                
                # Save the files in a dictionary with the directory as the key
                lgx_dir[dir] = dir_files
            
            logger.logger.info("Number of files in \\"+dir + ": " + str(files_count))     
    return lgx_dir, settingslist


"""
The code is a Python script that defines a function called locateReports to locate report files based on certain criteria. It uses the os, logging, datetime, os.path, and glob modules for file operations and logging.

The function iterates over directories in the given root_dir and checks if the domain is included in the include_domain list. It then searches for LGX files with the specified extension in the corresponding LGX folder. The function logs the filenames in a log file, excluding certain files specified in the exclude_files dictionary.

Finally, it returns a dictionary where the keys are the directory names with XML files, and the values are lists of file paths.
"""