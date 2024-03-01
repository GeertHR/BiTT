from helpfunctions import *
import init
import logger

def fillSQL(data, init_run = False):
    """
    Fills SQL tables with extracted report data.

    Args:
        data (list): A list of dictionaries containing extracted report data.
        init_run (bool): Indicates whether it's an initial run.

    Returns:
        int or None: Returns ConnectionError if a connection cannot be established, otherwise None.
    """
    try:
        cursor = OTDWH()
    except:
        logger.logger.error("Cannot connect to server")
        return ConnectionError

    if init_run == True:
        cursor.execute("EXEC logi.CreateTablesInit")
        cursor.commit()

    cursor.execute("EXEC logi.CreateTempTable")
    cursor.commit()
    
    for item in data:
        #KEY
        ReportName = item['ReportName']
        Domain = item['domain']
        PathName = item['path']
        DateExtracted = item['extr_date']
        ServerName = item['ServerName']
        DateCreated = item['created']

        DateModified = item['savedat']
        ModifiedBy = item['savedby']

        #HASH
        Query = item['query']
        Object = item['object']
        DatalayerID = item['DatalayerID']
        ConnectionID = item['ConnectionID']
        ServerConnection = item['ServerConnection']

        DataHash = (''.join([str(Query), str(Object),str(DatalayerID), str(ConnectionID), str(ServerConnection)])).replace("\"","").replace("'","")
        rc = (ReportName, Domain, PathName, ServerName, DateCreated, DateModified, ModifiedBy, Query, DataHash, DateExtracted, Object, DatalayerID, ConnectionID, ServerConnection)
        
        insert_query = """\
        EXEC logi.InsertData ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?"""
        cursor.execute(insert_query, rc)
        cursor.commit()

    if init_run == True:
        cursor.execute("EXEC logi.ExtractDataInit")
    else:
        cursor.execute("EXEC logi.ExtractData")
    cursor.commit()      
