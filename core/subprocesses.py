from subprocess import Popen, PIPE
from threading import Thread
from queue import Queue
import time

import tkinter as tk
from tkinter import ttk

from application import Window, Page


class CommandLine(ttk.Frame):
    """
    Ignore this, it is worthless.
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)
        self.master = master

        # Generate output textbox
        self.txt_output = tk.Text(master=self, state="disabled")
        self.txt_output.grid(row=0, sticky='nsew')
        self.txt_output.tag_configure("ERR", foreground="red")

        # Generate input entrybox
        self.ent_input = ttk.Entry(master=self)
        self.ent_input.grid(row=1, sticky='ew')
        self.ent_input.bind("<Return>", self.communicate)

        self.grid_columnconfigure(0, weight=1)  # Expand horizontally
        self.grid_rowconfigure(0, weight=1)     # Expand output vertically

        self.subprocess = Subprocess(update_func=self.update, delay_s=0.04)

    def update(self, queue):
        if not queue.empty():
            output, error = queue.get()
            self.txt_output.configure(state="normal")
            self.txt_output.insert(tk.END, output)
            self.txt_output.insert(tk.END, error, 'ERR')
            self.txt_output.configure(state="disabled")
            self.txt_output.see('end')
            queue.task_done()

    def communicate(self, event):
        text = self.ent_input.get()
        self.subprocess.communicate(input=text, shell=True)
        self.ent_input.delete(first=0, last='end')

    def quit(self):
        self.subprocess.quit()
        self.destroy()


class Subprocess:
    """
    Creates a secondary thread that calls a subprocess.
    """
    def __init__(self, update_func, delay_s: float = 0):
        self.update_func = update_func
        self.delay_s = delay_s

        self.queue = Queue()
        self.thread = Thread(target=self.read_pipe, daemon=True)
        self.thread.start()

    def communicate(self, input: str = None, shell=False):
        self.process = Popen(input,
                             shell=shell,
                             stdin=PIPE, stdout=PIPE, stderr=PIPE,
                             text=True)

    def read_pipe(self):
        while True:
            if hasattr(self, 'process'):
                output = self.process.stdout.readline()
                error = self.process.stderr.readline()
                if output or error:
                    self.queue.put((output, error))
                    self.update_func(self.queue)
            time.sleep(self.delay_s)

    def quit(self):
        if hasattr(self, 'process'):
            self.process.kill()

if __name__ == "__main__":
    class TestPage(Page):
        title = 'Test Subprocess'

        def make_content(self, frame):
            self.cmd = CommandLine(frame)
            self.cmd.pack(expand=True, fill="both")
            return frame

        def quit(self):
            self.cmd.quit()
            super().quit()

    class TestWindow(Window):
        window_title = 'AWS Terraria Utilites'
        initial_page = TestPage

    testwindow = TestWindow()
    testwindow.mainloop()
