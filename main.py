from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
import math

KV = """
<EquationInputLayout@MDBoxLayout>:
    orientation: "vertical"
    spacing: "12dp"
    padding: "12dp"

MDScreen:
    MDBoxLayout:
        orientation: "vertical"

        MDTextField:
            id: display
            text: "0"
            halign: "right"
            font_size: "49sp"
            readonly: True

        MDBoxLayout:
            size_hint_y: None
            height: "50dp"
            padding: "10dp"
            spacing: "10dp"

            MDRaisedButton:
                text: "History"
                on_release: app.show_history()

            MDRaisedButton:
                text: "Deg/Rad"
                on_release: app.toggle_mode()
            
            MDRaisedButton:
                text: "Mode"
                on_release: app.show_mode_selector()
                
            MDRaisedButton:
                text: "Mode"
                on_release: app.show_mode_dialog()

        GridLayout:
            cols: 4
            spacing: "5dp"
            padding: "10dp"

            # Scientific functions
            MDRectangleFlatButton:
                text: "sin"
                on_release: app.on_button_press("sin(")
            MDRectangleFlatButton:
                text: "cos"
                on_release: app.on_button_press("cos(")
            MDRectangleFlatButton:
                text: "tan"
                on_release: app.on_button_press("tan(")
            MDRectangleFlatButton:
                text: "√"
                on_release: app.on_button_press("sqrt(")

            MDRectangleFlatButton:
                text: "ln"
                on_release: app.on_button_press("ln(")
            MDRectangleFlatButton:
                text: "log"
                on_release: app.on_button_press("log(")
            MDRectangleFlatButton:
                text: "exp"
                on_release: app.on_button_press("exp(")
            MDRectangleFlatButton:
                text: "x!"
                on_release: app.on_button_press("factorial(")

            MDRectangleFlatButton:
                text: "pi"
                on_release: app.on_button_press("pi")
            MDRectangleFlatButton:
                text: "e"
                on_release: app.on_button_press("e")
            MDRectangleFlatButton:
                text: "^"
                on_release: app.on_button_press("^")
            MDRectangleFlatButton:
                text: "%"
                on_release: app.on_button_press("%")

            # Numbers & Operators
            MDRectangleFlatButton:
                text: "7"
                on_release: app.on_button_press("7")
            MDRectangleFlatButton:
                text: "8"
                on_release: app.on_button_press("8")
            MDRectangleFlatButton:
                text: "9"
                on_release: app.on_button_press("9")
            MDRectangleFlatButton:
                text: "/"
                on_release: app.on_button_press("/")

            MDRectangleFlatButton:
                text: "4"
                on_release: app.on_button_press("4")
            MDRectangleFlatButton:
                text: "5"
                on_release: app.on_button_press("5")
            MDRectangleFlatButton:
                text: "6"
                on_release: app.on_button_press("6")
            MDRectangleFlatButton:
                text: "*"
                on_release: app.on_button_press("*")

            MDRectangleFlatButton:
                text: "1"
                on_release: app.on_button_press("1")
            MDRectangleFlatButton:
                text: "2"
                on_release: app.on_button_press("2")
            MDRectangleFlatButton:
                text: "3"
                on_release: app.on_button_press("3")
            MDRectangleFlatButton:
                text: "-"
                on_release: app.on_button_press("-")

            MDRectangleFlatButton:
                text: "0"
                on_release: app.on_button_press("0")
            MDRectangleFlatButton:
                text: "."
                on_release: app.on_button_press(".")
            MDRectangleFlatButton:
                text: "="
                on_release: app.calculate_result()
            MDRectangleFlatButton:
                text: "+"
                on_release: app.on_button_press("+")

            MDRectangleFlatButton:
                text: "("
                on_release: app.on_button_press("(")
            MDRectangleFlatButton:
                text: ")"
                on_release: app.on_button_press(")")
            MDRectangleFlatButton:
                text: "C"
                on_release: app.clear_display()
"""

class EquationInputLayout(MDBoxLayout):
    pass

class CalculateApp(MDApp):
    angle_mode = "deg"
    history = []

    def build(self):
        return Builder.load_string(KV)

    def on_button_press(self, value):
        display = self.root.ids.display
        if display.text in ("0", "Error"):
            display.text = value
        else:
            display.text += value

    def toggle_mode(self):
        self.angle_mode = "rad" if self.angle_mode == "deg" else "deg"
        print(f"Mode: {self.angle_mode}")
    
    def show_mode_selector(self):
        items = [
            {
                "text": "Solve Linear (ax + b = 0)",
                "on_release": lambda x="linear": self.open_equation_dialog(x)
            },
            {
                "text": "Solve Quadratic (ax² + bx + c = 0)",
                "on_release": lambda x="quadratic": self.open_equation_dialog(x)
            }
        ]
        self.menu = MDDropdownMenu(
            caller=self.root.ids.display,
            items=items,
            width_mult=4
        )
        self.menu.open()

    def calculate_result(self):
        display = self.root.ids.display
        try:
            expr = display.text.replace("^", "**")

            def sin(x): return math.sin(math.radians(x)) if self.angle_mode == "deg" else math.sin(x)
            def cos(x): return math.cos(math.radians(x)) if self.angle_mode == "deg" else math.cos(x)
            def tan(x): return math.tan(math.radians(x)) if self.angle_mode == "deg" else math.tan(x)

            result = eval(expr, {"__builtins__": None}, {
                "sin": sin,
                "cos": cos,
                "tan": tan,
                "sqrt": math.sqrt,
                "log": math.log10,
                "ln": math.log,
                "exp": math.exp,
                "factorial": math.factorial,
                "pi": math.pi,
                "e": math.e,
                "abs": abs,
                "__name__": "calc"
            })
            result_str = str(result)
            self.history.append(f"{display.text} = {result_str}")
            display.text = result_str
        except Exception as e:
            display.text = "Error"
            print(f"Error: {e}")
            
    def open_equation_dialog(self, mode):
        self.menu.dismiss()

        self.coeff_inputs = {}

        if mode == "linear":
            fields = ["a", "b"]
        else:  # quadratic
            fields = ["a", "b", "c"]

        layout = EquationInputLayout()
        for label in fields:
            field = MDTextField(
                hint_text=f"Enter {label}",
                input_filter="float"
            )
            layout.add_widget(field)
            self.coeff_inputs[label] = field

        self.dialog = MDDialog(
            title=f"Solve {mode.title()} Equation",
            type="custom",
            content_cls=layout,
            buttons=[
                MDFlatButton(text="Cancel", on_release=lambda x: self.dialog.dismiss()),
                MDFlatButton(text="Solve", on_release=lambda x: self.solve_equation(mode))
            ]
        )
        self.dialog.open()
        
    def show_equation_inputs(self, eq_type):
        self.dialog.dismiss()  # close mode selection
        layout = MDBoxLayout(orientation="vertical", spacing="10dp", padding="10dp")
        self.coeff_inputs = {}

        if eq_type == "linear":
            required = ["a", "b"]
            label_text = "ax + b = 0"
        elif eq_type == "quadratic":
            required = ["a", "b", "c"]
            label_text = "ax² + bx + c = 0"
        else:
            return

        layout.add_widget(MDLabel(text=label_text, halign="center"))

        for coeff in required:
            input_field = MDTextField(
                hint_text=f"Enter {coeff}",
                input_filter="float",
                mode="rectangle"
            )
            self.coeff_inputs[coeff] = input_field
            layout.add_widget(input_field)

        layout.add_widget(
            MDRaisedButton(
                text="Solve",
                on_release=lambda x: self.solve_equation(eq_type)
            )
        )

        self.dialog = MDDialog(
            title=f"{eq_type.capitalize()} Equation Solver",
            type="custom",
            content_cls=layout,
            buttons=[
                MDFlatButton(text="Cancel", on_release=lambda x: self.dialog.dismiss())
            ]
        )
        self.dialog.open()
        
    def solve_equation(self, mode):
        try:
            coeffs = {}
            for k, v in self.coeff_inputs.items():
                if v.text.strip() == "":
                    self.root.ids.display.text = "Please enter all coefficients"
                    return
                coeffs[k] = float(v.text)
            if mode == "linear":
                a, b = coeffs["a"], coeffs["b"]
                if a == 0:
                    result = "No solution" if b != 0 else "Infinite solutions"
                else:
                    x = -b / a
                    result = f"x = {x:.4f}"
            else:
                a, b, c = coeffs["a"], coeffs["b"], coeffs["c"]
                D = b**2 - 4*a*c
                if D > 0:
                    x1 = (-b + math.sqrt(D)) / (2*a)
                    x2 = (-b - math.sqrt(D)) / (2*a)
                    result = f"x₁ = {x1:.4f}, x₂ = {x2:.4f}"
                elif D == 0:
                    x = -b / (2*a)
                    result = f"x = {x:.4f}"
                else:
                    real = -b / (2*a)
                    imag = math.sqrt(-D) / (2*a)
                    result = f"x₁ = {real:.4f} + {imag:.4f}i, x₂ = {real:.4f} - {imag:.4f}i"
        except Exception as e:
            result = "Error solving equation"
            print(e)
        self.dialog.dismiss()
        self.root.ids.display.text = result
        self.history.append(f"{mode.title()} => {result}")

    def clear_display(self):
        self.root.ids.display.text = "0"

    def show_history(self):
        if not self.history:
            history_text = "No history yet."
        else:
            history_text = "\n".join(self.history[-10:])

        self.dialog = MDDialog(
            title="Calculation History",
            text=history_text,
            buttons=[
                MDFlatButton(text="Close", on_release=lambda x: self.dialog.dismiss()),
                MDFlatButton(text="Clear", on_release=self.clear_history)
            ]
        )
        self.dialog.open()

    def clear_history(self, *args):
        self.history.clear()
        self.dialog.dismiss()
        
        

if __name__ == "__main__":
    CalculateApp().run()
