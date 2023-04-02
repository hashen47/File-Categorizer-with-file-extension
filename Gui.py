import tkinter, os
from tkinter import Frame, ttk, W, S, E, messagebox, filedialog



class Gui(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title("File Categorizer")
        self.master.configure(padx=10, pady=10)
        self.master.resizable(False, False)

        self.src = ""
        self.dst = ""

        self.set_styles()
        self.create_widgets()
        

    def set_styles(self):
        """
        change some builtin styles of some widgets
        :return None
        """
        self.style = ttk.Style() 
        self.style.configure("TButton", font=('Helvetica', 11))


    def create_widgets(self):
        """
        create all the widgets and add them to grid system
        :return None
        """

        # text variables
        self.src_entry_var = tkinter.StringVar()
        self.dst_entry_var = tkinter.StringVar()

        # widgets
        self.src_label = ttk.Label(master=self.master, text="src", font=("Helvetica", 13))
        self.src_label.grid(column=0, row=0, sticky=W)

        self.src_entry = ttk.Entry(master=self.master, state=tkinter.DISABLED, width=50, font=("Helvetica", 12), textvariable=self.src_entry_var)
        self.src_entry.grid(column=0, row=1)

        self.src_btn = ttk.Button(master=self.master, text="SET", command=self.set_src)
        self.src_btn.grid(column=1, row=1, padx=(10, 0))

        self.dst_label = ttk.Label(master=self.master, text="dst", font=("Helvetica", 13))
        self.dst_label.grid(column=0, row=2, columnspan=3, sticky=W, pady=(15, 0))

        self.dst_entry = ttk.Entry(master=self.master, state=tkinter.DISABLED, width=50, font=("Helvetica", 12), textvariable=self.dst_entry_var)
        self.dst_entry.grid(column=0, row=3)

        self.dst_btn = ttk.Button(master=self.master, text="SET", command=self.set_dst)
        self.dst_btn.grid(column=1, row=3, padx=(10, 0))

        self.progress_label = ttk.Label(master=self.master, text="progress", font=("Helvetica", 13))
        self.progress_label.grid(column=0, row=4, columnspan=3, sticky=W, pady=(15,0))

        self.progress_bar = ttk.Progressbar(master=self.master, value=0, length=560)
        self.progress_bar.grid(column=0, row=5, columnspan=3, sticky=W, pady=(5, 6))

        self.compleated = ttk.Label(master=self.master, text=f"compleated : 0/12")
        self.compleated.grid(column=0, row=6, sticky=W)

        self.current_progress = ttk.Label(master=self.master, text=f"{self.progress_bar['value']}%")
        self.current_progress.grid(column=1, row=6, sticky=E)

        self.cancel_btn = ttk.Button(master=self.master, text="cancel")
        self.cancel_btn.grid(column=1, row=7, sticky=E, pady=(20, 0))

        self.start_btn = ttk.Button(master=self.master, text="start")
        self.start_btn.grid(column=0, row=7, sticky=E, pady=(20, 0))


    
    def set_src(self):
        """
        set the source folder and
        update the src_entry_var value with it
        :return None
        """
        self.src = filedialog.askdirectory()
        if self.src:
            self.src_entry_var.set(self.src)
            messagebox.showinfo("Success", f"You chose {self.src} as the source directory")


    def set_dst(self):
        """
        set the distination folder and
        update the dst_entry_var value with it
        :return None
        """
        self.dst = filedialog.askdirectory() 
        if self.src:
            self.dst_entry_var.set(self.dst)
            messagebox.showinfo("Success", f"You chose {self.dst} as the destination directory")

    
    def run(self):
        """
        execute the mainloop
        :return None
        """
        self.master.mainloop()



gui = Gui()
gui.run()
