__author__ = 'ywang'


import cx_Oracle
import ConnectDB
import string
import xlrd
from xlwt import *
import ConfigParser
import os

def generate_raw_file(connectionString,sqlfile, input_directory, input_file):
    sqlString = []

    for line in sqlfile:
        sqlString.append(line)
    #print "".join(sqlString)

    con = cx_Oracle.connect(connectionString)
    cur = con.cursor()
    cur.execute("".join(sqlString))

    res = cur.fetchone()
    raw_file = open(input_directory+'\\'+input_file, 'w+')
    while res is not None:
        for field in res :
            raw_file.write(str(field))
        raw_file.write('\n')
        res = cur.fetchone()

    raw_file.close()
    cur.close()
    con.close()

# Total number of dynamic tables fields for each dynamic table. If more than 100, list out as red, if it is more than 50
def check_total_dynamic_table_field_number(input_directory,input_file, max_dynamic_number_fields) :
    raw_file= open(input_directory+input_file, 'r')
    result=[['Number of Dynamic table fields that exceeds '+str(max_dynamic_number_fields)]]
    result.append(['Dynamic table name','Category','Dynamic table type','Field count'])
    previous_dynamic_tables = []
    for line in raw_file:
        fields = line.split(' | ')

        if fields[29].strip()<>'' and int(fields[29])> max_dynamic_number_fields :
        #    result.append([fields[26].strip(),fields[27].strip(),fields[28].strip(),fields[29].strip()])
            if (fields[26].strip()+fields[27].strip()) not in previous_dynamic_tables :
                result.append([fields[26].strip(),fields[27].strip(),fields[28].strip(),fields[29].strip()])
                previous_dynamic_tables.append(fields[26].strip()+fields[27].strip())

    return result

#	2. Number of horizontal fields. List more than 10 horizontal fields
def check_total_dynamic_table_horizontal_field_number(input_directory,input_file,max_dynamic_number_hfields) :
    raw_file= open(input_directory+input_file, 'r')
    result=[['Number of Dynamic table horizontal fields that exceeds '+str(max_dynamic_number_hfields)]]
    result.append(['Dynamic table name','Category','Dynamic table type','Horizontal Field count'])
    previous_dynamic_tables = []
    for line in raw_file:
        fields = line.split(' | ')

        if fields[30].strip()<>'' and int(fields[30])>max_dynamic_number_hfields :
        #    result.append([fields[26].strip(),fields[27].strip(),fields[28].strip(),fields[29].strip()])
            if (fields[26].strip()+fields[27].strip()) not in previous_dynamic_tables :
                result.append([fields[26].strip(),fields[27].strip(),fields[28].strip(),fields[30].strip()])
                previous_dynamic_tables.append(fields[26].strip()+fields[27].strip())

    return result

#	3. Check if any *TBLFIELD, *TABLE is used
def check_total_dynamic_table_db_access_horizontal_field_number(input_directory,input_file,max_dynamic_number_db_access_hfields) :
    raw_file= open(input_directory+input_file, 'r')
    result=[['Number of Dynamic table horizontal fields that exceeds '+str(max_dynamic_number_hfields)]]
    result.append(['Dynamic table name','Category','Dynamic table type','Direct DB access Parser function used times'])
    previous_dynamic_tables = []
    for line in raw_file:
        fields = line.split(' | ')

        if fields[31].strip()<>'' and int(fields[31])>max_dynamic_number_db_access_hfields :
        #    result.append([fields[26].strip(),fields[27].strip(),fields[28].strip(),fields[29].strip()])
            if (fields[26].strip()+fields[27].strip()) not in previous_dynamic_tables :
                result.append([fields[26].strip(),fields[27].strip(),fields[28].strip(),fields[31].strip()])
                previous_dynamic_tables.append(fields[26].strip()+fields[27].strip())

    return result


#	4. Check if sensitivy flag is disabled for dynamic table that not select any S_* fields
def check_compute_sensitivity_flag(input_directory,input_file) :
    raw_file= open(input_directory+input_file, 'r')
    result=[['Dynamic tables which sensitivity compute flag can be disabled']]
    result.append(['Dynamic table name','Category'])

    for line in raw_file:
        fields = line.split(' | ')
        result.append([fields[0].strip(),fields[1].strip()])
    return result


def format_excel():
    fnt2 = Font()
    fnt2.name = 'Arial'
    fnt2.colour_index = 20
    fnt2.bold = False

    borders = Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1

    return fnt2,borders

def write_to_output_file(result, work_book, work_sheet_name):

    ws = work_book.add_sheet(work_sheet_name)

    contentstyle = XFStyle()
    contentstyle.font,contentstyle.borders = format_excel()

    TABLE_HEADER_FORMAT = easyxf(
                 'font: bold 1, name Tahoma, height 160;'
                 'align: vertical center, horizontal center, wrap on;'
                 'borders: left thin, right thin, top thin, bottom thin;'
                 'pattern: pattern solid, pattern_fore_colour yellow, pattern_back_colour yellow'
                 )

    TITLE_FORMAT = easyxf(
                 'font: bold 1, name Tahoma, height 300;'
                 'align: vertical center, horizontal center, wrap on;'
                 'borders: left thin, right thin, top thin, bottom thin;'
                 'pattern: pattern solid, pattern_fore_colour gray25, pattern_back_colour gray25'
                 )

    i = 0
    j = 0

    ws.col(i).width = 0x0d00 + i

    for row in result:
        for cell in row:
            if j < 12 and ws.col(j).width < len(cell)*300 :
                ws.col(j).width = len(cell)*320
            if i == 0 :
                ws.write_merge(i, j,i,j+3, str(cell),TITLE_FORMAT)
            elif i == 1 :
                ws.write(i, j, str(cell),TABLE_HEADER_FORMAT)
            else :
                ws.write(i, j, str(cell),contentstyle)
            j = j + 1
        j = 0
        i = i + 1
    return work_book

if __name__ == "__main__":
    #define directories
    input_directory=os.getcwd()+'\Input\\'
    output_directory=os.getcwd()+'\Output\\'
    sql_directory=os.getcwd()+'\SQLs\\'
    property_directory=os.getcwd()+'\\properties\\'

    #define sql files
    query_dm_sql='query_dm_config.sql'
    query_sensi_sql='query_sensitivity_flag.sql'

    #define input files
    dm_config_file = 'source.csv'
    sensi_file='computer_sensitivity_check.csv'

    #define property files
    parameter_file='parameters.txt'
    mxDbsource_file='dbsource.mxres'

    #define output file
    final_result_file = 'analyze_dynamic_table.xls'

    #read in property file
    config = ConfigParser.RawConfigParser()
    config.read(property_directory + parameter_file)
    max_dynamic_number_fields = config.getint('dynamic table', 'max_number_fields')
    max_dynamic_number_hfields = config.getint('dynamic table', 'max_number_h_fields')
    max_dynamic_number_db_access_hfields = config.getint('dynamic table', 'max_number_db_access_h_fields')

    #prepare conncection string
    connectionString = ConnectDB.loadMXDBSourcefile(property_directory + mxDbsource_file)

    #Generate input files
    sqlfile1 = open(sql_directory+query_dm_sql, 'r+')
    generate_raw_file(connectionString,sqlfile1,input_directory,dm_config_file)

    sqlfile2 = open(sql_directory+query_sensi_sql, 'r+')
    generate_raw_file(connectionString,sqlfile2,input_directory,sensi_file)

    #workbook for output result
    work_book = Workbook()

    #check Total number of dynamic tables fields for each dynamic table.
    result=check_total_dynamic_table_field_number(input_directory,dm_config_file,max_dynamic_number_fields)
    work_sheet_name='Field_Check'
    work_book=write_to_output_file(result,work_book, work_sheet_name)

    #check Number of horizontal fields
    result=check_total_dynamic_table_horizontal_field_number(input_directory,dm_config_file, max_dynamic_number_hfields)
    work_sheet_name='H_Field_Check'
    work_book=write_to_output_file(result,work_book, work_sheet_name)

    #Check horizontal fields with *TBLFIELD and *TABLE
    result=check_total_dynamic_table_db_access_horizontal_field_number(input_directory,dm_config_file, max_dynamic_number_db_access_hfields)
    work_sheet_name='H_DB_Field_Check'
    work_book=write_to_output_file(result,work_book, work_sheet_name)

    #check sensitivity flag can be disabled
    result=check_compute_sensitivity_flag(input_directory,sensi_file)
    work_sheet_name='Sensi_flag_Check'
    work_book=write_to_output_file(result,work_book, work_sheet_name)

    #output the work_book
    work_book.save(output_directory+final_result_file)



