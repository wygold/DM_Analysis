__author__ = 'ywang'


#!/usr/bin/python

from Tkinter import *
import ttk
import dynamic_table_analysis
import datamart_table_analysis
import performance_analysis
import feeder_analysis
import core_analysis
from property_utility import property_utility


import ConfigParser
import logging
import os
import thread
import threading
import time


class Datamart_analysis_tool(Frame):

    logger = ''

    def initialize_log(self,log_level=None, log_file = None):
        global logger
        logger = logging.getLogger(__name__)

        if log_level is None:
            logger.setLevel(logging.INFO)
        else :
            logger.setLevel(log_level)

        #define log file
        if log_file is None:
            log_directory =os.getcwd()+'\Logs\\'
            local_log_file = log_directory+'main_screen.log'
        else:
            local_log_file = log_file

        if logger.handlers == []:
            # create a file handler
            handler = logging.handlers.RotatingFileHandler(local_log_file, maxBytes=1024)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)

            if log_level is None:
                handler.setLevel(logging.INFO)
            else :
                handler.setLevel(log_level)

            # add the handlers to the logger
            logger.addHandler(handler)


    def __init__(self, master=None):

        global  parameters
        property_util = property_utility()
        parameters = property_util.parse_property_file()

        log_level = parameters['log']['log_level']
        log_file = parameters['log']['log_directory']+'\\main_screen.log'

        self.initialize_log(log_level,log_file)

        global root

        root = master

        Frame.__init__(self, master)

        self.create_main_frame()

        self.create_menu()

    def create_main_frame(self):
        logger = logging.getLogger(__name__)

        logger.info('Create master frame')

        check_buttons=[]
        view_output_buttons=dict()
        check_buttons_status=dict()

        main_frame_objects = dict()

        current_row = 0

        title = Label(root, text="Datamart Analysis Tool \n (MUREX Internal Use Only)", font=("Helvetica", 20))
        title.grid(columnspan=6,row=current_row)
        main_frame_objects['title']=title
        current_row = current_row + 1

        #Create empty line
        Label(root,text='').grid(row=current_row)
        current_row = current_row + 1

        #Load reload_data
        reload_check_button_status = BooleanVar()
        reload_check_button = Checkbutton(root, text="Reload Data?", variable=reload_check_button_status)
        if parameters['general']['reload_data'] is True:
            reload_check_button.select()
        else:
            reload_check_button.deselect()

        reload_check_button.grid(column=3,row=current_row,sticky=E)

        #Create log level
        log_level = parameters['log']['log_level']
        Label(root, text="Log: ").grid(column=0,row=current_row,sticky=W)
        log_dropdown_status = StringVar()
        log_dropdown_status.set(log_level)
        log_dropdown_values = [ 'DEBUG','INFO', 'WARNING', 'ERROR','CRITICAL']
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
        run_all_check_button.grid(row=current_row,column=0,sticky=W)

        expand_log_button = Button(root, text="Show log >", height=1, command=lambda: self.show_log(main_frame_objects))
        expand_log_button.grid(row=current_row,column=3)

        main_frame_objects['expand_log_button']=expand_log_button

        current_row = current_row + 1

        core_analysis_check_button_status = IntVar()
        core_analysis_check_button = Checkbutton(root, text="Core analysis",variable=core_analysis_check_button_status)
        check_buttons.append(core_analysis_check_button)
        check_buttons_status["core"] = core_analysis_check_button_status
        #performance_analysis_run_button = Button(master, text='Run', command=self.load_performance_analysis)
        core_analysis_config_button = Button(root, text='Config',command=lambda: self.create_config_frame('core'))
        view_output_buttons['core'] = Button(root, text='View Output',command=lambda: self.view_result_frame('core'),state='disabled')
        core_analysis_check_button.grid(row=current_row,sticky=W)
        #performance_analysis_run_button.grid(row=current_row,column=1)
        core_analysis_config_button.grid(row=current_row,column=2)
        view_output_buttons['core'].grid(row=current_row,column=3)
        current_row = current_row + 1

     
        dynamic_table_analysis_check_button_status = IntVar()
        dynamic_table_analysis_check_button = Checkbutton(root, text="Dynamic tables analysis",variable=dynamic_table_analysis_check_button_status)
        check_buttons.append(dynamic_table_analysis_check_button)
        check_buttons_status["dynamic table"] = dynamic_table_analysis_check_button_status
        dynamic_table_analysis_config_button = Button(root, text='Config',command=lambda: self.create_config_frame('dynamic table'))
        view_output_buttons['dynamic table'] = Button(root, text='View Output',command=lambda: self.view_result_frame('dynamic table'),state='disabled')
        dynamic_table_analysis_check_button.grid(row=current_row,sticky=W)
        dynamic_table_analysis_config_button.grid(row=current_row,column=2)
        view_output_buttons['dynamic table'].grid(row=current_row,column=3)
        current_row = current_row + 1

        datamart_table_analysis_check_button_status = IntVar()
        datamart_table_analysis_check_button = Checkbutton(root, text="Datamart tables analysis",variable=datamart_table_analysis_check_button_status)
        check_buttons.append(datamart_table_analysis_check_button)
        check_buttons_status["datamart table"] = datamart_table_analysis_check_button_status
        datamart_table_analysis_config_button = Button(root, text='Config', command=lambda: self.create_config_frame('datamart table') )
        view_output_buttons['datamart table'] = Button(root, text='View Output',command=lambda: self.view_result_frame('datamart table'),state='disabled')
        datamart_table_analysis_check_button.grid(row=current_row,sticky=W)
        datamart_table_analysis_config_button.grid(row=current_row,column=2)
        view_output_buttons['datamart table'].grid(row=current_row,column=3)
        current_row = current_row + 1

        feeder_analysis_check_button_status = IntVar()
        feeder_analysis_check_button = Checkbutton(root, text="TFs and BoFs analysis",variable=feeder_analysis_check_button_status)
        check_buttons.append(feeder_analysis_check_button)
        check_buttons_status["feeder"] = feeder_analysis_check_button_status
        feeder_analysis_config_button = Button(root, text='Config',command=lambda: self.create_config_frame('feeder'))
        view_output_buttons['feeder'] = Button(root, text='View Output',command=lambda: self.view_result_frame('feeder'),state='disabled')
        feeder_analysis_check_button.grid(row=current_row,sticky=W)
        feeder_analysis_config_button.grid(row=current_row,column=2)
        view_output_buttons['feeder'].grid(row=current_row,column=3)
        current_row = current_row + 1

        performance_analysis_check_button_status = IntVar()
        performance_analysis_check_button = Checkbutton(root, text="Performance analysis",variable=performance_analysis_check_button_status)
        check_buttons.append(performance_analysis_check_button)


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

        #create a empty
        Label(root, width=1, text='',height=18).grid(row=2, rowspan=current_row-2,column=4)


        #Create empty verticle line
        Label(root,text='',height=1).grid(row=current_row)


        #Create the scroll bar for the log text box
        log_scrollbar = Scrollbar(root)
        log_scrollbar.grid(row=2, rowspan=current_row-2,column=6, sticky='ens')
        log_scrollbar.grid_remove()

        #create a log text box
        log_text=Text(root, width=50,height=18,font=("Helvetica",8), yscrollcommand=log_scrollbar.set)
        log_text.grid(row=2, rowspan=current_row-2,column=5,sticky='ns')
        log_text.insert(END,'Welcome to Datamart analysis tools\n')
        log_text.grid_remove()
        main_frame_objects['log_text']=log_text


        log_scrollbar.config(command=log_text.yview)
        main_frame_objects['log_scrollbar']=log_scrollbar

        #Create clear log_text button
        clear_log_text_button = Button(root, text='Clear Log',command=lambda: log_text.delete(1.0,END))
        clear_log_text_button.grid(row=current_row,column=5, sticky=E)
        clear_log_text_button.grid_remove()
        main_frame_objects['clear_log_text_button']=clear_log_text_button

        #Create empty verticle line
        Label(root, width=1, text='').grid(row=2, rowspan=current_row-1,column=6)

        #create running button
        run_analysis_button=Button(root, text="Run Analysis",command=lambda: self.run_analysis(run_analysis_button,view_output_buttons, check_buttons_status,reload_check_button_status, log_dropdown_status,execution_progress_bar,log_text))
        run_analysis_button.grid(row=current_row,column=0)

        current_row = current_row + 1

        #Create empty line
        Label(root,text='').grid(row=current_row)
        current_row = current_row + 1

        #Create a seperate
        separator = ttk.Separator()
        separator.grid(row=current_row,columnspan=4,sticky=EW)
        current_row = current_row + 1



    def create_menu(self):
        menubar = Menu(root)

        # create a pulldown menu, and add it to the menu bar
        filemenu = Menu(menubar, tearoff=0)

        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        optionmenu = Menu(menubar, tearoff=0)
        optionmenu.add_command(label="General Setting", command=lambda: self.create_config_frame('general', window_title = 'General Settings'))
        optionmenu.add_command(label="Database Setting", command=lambda: self.create_config_frame('database', window_title = 'Database Settings'))
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
        about_root.wm_maxsize(260,180)
        about_root.wm_minsize(260,180)
        Label(about_root, text="Datamart analysis tool",padx=5, pady=10,font=("Helvetica", 18)).grid(row=current_row)
        current_row = current_row+1
        Label(about_root, text="Disclamer: The tool is internal use only \n Murex will not provide any support.",pady=10).grid(row=current_row)
        current_row = current_row+1
        Label(about_root, text="v1.1 (beta)",pady=10).grid(row=current_row)
        current_row = current_row+1

        Button(about_root, text="OK", command=about_root.destroy).grid(row=current_row)

    def switch_buttons(self, check_buttons, status=0):
        if status:
            for check_button in check_buttons:
                check_button.select()
        else:
            for check_button in check_buttons:
                check_button.deselect()

    #show log text window
    def show_log(self,main_frame_objects):
        log_text = main_frame_objects['log_text']
        log_text.grid()
        clear_log_text_button=main_frame_objects['clear_log_text_button']
        clear_log_text_button.grid()

        expand_log_button=main_frame_objects['expand_log_button']
        expand_log_button.grid_remove()

        log_scrollbar=main_frame_objects['log_scrollbar']
        log_scrollbar.grid()

        unexpand_log_button = Button(root, text="Hide log <", height=1, command=lambda: self.hide_log(main_frame_objects))
        unexpand_log_button.grid(row=4,column=3)
        main_frame_objects['unexpand_log_button']=unexpand_log_button

    #hide log text window
    def hide_log(self,main_frame_objects):
        log_text = main_frame_objects['log_text']
        log_text.grid_remove()
        clear_log_text_button=main_frame_objects['clear_log_text_button']
        clear_log_text_button.grid_remove()

        log_scrollbar=main_frame_objects['log_scrollbar']
        log_scrollbar.grid_remove()

        expand_log_button=main_frame_objects['expand_log_button']
        expand_log_button.grid()

        unexpand_log_button=main_frame_objects['unexpand_log_button']
        unexpand_log_button.grid_remove()

    def run_analysis(self,run_analysis_button, view_output_buttons, check_buttons_status,reload_check_button_status,log_dropdown_status,execution_progress_bar,log_text):
        log_text.delete(1.0,END)
        try:
            work_thread=threading.Thread( target=self.analysis_worker_thread, args=(run_analysis_button, view_output_buttons, check_buttons_status,reload_check_button_status,log_dropdown_status,execution_progress_bar,log_text,) )
            work_thread.start()
            observe_thread = threading.Thread(target=self.checking_execution_thread,  args=(work_thread,execution_progress_bar,check_buttons_status,run_analysis_button,view_output_buttons,))
            observe_thread.start()
        except:
            self.create_error_frame('Error','Unable to start thread')

    def analysis_worker_thread(self,run_analysis_button, view_output_buttons, check_buttons_status,reload_check_button_status,log_dropdown_status,execution_progress_bar,log_text):
        for analysis_type, button_status in check_buttons_status.iteritems():
            if analysis_type == 'core' and button_status.get() :
                monitor_log_file_stop= threading.Event()
                self.monitor_log_file(analysis_type,log_text,monitor_log_file_stop)
                self.load_core_analysis(reload_check_button_status.get(),log_dropdown_status.get())
                time.sleep(1)
                monitor_log_file_stop.set()
            if analysis_type == 'dynamic table' and button_status.get() :
                monitor_log_file_stop= threading.Event()
                self.monitor_log_file(analysis_type,log_text,monitor_log_file_stop)
                self.load_dynamic_table_analysis(reload_check_button_status.get(),log_dropdown_status.get())
                time.sleep(1)
                monitor_log_file_stop.set()
            if analysis_type == 'datamart table' and button_status.get() :
                monitor_log_file_stop= threading.Event()
                self.monitor_log_file(analysis_type,log_text,monitor_log_file_stop)
                self.load_datamart_table_analysis(reload_check_button_status.get(),log_dropdown_status.get())
                time.sleep(1)
                monitor_log_file_stop.set()
            if analysis_type == 'feeder' and button_status.get() :
                monitor_log_file_stop= threading.Event()
                self.monitor_log_file(analysis_type,log_text,monitor_log_file_stop)
                self.load_feeder_analysis(reload_check_button_status.get(),log_dropdown_status.get())
                time.sleep(1)
                monitor_log_file_stop.set()
            if analysis_type == 'performance' and button_status.get() :
                monitor_log_file_stop= threading.Event()
                self.monitor_log_file(analysis_type,log_text,monitor_log_file_stop)
                self.load_performance_analysis(reload_check_button_status.get(),log_dropdown_status.get())
                time.sleep(1)
                monitor_log_file_stop.set()

    def checking_execution_thread(self,work_thread,execution_progress_bar,check_buttons_status,run_analysis_button,view_output_buttons):
        logging.info('Monitoring thread starting')

        #disable view result buttons
        for analysis_type, button_status in check_buttons_status.iteritems():
            if analysis_type == 'core' and button_status.get() :
                view_output_buttons[analysis_type].config(state='disabled')
            if analysis_type == 'dynamic table' and button_status.get() :
                view_output_buttons[analysis_type].config(state='disabled')
            if analysis_type == 'datamart table' and button_status.get() :
                view_output_buttons[analysis_type].config(state='disabled')
            if analysis_type == 'feeder' and button_status.get() :
                view_output_buttons[analysis_type].config(state='disabled')
            if analysis_type == 'performance' and button_status.get() :
                view_output_buttons[analysis_type].config(state='disabled')

        #disable run result button
        run_analysis_button.config(state='disable')

        #start progress bar
        execution_progress_bar.start(30)

        while True:
            if not work_thread.isAlive() :
                execution_progress_bar.stop()
                run_analysis_button.config(state='active')
                for analysis_type, button_status in check_buttons_status.iteritems():
                    if analysis_type == 'core' and button_status.get() :
                        view_output_buttons[analysis_type].config(state='active')
                    if analysis_type == 'dynamic table' and button_status.get() :
                        view_output_buttons[analysis_type].config(state='active')
                    if analysis_type == 'datamart table' and button_status.get() :
                        view_output_buttons[analysis_type].config(state='active')
                    if analysis_type == 'feeder' and button_status.get() :
                        view_output_buttons[analysis_type].config(state='active')
                    if analysis_type == 'performance' and button_status.get() :
                        view_output_buttons[analysis_type].config(state='active')
                return
            time.sleep(2)

    def monitor_log_file(self, analysis_type,log_text,monitor_log_file_stop):

        log_monitor_thread = ''

        try:
            log_file_name= parameters[analysis_type]['log_file_name']
            log_monitor_thread=threading.Thread(target=self.monitor_log_file_thread, args=(log_file_name,log_text,monitor_log_file_stop,) )
            log_monitor_thread.start()
        except:
            self.show_error(log_text, 'Error: Unable to start working thread!')

        return log_monitor_thread

    def monitor_log_file_thread(self, log_file,log_text,monitor_log_file_stop):
        try:
            log_file=os.getcwd()+'\\'+parameters['log']['log_directory']+'\\'+log_file
            file = open(log_file,'r')

            #Find the size of the file and move to the end
            st_results = os.stat(log_file)
            st_size = st_results[6]
            file.seek(st_size)

            while (not monitor_log_file_stop.is_set()):
                where = file.tell()
                line = file.readline()
                if not line:
                    time.sleep(0.1)
                    file.seek(where)
                else:
                    log_text.insert(END,line)
                    log_text.yview(END)
                    #print line, # already has newline
        except:
            self.show_error(log_text, 'Error: Unable to monitor the log file '+log_file+'!')

        return

    def show_error(self,text_box, error_message):
        text_box.insert(END,error_message)

    def load_core_analysis(self,reload_check_button_status,log_dropdown_status):
        logger = logging.getLogger(__name__)
        logger.info('Run core_analysis')
        core_analysis.run(reload_check_button_status,log_dropdown_status)

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

    def create_config_frame(self,analysis_type,  window_title = None):

        logger = logging.getLogger(__name__)

        config_root = Toplevel()



        if window_title is None :
            config_root.wm_title("Config")
        else :
            config_root.wm_title(window_title)
        logger.info('Create config frame')

        for parameter_type, parameter in parameters.iteritems():
            if parameter_type == analysis_type:
                configs = parameter

        config_gui_items = dict()

        current_row=1

        #Create empty line
        Label(config_root,text='').grid(row=current_row)
        current_row = current_row + 1

        for config_name, config_content in configs.iteritems():
            config_text = Label(config_root, text=config_name+' ')
            config_text.grid(row=current_row,sticky=E)

            config_entry = Entry(config_root,width=30)
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

        #Create empty column
        Label(config_root,text=' ').grid(column=2,rowspan=4,sticky=NS)
        current_row = current_row + 1

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
            parameters[analysis_type][config_name]=config_entry.get()

        config.write(raw_file)

if __name__ == "__main__":
    root = Tk()
    root.wm_title("Datamart analysis")

    app = Datamart_analysis_tool(master=root)
    app.mainloop()