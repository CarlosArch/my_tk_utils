import tkinter as tk
from tkinter import ttk

MAIN_FONT = 'Arial'
XLARGE_FONT = (MAIN_FONT, 14)
LARGE_FONT = (MAIN_FONT, 12)
MEDIUM_FONT = (MAIN_FONT, 10)
SMALL_FONT = (MAIN_FONT, 8)
XSMALL_FONT = (MAIN_FONT, 6)

class Page(ttk.Frame):
    title = ''
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent.main, *args, **kwargs)

        self.header = self.make_header(ttk.Frame(self))
        if self.header:
            self.header.grid(row=0)

        self.content = self.make_content(ttk.Frame(self))
        if self.content:
            self.content.grid(row=1, sticky='nsew')

        self.footer = self.make_footer(ttk.Frame(self))
        if self.footer:
            self.footer.grid(row=2)

        self.grid_columnconfigure(0, weight=1) # Expand horizontally
        self.grid_rowconfigure(1, weight=1) # Expand only content vertically

    def make_header(self, frame):
        ttk.Label(
            frame,
            text=self.title,
            font=XLARGE_FONT
            ).pack(pady=10, padx=10, fill="both", expand=True)
        return frame

    def make_content(self, frame):
        ttk.Label(
            frame,
            text='This page has no content.',
            font=MEDIUM_FONT
            ).pack(pady=10, padx=10, fill="both", expand=True)
        return frame

    def make_footer(self, frame):
        # ttk.Label(
        #     frame,
        #     text='Maybe add a footer idk.',
        #     font=SMALL_FONT
        #     ).pack(pady=10, padx=10, fill="both", expand=True)
        # return frame
        return frame

    def quit(self):
        self.destroy()

class Window(tk.Tk):
    window_title = ''
    initial_page = None
    preload_pages = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(self.window_title)

        self.main = ttk.Frame(self)
        self.main.pack(fill="both", expand=True)
        self.main.grid_rowconfigure(0, weight=1)
        self.main.grid_columnconfigure(0, weight=1)

        self.menu = self.generate_menu(tk.Menu(self))
        if self.menu:
            tk.Tk.config(self, menu=self.menu)

        self.pages = {}
        for page in self.preload_pages:
            self.load_page(page)

        self.show_page(self.initial_page)

        self.protocol("WM_DELETE_WINDOW", self.quit)

    def generate_menu(self, menu):
        return menu

    def load_page(self, page: Page):
        """
        Loads a page into Application
        """
        self.pages[page] = page(parent=self)
        self.pages[page].grid(row=0, column=0, sticky='nsew')

    def show_page(self, page):
        """
        Raises a page into Application, loads it if not yet loaded.
        """
        if not page in self.pages:
            self.load_page(page)
        self.pages[page].tkraise()

    def quit(self):
        for page in self.pages.values():
            page.quit()
        self.destroy()

if __name__ == "__main__":
    class TestHomePage(Page):
        title = 'This is a Test'

    class TestApp(Window):
        window_title = 'Test Application'
        initial_page = TestHomePage

    TestApp().mainloop()