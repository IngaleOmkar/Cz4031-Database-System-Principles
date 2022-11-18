"""
contains code for GUI
"""

import PySimpleGUI as sg
from preprocessing import *
import annotation

class GUI():

    def __init__(self):
        return

    def initialise_GUI(self):

        sg.theme('LightGrey1')   #theme of GUI
        font = 'Consolas'

        # All the stuff inside the window.
        col1 = [
            [sg.Text('Host:', font=(font, 12), justification='left')],
            [sg.Text('Port:', font=(font, 12), justification='left')],
            [sg.Text('Database:', font=(font, 12), justification='left')],
            [sg.Text('Username:', font=(font, 12), justification='left')],
            [sg.Text('Password:', font=(font, 12), justification='left')],
        ]

        col2 = [
            [sg.Input(key='host', font=(font, 12), default_text='localhost')],
            [sg.Input(key='port', font=(font, 12), default_text='5432')],
            [sg.Input(key='database', font=(font, 12), default_text='TPC-H')],
            [sg.Input(key='username', font=(font, 12), default_text='postgres')],
            [sg.InputText('', key='password', password_char='*', font=(font, 12))],
        ]

        layout = [  
            [sg.Text('Query Execution Plan Annotator', key='-text-', font=(font, 20))],
            [sg.Frame(layout=col1, title=''), sg.Frame(layout=col2, title='')],
            [sg.Button('Submit')]
        ]

        # Create the Window
        window = sg.Window('CX4031 Project 2 GUI', layout, element_justification='c').Finalize()
        
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window.read()
            if event == 'Submit':   # when user clicks submit button

                # get all inputs
                host = values['host'].lower()   #localhost
                port = values['port']   #5432
                database = values['database']   #whatever ur database name is
                username = values['username'].lower()   #postgres
                password = values['password']   #whatever ur password is
                window.close()
                return host, port, database, username, password

            if event == sg.WIN_CLOSED: # if user closes window
                break

        window.close()

    def structure_query(self):
        #make query text look nice
        pretty_query_text = ''
        for text in self.query.lower().split(' '):
            if text == 'from' or  text == "where":
                pretty_query_text += '\n' + text + " "
            elif text == 'and' or  text == "or":
                pretty_query_text += '\n\t' + text + " "
            else:
                pretty_query_text += text + " "
        self.query = pretty_query_text
    
    def new_query(self):
        query = sg.popup_get_text('Enter Query', font=('Consolas', 12), size=(50, 15))
        if query is not None:
            self.query = query
            self.json_query = self.connect.getQueryPlan(query)
            self.query_json_canvas.itemconfig("jsonquery", text = self.json_query)
            self.structure_query()
            self.query_text_canvas.itemconfig("querytext", text = self.query)
            self.canvas.delete('all')
            draw(self.json_query, self.canvas)

    def main_window(self, connect):
        # The main application window
        self.connect = connect
        root = tk.Tk()
        root.title("Query Visualizer")
        
        # Fix root size to 1000x1000
        root.geometry("800x800")
        #root.resizable(0, 0)

        # Function to close the main window
        def close():
            root.destroy()
            return
        
        frame = tk.Frame(root, width = 1000, height = 1200)
        frame.pack(expand=True, fill="both")

        #query plan canvas
        self.canvas = tk.Canvas(frame, bg='white', bd=2)

        scrollbar_v = tk.Scrollbar(frame, orient = tk.VERTICAL)
        scrollbar_v.place(relx=0.99, rely=0, relheight=0.5, relwidth=0.01)
        scrollbar_v.config(command=self.canvas.yview)

        scrollbar_h = tk.Scrollbar(frame, orient = tk.HORIZONTAL)
        scrollbar_h.place(relx=0, rely=0.48, relheight=0.02, relwidth=0.99)
        scrollbar_h.config(command=self.canvas.xview)

        self.canvas.config(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("jsonquery")))
        self.canvas.place(relx=0, rely=0, relheight=0.48, relwidth=0.99)
        
        #query text
        self.query_text_canvas = tk.Canvas(frame, bg = 'white')

        query_text_scrollbar_v = tk.Scrollbar(frame, orient = tk.VERTICAL)
        query_text_scrollbar_v.place(relx=0.49, rely=0.5, relwidth=0.01, relheight=0.5)
        query_text_scrollbar_v.config(command=self.query_text_canvas.yview)

        query_text_scrollbar_h = tk.Scrollbar(frame, orient = tk.HORIZONTAL)
        query_text_scrollbar_h.place(relx=0, rely=0.98, relwidth=0.5, relheight=0.02)
        query_text_scrollbar_h.config(command=self.query_text_canvas.xview)

        self.query_text_canvas.config(yscrollcommand = query_text_scrollbar_v.set, xscrollcommand = query_text_scrollbar_h.set)
        self.query_text_canvas.bind('<Configure>', lambda e: self.query_text_canvas.configure(scrollregion=self.query_text_canvas.bbox("all")))
        self.query_text_canvas.place(relx=0, rely=0.5, relheight=0.48, relwidth=0.49)
        self.query_text_canvas.create_text(250, 70, text='', tags='querytext')

        #query json
        self.query_json_canvas = tk.Canvas(frame, bg = 'white')
        query_json_scrollbar_v = tk.Scrollbar(frame, orient = tk.VERTICAL)
        query_json_scrollbar_v.place(relx=0.99, rely=0.5, relwidth=0.01, relheight=0.5)
        query_json_scrollbar_v.config(command=self.query_json_canvas.yview)

        query_json_scrollbar_h = tk.Scrollbar(frame, orient = tk.HORIZONTAL)
        query_json_scrollbar_h.place(relx=0.5, rely=0.98, relwidth=0.5, relheight=0.02)
        query_json_scrollbar_h.config(command=self.query_json_canvas.xview)

        self.query_json_canvas.config(xscrollcommand=query_json_scrollbar_h.set, yscrollcommand=query_json_scrollbar_v.set)
        self.query_json_canvas.bind('<Configure>', lambda e: self.query_json_canvas.configure(scrollregion=self.query_json_canvas.bbox("all")))
        self.query_json_canvas.place(relx=0.5, rely=0.5, relheight=0.48, relwidth=0.49)
        self.query_json_canvas.create_text(250, 70, text = '', tags="jsonquery")
       
       
        # Create file menu with option to exit
        menu = tk.Menu(root)
        root.config(menu=menu)
        filemenu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Exit", command=close)
        filemenu.add_command(label="New Query", command=self.new_query)


        root.mainloop()