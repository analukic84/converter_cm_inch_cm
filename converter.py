"""
CONVERTER

Centimeters to Inches
Inches to Centimeters
"""

import tkinter as tk
from tkinter import ttk
from tkinter import font
import sys


CALCULATE_BUTTON_BACKGROUND = "#46a649"
CLEAR_BUTTON_BACKGROUND = "#6ace6d"
GO_TO_BUTTON_BACKGROUND = "#94f797"
DARKER_ACTIVE_BUTTON = "#327435"
FRAME_LABEL_BACKGROUND = "#c7e1c7"
BLACK_TEXT = "black"


class Converter(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Converter")
        self.resizable(False, False)

        self.style = ttk.Style()
        self.style.theme_use("clam")

        font.nametofont("TkDefaultFont").configure(size=15)

        self.style.configure("CalculateButton.TButton",
                             background=CALCULATE_BUTTON_BACKGROUND,
                             foreground=BLACK_TEXT)

        self.style.configure("ClearButton.TButton",
                             background=CLEAR_BUTTON_BACKGROUND,
                             foreground=BLACK_TEXT)

        self.style.configure("GoButton.TButton",
                             background=GO_TO_BUTTON_BACKGROUND,
                             foreground=BLACK_TEXT,
                             font=("TkDefaultFont", 12))

        for style in ("CalculateButton.TButton", "ClearButton.TButton", "GoButton.TButton"):
            self.style.map(style,
                           background=[("pressed", "white"), ("active", DARKER_ACTIVE_BUTTON)],
                           foreground=[("pressed", DARKER_ACTIVE_BUTTON)]
                           )

        self.style.configure("MainFrame.TFrame", background=FRAME_LABEL_BACKGROUND)

        self.style.configure("Labels.TLabel", background=FRAME_LABEL_BACKGROUND)

        self.centimeter_value = tk.StringVar()
        self.inch_value = tk.StringVar()

        main_frame = ttk.Frame(self)
        main_frame.grid(sticky="NSEW")

        self.frames = dict()

        for frame_class in (CentimeterConverter, InchConverter):
            frame = frame_class(main_frame, self)
            self.frames[frame_class] = frame
            frame.grid(row=0, column=0, sticky="NSEW")
            self.bind("<Return>", frame.convert, add="+")
            self.bind("<KP_Enter>", frame.convert, add="+")

        self.show_frame(CentimeterConverter)

        self.bind("<Escape>", self.exit_program)

    def show_frame(self, class_frame):
        frame = self.frames[class_frame]
        if class_frame == CentimeterConverter:
            frame.centimeter_input.focus()
        elif class_frame == InchConverter:
            frame.inch_input.focus()
        frame.tkraise()

    def exit_program(self, *args):
        sys.exit()


class CentimeterConverter(ttk.Frame):
    def __init__(self, container, parent):
        super().__init__(container)

        self.parent = parent

        self["style"] = "MainFrame.TFrame"

#        self.columnconfigure((0, 1), weight=1)

        centimeter_label = ttk.Label(self, text="Centimeters: ", style="Labels.TLabel")
        centimeter_label.grid(row=0, column=0, sticky="W")

        self.centimeter_input = ttk.Entry(
            self,
            width=12,
            textvariable=parent.centimeter_value,
            cursor="pencil",
            font=("TkDefaultFont", 15),
        )
        self.centimeter_input.focus()
        self.centimeter_input.grid(row=0, column=1, sticky="E")

        inch_label = ttk.Label(self, text="Inches: ", style="Labels.TLabel")
        inch_label.grid(row=1, column=0, sticky="W")

        inch_convert_value = ttk.Label(self, width=12, textvariable=parent.inch_value, style="Labels.TLabel")
        inch_convert_value.grid(row=1, column=1, sticky="E")

        calculate_button = ttk.Button(self, text="Calculate", command=self.convert, style="CalculateButton.TButton")
        calculate_button.grid(row=2, column=0, sticky="NSEW")

        clear_button = ttk.Button(self, text="Clear", command=self.clear_content, style="ClearButton.TButton")
        clear_button.grid(row=2, column=1, sticky="EW")

        go_to_inch_converter = ttk.Button(
            self,
            text="Go to inch converter",
            command=self.switch,
            style="GoButton.TButton"
        )
        go_to_inch_converter.grid(row=3, column=0, columnspan=2, sticky="EW")

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    # calculating values
    def convert(self, *args, **kwargs):
        try:
            centimeter_value = int(self.parent.centimeter_value.get())
            inch_value = centimeter_value * 0.393700787
            self.parent.inch_value.set(f"{inch_value:.2f}")
        except:
            pass

    # clear content from entry and calculated field
    def clear_content(self):
        self.centimeter_input.delete(0, "end")
        self.parent.inch_value.set(value="")

    # clear and switch to another frame
    def switch(self):
        self.clear_content()
        return self.parent.show_frame(InchConverter)


class InchConverter(ttk.Frame):
    def __init__(self, container, parent):
        super().__init__(container)

        self.parent = parent

        self["style"] = "MainFrame.TFrame"

        self.columnconfigure((0, 1), weight=1)

        inch_label = ttk.Label(self, text="Inches: ", style="Labels.TLabel")
        inch_label.grid(row=0, column=0, sticky="W")

        self.inch_input = ttk.Entry(
            self,
            width=12,
            textvariable=parent.inch_value,
            cursor="pencil",
            font=("TkDefaultFont", 15)
        )
        self.inch_input.grid(row=0, column=1, sticky="E")

        centimeter_label = ttk.Label(self, text="Centimeters: ", style="Labels.TLabel")
        centimeter_label.grid(row=1, column=0, sticky="W")

        centimeter_convert_value = ttk.Label(self, width=12, textvariable=parent.centimeter_value, style="Labels.TLabel")
        centimeter_convert_value.grid(row=1, column=1, sticky="E")

        calculate_button = ttk.Button(self, text="Calculate", command=self.convert, style="CalculateButton.TButton")
        calculate_button.grid(row=2, column=0, sticky="EW")

        clear_button = ttk.Button(self, text="Clear", command=self.clear_content, style="ClearButton.TButton")
        clear_button.grid(row=2, column=1, sticky="EW")

        go_to_centimeter_converter = ttk.Button(
            self,
            text="Go to centimeter converter",
            command=self.switch_and_clear,
            style="GoButton.TButton"
        )
        go_to_centimeter_converter.grid(row=4, column=0, columnspan=2, sticky="EW")

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    # calculating values
    def convert(self, *args, **kwargs):
        try:
            inch_value = int(self.parent.inch_value.get())
            centimeter_value = inch_value / 0.393700787
            self.parent.centimeter_value.set(f"{centimeter_value:.2f}")
        except:
            pass

    # clear content from entry and calculated field
    def clear_content(self):
        self.inch_input.delete(0, "end")
        self.parent.centimeter_value.set(value="")
        self.inch_input.focus()

    # clear and switch to another frame
    def switch_and_clear(self):
        self.clear_content()
        return self.parent.show_frame(CentimeterConverter)


root = Converter()
root.mainloop()