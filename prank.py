#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Author: i96751414
  Date: 12/01/2018
  Use it, prank your friends.
"""

import sys

PY3 = sys.version_info >= (3,)
if PY3:
    # noinspection PyUnresolvedReferences
    import tkinter as tk
else:
    # noinspection PyPep8Naming
    # noinspection PyUnresolvedReferences
    import Tkinter as tk

APPLICATION_TITLE = "Question..."
BUTTON_YES_TEXT = "Yes"
BUTTON_NO_TEXT = "No"
BUTTON_MAYBE_TEXT = "Maybe..."
LABEL_QUESTION = "Are you dumb?"
BUTTON_YES_MESSAGE_TITLE = "Well..."
BUTTON_YES_MESSAGE_TEXT = "I knew it!!"
BUTTON_CLOSE_MESSAGE_TITLE = "Hey!"
BUTTON_CLOSE_MESSAGE_TEXT = "Try other thing!"


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # Disable close button
        self.protocol('WM_DELETE_WINDOW', self.button_close_warning)

        # Set main window properties
        self.__height = 350
        self.__width = 700
        self.minsize(self.__width, self.__height)
        self.resizable(False, False)
        self.title(APPLICATION_TITLE)

        # Set Label
        self.labelQuestion = tk.Label(text=LABEL_QUESTION, font=("", "14"))
        self.labelQuestion.place(x=0, y=20, width=self.__width)

        # Set Buttons
        buttons_padding_x = 50
        buttons_padding_y = 50
        buttons_width = 170
        buttons_height = 45

        distance_between_buttons = (self.__width - 3 * buttons_width - 2 * buttons_padding_x) / 2
        buttons_y = self.__height - buttons_height - buttons_padding_y

        self.buttonNo = tk.Button(text=BUTTON_NO_TEXT, takefocus=False)
        self.buttonNo.place(x=buttons_padding_x + buttons_width + distance_between_buttons, y=buttons_y,
                            height=buttons_height, width=buttons_width)
        self.buttonNo.bind("<Motion>", self.button_no_mouse_over)
        self.buttonNo.bind("<Button-1>", lambda e: "break")

        self.buttonMaybe = tk.Button(text=BUTTON_MAYBE_TEXT, takefocus=False)
        self.buttonMaybe.place(x=buttons_padding_x + 2 * buttons_width + 2 * distance_between_buttons, y=buttons_y,
                               height=buttons_height, width=buttons_width)
        self.buttonMaybe.bind("<Motion>", self.button_maybe_mouse_over)
        self.buttonMaybe.bind("<Button-1>", lambda e: "break")

        self.buttonYes = tk.Button(text=BUTTON_YES_TEXT, takefocus=False)
        self.buttonYes.place(x=buttons_padding_x, y=buttons_y, height=buttons_height, width=buttons_width)
        self.buttonYes.bind("<ButtonRelease-1>", self.button_yes_click)
        self.buttonYes.bind("<Motion>", self.button_yes_mouse_over)

    def button_maybe_mouse_over(self, e):
        button_width = self.buttonMaybe.winfo_width()
        button_height = self.buttonMaybe.winfo_height()

        if e.x <= e.y and e.x <= button_height - e.y and e.x <= button_width - e.x:
            self.buttonMaybe.place(x=self.buttonMaybe.winfo_x() + e.x + 1)
        elif e.y < e.x and e.y < button_height - e.y and e.y < button_width - e.x:
            self.buttonMaybe.place(y=self.buttonMaybe.winfo_y() + e.y + 1)
        elif button_width - e.x <= e.x and button_width - e.x <= e.y and button_width - e.x <= button_height - e.y:
            self.buttonMaybe.place(x=self.buttonMaybe.winfo_x() + e.x - button_width - 1)
        else:
            self.buttonMaybe.place(y=self.buttonMaybe.winfo_y() + e.y - button_height - 1)

    def button_yes_mouse_over(self, e):
        self.buttonYes.place(x=int(self.buttonYes.winfo_x() + (e.x - self.buttonYes.winfo_width() / 2)),
                             y=int(self.buttonYes.winfo_y() + (e.y - self.buttonYes.winfo_height() / 2)))

    def button_no_mouse_over(self, e):
        button_width = self.buttonNo.winfo_width()
        button_height = self.buttonNo.winfo_height()

        # Make sure we don't hit the limits
        if e.x == 0:
            e.x = 1
        elif e.x == button_width:
            e.x -= 1
        if e.y == 0:
            e.y = 1
        elif e.y == button_height:
            e.y -= 1

        a = abs(button_width / 2.0 - e.x) / (button_width / 2.0) * 0.95
        b = abs(button_height / 2.0 - e.y) / (button_height / 2.0)

        if a > b:
            new_width = int(button_width * a)
            new_height = int(button_height * a)
        else:
            new_width = int(button_width * b)
            new_height = int(button_height * b)

        if new_width > 2 and new_height > 2:
            width_offset = int((button_width - new_width) / 2)
            # Make sure the button decreases its size
            if width_offset == 0:
                width_offset = 1
                new_width = button_width - 2
            # Make sure the button keeps the center in the same position
            elif (button_width - new_width) % 2:
                new_width -= 1
                width_offset += 1

            height_offset = int((button_height - new_height) / 2)
            # Make sure the button decreases its size
            if height_offset == 0:
                height_offset = 1
                new_height = button_height - 2
            # Make sure the button keeps the center in the same position
            elif (button_height - new_height) % 2:
                new_height -= 1
                height_offset += 1

            self.buttonNo.place(x=self.buttonNo.winfo_x() + width_offset,
                                y=self.buttonNo.winfo_y() + height_offset,
                                height=new_height, width=new_width)

        else:
            self.buttonNo.place(height=0, width=0)

    def button_yes_click(self, _):
        msg = OkMsgBox(BUTTON_YES_MESSAGE_TITLE, BUTTON_YES_MESSAGE_TEXT)
        self.center_window(msg)
        msg.grab_set()
        self.wait_window(msg)
        self.destroy()

    def button_close_warning(self):
        msg = OkMsgBox(BUTTON_CLOSE_MESSAGE_TITLE, BUTTON_CLOSE_MESSAGE_TEXT)
        self.center_window(msg)
        msg.grab_set()

    def center_window(self, window):
        window.update()
        w = window.winfo_width()
        h = window.winfo_height()
        x = self.winfo_x() + (self.winfo_width() - w) / 2
        y = self.winfo_y() + (self.winfo_height() - h) / 2
        window.geometry("%dx%d+%d+%d" % (w, h, x, y))


class OkMsgBox(tk.Toplevel):
    def __init__(self, title, message):
        tk.Toplevel.__init__(self)

        self.title(title)

        self.label = tk.Label(self, text=message, bg="white")
        self.label.pack(ipadx=50, ipady=10, fill="both", expand=True)

        self.button = tk.Button(self, text="OK", command=self.destroy)
        self.button.pack(pady=10, padx=10, ipadx=20, side="right")

        self.resizable(False, False)


def main():
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()
