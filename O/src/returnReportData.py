import os
import xml.etree.ElementTree as ET
import logger
from os.path import normpath, basename
from datetime import datetime
import time
import dateutil.parser

def getReportData(root):
    """
    Extracts report data from the XML root.

    Args:
        root (ElementTree.Element): The root element of the XML file.

    Returns:
        dict: A dictionary containing extracted report data.
    """
    reportCaption = ''
    securityreportrightsid = ''
    reportID = ''
    sharedElementFile = ''
    sharedElementID = ''
    elementID = ''
    savedby = ''
    savedat = ''
    DatalayerID = ''
    ConnectionID = ''

    # Extract information from specific nodes in the XML root
    for tags in root.iter('Report'):
        if tags.tag == 'Report':
            reportCaption  = tags.get('Caption')
            reportID = tags.get('ID')
            securityreportrightsid = tags.get('SecurityReportRightID')
            savedby = tags.get('SavedBy')

            savedat_format = tags.get('SavedAt')
            if (savedat_format == None) or (savedat_format == ''):
                savedat = ''
            else:
                savedat = dateutil.parser.parse(savedat_format)

    for tags in root.iter('IncludeSharedElement'):
        if tags.tag == 'IncludeSharedElement':
            sharedElementFile = tags.get('DefinitionFile')
            sharedElementID = tags.get('SharedElementID')
            elementID = tags.get('ID')

    for tags in root.iter('SharedElement'):
        if tags.tag == 'SharedElement':
            elementID = tags.get('ID')

    return {'reportCaption': reportCaption, 'securityreportrightsid': securityreportrightsid,
            'reportID': reportID, 'sharedElementFile': sharedElementFile, 'sharedElementID': sharedElementID,
            'elementID': elementID,'savedby': savedby,'savedat': savedat}

def getReportQuery(root, domain, ConnectionInfo):
    """
    Extracts report queries and related data from the XML root.

    Args:
        root (ElementTree.Element): The root element of the XML file.
        domain (str): The domain associated with the report.
        ConnectionInfo (dict): A dictionary containing connection information.

    Returns:
        list: A list of dictionaries containing extracted report queries and data.
    """
    #extract query and get datalayer information
    final_querys = []
    final_query = ''
    for tags in root.iter('DataLayer'): 
        for b in tags.iter('*'):                  
            if b.get('Type') == 'SQL':
                src_query = b.get('Source')
                src_query.replace('&#xD;'," ")
                src_query.replace('&#xA'," ")
                final_query = " ".join(src_query.split())
                DatalayerID = tags.get('ID')
                ConnectionID = tags.get('ConnectionID')
                #Get serverconnection by connection id...
                if domain in ConnectionInfo and ConnectionID in ConnectionInfo[domain]:
                    server_connection = ConnectionInfo[domain][ConnectionID]
                else:
                    server_connection = ''
        if final_query == '':
            pass
        else:
            final_querys.append({'query':final_query, 'DatalayerID':DatalayerID, 'ConnectionID':ConnectionID, 'ServerConnection':server_connection})
    final_querys = [dict(s) for s in set(frozenset(d.items()) for d in final_querys)]
    return final_querys

def getObjectsFromQuery(query):
    """
    Extracts object names from a given SQL query.

    Args:
        query (str): The SQL query.

    Returns:
        list: A list of extracted object names.
    """
    query = query.split()
    objects = []
    wordindex = []

    # Loop through each word in the query and store the index when 'FROM' or 'JOIN' is found
    for word in query:
        wordUp = word.upper()
        if ('FROM' == wordUp) or ('JOIN' == wordUp) == True:
            wordindex.append(query.index(word))

    # Extract the words that come after 'FROM' or 'JOIN'
    for index in wordindex:
        indexplus = 1
        while True:
            if (',' in query[index+indexplus]) == True:
                objects.append((query[index+indexplus].replace(",", "")).split('.')[-1])
                indexplus += 1
            else:
                if ('(' in query[index+indexplus]) == False:
                    objects.append((query[index+indexplus]).split('.')[-1])
                break

    # Remove duplicate values from the list of objects
    objects = list(dict.fromkeys(objects))
    return objects

def returnReportData(reportDirectoryList, ConnectionInfo):
    """
    Returns report data extracted from XML files.

    Args:
        reportDirectoryList (dict): A dictionary containing domain directories and their associated XML file paths.
        ConnectionInfo (dict): A dictionary containing connection information.

    Returns:
        list: A list of dictionaries containing extracted report data.
    """
    reportsData = []
    for loc_dir, dir_list in reportDirectoryList.items():
        for location in dir_list:
            if os.path.exists(location):
                ReportName = basename(normpath(location))
                print("Extracting " + ReportName)
                try:
                    tree = ET.parse(location)
                except:
                    logger.logger.error("Unable to parse file" + location)
                    break
                root = tree.getroot()
                
                # Remove remark nodes from the XML
                for element in list(root.iter()):
                    if element.tag == 'Remark':
                        for child in element:
                            element.remove(child)

                file_data = getReportData(root)

                now = datetime.now()
                time_now = now.strftime("%Y-%m-%d %H:%M:%S")
                
                ti_m = os.path.getctime(location)
                DateCreated = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(time.ctime(ti_m)))

                path_edit = location.replace("/","\\")

                #
                normalized_path = os.path.normpath(location)
                path_components = normalized_path.split(os.path.sep)
                server_name = next(s for s in path_components if s)

                
                data = {'path': path_edit, 'ServerName':server_name, 'domain': loc_dir, 'ReportName': ReportName, 'extr_date': time_now, 'created': DateCreated}
                
                query_list = getReportQuery(root, loc_dir, ConnectionInfo)

                for dicti in query_list:
                    for obj in getObjectsFromQuery(dicti['query']):
                        reportData = {**data, **file_data, **dicti, 'object': obj}
                        reportsData.append(reportData)
            else:
                logger.logger.info("Path " + location + " doesn't exist")
    
    return reportsData


# The function retrieves data from XML files.
# The function returns a list of dictionaries with extracted report data.
# Each dictionary contains information about the report, its domain, and associated queries.

