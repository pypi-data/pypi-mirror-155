#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk


class UserinputApp:
    def __init__(self, master=None):
        # build ui
        self.mainwindow = tk.Tk() if master is None else tk.Toplevel(master)
        self.fcontainer = ttk.Frame(self.mainwindow)
        self.frame_2 = ttk.Frame(self.fcontainer)
        self.label_1 = ttk.Label(self.frame_2)
        self.label_1.configure(text="User Input Demo")
        self.label_1.pack(side="top")
        self.frame_2.configure(height=200, padding="0 0 0 10", width=200)
        self.frame_2.pack(expand="true", fill="x", side="top")
        self.fwidgets = ttk.Frame(self.fcontainer)
        self.frame2 = ttk.Frame(self.fwidgets)
        self.label_2 = ttk.Label(self.frame2)
        self.label_2.configure(text="Entry", width=-14)
        self.label_2.pack(side="left")
        self.frame_3 = ttk.Frame(self.frame2)
        self.entry_1 = ttk.Entry(self.frame_3)
        self.entryvar = tk.StringVar(value="")
        self.entry_1.configure(textvariable=self.entryvar)
        self.entry_1.pack(expand="true", fill="x", side="top")
        self.label_1_2 = ttk.Label(self.frame_3)
        self.label_1_2.configure(
            font="TkSmallCaptionFont",
            text="An entry associated with a StringVar named entryvar.",
        )
        self.label_1_2.pack(fill="x", side="top")
        self.frame_3.configure(height=200, width=200)
        self.frame_3.pack()
        self.frame2.configure(height=200, width=200)
        self.frame2.pack(expand="true", fill="x", side="top")
        self.separator_1 = ttk.Separator(self.fwidgets)
        self.separator_1.configure(orient="horizontal")
        self.separator_1.pack(fill="x", pady=10)
        self.frame7 = ttk.Frame(self.fwidgets)
        self.label1 = ttk.Label(self.frame7)
        self.label1.configure(text="Validated Entry", width=-14)
        self.label1.pack(side="left")
        self.frame8 = ttk.Frame(self.frame7)
        self.validated_entry = ttk.Entry(self.frame8)
        self.validated_entry_var = tk.StringVar(value="")
        self.validated_entry.configure(
            textvariable=self.validated_entry_var, validate="key"
        )
        self.validated_entry.pack(expand="true", fill="x", side="top")
        _validatecmd = (
            self.validated_entry.register(self.validate_entry_cb),
            "%d_action",
            "%p_entry_value",
        )
        self.validated_entry.configure(validatecommand=_validatecmd)
        self.label2 = ttk.Label(self.frame8)
        self.label2.configure(
            font="TkSmallCaptionFont",
            text="Only lowercase and 10 characters allowed.\nValidation mode: key",
        )
        self.label2.pack(fill="x", side="top")
        self.frame8.configure(height=200, width=200)
        self.frame8.pack(fill="x")
        self.frame7.configure(height=200, width=200)
        self.frame7.pack(expand="true", fill="x", side="top")
        self.separator2 = ttk.Separator(self.fwidgets)
        self.separator2.configure(orient="horizontal")
        self.separator2.pack(fill="x", pady=10)
        self.frame3 = ttk.Frame(self.fwidgets)
        self.label_3 = ttk.Label(self.frame3)
        self.label_3.configure(text="Spinbox", width=-14)
        self.label_3.pack(side="left")
        self.frame_4 = ttk.Frame(self.frame3)
        self.spinbox_1 = ttk.Spinbox(self.frame_4)
        self.spinvar = tk.IntVar(value="")
        self.spinbox_1.configure(
            from_=0, increment=5, textvariable=self.spinvar, to=100
        )
        self.spinbox_1.pack(fill="x", side="top")
        self.label_3_4 = ttk.Label(self.frame_4)
        self.label_3_4.configure(
            font="TkSmallCaptionFont", text="A Spinbox with a IntVar named spinvar."
        )
        self.label_3_4.pack(fill="x", side="top")
        self.frame_4.configure(height=200, width=200)
        self.frame_4.pack(fill="x")
        self.frame3.configure(height=200, width=200)
        self.frame3.pack(expand="true", fill="x", side="top")
        self.separator_1_2 = ttk.Separator(self.fwidgets)
        self.separator_1_2.configure(orient="horizontal")
        self.separator_1_2.pack(fill="x", pady=10)
        self.frame4 = ttk.Frame(self.fwidgets)
        self.label_4 = ttk.Label(self.frame4)
        self.label_4.configure(text="Combobox", width=-14)
        self.label_4.pack(side="left")
        self.frame_5 = ttk.Frame(self.frame4)
        self.combobox = ttk.Combobox(self.frame_5)
        self.combovar = tk.StringVar(value="")
        self.combobox.configure(textvariable=self.combovar, values="A B C D E F G")
        self.combobox.pack(fill="x", side="top")
        self.label_3_4_5 = ttk.Label(self.frame_5)
        self.label_3_4_5.configure(
            font="TkSmallCaptionFont",
            text="A Combobox with a StringVar named combovar.",
        )
        self.label_3_4_5.pack(fill="x", side="top")
        self.frame_5.configure(height=200, padding="0 4", width=200)
        self.frame_5.pack(fill="x")
        self.frame4.configure(height=200, width=200)
        self.frame4.pack(expand="true", fill="x", side="top")
        self.separator_1_3 = ttk.Separator(self.fwidgets)
        self.separator_1_3.configure(orient="horizontal")
        self.separator_1_3.pack(fill="x", pady=10)
        self.frame5 = ttk.Frame(self.fwidgets)
        self.label_5 = ttk.Label(self.frame5)
        self.label_5.configure(text="Checkbutton\xa0\xa0", width=-14)
        self.label_5.pack(side="left")
        self.frame_6 = ttk.Frame(self.frame5)
        self.frame_8 = ttk.Frame(self.frame_6)
        self.checkbutton_1 = ttk.Checkbutton(self.frame_8)
        self.option1var = tk.IntVar(value="")
        self.checkbutton_1.configure(
            offvalue=0, onvalue=1, text="Option 1", variable=self.option1var
        )
        self.checkbutton_1.pack(side="top")
        self.checkbutton_2 = ttk.Checkbutton(self.frame_8)
        self.option2var = tk.IntVar(value="")
        self.checkbutton_2.configure(
            offvalue=0, onvalue=1, text="Option 2", variable=self.option2var
        )
        self.checkbutton_2.pack(side="top")
        self.checkbutton_3 = ttk.Checkbutton(self.frame_8)
        self.option3var = tk.IntVar(value="")
        self.checkbutton_3.configure(
            offvalue=0, onvalue=1, text="Option 3", variable=self.option3var
        )
        self.checkbutton_3.pack(side="top")
        self.frame_8.configure(height=200, width=200)
        self.frame_8.pack(side="left")
        self.message_2 = tk.Message(self.frame_6)
        self.message_2.configure(
            aspect=350,
            font="TkSmallCaptionFont",
            text="Checkbuttons associated with one variable each.",
        )
        self.message_2.pack(fill="x", side="top")
        self.frame_6.configure(height=200, width=200)
        self.frame_6.pack(fill="x")
        self.frame5.configure(height=200, width=200)
        self.frame5.pack(expand="true", fill="x", side="top")
        self.separator_1_4 = ttk.Separator(self.fwidgets)
        self.separator_1_4.configure(orient="horizontal")
        self.separator_1_4.pack(fill="x", pady=10)
        self.frame6 = ttk.Frame(self.fwidgets)
        self.label_6 = ttk.Label(self.frame6)
        self.label_6.configure(text="Radiobutton", width=-14)
        self.label_6.pack(side="left")
        self.frame_7 = ttk.Frame(self.frame6)
        self.frame_1 = ttk.Frame(self.frame_7)
        self.radiobutton_1 = ttk.Radiobutton(self.frame_1)
        self.group1var = tk.StringVar(value="A")
        self.radiobutton_1.configure(
            text="Option A", value="A", variable=self.group1var
        )
        self.radiobutton_1.pack(fill="x", side="top")
        self.radiobutton_2 = ttk.Radiobutton(self.frame_1)
        self.radiobutton_2.configure(
            text="Option B", value="B", variable=self.group1var
        )
        self.radiobutton_2.pack(fill="x", side="top")
        self.radiobutton_3 = ttk.Radiobutton(self.frame_1)
        self.radiobutton_3.configure(
            text="Option C", value="C", variable=self.group1var
        )
        self.radiobutton_3.pack(fill="x", side="top")
        self.frame_1.configure(height=200, width=200)
        self.frame_1.pack(side="left")
        self.message_2_3 = tk.Message(self.frame_7)
        self.message_2_3.configure(
            aspect=350,
            font="TkSmallCaptionFont",
            text="Radiobuttons associated with one variable named group1var.",
        )
        self.message_2_3.pack(fill="x", side="top")
        self.frame_7.configure(height=200, width=200)
        self.frame_7.pack(fill="x")
        self.frame6.configure(height=200, width=200)
        self.frame6.pack(expand="true", fill="x", side="top")
        self.separator1 = ttk.Separator(self.fwidgets)
        self.separator1.configure(orient="horizontal")
        self.separator1.pack(fill="x", pady=10, side="top")
        self.frame1 = ttk.Frame(self.fwidgets)
        self.label3 = ttk.Label(self.frame1)
        self.label3.configure(text="Option Menu", width=-14)
        self.label3.pack(side="left")
        self.frame9 = ttk.Frame(self.frame1)
        self.label4 = ttk.Label(self.frame9)
        self.label4.configure(text="Select Method:")
        self.label4.pack(anchor="w", side="top")
        self.optionmenu_var = tk.StringVar(value="None")
        __values = ["None", "A", "B", "C", "D"]
        self.optionmenu1 = tk.OptionMenu(
            self.frame9,
            self.optionmenu_var,
            *__values,
            command=self.option_menu_clicked
        )
        self.optionmenu1.pack(fill="x", ipadx=50, side="top")
        self.frame9.configure(height=200, width=200)
        self.frame9.pack(side="left")
        self.frame1.configure(height=200, width=200)
        self.frame1.pack(expand="true", fill="x", side="top")
        self.fwidgets.configure(height=200, width=200)
        self.fwidgets.pack(side="top")
        self.bframe = ttk.Frame(self.fcontainer)
        self.button_1 = ttk.Button(self.bframe)
        self.button_1.configure(text="Change values")
        self.button_1.pack(padx="0 10", side="left")
        self.button_1.configure(command=self.on_change_clicked)
        self.button_2 = ttk.Button(self.bframe)
        self.button_2.configure(text="Print Values")
        self.button_2.pack(side="left")
        self.button_2.configure(command=self.on_print_clicked)
        self.bframe.configure(height=200, padding="0 10 0 0", width=200)
        self.bframe.pack(side="top")
        self.fcontainer.configure(height=200, padding="5 0 5 2", width=200)
        self.fcontainer.pack(expand="true", fill="both", side="top")
        self.mainwindow.configure(height=200, width=200)
        self.mainwindow.title("User Input Examples")

        # Main widget
        self.mainwindow = self.mainwindow

    def run(self):
        self.mainwindow.mainloop()

    def validate_entry_cb(self, d_action, p_entry_value):
        pass

    def option_menu_clicked(self, option):
        pass

    def on_change_clicked(self):
        pass

    def on_print_clicked(self):
        pass


if __name__ == "__main__":
    app = UserinputApp()
    app.run()
