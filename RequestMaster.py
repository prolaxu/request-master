import tkinter as tk
import json
import sys
import os
import requests


class App:
    def __init__(self):
        configfile = open('config.json', 'r')
        configx = ""
        for x in configfile:
            configx = configx+x
        config = json.loads(configx)
        self.root = tk.Tk()
        self.header(config)
        self.main()
        self.root.mainloop()

    def header(self, config):
        self.root.title(config['title'])
        self.title = config['title']
        self.root.minsize(int(config['size']['min']['x']), int(
            config['size']['min']['y']))
        self.root.maxsize(int(config['size']['max']['x']), int(
            config['size']['min']['y']))
        program_directory = sys.path[0]
        print(program_directory)
        try:
            self.root.iconphoto(True, tk.PhotoImage(
                file=os.path.join(program_directory, config['icon'])))
        except:
            print("Unable to load icon only png supported.")

    def request(self):
        print("request send")
        print("URL     : "+self.url.get())
        print("Medthod : "+self.variable.get())
        print("Agent   : "+self.agent.get())
        print("Data    : "+self.data.get("1.0", 'end-1c'))
        x=""
        myobj = self.data.get("1.0", 'end-1c')
        useragent = {'User-agent': self.agent.get()}
        if (self.variable.get() == 'get'):
                x = requests.get(self.url.get(), headers=useragent ,params=json.loads(myobj))
        else:
                x = requests.post(self.url.get(), headers=useragent, data=json.loads(myobj))
        print(x.text)

        # insert text
        self.op.delete('1.0', 'end-1c')
        content = x.text
        self.op.insert('1.0', content)
        # disable text widget to prevent editing
        # self.op.configure(state='disabled')

    def dataloader(self):
        self.dloader = tk.Frame(self.root, width=50)
        self.dloader.grid(row=0, column=1)
        # lb = tk.Label(self.root, text="Response")
        # lb.grid(row=0, column=0)
        # create text widget
        self.op = tk.Text(self.dloader, relief='flat', height=15)
        # scrolling
        scroll = tk.Scrollbar(
            self.dloader, orient='vertical', command=self.op.yview)
        self.op.configure(yscrollcommand=scroll.set)

        scroll.pack(side='right', fill='y')
        self.op.pack(side='left', fill='both', expand=True)

    def main(self):
        self.frame = tk.Frame(self.root)
        self.frame.grid(row=0, column=0)
        h1 = tk.Label(self.frame, text=self.title)
        h1.grid(row=0, column=2)

        txt = tk.Label(self.frame, text="Url : ")
        txt.grid(row=1, column=1)
        self.url = tk.Entry(self.frame, width=40)
        self.url.grid(row=1, column=2)
        self.url.insert(0, "http://www.example.com/")
        self.variable = tk.StringVar(self.frame)
        self.variable.set("post")  # default value

        txt = tk.Label(self.frame, text="Method : ")
        txt.grid(row=2, column=1)
        self.w = tk.OptionMenu(self.frame, self.variable, "post", "get")
        self.w.config(width=35, indicatoron=False)
        self.w.grid(row=2, column=2)

        txt = tk.Label(self.frame, text="Agent : ")
        txt.grid(row=3, column=1)
        self.agent = tk.Entry(self.frame, width=40)
        self.agent.grid(row=3, column=2)
        self.agent.insert(
            0, "Mozilla/5.0")
        txt = tk.Label(self.frame, text="Data : ")
        txt.grid(row=4, column=1)
        self.data = tk.Text(self.frame, width=35, height=8)
        self.data.grid(row=4, column=2)
        self.data.insert('1.0',
                         "{ \n \"name\" : \" value\",\n \"name 2\" : \" value2\" \n}")

        submit = tk.Button(self.frame, text="Rquest", command=self.request)
        submit.grid(row=5, column=2)
        self.dataloader()


App()
