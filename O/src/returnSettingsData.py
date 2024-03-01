
#IN {domein:settingspath}#UIT {domein:{connection id:serverconnection}}
import os
import xml.etree.ElementTree as ET
import logger
import init
import re

def searchServerVar(servervar, session_vars):
    """
    Searches for a server variable in session variables.

    Args:
        servervar (str): The server variable string.
        session_vars (dict): A dictionary containing session variables.

    Returns:
        str: The value of the server variable if found, otherwise an empty string.
    """
    if startupProcess == False:
        return ""
    servervar = servervar.split('@Session.')[1].split('~')[0]
    if servervar in session_vars:
        return session_vars[servervar]

def searchConnectionStringVar(stringvar, session_vars):
    """
    Searches for a connection string variable in session variables.

    Args:
        stringvar (str): The connection string variable string.
        session_vars (dict): A dictionary containing session variables.

    Returns:
        str: The value of the connection string variable if found, otherwise an empty string.
    """
    if startupProcess == False:
        return ""
    
    #get variable and get connection information from connectionstring

    connvar = stringvar.split('@Session.')[1].split('~')[0]
    if connvar in session_vars:
        dic = dict(re.findall(r'([^=;]+)=([^;]+)', session_vars[connvar]))
        items = {key.strip(): value.strip() for key, value in dic.items()}
        if 'Data Source' in items:
            finalvar = items['Data Source']
            return finalvar
        if 'Server' in items:
            finalvar = items['Server'] 
            return finalvar
        return ""
        


def get_vars_file(process_file, process_task, settingspath, servername):
    """
    Retrieves variables from a process file based on settings.

    Args:
        process_file (str): The process file name.
        process_task (str): The task ID within the process file.
        settingspath (str): The path to the settings file.
        servername (str): The server name associated with the settings.

    Returns:
        dict: A dictionary containing session variables.
    """
    processpath = settingspath.replace("_Settings.lgx", "_Processes\\") + process_file + '.lgx'
    print(processpath)

    
    env_id = ""
    for env, server_list in init.serverinfo.items():
        if servername in server_list:
            env_id = env

    if env_id == "":
        logger.logger.error("Unknown environment server "+servername)
        startupProcess = False
        return


    if os.path.exists(processpath):
        ptree = ET.parse(processpath)
        proot = ptree.getroot()

        #remove remark nodes
        for element in list(proot.iter()):
            if element.tag == 'Remark':
                for child in element:
                    element.remove(child)

        sessionparams = {}

        #Search file for procedure nodes with sessionparams

        for tags in proot.iter('Procedure'):
            if tags.tag == 'Procedure' and tags.get('Type') == 'If' and tags.get('ID') == env_id:
                for proc_var in tags:
                    if proc_var.get('Type') == "SetSessionVars":
                        var_id = proc_var.get('ID')
                        if var_id != 'vars_Global':
                            for sessionparam in proc_var:
                                attributes = sessionparam.attrib  # Get all attributes of the node
                                sessionparams.update(attributes)
        return sessionparams


def get_connection_info(root, session_vars):
    """
    Extracts connection information from XML root using session variables.

    Args:
        root (ElementTree.Element): The root element of the XML file.
        session_vars (dict): A dictionary containing session variables.

    Returns:
        dict: A dictionary containing connection information.
    """
    connection_info = {}
    for tags in root.iter('Connection'): 
        if tags.tag == 'Connection':                    #search all connection nodes sql:server , oracle:data source

            if tags.get('Type') == 'SqlServer':
                id = tags.get('ID')

                if tags.get('SqlServer') is not None:        
                    server = tags.get('SqlServer')
                    if ("@Session." in server) == True:     #if session variable: get var with searchSqlVar function
                        connection_info[id] = searchServerVar(server, session_vars) #add to dict
                    else:
                        connection_info[id] = server    #add to dict

                if tags.get('SqlServerConnectionString') is not None:
                    connectionstring = tags.get('SqlServerConnectionString')
                    if ("@Session." in connectionstring) == True:     #if session variable: get var with searchSqlVar function
                        connection_info[id] = searchConnectionStringVar(connectionstring, session_vars)   #add to dict

            if tags.get('Type') == 'Oracle':
                id = tags.get('ID')

                if tags.get('OracleServer') is not None:        
                    server = tags.get('OracleServer')
                    if ("@Session." in server) == True:     #if session variable: get var with searchSqlVar function
                        connection_info[id] = searchServerVar(server, session_vars) #add to dict
                    else:
                        connection_info[id] = server    #add to dict

                if tags.get('OracleConnectionString') is not None:
                    connectionstring = tags.get('OracleConnectionString')
                    if ("@Session." in connectionstring) == True:     #if session variable: get var with searchSqlVar function
                        connection_info[id] = searchConnectionStringVar(connectionstring, session_vars)   #add to dict
    return connection_info


def returnSettingsData(dir_list):
    """
    Returns connection information extracted from settings files.

    Args:
        dir_list (dict): A dictionary containing domain directories and their associated settings file paths.

    Returns:
        dict: A dictionary containing extracted connection information.
    """
    final_connection_info = {}
    for domain, settingspath in dir_list.items():
        if os.path.exists(settingspath):
            path_components = settingspath.split(os.path.sep)
            server_name = next(s for s in path_components if s)

            tree = ET.parse(settingspath)
            root = tree.getroot()

            #remove remark nodes
            for element in list(root.iter()):
                if element.tag == 'Remark':
                    for child in element:
                        element.remove(child)

            global startupProcess
            startupProcess = True
            global session_vars
            session_vars = {}
            try:
                for tags in root.iter('StartupProcess'): 
                    if tags.tag == 'StartupProcess':
                         process_file = tags.get('Process')         #file with variables
                         process_task = tags.get('TaskID')          #task inside file
                session_vars = get_vars_file(process_file, process_task, settingspath, server_name)
            except:         
                logger.logger.error("No startup process in file")       #when there is no startupprocess in the file, the variables are disabled
                startupProcess = False
    
            connection_info = get_connection_info(root, session_vars)
            final_connection_info[domain] = connection_info
    return final_connection_info

#returnSettingsData({'ActionTracking': '\\\\epzlogi01a\\wwwroot\\ActionTracking\\_Definitions\\_Settings.lgx'})
