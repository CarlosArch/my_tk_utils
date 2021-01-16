import tkinter as tk
from tkinter import ttk


class Input:
    """ Base class for an input that contains a label and a widget.

        Parameters
        ----------
        widget_class : tk.Widget
            Widget to use for data entry.
        master : optional
            Parent of the frame.
            Can be left empty, but must be re_initialize()'d later.
        label_text : str, optional
            Text to place in the input's label, by default ''.
        default : optional
            Default value to put in the widget, by default None.
        **widget_options
            Keyword arguments to pass to the widget.


        Attributes
        ----------
        widget_class: tk.Widget
        master
            Parent of the frame.
            If it is None, re_initialize() must be called after setting one.
        label_text: str
            Text to place in the input's label.
        default
            Default value in the widget to be placed with reset().
        widget_options: dict
            Keyword arguments passed over to the widget.
    """
    def __init__(self,
                 widget_class: tk.Widget,
                 master = None,
                 label_text: str = '',
                 default = None,
                 **widget_options):
        self.widget_class = widget_class
        self.master = master
        self.label_text = label_text
        self.default = default
        self.widget_options = widget_options

        if master is not None:
            if label_text:
                self.label = ttk.Label(master, text=f'{label_text}:')
            self.widget = widget_class(master, **widget_options)
            self.reset()

    def re_initialize(self):
        """ Helper function to apply changes to attributes.
        """
        Input.__init__(self,
                       widget_class=self.widget_class,
                       master=self.master,
                       label_text=self.label_text,
                       default=self.default,
                       **self.widget_options)

    def reset(self):
        """ Writes default to widget if there is one.
        """
        if self.default is not None:
            self.write(self.default)

    def clear(self):
        """ Clears widget.
        """
        raise NotImplementedError

    def write(self, what):
        """ Writes a value to the widget.

           Parameters
           ----------
           what
               what to write to the widget.
        """
        raise NotImplementedError

    def grid(self, **options):
        """ Grids the frame containing the widgets.

            Parameters
            ----------
            **options
                keyword arguments to pass over to frame's grid() method.
        """
        raise NotImplementedError

    def pack(self, **options):
        """ Packs the frame containing the widgets.

            Parameters
            ----------
            **options
                keyword arguments to pass over to frame's pack() method.
        """
        raise NotImplementedError

    def place(self, **options):
        """ Places the frame containing the widgets.

            Parameters
            ----------
            **options
                keyword arguments to pass over to frame's place() method.
        """
        raise NotImplementedError


class BaseTextInput(Input):
    def __init__(self,
                 master = None,
                 label_text: str = '',
                 default: str = None,
                 **widget_options):
        if default and not 'width' in widget_options:
            widget_options['width'] = len(default) + 2
        super().__init__(widget_class=ttk.Entry,
                         master=master,
                         label_text=label_text,
                         default=default,
                         **widget_options)

    def clear(self):
        self.delete(first=0, last=tk.END)

    def write(self, text: str):
        self.clear()
        self.insert(index=0, string=str(text))

    # Pass over to widget
    def get(self, *args, **kwargs):
        return self.widget.get(*args, **kwargs)
    def delete(self, *args, **kwargs):
        return self.widget.delete(*args, **kwargs)
    def insert(self, *args, **kwargs):
        return self.widget.insert(*args, **kwargs)


class TextInput(tk.Frame):
    def __init__(self,
                 master,
                 label_text: str = '',
                 default: str = None,
                 frame_options: dict = {},
                 **widget_options):
        self.master = master
        super().__init__(master, **frame_options)
        self.input = BaseTextInput(self, label_text, default, **widget_options)

    def geometry_slaves(self):
        return self.grid_slaves() + self.pack_slaves() + self.place_slaves()

    def default_grid(self):
        self.input.label.grid(column=0, row=0, sticky='e')
        self.input.widget.grid(column=1, row=0, sticky='ew')

    def grid(self, *args, **kwargs):
        if not self.geometry_slaves():
            self.default_grid()
        super().grid(*args, **kwargs)

    def pack(self, *args, **kwargs):
        if not self.geometry_slaves():
            self.default_grid()
        super().pack(*args, **kwargs)

    def place(self, *args, **kwargs):
        if not self.geometry_slaves():
            self.default_grid()
        super().place(*args, **kwargs)


class FormTextInput(BaseTextInput):
    pass


class Form(ttk.Frame):
    inputs = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key, item in self.inputs.items():
            # Alternative call
            setattr(self, key, item)

            # Re-master the inputs
            item.master = self
            item.re_initialize()

    def reset(self):
        for item in self.inputs.values():
            item.reset()

    def clear(self):
        for item in self.inputs.values():
            item.clear()

    def submit(self):
        raise NotImplementedError

    def default_grid(self):
        self.grid_columnconfigure(1, weight=1)
        for i, item in enumerate(self.inputs.values()):
            item.label.grid(row=i, column=0, sticky='e')
            item.widget.grid(row=i, column=1, sticky='ew')
        i += 1
        buttons_frame = tk.Frame(self)
        buttons_frame.grid(row=i, columnspan=2, pady=(5, 0))

        clear_button = ttk.Button(buttons_frame, text="Clear",
                                  command=self.clear)
        clear_button.grid(row=0, column=0, padx=(0, 5))
        submit_button = ttk.Button(buttons_frame, text="Submit",
                                   command=self.submit)
        submit_button.grid(row=0, column=1, padx=(5, 0))

    def pack(self, *args, **kwargs):
        self.default_grid()
        super().pack(*args, **kwargs)
    def grid(self, *args, **kwargs):
        self.default_grid()
        super().grid(*args, **kwargs)
    def place(self, *args, **kwargs):
        self.default_grid()
        super().place(*args, **kwargs)

if __name__ == "__main__":
    class DBConnForm(Form):
        inputs = {
            'driver' : FormTextInput(label_text='Driver',
                                     default='{SQL SERVER}'),
            'host' : FormTextInput(label_text='Host',
                                   default='localhost/'),
            'database' : FormTextInput(label_text='Database'),
            'user' : FormTextInput(label_text='Username'),
            'password' : FormTextInput(label_text='Password', show='*'),
        }

        def submit(self):
            print('')
            print('Submitted values: ')
            for key, item in self.inputs.items():
                print(f'  {key} : {item.get()}')

            # Another way of getting values:
            # self.user.get()

    print(' --- TESTING FORMS --- ')
    window = tk.Tk()
    form = DBConnForm(window)
    form.pack(fill="both", expand=True, padx=10, pady=10)

    standalone_input = TextInput(window, label_text='standalone', default='something default')
    standalone_input.pack(fill="both", expand=True, padx=10, pady=10)
    window.mainloop()
