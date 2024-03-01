import pypyodbc 
from init import *


def conToServerWithCur(server):
    connection = pypyodbc.connect(server)
    return connection.cursor()

def OTDWH():
    return conToServerWithCur('Driver={SQL Server};Server='+srv_1+';Database='+srv_1_database +';Trusted_Connection=yes')
