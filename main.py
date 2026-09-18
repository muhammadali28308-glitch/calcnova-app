import math
from functools import partial

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

# ===========================
# Colors (same theme as Tkinter version)
# ===========================

BG_COLOR = get_color_from_hex("#1E1E1E")
DISPLAY_BG = get_color_from_hex("#2B2B2B")
COLOR_DEFAULT = get_color_from_hex("#333333")
COLOR_OPERATOR = get_color_from_hex("#FF9500")
COLOR_CLEAR = get_color_from_hex("#555555")
COLOR_MEMORY = get_color_from_hex("#0066CC")
COLOR_UTILITY = get_color_from_hex("#009688")
COLOR_SCI = get_color_from_hex("#444444")

Window.clearcolor = BG_COLOR


def show_popup(title, message):
    """Kivy version of messagebox.showinfo / showerror"""
    layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
    layout.add_widget(Label(text=str(message)))
    close_btn = Button(text="OK", size_hint=(1, 0.3))
    layout.add_widget(close_btn)

    popup = Popup(title=title, content=layout, size_hint=(0.8, 0.4))
    close_btn.bind(on_release=popup.dismiss)
    popup.open()


class CalcNova(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.memory = 0
        self.history = []

        # ---------------- Display ----------------
        self.display = TextInput(
            font_size=30,
            multiline=False,
            halign="right",
            background_color=DISPLAY_BG,
            foreground_color=[1, 1, 1, 1],
            cursor_color=[1, 1, 1, 1],
            size_hint=(1, 0.15),
            padding=[10, 20, 10, 10],
        )
        self.add_widget(self.display)

        # ---------------- Scrollable Button Grid ----------------
        scroll = ScrollView(size_hint=(1, 0.85))
        self.grid = GridLayout(cols=4, spacing=4, padding=4, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter("height"))
        scroll.add_widget(self.grid)
        self.add_widget(scroll)

        self.build_buttons()

    # ===========================
    # Core actions
    # ===========================

    def press(self, value):
        self.display.text += value

    def clear(self):
        self.display.text = ""

    def backspace(self):
        self.display.text = self.display.text[:-1]

    def calculate(self):
        try:
            expression = self.display.text
            expression = expression.replace("×", "*")
            expression = expression.replace("÷", "/")
            expression = expression.replace("^", "**")

            result = eval(expression)
            self.history.append(f"{expression} = {result}")
            self.display.text = str(result)
        except Exception:
            show_popup("Error", "Invalid Expression")

    def square_root(self):
        try:
            number = float(self.display.text)
            self.display.text = str(math.sqrt(number))
        except Exception:
            show_popup("Error", "Invalid Number")

    def square(self):
        try:
            number = float(self.display.text)
            self.display.text = str(number ** 2)
        except Exception:
            show_popup("Error", "Invalid Number")

    def sin(self):
        try:
            number = float(self.display.text)
            self.display.text = str(round(math.sin(math.radians(number)), 10))
        except Exception:
            show_popup("Error", "Invalid Number")

    def cos(self):
        try:
            number = float(self.display.text)
            self.display.text = str(round(math.cos(math.radians(number)), 10))
        except Exception:
            show_popup("Error", "Invalid Number")

    def tan(self):
        try:
            number = float(self.display.text)
            self.display.text = str(round(math.tan(math.radians(number)), 10))
        except Exception:
            show_popup("Error", "Invalid Number")

    def log(self):
        try:
            number = float(self.display.text)
            self.display.text = str(math.log10(number))
        except Exception:
            show_popup("Error", "Invalid Number")

    def ln(self):
        try:
            number = float(self.display.text)
            self.display.text = str(math.log(number))
        except Exception:
            show_popup("Error", "Invalid Number")

    def percent(self):
        try:
            number = float(self.display.text)
            self.display.text = str(number / 100)
        except Exception:
            show_popup("Error", "Invalid Number")

    def factorial(self):
        try:
            number = int(self.display.text)
            if number < 0:
                show_popup("Error", "Negative numbers not allowed")
                return
            self.display.text = str(math.factorial(number))
        except Exception:
            show_popup("Error", "Enter a valid integer")

    def reciprocal(self):
        try:
            number = float(self.display.text)
            if number == 0:
                show_popup("Error", "Cannot divide by zero")
                return
            self.display.text = str(1 / number)
        except Exception:
            show_popup("Error", "Invalid Number")

    def absolute(self):
        try:
            number = float(self.display.text)
            self.display.text = str(abs(number))
        except Exception:
            show_popup("Error", "Invalid Number")

    def toggle_sign(self):
        text = self.display.text
        if text.startswith("-"):
            self.display.text = text[1:]
        else:
            self.display.text = "-" + text

    def memory_clear(self):
        self.memory = 0
        show_popup("Memory", "Memory Cleared")

    def memory_recall(self):
        self.display.text = str(self.memory)

    def memory_add(self):
        try:
            value = float(self.display.text)
            self.memory += value
            self.history.append(f"M+ : {value}")
            show_popup("Memory", f"Current Memory : {self.memory}")
        except Exception:
            show_popup("Error", "Invalid Number")

    def memory_subtract(self):
        try:
            value = float(self.display.text)
            self.memory -= value
            self.history.append(f"M- : {value}")
            show_popup("Memory", f"Current Memory : {self.memory}")
        except Exception:
            show_popup("Error", "Invalid Number")

    def show_history(self):
        if len(self.history) == 0:
            show_popup("History", "No History Available")
            return
        text = "\n".join(self.history)
        show_popup("Calculation History", text)

    def clear_history(self):
        self.history.clear()
        show_popup("History", "History Cleared Successfully")

    def copy_result(self):
        try:
            from kivy.core.clipboard import Clipboard
            value = self.display.text
            if value:
                Clipboard.copy(value)
                show_popup("Copied", "Result Copied Successfully")
            else:
                show_popup("Error", "Nothing To Copy")
        except Exception:
            show_popup("Error", "Copy Failed")

    # ===========================
    # Build all buttons
    # ===========================

    def build_buttons(self):
        all_buttons = [
            ("C", self.clear),
            ("⌫", self.backspace),
            ("√", self.square_root),
            ("x²", self.square),
            ("7", partial(self.press, "7")),
            ("8", partial(self.press, "8")),
            ("9", partial(self.press, "9")),
            ("÷", partial(self.press, "÷")),
            ("4", partial(self.press, "4")),
            ("5", partial(self.press, "5")),
            ("6", partial(self.press, "6")),
            ("×", partial(self.press, "×")),
            ("1", partial(self.press, "1")),
            ("2", partial(self.press, "2")),
            ("3", partial(self.press, "3")),
            ("-", partial(self.press, "-")),
            ("±", self.toggle_sign),
            ("0", partial(self.press, "0")),
            (".", partial(self.press, ".")),
            ("+", partial(self.press, "+")),
            ("=", self.calculate),
            ("Sin", self.sin),
            ("Cos", self.cos),
            ("Tan", self.tan),
            ("Log", self.log),
            ("Ln", self.ln),
            ("%", self.percent),
            ("x^y", partial(self.press, "^")),
            ("n!", self.factorial),
            ("1/x", self.reciprocal),
            ("|x|", self.absolute),
            ("π", partial(self.press, str(math.pi))),
            ("e", partial(self.press, str(math.e))),
            ("MC", self.memory_clear),
            ("MR", self.memory_recall),
            ("M+", self.memory_add),
            ("M-", self.memory_subtract),
            ("History", self.show_history),
            ("Copy", self.copy_result),
            ("Clear H", self.clear_history),
        ]

        for text, callback in all_buttons:
            color = COLOR_DEFAULT

            if text in ["+", "-", "×", "÷", "="]:
                color = COLOR_OPERATOR
            elif text in ["C", "⌫", "√", "x²"]:
                color = COLOR_CLEAR
            elif text in ["MC", "MR", "M+", "M-"]:
                color = COLOR_MEMORY
            elif text in ["History", "Copy", "Clear H"]:
                color = COLOR_UTILITY
            else:
                if not text.isdigit() and text not in [".", "±"]:
                    color = COLOR_SCI

            btn = Button(
                text=text,
                background_normal="",
                background_color=color,
                color=[1, 1, 1, 1],
                bold=True,
                size_hint_y=None,
                height=55,
            )
            btn.bind(on_release=lambda inst, cb=callback: cb())
            self.grid.add_widget(btn)


class CalcNovaApp(App):
    title = "CalcNova - Scientific Calculator"

    def build(self):
        return CalcNova()


if __name__ == "__main__":
    CalcNovaApp().run()
