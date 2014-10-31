__author__ = 'ywang'


import cx_Oracle
import os.path
import xml.etree.ElementTree as ET


def testConnection(connectionString) :
    # con = cx_Oracle.connect('UOB_DELIVERY_TEST_MX/UOB_DELIVERY_TEST_MX@mx1068vm/MX1068VM')
    con = cx_Oracle.connect(connectionString)
    print con.version
    con.close()

def loadMXDBSourcefile(sourcefile) :
    tree = ET.parse(sourcefile)
    root = tree.getroot()
    dbServerType= tree.find('./MxAnchors/MxAnchor/DbServerType')
    dbHostName= tree.find('./MxAnchors/MxAnchor/DbHostName')
    dbServerPortNumber=tree.find('./MxAnchors/MxAnchor/DbServerPortNumber')
    dbServerOrServiceName=tree.find('./MxAnchors/MxAnchor/DbServerOrServiceName')
    dbUser=tree.find('./MxAnchors/MxAnchor/DbDefaultCredential/DbUser')
    dbPassword=tree.find('./MxAnchors/MxAnchor/DbDefaultCredential/DbUser')

    connectionString=dbUser.text+'/'+dbPassword.text+'@'+dbHostName.text+':'+dbServerPortNumber.text\
                     +'/'+dbServerOrServiceName.text
    return connectionString

if __name__ == "__main__":

    connectionString = loadMXDBSourcefile('D:\Dropbox\Project\DM_Analysis\properties\dbsource.mxres')
    testConnection(connectionString)

    # cur = con.cursor()
    # cur.execute('select M_LABEL,M_REQUEST from ACT_REQXTR_DBF')
    #
    # # res = cur.fetchone()
    # res = cur.fetchone()
    # print res[1]
    #
    # res = cur.fetchone()
    # print res[1]
    #
    # cur.close()
    # con.close()
