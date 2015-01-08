__author__ = 'ywang'

from xlwt import *
import logging
from logging import handlers

class io_utility:

    logger = ''

    def initialize_log(self,log_level = logging.DEBUG, log_file = None):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

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

    TEXT_FORMAT = easyxf(
        'font: bold 1, name Roma, height 160;'
        'align: vertical center, horizontal center, wrap on;'
        'borders: left thin, right thin, top thin, bottom thin;'
        'pattern: pattern solid, pattern_fore_colour white, pattern_back_colour gray25'
    )

    HIGHLIGHTED_TEXT_FORMAT = easyxf(
        'font: bold 1, name Roma, height 160;'
        'align: vertical center, horizontal center, wrap on;'
        'borders: left thin, right thin, top thin, bottom thin;'
        'pattern: pattern solid, pattern_fore_colour green, pattern_back_colour gray25'
    )

    def read_txt(self,filename):
        pass

    def write_txt(self,filename):
        pass

    def read_csv(self,filename):
        pass

    def write_csv(self,content, filename):
        pass

    def add_worksheet(self,content, workbook, sheetname, highlighted=False):
        self.logger.info('Start to create worksheet %s',sheetname)
        ws = workbook.add_sheet(sheetname)

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

    def save_workbook(self,workbook,output_file):
        workbook.save(output_file)

    def __init__(self, log_level=logging.DEBUG, log_file=None):
        self.initialize_log(log_level,log_file)
        self.logger.info('Initialize io_utility class')

if __name__ == "__main__":
    #io=io_utility()

    a={'a':[1,2],'b':[3,4],'c':[5,6],'d':[7,8,9]}
    b='c'
    for b in a.keys():
        print b

    # io.logger.info('aaa')
    # io.logger.warning('bbb')
    # io.set_log_level(logging.WARNING)
    # io.logger.info('ccc')
    # io.logger.warning('dddd')