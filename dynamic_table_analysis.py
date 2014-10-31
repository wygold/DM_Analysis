__author__ = 'ywang'


import cx_Oracle
import ConnectDB
import string


def generate_raw_file(connectionString,sqlfile, input_directory):
    sqlString = []

    for line in sqlfile:
        sqlString.append(line)
    #print "".join(sqlString)

    con = cx_Oracle.connect(connectionString)
    cur = con.cursor()
    cur.execute("".join(sqlString))

    res = cur.fetchone()
    raw_file = open(input_directory+'\source.csv', 'w+')
    while res is not None:
        for field in res :
            raw_file.write(str(field))
            raw_file.write(' | ')
        raw_file.write('\n')
        res = cur.fetchone()

    raw_file.close()
    cur.close()
    con.close()

def read_raw_file(input_directory) :
    raw_file= open(input_directory+'\source.csv', 'r')
    for line in raw_file:
        fields = line.split(' | ')
        print fields[26]+'   '+fields[27]+'   '+fields[28]+'   '

def check_total_dynamic_table_field_number(input_directory) :
    raw_file= open(input_directory+'\source.csv', 'r')
    result=[['Dynamic table name','Category','Dynamic table type','Field count']]
    previous_dynamic_tables = []
    for line in raw_file:
        fields = line.split(' | ')

        if fields[29].strip()<>'' and int(fields[29])>100 :
        #    result.append([fields[26].strip(),fields[27].strip(),fields[28].strip(),fields[29].strip()])
            if (fields[26].strip()+fields[27].strip()) not in previous_dynamic_tables :
                result.append([fields[26].strip(),fields[27].strip(),fields[28].strip(),fields[29].strip()])
                previous_dynamic_tables.append(fields[26].strip()+fields[27].strip())

    return result

def write_to_output_file(output_directory):
    pass

if __name__ == "__main__":

    mxDbsourcefile=('D:\Dropbox\Project\DM_Analysis\properties\dbsource.mxres')
    input_directory=('D:\Dropbox\Project\DM_Analysis\Input\\')
    output_directory=('D:\Dropbox\Project\DM_Analysis\Output\\')
    connectionString = ConnectDB.loadMXDBSourcefile('D:\Dropbox\Project\DM_Analysis\properties\dbsource.mxres')

    sqlfile = open('D:\Dropbox\Project\DM_Analysis\SQLs\qurey_dm_config.txt', 'r+')

    generate_raw_file(connectionString,sqlfile,input_directory)

    result=check_total_dynamic_table_field_number(input_directory)



    for r in result:
        print r