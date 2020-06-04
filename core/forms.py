import tkinter as tk
from tkinter import ttk

class Input:
    def __init__(self, *args, **kwargs):
        self.widget = None
        self.label = None
        self.options = None

    def clear(self):
        raise NotImplementedError('clear() method not implemented.')

    def write(self):
        raise NotImplementedError('write() method not implemented.')

class TextInput(Input):
    def __init__(self, label, **options):
        super().__init__()
        self.label = label
        self.options = options

    def initialize(self, parent):
        self.label = ttk.Label(parent, text=f'{self.label}:')
        self.widget = ttk.Entry(parent, **self.options)

    def draw(self, row=0):
        self.label.grid(row=row, column=0, sticky='e')
        self.widget.grid(row=row, column=1, sticky='ew')

    def clear(self):
        self.delete(first=0, last=tk.END)

    def write(self, text):
        self.clear()
        text = str(text) if text else ''
        self.insert(index=0, string=str(text))

    # Pass over to widget
    def get(self, *args, **kwargs):
        return self.widget.get(*args, **kwargs)
    def delete(self, *args, **kwargs):
        return self.widget.delete(*args, **kwargs)
    def insert(self, *args, **kwargs):
        return self.widget.insert(*args, **kwargs)

class Form(ttk.Frame):
    inputs = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key, item in self.inputs.items():
            setattr(self, key, item)
            item.initialize(self)
        self.draw()

    def clear(self):
        for item in self.inputs.values():
            item.clear()

    def submit(self):
        raise NotImplementedError('submit() not implemented.')

    def draw(self):
        for i, item in enumerate(self.inputs.values()):
            item.draw(i)
        i += 1
        frame = tk.Frame(self)
        frame.grid(row=i, columnspan=2, pady=(5, 0))

        clear_button = ttk.Button(frame, text="Clear", command=self.clear)
        clear_button.grid(row=0, column=0, padx=(0, 5))
        submit_button = ttk.Button(frame, text="Submit", command=self.submit)
        submit_button.grid(row=0, column=1, padx=(5, 0))

if __name__ == "__main__":
    class DBConnForm(Form):
        inputs = {
            'driver' : TextInput(label='Driver'),
            'host' : TextInput(label='Host'),
            'database' : TextInput(label='DataBase'),
            'user' : TextInput(label='Username'),
            'password' : TextInput(label='Password', show='*'),
        }

        def submit(self):
            print('')
            print('Submitted values: ')
            for key, item in self.inputs.items():
                print(f'\t{key} : {item.get()}')

            # Another way of getting values:
            # self.user.get()

    print(' --- TESTING FORMS --- ')
    window = tk.Tk()
    form = DBConnForm(window)
    form.pack(fill="both", expand=True, padx=10, pady=10)
    window.mainloop()
