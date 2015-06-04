__author__ = 'ywang'

import xlwt
from xlwt import *
import logging
from logging import handlers

class io_utility:

    logger = ''

    def initialize_log(self,log_level = logging.DEBUG, log_file = None):
        self.logger = logging.getLogger(__name__)


        if self.logger.handlers == []:
            # create a file handler
            if log_file is None:
                handler = logging.handlers.RotatingFileHandler('io_utlity.log',maxBytes=1024)
            else:
                handler = logging.handlers.RotatingFileHandler(log_file,maxBytes=1024)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)

            self.logger.setLevel(log_level)
            handler.setLevel(log_level)

            # add the handlers to the logger
            self.logger.addHandler(handler)

    def set_log_level(self, log_level= logging.DEBUG):
        for handler in self.logger.handlers:
            handler.setLevel(log_level)

    #define format for excel file
    TABLE_HEADER_FORMAT = easyxf(
        'font: bold 1, name Tahoma, height 160;'
        'align: vertical center, horizontal center, wrap on;'
        'borders: left thin, right thin, top thin, bottom thin;'
        'pattern: pattern solid, pattern_fore_colour yellow, pattern_back_colour yellow'
    )

    TITLE_FORMAT = easyxf(
        'font: bold 1, name Tahoma, height 220;'
        'align: vertical center, horizontal center, wrap on;'
        'borders: left thin, right thin, top thin, bottom thin;'
        'pattern: pattern solid, pattern_fore_colour gray25, pattern_back_colour gray25'
    )

    REVIEW_FORMAT = easyxf(
        'font:  name Tahoma, height 200;'
        'align: wrap on;'
        'borders: left thin, right thin, top thin, bottom thin;'
        'pattern: pattern solid, pattern_fore_colour white, pattern_back_colour gray25'
    )

    TEXT_FORMAT = easyxf(
        'font:  bold 1, name Roma, height 160;'
        'align: vertical center, horizontal center, wrap on;'
        'borders: left thin, right thin, top thin, bottom thin;'
        'pattern: pattern solid, pattern_fore_colour white, pattern_back_colour gray25'
    )

    HIGHLIGHTED_TEXT_FORMAT = easyxf(
        'font: colour white, bold 1, name Roma, height 160;'
        'align: vertical center, horizontal center, wrap on;'
        'borders: left thin, right thin, top thin, bottom thin;'
        'pattern: pattern solid, pattern_fore_colour green, pattern_back_colour gray25'
    )

    TEXT_FORMAT_ALIGN_LEFT = easyxf(
        'font:  bold 1, name Roma, height 160;'
        'align: vertical center, horizontal left, wrap on;'
        'borders: left thin, right thin, top thin, bottom thin;'
        'pattern: pattern solid, pattern_fore_colour white, pattern_back_colour gray25'
    )

    TEXT_FORMAT_CONTENT = easyxf(
        'font: underline on, bold 1, name Roma, height 160;'
        'align: vertical center, horizontal left, wrap on;'
        'borders: left thin, right thin, top thin, bottom thin;'
        'pattern: pattern solid, pattern_fore_colour white, pattern_back_colour gray25'
    )

    TEXT_FORMAT_LINK = easyxf(
        'font:  colour white, underline on, bold 1, name Roma, height 160;'
        'align: vertical center, horizontal center, wrap on;'
        'borders: left thin, right thin, top thin, bottom thin;'
        'pattern: pattern solid, pattern_fore_colour dark_blue_ega, pattern_back_colour yellow'
    )


    def read_txt(self,filename):
        pass

    def write_txt(self,filename):
        pass

    def read_csv(self,filename):
        pass

    def write_csv(self,content, filename):
        pass

    def add_worksheet(self,content, workbook, sheetname, highlighted=False, previous_sheet = None, next_sheet = None, analyze_review = None):
        self.logger.info('Start to create worksheet %s',sheetname)
        ws = workbook.add_sheet(sheetname)

        i = 1
        j = 0
        title = ''
        title_length = 0
        total_length = 0
        cell = ''

        content = self.add_sequence_column(content)
        content = self.add_analyze_review(content,analyze_review)

        if highlighted==False:
            for row in content:
                for rawcell in row:
                    if type(rawcell) is str:
                        cell=rawcell
                    else:
                        cell=str(rawcell)

                    if i >= 2 and ws.col(j).width < len(cell) * 300:
                        width= len(cell) * 500
                        if width > 15000 :
                            ws.col(30).width = 20000
                        else :
                            ws.col(30).width = width
                    if i == 1:
                        title = str(cell)
                    elif i == 2:
                        review = str(cell)
                        width= len(cell) * 500
                        if width > 15000 :
                            ws.col(30).width = 20000
                        else :
                            ws.col(30).width = width
                        ws.write(i, 40, str(cell), self.REVIEW_FORMAT)
                    elif i == 3 :
                        if j == 0:
                            ws.write_merge(1, 1, 0, len(row) - 1, title, self.TITLE_FORMAT)
                            ws.write_merge(2, 2, 0, len(row) - 1, review, self.REVIEW_FORMAT)
                            ws.col(j).width = len(cell) * 320
                            self.logger.debug('Create sheet title: %s',title)
                        ws.write(i, j, str(cell), self.TABLE_HEADER_FORMAT)
                        self.logger.debug('Write field title: %s ',str(cell))
                    else:
                        self.logger.debug('Write field [%s,%s] content: %s ',str(i), str(j), str(cell))
                        ws.write(i, j, str(cell), self.TEXT_FORMAT)

                    j = j + 1
                j = 0
                i = i + 1
        else:
            for row in content:
                highlighted = row[-1]
                for rawcell in row:
                    if type(rawcell) is str:
                        cell=rawcell
                    else:
                        cell=str(rawcell)
                    if i>=2 and j < 12 and ws.col(j).width < len(cell)*300 :
                        width= len(cell) * 320
                        if width > 15000 :
                            ws.col(j).width = 15000
                        else :
                            ws.col(j).width = width
                    if i == 1 :
                        title = str(cell)
                    elif i == 2:
                        review = str(cell)
                        width= len(cell) * 500
                        if width > 15000 :
                            ws.col(30).width = 20000
                        else :
                            ws.col(30).width = width
                        ws.write(i, 40, str(cell), self.REVIEW_FORMAT)
                    elif i == 3 :
                        if j ==  0:
                            self.logger.debug('Create sheet title: %s',title)
                            ws.write_merge(1, 1, 0, len(row) - 1, title, self.TITLE_FORMAT)
                            ws.write_merge(2, 2, 0, len(row) - 1, review, self.REVIEW_FORMAT)
                            width= len(cell) * 320
                            if width > 15000 :
                                ws.col(j).width = 15000
                            else :
                                ws.col(j).width = width
                        ws.write(i, j, str(cell),self.TABLE_HEADER_FORMAT)
                        self.logger.debug('Write field title: %s',str(cell))
                    elif highlighted=='True':
                        ws.write(i, j, str(cell),self.HIGHLIGHTED_TEXT_FORMAT)
                        self.logger.debug('Write highlighted field [%s,%s] content: %s',str(i), str(j),str(cell))
                    else:
                        ws.write(i, j, str(cell),self.TEXT_FORMAT)
                        self.logger.debug('Write unhighlighted field [%s,%s]  content: %s',str(i), str(j), str(cell))
                    j = j + 1
                j = 0
                i = i + 1


        #create shortcuts
        if previous_sheet is not None or next_sheet is not None :
            #create previous sheet short cut at the top
            if previous_sheet is not None :
                link ='HYPERLINK("#\''+ previous_sheet + '\'!A1", "' + ' <-- '+previous_sheet+'")'
                ws.write(0, 0, xlwt.Formula(link), self.TEXT_FORMAT_LINK)
                self.logger.debug('Write field [%s,%s] content: %s ', str(0), str(0), str(previous_sheet))
                width= len(previous_sheet) * 380
                if width > ws.col(0).width :
                    ws.col(0).width = width


            #create content sheet shortcut at the top
            link ='HYPERLINK("#\''+ 'Content' + '\'!A1", "' + ' ^ Content '+'")'
            if len(row) > 2:
                ws.write_merge(0, 0, 1, len(row) - 2, xlwt.Formula(link), self.TEXT_FORMAT_LINK)


            # else:
            #     ws.write(0, 1, xlwt.Formula(link), self.TEXT_FORMAT_SHORTCUT)
            # self.logger.debug('Write field [%s,%s] content: %s ', str(0), str(0), str(previous_sheet))

            #create next sheet shortcut at the top
            if next_sheet is not None :
                link ='HYPERLINK("#\''+ next_sheet + '\'!A1", "' + next_sheet +' --> '+'")'
                column = 0
                if len(row) > 2:
                    ws.write(0, len(row) - 1, xlwt.Formula(link), self.TEXT_FORMAT_LINK)
                    column = len(row) - 1
                elif len(row) == 2:
                    ws.write(0,1, xlwt.Formula(link), self.TEXT_FORMAT_LINK)
                    column = 1
                else:
                    ws.write(0,2, xlwt.Formula(link), self.TEXT_FORMAT_LINK)
                    column = 2
                width= len(next_sheet) * 320
                if width > ws.col(column).width :
                    ws.col(column).width = width
            else:
                ws.write(0, len(row) - 1, '', self.TEXT_FORMAT_LINK)

            self.logger.debug('Write field [%s,%s] content: %s ', str(0), str(2), str(next_sheet))

            #create previous sheet short cut at the bottem
            if previous_sheet is not None :
                link ='HYPERLINK("#\''+ previous_sheet + '\'!A1", "' + ' <-- '+previous_sheet+'")'
                ws.write(i, 0, xlwt.Formula(link), self.TEXT_FORMAT_LINK)
                self.logger.debug('Write field [%s,%s] content: %s ', str(0), str(0), str(previous_sheet))

            #create content sheet shortcut at the top
            link ='HYPERLINK("#\''+ sheetname + '\'!A1", "' + ' ^ Top '+'")'
            if len(row) > 2:
                ws.write_merge(i, i, 1, len(row) - 2, xlwt.Formula(link), self.TEXT_FORMAT_LINK)
            # else:
            #     ws.write(0, 1, xlwt.Formula(link), self.TEXT_FORMAT_SHORTCUT)
            # self.logger.debug('Write field [%s,%s] content: %s ', str(0), str(0), str(previous_sheet))

            #create next sheet shortcut at the top
            if next_sheet is not None :
                link ='HYPERLINK("#\''+ next_sheet + '\'!A1", "' + next_sheet + ' --> '+'")'
                if len(row) > 2:
                    ws.write(i, len(row) - 1, xlwt.Formula(link), self.TEXT_FORMAT_LINK)
                elif len(row) == 2:
                    ws.write(i,1, xlwt.Formula(link), self.TEXT_FORMAT_LINK)
                else:
                    ws.write(i,2, xlwt.Formula(link), self.TEXT_FORMAT_LINK)
                self.logger.debug('Write field [%s,%s] content: %s ', str(0), str(2), str(next_sheet))
            else:
                ws.write(i, len(row) - 1, '', self.TEXT_FORMAT_LINK)

        self.logger.info('End creating worksheet %s',sheetname)

        return workbook


    def add_raw_worksheet(self,content, workbook, sheetname, highlighted=False):
        self.logger.info('Start to create worksheet %s',sheetname)
        ws = workbook.add_sheet(sheetname)

        content = self.add_sequence_column(content)

        i = 0
        j = 0
        title = ''
        cell = ''

        if highlighted==False:
            for row in content:
                for rawcell in row:
                    if type(rawcell) is str:
                        cell=rawcell
                    else:
                        cell=str(rawcell)

                    if i >= 1 and ws.col(j).width < len(cell) * 300:
                        width= len(cell) * 320
                        if width > 15000 :
                            ws.col(j).width = 15000
                        else :
                            ws.col(j).width = width
                    if i == 0:
                        title = str(cell)
                    elif i == 1:
                        if j == 0:
                            ws.write_merge(0, 0, 0, len(row) - 1, title, self.TITLE_FORMAT)
                            self.logger.debug('Create sheet title: %s',title)
                        ws.write(i, j, str(cell), self.TABLE_HEADER_FORMAT)
                        self.logger.debug('Write field title: %s ',str(cell))
                    else:
                        ws.write(i, j, str(cell), self.TEXT_FORMAT)
                        self.logger.debug('Write field [%s,%s] content: %s ',str(i), str(j), str(cell))
                    j = j + 1
                j = 0
                i = i + 1
        else:
            for row in content:
                highlighted = row[-1]
                for rawcell in row:
                    if type(rawcell) is str:
                        cell=rawcell
                    else:
                        cell=str(rawcell)
                    if i>=1 and j < 12 and ws.col(j).width < len(cell)*300 :
                        width= len(cell) * 320
                        if width > 15000 :
                            ws.col(j).width = 15000
                        else :
                            ws.col(j).width = width
                    if i == 0 :
                        title = str(cell)
                    elif i == 1 :
                        if j ==  0:
                            ws.write_merge(0,0,0,len(row)-1, title,self.TITLE_FORMAT)
                            self.logger.debug('Create sheet title: %s',title)
                        ws.write(i, j, str(cell),self.TABLE_HEADER_FORMAT)
                        self.logger.debug('Write field title: %s',str(cell))
                    elif highlighted=='True':
                        ws.write(i, j, str(cell),self.HIGHLIGHTED_TEXT_FORMAT)
                        self.logger.debug('Write highlighted field [%s,%s] content: %s',str(i), str(j),str(cell))
                    else:
                        ws.write(i, j, str(cell),self.TEXT_FORMAT)
                        self.logger.debug('Write unhighlighted field [%s,%s]  content: %s',str(i), str(j), str(cell))
                    j = j + 1
                j = 0
                i = i + 1
        self.logger.info('End creating worksheet %s',sheetname)

        return workbook

    def add_content_worksheet(self,content, workbook, sheetname, highlighted=False):
        self.logger.info('Start to create worksheet %s',sheetname)
        ws = workbook.add_sheet(sheetname)

        i = 0
        j = 0
        title = ''
        title_length = 0
        total_length = 0
        cell = ''

        for row in content:
            for rawcell in row:
                if type(rawcell) is str:
                    cell = rawcell
                else:
                    cell = str(rawcell)

                if i >= 1 and ws.col(j).width < len(cell) * 300:
                    width = len(cell) * 320
                    if width > 15000:
                        ws.col(j).width = 15000
                    else:
                        ws.col(j).width = width
                if i == 0:
                    title = str(cell)
                elif i == 1:
                    if j == 0:
                        ws.write_merge(0, 0, 0, len(row) - 1, title, self.TITLE_FORMAT)
                        ws.col(j).width = len(cell) * 320
                        self.logger.debug('Create sheet title: %s', title)
                        link ='HYPERLINK("#\''+ cell + '\'!A1", "'+str(i)+'. '+cell+'")'
                        ws.write(i, j, xlwt.Formula(link), self.TEXT_FORMAT_CONTENT)
                    else :
                        ws.write(i, j, cell, self.TEXT_FORMAT_ALIGN_LEFT)
                else:
                    if j == 0 :
                        link ='HYPERLINK("#\''+ cell + '\'!A1", "'+str(i)+'. '+cell+'")'
                        ws.write(i, j, xlwt.Formula(link), self.TEXT_FORMAT_CONTENT)
                    else:
                        ws.write(i, j, cell, self.TEXT_FORMAT_ALIGN_LEFT)
                self.logger.debug('Write field [%s,%s] content: %s ', str(i), str(j), str(cell))
                j = j + 1
            j = 0
            i = i + 1

        self.logger.info('End creating worksheet %s',sheetname)

        return workbook

    def add_sequence_column(self,content):
        self.logger.info('Start to add a sequence col to the content ')

        row_num = 0
        new_row = []
        new_content = []

        for row in content:
            #skip first row
            if row_num == 0 :
                new_content.append(row)
            #skip first row
            elif row_num == 1 :
                new_row=list(row)
                new_row.insert(0,'#')
                new_content.append(new_row)
            else :
                new_row=list(row)
                new_row.insert(0,row_num-1)
                new_content.append(new_row)
            row_num = row_num + 1

        self.logger.info('Finish to add a sequence col to the content ')

        return new_content

    def add_analyze_review(self,content,analyze_review):
        self.logger.info('Start to add review to the content')
        content.insert(1,[analyze_review])
        return content


    def save_workbook(self,workbook,output_file):
        workbook.save(output_file)

    def __init__(self, log_level=logging.DEBUG, log_file=None):
        self.initialize_log(log_level,log_file)
        self.logger.debug('Initialize io_utility class')

if __name__ == "__main__":
    pass