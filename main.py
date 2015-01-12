__author__ = 'ywang'


#!/usr/bin/python

from Tkinter import *
import ttk
import dynamic_table_analysis
import datamart_table_analysis
import performance_analysis
import feeder_analysis
import ConfigParser
import logging
import os
import thread
import threading
import time


class Datamart_analysis_tool(Frame):

    log_level = logging.DEBUG
    logger = ''


    def initialize_log( log_level=None, log_file = None):
        global logger
        logger = logging.getLogger(__name__)

        log_level = logging.INFO

        logger.setLevel(log_level)

        #define log file
        log_directory =os.getcwd()+'\Logs\\'
        log_file = log_directory+'main_screen.log'

        # create a file handler
        handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=1024)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        if log_level is not None:
            handler.setLevel(log_level)
        else:
            handler.setLevel(log_level)

        # add the handlers to the logger
        logger.addHandler(handler)

        logger.info('Log initialized')

    def __init__(self, master=None):
        self.initialize_log()

        logger = logging.getLogger(__name__)

        global root
        root = master

        Frame.__init__(self, master)

        self.create_main_frame()

        self.create_menu()

    def create_main_frame(self):
        logger = logging.getLogger(__name__)

        logger.info('Create master frame')

        frame= Frame(root)

        leftframe = Frame(root)

        check_buttons=[]
        view_output_buttons=dict()
        check_buttons_status=dict()

        current_row = 0

        title = Label(root, text="Datamart Analysis Tool", font=("Helvetica", 20))
        title.grid(columnspan=3,row=current_row)
        current_row = current_row + 1

        #Create empty line
        Label(root,text='').grid(row=current_row)
        current_row = current_row + 1

        #Load reload_data
        general_config=self.load_config('general')
        reload_check_button_status = BooleanVar()
        reload_check_button = Checkbutton(root, text="Reload Data?", variable=reload_check_button_status)
        if general_config['reload_data'] is True:
            reload_check_button.select()
        else:
            reload_check_button.deselect()

        reload_check_button.grid(column=3,row=current_row,sticky=E)

        #Create log level
        log_config=self.load_config('log')
        log_level = log_config['log_level']
        Label(root, text="Log: ").grid(column=0,row=current_row,sticky=W)
        log_dropdown_status = StringVar()
        log_dropdown_status.set(log_level)
        log_dropdown_values = ['INFO', 'DEBUG', 'WARNING', 'ERROR','CRITICAL']
        log_dropdown = OptionMenu(root, log_dropdown_status, *log_dropdown_values)
        log_dropdown.grid(column=0,row=current_row)
        current_row = current_row + 1


        #Create a seperate
        separator = ttk.Separator()
        separator.grid(row=current_row,columnspan=4,sticky=EW)
        current_row = current_row + 1


        #Create labels and buttons
        run_all_check_button_status = IntVar()
        run_all_check_button = Checkbutton(root, text="Select all", height=1, variable=run_all_check_button_status, command=lambda: self.switch_buttons(check_buttons,run_all_check_button_status.get()))
        run_all_check_button.grid(row=current_row,sticky=W)
        current_row = current_row + 1

        dynamic_table_analysis_check_button_status = IntVar()
        dynamic_table_analysis_check_button = Checkbutton(root, text="Dynamic table analysis",variable=dynamic_table_analysis_check_button_status)
        check_buttons.append(dynamic_table_analysis_check_button)
        check_buttons_status["Dynamic table analysis"] = dynamic_table_analysis_check_button_status
        dynamic_table_analysis_config_button = Button(root, text='Config',command=lambda: self.create_config_frame('dynamic table'))
        view_output_buttons['dynamic table'] = Button(root, text='View Output',command=lambda: self.view_result_frame('dynamic table'),state='disabled')
        dynamic_table_analysis_check_button.grid(row=current_row,sticky=W)
        dynamic_table_analysis_config_button.grid(row=current_row,column=2)
        view_output_buttons['dynamic table'].grid(row=current_row,column=3)
        current_row = current_row + 1

        datamart_table_analysis_check_button_status = IntVar()
        datamart_table_analysis_check_button = Checkbutton(root, text="Datamart table analysis",variable=datamart_table_analysis_check_button_status)
        check_buttons.append(datamart_table_analysis_check_button)
        check_buttons_status["Datamart table analysis"] = datamart_table_analysis_check_button_status
        datamart_table_analysis_config_button = Button(root, text='Config', command=lambda: self.create_config_frame('datamart table') )
        view_output_buttons['datamart table'] = Button(root, text='View Output',command=lambda: self.view_result_frame('datamart table'),state='disabled')
        datamart_table_analysis_check_button.grid(row=current_row,sticky=W)
        datamart_table_analysis_config_button.grid(row=current_row,column=2)
        view_output_buttons['datamart table'].grid(row=current_row,column=3)
        current_row = current_row + 1

        feeder_analysis_check_button_status = IntVar()
        feeder_analysis_check_button = Checkbutton(root, text="Feeder analysis",variable=feeder_analysis_check_button_status)
        check_buttons.append(feeder_analysis_check_button)
        check_buttons_status["Feeder analysis"] = feeder_analysis_check_button_status
        feeder_analysis_config_button = Button(root, text='Config',command=lambda: self.create_config_frame('feeder'))
        view_output_buttons['feeder'] = Button(root, text='View Output',command=lambda: self.view_result_frame('feeder'),state='disabled')
        feeder_analysis_check_button.grid(row=current_row,sticky=W)
        feeder_analysis_config_button.grid(row=current_row,column=2)
        view_output_buttons['feeder'].grid(row=current_row,column=3)
        current_row = current_row + 1

        performance_analysis_check_button_status = IntVar()
        performance_analysis_check_button = Checkbutton(root, text="Performance analysis",variable=performance_analysis_check_button_status)
        check_buttons.append(performance_analysis_check_button)
        check_buttons_status["Performance analysis"] = performance_analysis_check_button_status
        #performance_analysis_run_button = Button(master, text='Run', command=self.load_performance_analysis)
        performance_analysis_config_button = Button(root, text='Config',command=lambda: self.create_config_frame('performance'))
        view_output_buttons['performance'] = Button(root, text='View Output',command=lambda: self.view_result_frame('performance'),state='disabled')
        performance_analysis_check_button.grid(row=current_row,sticky=W)
        #performance_analysis_run_button.grid(row=current_row,column=1)
        performance_analysis_config_button.grid(row=current_row,column=2)
        view_output_buttons['performance'].grid(row=current_row,column=3)
        current_row = current_row + 1

        #Create empty line
        Label(root,text='').grid(row=current_row)
        current_row = current_row + 1

        #create progress bar
        execution_progress_bar = ttk.Progressbar(root, orient='horizontal', mode='indeterminate',length=180)
        execution_progress_bar.grid(row=current_row,column=1, columnspan=3,sticky=W)

        #create running button
        run_analysis_button=Button(root, text="Run Analysis",command=lambda: self.run_anslysis(run_analysis_button,view_output_buttons, check_buttons_status,reload_check_button_status, log_dropdown_status,execution_progress_bar))
        run_analysis_button.grid(row=current_row,column=0)



        current_row = current_row + 1

        #Create empty line
        Label(root,text='',height=1).grid(row=current_row)
        current_row = current_row + 1

    def create_menu(self):
        menubar = Menu(root)

        # create a pulldown menu, and add it to the menu bar
        filemenu = Menu(menubar, tearoff=0)

        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        optionmenu = Menu(menubar, tearoff=0)
        optionmenu.add_command(label="General Setting", command=lambda: self.create_config_frame('general'))
        menubar.add_cascade(label="Option", menu=optionmenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.create_about_frame)
        menubar.add_cascade(label="Help", menu=helpmenu)

        # display the menu
        root.config(menu=menubar)

    def create_about_frame(self):
        logger = logging.getLogger(__name__)

        about_root = Toplevel()

        about_root.wm_title("About")

        logger.info('Create help frame')

        current_row=0
        about_root.wm_maxsize(260,130)
        about_root.wm_minsize(260,130)
        Label(about_root, text="Datamart analysis tool",padx=5, pady=10,font=("Helvetica", 18)).grid(row=current_row)
        current_row = current_row+1
        Label(about_root, text="v1.0 by Wang Yong",pady=10).grid(row=current_row)
        current_row = current_row+1

        Button(about_root, text="OK", command=about_root.destroy).grid(row=current_row)

    def switch_buttons(self, check_buttons, status=0):
        if status:
            for check_button in check_buttons:
                check_button.select()
        else:
            for check_button in check_buttons:
                check_button.deselect()

    def run_anslysis(self,run_analysis_button, view_output_buttons, check_buttons_status,reload_check_button_status,log_dropdown_status,execution_progress_bar):
        any_button_checked = False

        global execution_threads
        execution_threads = dict()

        for analysis_type, button_status in check_buttons_status.iteritems():
            if analysis_type == 'Dynamic table analysis' and button_status.get() :
                try:
                    execution_threads['dynamic table']=threading.Thread( target=self.load_dynamic_table_analysis, args=(reload_check_button_status.get(),log_dropdown_status.get(),) )
                    execution_threads['dynamic table'].start()
                except:
                    self.create_error_frame('Error','Unable to start thread')
                any_button_checked = True
            if analysis_type == 'Datamart table analysis' and button_status.get() :
                try:
                    execution_threads['datamart table']=threading.Thread(target=self.load_datamart_table_analysis,  args=(reload_check_button_status.get(),log_dropdown_status.get(),) )
                    execution_threads['datamart table'].start()
                except:
                    self.create_error_frame('Error','Unable to start thread')
                any_button_checked = True
            if analysis_type == 'Feeder analysis' and button_status.get() :
                try:
                    execution_threads['feeder']=threading.Thread(target=self.load_feeder_analysis,  args=(reload_check_button_status.get(),log_dropdown_status.get(),) )
                    execution_threads['feeder'].start()
                except:
                    self.create_error_frame('Error','Unable to start thread')
                any_button_checked = True
            if analysis_type == 'Performance analysis' and button_status.get() :
                try:
                    execution_threads['performance']=threading.Thread(target=self.load_performance_analysis,  args=(reload_check_button_status.get(),log_dropdown_status.get(),))
                    execution_threads['performance'].start()
                except:
                    self.create_error_frame('Error','Unable to start thread')
                any_button_checked = True

        if any_button_checked is False:
            self.create_error_frame('Error','Nothing is selected!')
        else:
            run_analysis_button.config(state='disable')
            execution_progress_bar.start(30)
            observe_thread = threading.Thread(target=self.checking_execution_thread,  args=(execution_threads,execution_progress_bar,run_analysis_button,view_output_buttons,))
            observe_thread.start()

    def checking_execution_thread(self,execution_threads,execution_progress_bar,run_analysis_button,view_output_buttons):
        logging.info('Monitoring thread starting')

        thread_to_kill=[]

        while True:
            if len(execution_threads) == 0:
                execution_progress_bar.stop()
                run_analysis_button.config(state='active')
                return
            for thread_name, thread in execution_threads.iteritems():
                if not thread.isAlive():
                    view_output_buttons[thread_name].config(state='active')
                    thread_to_kill.append(thread_name)
                else:
                    view_output_buttons[thread_name].config(state='disabled')

            for thread_name in thread_to_kill:
                execution_threads.pop(thread_name,None)

            time.sleep(2)

    def load_dynamic_table_analysis(self,reload_check_button_status,log_dropdown_status):
        logger = logging.getLogger(__name__)
        logger.info('Run dynamic_table_analysis')
        dynamic_table_analysis.run(reload_check_button_status,log_dropdown_status)

    def load_datamart_table_analysis(self,reload_check_button_status,log_dropdown_status):
        logger = logging.getLogger(__name__)
        logger.info('Run datamart_table_analysis')
        datamart_table_analysis.run(reload_check_button_status,log_dropdown_status)

    def load_performance_analysis(self,reload_check_button_status,log_dropdown_status):
        logger = logging.getLogger(__name__)
        logger.info('Run performance_analysis')
        performance_analysis.run(reload_check_button_status,log_dropdown_status)

    def load_feeder_analysis(self,reload_check_button_status,log_dropdown_status):
        logger = logging.getLogger(__name__)
        logger.info('Run feeder_analysis')
        feeder_analysis.run(reload_check_button_status,log_dropdown_status)

    def load_config(self, analysis_type=None):
        logger = logging.getLogger(__name__)
        logger.info('Run feeder_analysis')

        #propery file defitnion
        property_directory=os.getcwd()+'\\properties\\'
        parameter_file='parameters.txt'

        #Read in property file
        config = ConfigParser.RawConfigParser()
        config.read(property_directory + parameter_file)

        configs = dict()

        if analysis_type == None :
            pass
        elif analysis_type == 'dynamic table':
            max_dynamic_number_fields = config.getint('dynamic table', 'max_number_fields')
            max_dynamic_number_hfields = config.getint('dynamic table', 'max_number_h_fields')
            max_dynamic_number_db_access_hfields = config.getint('dynamic table', 'max_number_db_access_h_fields')
            output_file_name = config.get('dynamic table', 'output_file_name')
            configs['max_number_fields']=max_dynamic_number_fields
            configs['max_number_h_fields']=max_dynamic_number_hfields
            configs['max_number_db_access_h_fields']=max_dynamic_number_db_access_hfields
            configs['output_file_name']=output_file_name

        elif analysis_type == 'datamart table' :
            max_datamart_fields = config.getint('datamart table', 'max_number_fields')
            output_file_name = config.get('dynamic table', 'output_file_name')
            configs['max_number_fields']=max_datamart_fields
            configs['output_file_name']=output_file_name

        elif analysis_type == 'performance' :
            period_days = config.getint('performance', 'period_days')
            start_date = config.get('performance', 'start_date')
            end_date = config.get('performance', 'end_date')
            time_alert_processing_script = config.get('performance', 'time_alert_processing_script')
            time_alert_batch_feeder = config.get('performance', 'time_alert_batch_feeder')
            time_alert_batch_extraction =config.get('performance', 'time_alert_batch_extraction')
            output_file_name = config.get('dynamic table', 'output_file_name')
            configs['period_days']=period_days
            configs['start_date']=start_date
            configs['end_date']=end_date
            configs['time_alert_processing_script']=time_alert_processing_script
            configs['time_alert_batch_feeder']=time_alert_batch_feeder
            configs['time_alert_batch_extraction']=time_alert_batch_extraction
            configs['output_file_name']=output_file_name

        elif analysis_type == 'feeder' :
            output_file_name = config.get('dynamic table', 'output_file_name')
            configs['output_file_name']=output_file_name

        elif analysis_type == 'general' :
            #general settings
            reload_data = config.getboolean('general', 'reload_data')
            input_directory = config.get('general', 'input_directory')
            output_directory = config.get('general', 'output_directory')
            sql_directory = config.get('general', 'sql_directory')
            log_directory = config.get('general', 'log_directory')
            configs['reload_data']=reload_data
            configs['input_directory']=input_directory
            configs['output_directory']=output_directory
            configs['sql_directory']=sql_directory
            configs['log_directory']=log_directory

        elif analysis_type == 'log' :
            #general settings
            log_level = config.get('log', 'log_level')
            configs['log_level']=log_level

        return configs

    def view_result_frame(self,analysis_type):
        logger = logging.getLogger(__name__)

        logger.info('View %s output excel file',analysis_type)

        #propery file defitnion
        property_directory=os.getcwd()+'\\properties\\'
        parameter_file='parameters.txt'

        #Read in property file
        config = ConfigParser.RawConfigParser()
        config.read(property_directory + parameter_file)
        output_folder = config.get('general', 'output_directory')
        output_file = output_folder + '\\'+config.get(analysis_type, 'output_file_name')


        os.system("start excel "+output_file);

    def create_config_frame(self,analysis_type):

        logger = logging.getLogger(__name__)

        config_root = Toplevel()

        config_root.wm_title("Config")

        logger.info('Create config frame')

        configs=self.load_config(analysis_type)

        config_gui_items = dict()

        title = Label(config_root, text="Config Settings for "+analysis_type, font=("Helvetica", 20))
        title.grid(columnspan=3,row=0)

        current_row=2

        for config_name, config_content in configs.iteritems():
            config_text = Label(config_root, text=config_name)
            config_text.grid(row=current_row,sticky=W)

            config_entry = Entry(config_root)
            config_entry.grid(row=current_row,column=1,sticky=W)
            config_entry.insert(0,config_content)

            config_gui_items[config_name]=config_entry

            current_row = current_row + 1

        #Create empty line
        Label(config_root,text='').grid(row=current_row)
        current_row = current_row + 1

        save_button = Button(config_root, text='Apply', command=lambda: self.save_config(analysis_type,config_gui_items))
        save_button.grid(column=1,row=current_row,sticky=W)

        exit_button =Button(config_root, text='Exit', command=config_root.destroy)
        exit_button.grid(column=1,row=current_row)

    def create_error_frame(self,title, content):
        logger = logging.getLogger(__name__)

        error_root = Toplevel()

        error_root.wm_title("Error")

        error_root.minsize(200,100)
        error_root.maxsize(200,100)

        logger.info('Create error frame')

        current_row=0

        #create title
        Label(error_root,text='').grid(column=0,row=current_row, sticky=E)
        Label(error_root, text=title, font=("Helvetica", 15)).grid(column=1,row=current_row)
        Label(error_root,text='').grid(column=2,row=current_row, sticky=E)
        current_row = current_row+1


        #create content
        Label(error_root,text='',padx=20).grid(column=0,row=current_row, sticky=E)
        Label(error_root,text=content).grid(column=1,row=current_row, sticky=E)
        Label(error_root,text='').grid(column=2,row=current_row, sticky=E)
        current_row = current_row + 1

        #create blank line
        Label(error_root,text='').grid(column=0,row=current_row, sticky=E)
        current_row=current_row + 1

        #create exit button
        Label(error_root,text='').grid(column=0,row=current_row, sticky=E)
        Button(error_root, text='Ok', command=error_root.destroy).grid(column=1,row=current_row)
        Label(error_root,text='').grid(column=2,row=current_row, sticky=E)
        current_row = current_row + 1


    def save_config(self,analysis_type, config_gui_items):
        logger = logging.getLogger(__name__)
        logger.info('Save config')

        #propery file defitnion
        property_directory=os.getcwd()+'\\properties\\'
        parameter_file='parameters.txt'

        #Write property file
        config = ConfigParser.RawConfigParser()
        config.read(property_directory + parameter_file)

        raw_file= open(property_directory+parameter_file, 'w')

        for config_name, config_entry in config_gui_items.iteritems():
            config.set(analysis_type,config_name,config_entry.get())

        config.write(raw_file)


if __name__ == "__main__":
    root = Tk()
    root.wm_title("Datamart analysis")

    app = Datamart_analysis_tool(master=root)
    app.mainloop()