from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import OneLineListItem, MDList
from kivymd.uix.gridlayout import MDGridLayout
import math
import numpy as np
from collections import Counter
import statistics

KV = """
<EquationInputLayout@MDBoxLayout>:
    orientation: "vertical"
    spacing: "12dp"
    padding: "12dp"
    size_hint_y: None
    height: self.minimum_height
<MatrixInputLayout@MDGridLayout>:
    cols: 2
    spacing: "10dp"
    padding: "10dp"
    size_hint_y: None
    height: self.minimum_height
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
            height: "100dp"
            padding: "10dp"
            spacing: "10dp"
            MDGridLayout:
                cols: 4
                rows: 2
                spacing: "10dp"
                MDRaisedButton:
                    text: "History"
                    on_release: app.show_history()
                MDRaisedButton:
                    text: "Deg/Rad"
                    on_release: app.toggle_mode()
                MDRaisedButton:
                    text: "Equations"
                    on_release: app.show_mode_selector()
                MDRaisedButton:
                    text: "Functions"
                    on_release: app.show_function_dialog()
                MDRaisedButton:
                    text: "Base Conv"
                    on_release: app.open_base_conversion_dialog()
                MDRaisedButton:
                    text: "Unit Conv"
                    on_release: app.open_unit_conversion_dialog()
                MDRaisedButton:
                    text: "Constants"
                    on_release: app.open_constants_dialog()
                MDRaisedButton:
                    text: "Bitwise"
                    on_release: app.open_bitwise_dialog()
                MDRaisedButton:
                    text: "Stats"
                    on_release: app.open_stats_dialog()
                MDRaisedButton:
                    text: "Matrix"
                    on_release: app.open_matrix_dialog()
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
            # Inverse trig functions
            MDRectangleFlatButton:
                text: "asin"
                on_release: app.on_button_press("asin(")
            MDRectangleFlatButton:
                text: "acos"
                on_release: app.on_button_press("acos(")
            MDRectangleFlatButton:
                text: "atan"
                on_release: app.on_button_press("atan(")
            MDRectangleFlatButton:
                text: "x²"
                on_release: app.on_button_press("^2")
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

class MatrixInputLayout(MDGridLayout):
    pass

class CalculateApp(MDApp):
    angle_mode = "deg"
    history = []
    input_base = "decimal"
    output_base = "binary"
    
    # Unit conversion factors
    unit_conversions = {
        "length": {
            "m": 1.0,
            "km": 1000.0,
            "cm": 0.01,
            "mm": 0.001,
            "mile": 1609.34,
            "yard": 0.9144,
            "foot": 0.3048,
            "inch": 0.0254
        },
        "weight": {
            "kg": 1.0,
            "g": 0.001,
            "mg": 0.000001,
            "lb": 0.453592,
            "oz": 0.0283495
        },
        "temperature": {
            # Temperature is special because it's not multiplicative
            "celsius": "C",
            "fahrenheit": "F",
            "kelvin": "K"
        },
        "area": {
            "m²": 1.0,
            "km²": 1000000.0,
            "cm²": 0.0001,
            "mm²": 0.000001,
            "acre": 4046.86,
            "hectare": 10000.0,
            "ft²": 0.092903,
            "in²": 0.00064516
        },
        "volume": {
            "m³": 1.0,
            "L": 0.001,
            "mL": 0.000001,
            "gal": 0.00378541,
            "qt": 0.000946353,
            "pt": 0.000473176,
            "fl oz": 0.0000295735,
            "in³": 0.0000163871
        },
        "speed": {
            "m/s": 1.0,
            "km/h": 0.277778,
            "mph": 0.44704,
            "ft/s": 0.3048,
            "knot": 0.514444
        },
        "time": {
            "s": 1.0,
            "min": 60.0,
            "h": 3600.0,
            "day": 86400.0,
            "week": 604800.0,
            "year": 31536000.0
        }
    }
    
    # Physical constants
    physical_constants = {
        "Speed of light (c)": 299792458,
        "Planck constant (h)": 6.62607015e-34,
        "Gravitational constant (G)": 6.67430e-11,
        "Avogadro's number (N_A)": 6.02214076e23,
        "Gas constant (R)": 8.314462618,
        "Elementary charge (e)": 1.602176634e-19,
        "Electron mass (m_e)": 9.1093837015e-31,
        "Proton mass (m_p)": 1.67262192369e-27,
        "Neutron mass (m_n)": 1.67492749804e-27,
        "Boltzmann constant (k_B)": 1.380649e-23,
        "Stefan-Boltzmann constant (σ)": 5.670374419e-8,
        "Faraday constant (F)": 96485.33212,
        "Rydberg constant (R_∞)": 10973731.568160,
        "Vacuum permeability (μ₀)": 1.25663706212e-6,
        "Vacuum permittivity (ε₀)": 8.8541878128e-12
    }
    
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
            },
            {
                "text": "Solve 2x2 System",
                "on_release": lambda x="2x2": self.open_system_dialog(x)
            },
            {
                "text": "Solve 3x3 System",
                "on_release": lambda x="3x3": self.open_system_dialog(x)
            }
        ]
        self.menu = MDDropdownMenu(
            caller=self.root.ids.display,
            items=items,
            width_mult=4
        )
        self.menu.open()
    
    def show_function_dialog(self):
        items = [
            {"text": "abs(x)", "on_release": lambda x="abs(": self.on_button_press(x)},
            {"text": "1/x", "on_release": lambda x="1/": self.on_button_press(x)},
            {"text": "x^y", "on_release": lambda x="^": self.on_button_press(x)},
            {"text": "x^(1/y)", "on_release": lambda x="^(1/": self.on_button_press(x)},
            {"text": "sinh", "on_release": lambda x="sinh(": self.on_button_press(x)},
            {"text": "cosh", "on_release": lambda x="cosh(": self.on_button_press(x)},
            {"text": "tanh", "on_release": lambda x="tanh(": self.on_button_press(x)},
            {"text": "asinh", "on_release": lambda x="asinh(": self.on_button_press(x)},
            {"text": "acosh", "on_release": lambda x="acosh(": self.on_button_press(x)},
            {"text": "atanh", "on_release": lambda x="atanh(": self.on_button_press(x)}
        ]
        self.menu = MDDropdownMenu(
            caller=self.root.ids.display,
            items=items,
            width_mult=4
        )
        self.menu.open()
    
    def open_base_conversion_dialog(self):
        # Dismiss any existing menu
        if hasattr(self, 'menu') and self.menu:
            self.menu.dismiss()
        
        layout = EquationInputLayout()
        
        # Input field
        input_field = MDTextField(
            hint_text="Enter number",
            size_hint_y=None,
            height="50dp"
        )
        layout.add_widget(input_field)
        
        # Input base selection
        input_base_layout = MDBoxLayout(size_hint_y=None, height="50dp", spacing="10dp")
        input_base_layout.add_widget(MDLabel(text="Input Base:", size_hint_x=0.4))
        input_base_button = MDRaisedButton(
            text=self.input_base.capitalize(),
            size_hint_x=0.6,
            on_release=lambda x: self.show_base_menu(x, "input")
        )
        input_base_layout.add_widget(input_base_button)
        layout.add_widget(input_base_layout)
        
        # Output base selection
        output_base_layout = MDBoxLayout(size_hint_y=None, height="50dp", spacing="10dp")
        output_base_layout.add_widget(MDLabel(text="Output Base:", size_hint_x=0.4))
        output_base_button = MDRaisedButton(
            text=self.output_base.capitalize(),
            size_hint_x=0.6,
            on_release=lambda x: self.show_base_menu(x, "output")
        )
        output_base_layout.add_widget(output_base_button)
        layout.add_widget(output_base_layout)
        
        # Convert button
        convert_button = MDRaisedButton(
            text="Convert",
            size_hint_y=None,
            height="50dp",
            on_release=lambda x: self.convert_base(input_field.text)
        )
        layout.add_widget(convert_button)
        
        # Store references
        self.input_base_button = input_base_button
        self.output_base_button = output_base_button
        
        self.dialog = MDDialog(
            title="Base Conversion",
            type="custom",
            content_cls=layout,
            buttons=[
                MDFlatButton(text="Close", on_release=lambda x: self.dialog.dismiss())
            ]
        )
        self.dialog.open()
    
    def show_base_menu(self, caller, base_type):
        bases = ["binary", "octal", "decimal", "hexadecimal"]
        items = [
            {"text": base.capitalize(), "on_release": lambda x=base: self.set_base(base_type, x)}
            for base in bases
        ]
        self.menu = MDDropdownMenu(
            caller=caller,
            items=items,
            width_mult=4
        )
        self.menu.open()
    
    def set_base(self, base_type, base):
        if base_type == "input":
            self.input_base = base
            self.input_base_button.text = base.capitalize()
        else:
            self.output_base = base
            self.output_base_button.text = base.capitalize()
    
    def convert_base(self, num_str):
        try:
            # Convert input string to decimal based on input base
            if self.input_base == "binary":
                num = int(num_str, 2)
            elif self.input_base == "octal":
                num = int(num_str, 8)
            elif self.input_base == "decimal":
                num = float(num_str) if '.' in num_str else int(num_str)
            elif self.input_base == "hexadecimal":
                num = int(num_str, 16)
            
            # Convert decimal number to output base
            if self.output_base == "binary":
                if isinstance(num, float):
                    result = self.float_to_base(num, 2)
                else:
                    result = bin(num)[2:]  # Remove '0b' prefix
            elif self.output_base == "octal":
                if isinstance(num, float):
                    result = self.float_to_base(num, 8)
                else:
                    result = oct(num)[2:]  # Remove '0o' prefix
            elif self.output_base == "decimal":
                result = str(num)
            elif self.output_base == "hexadecimal":
                if isinstance(num, float):
                    result = self.float_to_base(num, 16)
                else:
                    result = hex(num)[2:]  # Remove '0x' prefix
            
            # Display result
            self.root.ids.display.text = result
            self.history.append(f"Base Conv: {num_str} ({self.input_base}) → {result} ({self.output_base})")
            self.dialog.dismiss()
        except Exception as e:
            self.root.ids.display.text = "Error"
            print(f"Conversion error: {e}")
    
    def float_to_base(self, num, base):
        """Convert a floating point number to a given base"""
        # Separate integer and fractional parts
        integer_part = int(num)
        fractional_part = num - integer_part
        
        # Convert integer part
        if integer_part == 0:
            integer_str = "0"
        else:
            integer_str = ""
            n = integer_part
            while n > 0:
                remainder = n % base
                integer_str = (str(remainder) if remainder < 10 else chr(ord('A') + remainder - 10)) + integer_str
                n = n // base
        
        # Convert fractional part (up to 10 digits)
        fractional_str = ""
        if fractional_part > 0:
            fractional_str = "."
            f = fractional_part
            for _ in range(10):  # Limit to 10 fractional digits
                f *= base
                digit = int(f)
                fractional_str += str(digit) if digit < 10 else chr(ord('A') + digit - 10)
                f -= digit
                if f == 0:
                    break
        
        return integer_str + fractional_str
    
    def open_unit_conversion_dialog(self):
        # Dismiss any existing menu
        if hasattr(self, 'menu') and self.menu:
            self.menu.dismiss()
        
        layout = EquationInputLayout()
        
        # Category selection
        category_layout = MDBoxLayout(size_hint_y=None, height="50dp", spacing="10dp")
        category_layout.add_widget(MDLabel(text="Category:", size_hint_x=0.4))
        category_button = MDRaisedButton(
            text="length",
            size_hint_x=0.6,
            on_release=lambda x: self.show_category_menu(x)
        )
        category_layout.add_widget(category_button)
        layout.add_widget(category_layout)
        
        # Input field
        input_field = MDTextField(
            hint_text="Enter value",
            size_hint_y=None,
            height="50dp"
        )
        layout.add_widget(input_field)
        
        # From unit selection
        from_unit_layout = MDBoxLayout(size_hint_y=None, height="50dp", spacing="10dp")
        from_unit_layout.add_widget(MDLabel(text="From:", size_hint_x=0.4))
        from_unit_button = MDRaisedButton(
            text="m",
            size_hint_x=0.6,
            on_release=lambda x: self.show_unit_menu(x, "from")
        )
        from_unit_layout.add_widget(from_unit_button)
        layout.add_widget(from_unit_layout)
        
        # To unit selection
        to_unit_layout = MDBoxLayout(size_hint_y=None, height="50dp", spacing="10dp")
        to_unit_layout.add_widget(MDLabel(text="To:", size_hint_x=0.4))
        to_unit_button = MDRaisedButton(
            text="m",
            size_hint_x=0.6,
            on_release=lambda x: self.show_unit_menu(x, "to")
        )
        to_unit_layout.add_widget(to_unit_button)
        layout.add_widget(to_unit_layout)
        
        # Convert button
        convert_button = MDRaisedButton(
            text="Convert",
            size_hint_y=None,
            height="50dp",
            on_release=lambda x: self.convert_unit(input_field.text)
        )
        layout.add_widget(convert_button)
        
        # Store references
        self.category_button = category_button
        self.from_unit_button = from_unit_button
        self.to_unit_button = to_unit_button
        self.current_category = "length"
        
        self.dialog = MDDialog(
            title="Unit Conversion",
            type="custom",
            content_cls=layout,
            buttons=[
                MDFlatButton(text="Close", on_release=lambda x: self.dialog.dismiss())
            ]
        )
        self.dialog.open()
    
    def show_category_menu(self, caller):
        categories = list(self.unit_conversions.keys())
        items = [
            {"text": cat.capitalize(), "on_release": lambda x=cat: self.set_category(x)}
            for cat in categories
        ]
        self.menu = MDDropdownMenu(
            caller=caller,
            items=items,
            width_mult=4
        )
        self.menu.open()
    
    def set_category(self, category):
        self.current_category = category
        self.category_button.text = category.capitalize()
        
        # Reset unit buttons to first unit in the category
        first_unit = list(self.unit_conversions[category].keys())[0]
        self.from_unit_button.text = first_unit
        self.to_unit_button.text = first_unit
    
    def show_unit_menu(self, caller, unit_type):
        units = list(self.unit_conversions[self.current_category].keys())
        items = [
            {"text": unit, "on_release": lambda x=unit: self.set_unit(unit_type, x)}
            for unit in units
        ]
        self.menu = MDDropdownMenu(
            caller=caller,
            items=items,
            width_mult=4
        )
        self.menu.open()
    
    def set_unit(self, unit_type, unit):
        if unit_type == "from":
            self.from_unit_button.text = unit
        else:
            self.to_unit_button.text = unit
    
    def convert_unit(self, value_str):
        try:
            value = float(value_str)
            from_unit = self.from_unit_button.text
            to_unit = self.to_unit_button.text
            category = self.current_category
            
            if category == "temperature":
                # Special handling for temperature
                if from_unit == "celsius":
                    if to_unit == "fahrenheit":
                        result = (value * 9/5) + 32
                    elif to_unit == "kelvin":
                        result = value + 273.15
                    else:
                        result = value
                elif from_unit == "fahrenheit":
                    if to_unit == "celsius":
                        result = (value - 32) * 5/9
                    elif to_unit == "kelvin":
                        result = (value - 32) * 5/9 + 273.15
                    else:
                        result = value
                elif from_unit == "kelvin":
                    if to_unit == "celsius":
                        result = value - 273.15
                    elif to_unit == "fahrenheit":
                        result = (value - 273.15) * 9/5 + 32
                    else:
                        result = value
            else:
                # For all other categories, use conversion factors
                from_factor = self.unit_conversions[category][from_unit]
                to_factor = self.unit_conversions[category][to_unit]
                
                # Convert to base unit first, then to target unit
                base_value = value * from_factor
                result = base_value / to_factor
            
            # Display result
            self.root.ids.display.text = str(result)
            self.history.append(f"Unit Conv: {value} {from_unit} → {result} {to_unit}")
            self.dialog.dismiss()
        except Exception as e:
            self.root.ids.display.text = "Error"
            print(f"Unit conversion error: {e}")
    
    def open_constants_dialog(self):
        # Dismiss any existing menu
        if hasattr(self, 'menu') and self.menu:
            self.menu.dismiss()
        
        layout = EquationInputLayout()
        
        # Add a scrollable list of constants
        scroll_view = MDScrollView(size_hint=(1, None), height=400)
        list_layout = MDList()
        
        for name, value in self.physical_constants.items():
            item = OneLineListItem(
                text=f"{name}: {value}",
                on_release=lambda x=value: self.insert_constant(x)
            )
            list_layout.add_widget(item)
        
        scroll_view.add_widget(list_layout)
        layout.add_widget(scroll_view)
        
        self.dialog = MDDialog(
            title="Physical Constants",
            type="custom",
            content_cls=layout,
            buttons=[
                MDFlatButton(text="Close", on_release=lambda x: self.dialog.dismiss())
            ]
        )
        self.dialog.open()
    
    def insert_constant(self, value):
        display = self.root.ids.display
        if display.text in ("0", "Error"):
            display.text = str(value)
        else:
            display.text += str(value)
        self.dialog.dismiss()
    
    def open_bitwise_dialog(self):
        # Dismiss any existing menu
        if hasattr(self, 'menu') and self.menu:
            self.menu.dismiss()
        
        layout = EquationInputLayout()
        
        # Input fields
        input1 = MDTextField(
            hint_text="Enter first integer",
            size_hint_y=None,
            height="50dp"
        )
        layout.add_widget(input1)
        
        input2 = MDTextField(
            hint_text="Enter second integer (not needed for NOT)",
            size_hint_y=None,
            height="50dp"
        )
        layout.add_widget(input2)
        
        # Operation buttons
        ops_layout = MDGridLayout(cols=3, spacing="10dp", size_hint_y=None, height="50dp")
        ops_layout.add_widget(MDRaisedButton(text="AND", on_release=lambda x: self.bitwise_op("AND", input1.text, input2.text)))
        ops_layout.add_widget(MDRaisedButton(text="OR", on_release=lambda x: self.bitwise_op("OR", input1.text, input2.text)))
        ops_layout.add_widget(MDRaisedButton(text="XOR", on_release=lambda x: self.bitwise_op("XOR", input1.text, input2.text)))
        ops_layout.add_widget(MDRaisedButton(text="NOT", on_release=lambda x: self.bitwise_op("NOT", input1.text, "")))
        ops_layout.add_widget(MDRaisedButton(text="<<", on_release=lambda x: self.bitwise_op("LSHIFT", input1.text, input2.text)))
        ops_layout.add_widget(MDRaisedButton(text=">>", on_release=lambda x: self.bitwise_op("RSHIFT", input1.text, input2.text)))
        layout.add_widget(ops_layout)
        
        self.dialog = MDDialog(
            title="Bitwise Operations",
            type="custom",
            content_cls=layout,
            buttons=[
                MDFlatButton(text="Close", on_release=lambda x: self.dialog.dismiss())
            ]
        )
        self.dialog.open()
    
    def bitwise_op(self, op, val1_str, val2_str):
        try:
            val1 = int(val1_str)
            if op == "NOT":
                result = ~val1
            else:
                val2 = int(val2_str)
                if op == "AND":
                    result = val1 & val2
                elif op == "OR":
                    result = val1 | val2
                elif op == "XOR":
                    result = val1 ^ val2
                elif op == "LSHIFT":
                    result = val1 << val2
                elif op == "RSHIFT":
                    result = val1 >> val2
            
            self.root.ids.display.text = str(result)
            self.history.append(f"Bitwise {op}: {val1} {op} {val2 if val2_str else ''} = {result}")
            self.dialog.dismiss()
        except Exception as e:
            self.root.ids.display.text = "Error"
            print(f"Bitwise error: {e}")
    
    def open_stats_dialog(self):
        # Dismiss any existing menu
        if hasattr(self, 'menu') and self.menu:
            self.menu.dismiss()
        
        layout = EquationInputLayout()
        
        # Input field for numbers
        numbers_input = MDTextField(
            hint_text="Enter comma-separated numbers",
            size_hint_y=None,
            height="50dp"
        )
        layout.add_widget(numbers_input)
        
        # Operation buttons
        ops_layout = MDGridLayout(cols=3, spacing="10dp", size_hint_y=None, height="100dp")
        ops_layout.add_widget(MDRaisedButton(text="Mean", on_release=lambda x: self.stats_op("mean", numbers_input.text)))
        ops_layout.add_widget(MDRaisedButton(text="Median", on_release=lambda x: self.stats_op("median", numbers_input.text)))
        ops_layout.add_widget(MDRaisedButton(text="Mode", on_release=lambda x: self.stats_op("mode", numbers_input.text)))
        ops_layout.add_widget(MDRaisedButton(text="Std Dev", on_release=lambda x: self.stats_op("std", numbers_input.text)))
        ops_layout.add_widget(MDRaisedButton(text="Variance", on_release=lambda x: self.stats_op("var", numbers_input.text)))
        ops_layout.add_widget(MDRaisedButton(text="nPr", on_release=lambda x: self.stats_op("npr", numbers_input.text)))
        ops_layout.add_widget(MDRaisedButton(text="nCr", on_release=lambda x: self.stats_op("ncr", numbers_input.text)))
        layout.add_widget(ops_layout)
        
        self.dialog = MDDialog(
            title="Descriptive Statistics",
            type="custom",
            content_cls=layout,
            buttons=[
                MDFlatButton(text="Close", on_release=lambda x: self.dialog.dismiss())
            ]
        )
        self.dialog.open()
    
    def stats_op(self, op, numbers_str):
        try:
            if op in ["npr", "ncr"]:
                # For permutations and combinations, we need exactly two numbers
                numbers = [float(x.strip()) for x in numbers_str.split(',')]
                if len(numbers) != 2:
                    self.root.ids.display.text = "Error: Need exactly 2 numbers for nPr/nCr"
                    return
                n, r = int(numbers[0]), int(numbers[1])
                
                if op == "npr":
                    result = math.perm(n, r)
                else:  # ncr
                    result = math.comb(n, r)
            else:
                # For other statistics, we need a list of numbers
                numbers = [float(x.strip()) for x in numbers_str.split(',')]
                
                if op == "mean":
                    result = sum(numbers) / len(numbers)
                elif op == "median":
                    sorted_numbers = sorted(numbers)
                    n = len(sorted_numbers)
                    if n % 2 == 1:
                        result = sorted_numbers[n//2]
                    else:
                        result = (sorted_numbers[n//2 - 1] + sorted_numbers[n//2]) / 2
                elif op == "mode":
                    counts = Counter(numbers)
                    max_count = max(counts.values())
                    modes = [k for k, v in counts.items() if v == max_count]
                    result = modes[0] if len(modes) == 1 else modes
                elif op == "std":
                    result = statistics.stdev(numbers)
                elif op == "var":
                    result = statistics.variance(numbers)
            
            self.root.ids.display.text = str(result)
            self.history.append(f"Stats {op}: {numbers_str} = {result}")
            self.dialog.dismiss()
        except Exception as e:
            self.root.ids.display.text = "Error"
            print(f"Stats error: {e}")
    
    def open_matrix_dialog(self):
        # Dismiss any existing menu
        if hasattr(self, 'menu') and self.menu:
            self.menu.dismiss()
        
        layout = EquationInputLayout()
        
        # Matrix size selection
        size_layout = MDBoxLayout(size_hint_y=None, height="50dp", spacing="10dp")
        size_layout.add_widget(MDLabel(text="Matrix Size:", size_hint_x=0.4))
        size_button = MDRaisedButton(
            text="2x2",
            size_hint_x=0.6,
            on_release=lambda x: self.show_matrix_size_menu(x)
        )
        size_layout.add_widget(size_button)
        layout.add_widget(size_layout)
        
        # Operation selection
        op_layout = MDBoxLayout(size_hint_y=None, height="50dp", spacing="10dp")
        op_layout.add_widget(MDLabel(text="Operation:", size_hint_x=0.4))
        op_button = MDRaisedButton(
            text="Add",
            size_hint_x=0.6,
            on_release=lambda x: self.show_matrix_op_menu(x)
        )
        op_layout.add_widget(op_button)
        layout.add_widget(op_layout)
        
        # Matrix inputs
        self.matrix_inputs = {}
        self.matrix_layout = MatrixInputLayout()
        layout.add_widget(self.matrix_layout)
        
        # Calculate button
        calc_button = MDRaisedButton(
            text="Calculate",
            size_hint_y=None,
            height="50dp",
            on_release=lambda x: self.perform_matrix_operation()
        )
        layout.add_widget(calc_button)
        
        # Store references
        self.size_button = size_button
        self.op_button = op_button
        self.matrix_size = "2x2"
        self.matrix_operation = "add"
        
        # Initialize matrix inputs
        self.setup_matrix_inputs()
        
        self.dialog = MDDialog(
            title="Matrix Operations",
            type="custom",
            content_cls=layout,
            buttons=[
                MDFlatButton(text="Close", on_release=lambda x: self.dialog.dismiss())
            ]
        )
        self.dialog.open()
    
    def show_matrix_size_menu(self, caller):
        sizes = ["2x2", "3x3"]
        items = [
            {"text": size, "on_release": lambda x=size: self.set_matrix_size(x)}
            for size in sizes
        ]
        self.menu = MDDropdownMenu(
            caller=caller,
            items=items,
            width_mult=4
        )
        self.menu.open()
    
    def set_matrix_size(self, size):
        self.matrix_size = size
        self.size_button.text = size
        self.setup_matrix_inputs()
    
    def show_matrix_op_menu(self, caller):
        ops = ["Add", "Subtract", "Multiply", "Transpose", "Inverse", "Determinant"]
        items = [
            {"text": op, "on_release": lambda x=op.lower(): self.set_matrix_operation(x)}
            for op in ops
        ]
        self.menu = MDDropdownMenu(
            caller=caller,
            items=items,
            width_mult=4
        )
        self.menu.open()
    
    def set_matrix_operation(self, op):
        self.matrix_operation = op
        self.op_button.text = op.capitalize()
        self.setup_matrix_inputs()
    
    def setup_matrix_inputs(self):
        # Clear existing inputs
        self.matrix_layout.clear_widgets()
        self.matrix_inputs.clear()
        
        if self.matrix_size == "2x2":
            if self.matrix_operation in ["add", "subtract", "multiply"]:
                # Two matrices
                self.matrix_inputs["A"] = {}
                self.matrix_inputs["B"] = {}
                
                # Matrix A
                self.matrix_layout.add_widget(MDLabel(text="Matrix A", halign="center"))
                for i in range(2):
                    for j in range(2):
                        field = MDTextField(
                            hint_text=f"A{i+1}{j+1}",
                            input_filter="float",
                            size_hint_y=None,
                            height="40dp"
                        )
                        self.matrix_layout.add_widget(field)
                        self.matrix_inputs["A"][(i, j)] = field
                
                # Matrix B
                self.matrix_layout.add_widget(MDLabel(text="Matrix B", halign="center"))
                for i in range(2):
                    for j in range(2):
                        field = MDTextField(
                            hint_text=f"B{i+1}{j+1}",
                            input_filter="float",
                            size_hint_y=None,
                            height="40dp"
                        )
                        self.matrix_layout.add_widget(field)
                        self.matrix_inputs["B"][(i, j)] = field
            else:
                # Single matrix
                self.matrix_inputs["A"] = {}
                self.matrix_layout.add_widget(MDLabel(text="Matrix", halign="center"))
                for i in range(2):
                    for j in range(2):
                        field = MDTextField(
                            hint_text=f"M{i+1}{j+1}",
                            input_filter="float",
                            size_hint_y=None,
                            height="40dp"
                        )
                        self.matrix_layout.add_widget(field)
                        self.matrix_inputs["A"][(i, j)] = field
        else:  # 3x3
            if self.matrix_operation in ["add", "subtract", "multiply"]:
                # Two matrices
                self.matrix_inputs["A"] = {}
                self.matrix_inputs["B"] = {}
                
                # Matrix A
                self.matrix_layout.add_widget(MDLabel(text="Matrix A", halign="center"))
                for i in range(3):
                    for j in range(3):
                        field = MDTextField(
                            hint_text=f"A{i+1}{j+1}",
                            input_filter="float",
                            size_hint_y=None,
                            height="40dp"
                        )
                        self.matrix_layout.add_widget(field)
                        self.matrix_inputs["A"][(i, j)] = field
                
                # Matrix B
                self.matrix_layout.add_widget(MDLabel(text="Matrix B", halign="center"))
                for i in range(3):
                    for j in range(3):
                        field = MDTextField(
                            hint_text=f"B{i+1}{j+1}",
                            input_filter="float",
                            size_hint_y=None,
                            height="40dp"
                        )
                        self.matrix_layout.add_widget(field)
                        self.matrix_inputs["B"][(i, j)] = field
            else:
                # Single matrix
                self.matrix_inputs["A"] = {}
                self.matrix_layout.add_widget(MDLabel(text="Matrix", halign="center"))
                for i in range(3):
                    for j in range(3):
                        field = MDTextField(
                            hint_text=f"M{i+1}{j+1}",
                            input_filter="float",
                            size_hint_y=None,
                            height="40dp"
                        )
                        self.matrix_layout.add_widget(field)
                        self.matrix_inputs["A"][(i, j)] = field
    
    def perform_matrix_operation(self):
        try:
            # Get matrix A
            if self.matrix_size == "2x2":
                A = np.zeros((2, 2))
                for i in range(2):
                    for j in range(2):
                        A[i, j] = float(self.matrix_inputs["A"][(i, j)].text)
            else:  # 3x3
                A = np.zeros((3, 3))
                for i in range(3):
                    for j in range(3):
                        A[i, j] = float(self.matrix_inputs["A"][(i, j)].text)
            
            # Perform operation
            if self.matrix_operation == "add":
                # Get matrix B
                if self.matrix_size == "2x2":
                    B = np.zeros((2, 2))
                    for i in range(2):
                        for j in range(2):
                            B[i, j] = float(self.matrix_inputs["B"][(i, j)].text)
                else:  # 3x3
                    B = np.zeros((3, 3))
                    for i in range(3):
                        for j in range(3):
                            B[i, j] = float(self.matrix_inputs["B"][(i, j)].text)
                
                result = A + B
            elif self.matrix_operation == "subtract":
                # Get matrix B
                if self.matrix_size == "2x2":
                    B = np.zeros((2, 2))
                    for i in range(2):
                        for j in range(2):
                            B[i, j] = float(self.matrix_inputs["B"][(i, j)].text)
                else:  # 3x3
                    B = np.zeros((3, 3))
                    for i in range(3):
                        for j in range(3):
                            B[i, j] = float(self.matrix_inputs["B"][(i, j)].text)
                
                result = A - B
            elif self.matrix_operation == "multiply":
                # Get matrix B
                if self.matrix_size == "2x2":
                    B = np.zeros((2, 2))
                    for i in range(2):
                        for j in range(2):
                            B[i, j] = float(self.matrix_inputs["B"][(i, j)].text)
                else:  # 3x3
                    B = np.zeros((3, 3))
                    for i in range(3):
                        for j in range(3):
                            B[i, j] = float(self.matrix_inputs["B"][(i, j)].text)
                
                result = np.dot(A, B)
            elif self.matrix_operation == "transpose":
                result = A.T
            elif self.matrix_operation == "inverse":
                result = np.linalg.inv(A)
            elif self.matrix_operation == "determinant":
                result = np.linalg.det(A)
            
            # Format result
            if isinstance(result, np.ndarray):
                # Format as matrix string
                result_str = "["
                for i in range(result.shape[0]):
                    if i > 0:
                        result_str += " "
                    row_str = "["
                    for j in range(result.shape[1]):
                        row_str += f"{result[i, j]:.4f}"
                        if j < result.shape[1] - 1:
                            row_str += ", "
                    row_str += "]"
                    result_str += row_str
                    if i < result.shape[0] - 1:
                        result_str += "\n"
                result_str += "]"
            else:
                result_str = f"{result:.4f}"
            
            self.root.ids.display.text = result_str
            self.history.append(f"Matrix {self.matrix_operation}: {result_str}")
            self.dialog.dismiss()
        except Exception as e:
            self.root.ids.display.text = "Error"
            print(f"Matrix error: {e}")
    
    def calculate_result(self):
        display = self.root.ids.display
        try:
            expr = display.text.replace("^", "**")
            
            # Define functions with proper angle mode handling
            def sin(x): 
                return math.sin(math.radians(x)) if self.angle_mode == "deg" else math.sin(x)
            
            def cos(x): 
                return math.cos(math.radians(x)) if self.angle_mode == "deg" else math.cos(x)
            
            def tan(x): 
                return math.tan(math.radians(x)) if self.angle_mode == "deg" else math.tan(x)
            
            def asin(x): 
                result = math.asin(x)
                return math.degrees(result) if self.angle_mode == "deg" else result
            
            def acos(x): 
                result = math.acos(x)
                return math.degrees(result) if self.angle_mode == "deg" else result
            
            def atan(x): 
                result = math.atan(x)
                return math.degrees(result) if self.angle_mode == "deg" else result
            
            # Hyperbolic functions
            def sinh(x): 
                return math.sinh(x)
            
            def cosh(x): 
                return math.cosh(x)
            
            def tanh(x): 
                return math.tanh(x)
            
            def asinh(x): 
                return math.asinh(x)
            
            def acosh(x): 
                return math.acosh(x)
            
            def atanh(x): 
                return math.atanh(x)
            
            # Safe evaluation environment
            result = eval(expr, {"__builtins__": None}, {
                "sin": sin, "cos": cos, "tan": tan,
                "asin": asin, "acos": acos, "atan": atan,
                "sinh": sinh, "cosh": cosh, "tanh": tanh,
                "asinh": asinh, "acosh": acosh, "atanh": atanh,
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
            
            # Format the result nicely
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                result_str = str(result)
            else:
                result_str = str(result)
                
            self.history.append(f"{display.text} = {result_str}")
            display.text = result_str
        except Exception as e:
            display.text = "Error"
            print(f"Error: {e}")
    
    def open_equation_dialog(self, mode):
        # Dismiss menu if it exists
        if hasattr(self, 'menu') and self.menu:
            self.menu.dismiss()
        
        self.coeff_inputs = {}
        if mode == "linear":
            fields = ["a", "b"]
            equation_text = "ax + b = 0"
        else:  # quadratic
            fields = ["a", "b", "c"]
            equation_text = "ax² + bx + c = 0"
            
        layout = EquationInputLayout()
        # Add equation label
        layout.add_widget(MDLabel(text=equation_text, halign="center"))
        
        for label in fields:
            field = MDTextField(
                hint_text=f"Enter {label}",
                input_filter="float",
                size_hint_y=None,
                height="50dp"
            )
            layout.add_widget(field)
            self.coeff_inputs[label] = field
            
        # Add solve button
        solve_button = MDRaisedButton(
            text="Solve",
            size_hint_y=None,
            height="50dp",
            on_release=lambda x: self.solve_equation(mode)
        )
        layout.add_widget(solve_button)
        
        self.dialog = MDDialog(
            title=f"Solve {mode.title()} Equation",
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
            else:  # quadratic
                a, b, c = coeffs["a"], coeffs["b"], coeffs["c"]
                if a == 0:
                    # If a=0, it's not quadratic but linear
                    if b == 0:
                        result = "No solution" if c != 0 else "Infinite solutions"
                    else:
                        x = -c / b
                        result = f"x = {x:.4f}"
                else:
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
    
    def open_system_dialog(self, system_type):
        # Dismiss menu if it exists
        if hasattr(self, 'menu') and self.menu:
            self.menu.dismiss()
        
        self.coeff_inputs = {}
        
        if system_type == "2x2":
            # 2x2 system: a1x + b1y = c1, a2x + b2y = c2
            equation_text = "System of 2 equations with 2 unknowns:\n" \
                           "a₁x + b₁y = c₁\n" \
                           "a₂x + b₂y = c₂"
            fields = ["a₁", "b₁", "c₁", "a₂", "b₂", "c₂"]
        else:  # 3x3
            # 3x3 system: a1x + b1y + c1z = d1, a2x + b2y + c2z = d2, a3x + b3y + c3z = d3
            equation_text = "System of 3 equations with 3 unknowns:\n" \
                           "a₁x + b₁y + c₁z = d₁\n" \
                           "a₂x + b₂y + c₂z = d₂\n" \
                           "a₃x + b₃y + c₃z = d₃"
            fields = ["a₁", "b₁", "c₁", "d₁", 
                     "a₂", "b₂", "c₂", "d₂", 
                     "a₃", "b₃", "c₃", "d₃"]
        
        # Create main layout
        main_layout = EquationInputLayout()
        
        # Add equation label
        main_layout.add_widget(MDLabel(text=equation_text, halign="center"))
        
        # Create scrollable area for input fields
        scroll_view = MDScrollView(size_hint=(1, None), height=300)
        
        # Create layout for input fields
        input_layout = EquationInputLayout(orientation='vertical', size_hint_y=None)
        input_layout.bind(minimum_height=input_layout.setter('height'))
        
        # Add input fields
        for label in fields:
            field = MDTextField(
                hint_text=f"Enter {label}",
                input_filter="float",
                size_hint_y=None,
                height="50dp"
            )
            input_layout.add_widget(field)
            self.coeff_inputs[label] = field
        
        # Add input layout to scroll view
        scroll_view.add_widget(input_layout)
        main_layout.add_widget(scroll_view)
        
        # Add solve button
        solve_button = MDRaisedButton(
            text="Solve",
            size_hint_y=None,
            height="50dp",
            on_release=lambda x: self.solve_system(system_type)
        )
        main_layout.add_widget(solve_button)
        
        self.dialog = MDDialog(
            title=f"Solve {system_type} System",
            type="custom",
            content_cls=main_layout,
            buttons=[
                MDFlatButton(text="Cancel", on_release=lambda x: self.dialog.dismiss())
            ]
        )
        self.dialog.open()
    
    def solve_system(self, system_type):
        try:
            coeffs = {}
            for k, v in self.coeff_inputs.items():
                if v.text.strip() == "":
                    self.root.ids.display.text = "Please enter all coefficients"
                    return
                coeffs[k] = float(v.text)
            
            if system_type == "2x2":
                # Extract coefficients
                a1, b1, c1 = coeffs["a₁"], coeffs["b₁"], coeffs["c₁"]
                a2, b2, c2 = coeffs["a₂"], coeffs["b₂"], coeffs["c₂"]
                
                # Calculate determinant
                det = a1 * b2 - a2 * b1
                
                if det != 0:
                    # Unique solution
                    x = (c1 * b2 - c2 * b1) / det
                    y = (a1 * c2 - a2 * c1) / det
                    result = f"x = {x:.4f}, y = {y:.4f}"
                else:
                    # Check if the system is consistent
                    if a1 * c2 == a2 * c1 and b1 * c2 == b2 * c1:
                        result = "Infinite solutions"
                    else:
                        result = "No solution"
            
            else:  # 3x3
                # Extract coefficients
                a1, b1, c1, d1 = coeffs["a₁"], coeffs["b₁"], coeffs["c₁"], coeffs["d₁"]
                a2, b2, c2, d2 = coeffs["a₂"], coeffs["b₂"], coeffs["c₂"], coeffs["d₂"]
                a3, b3, c3, d3 = coeffs["a₃"], coeffs["b₃"], coeffs["c₃"], coeffs["d₃"]
                
                # Calculate determinant of coefficient matrix
                det = (a1 * (b2 * c3 - b3 * c2) - 
                       b1 * (a2 * c3 - a3 * c2) + 
                       c1 * (a2 * b3 - a3 * b2))
                
                if det != 0:
                    # Unique solution using Cramer's rule
                    # Calculate determinants for x, y, z
                    det_x = (d1 * (b2 * c3 - b3 * c2) - 
                             b1 * (d2 * c3 - d3 * c2) + 
                             c1 * (d2 * b3 - d3 * b2))
                    
                    det_y = (a1 * (d2 * c3 - d3 * c2) - 
                             d1 * (a2 * c3 - a3 * c2) + 
                             c1 * (a2 * d3 - a3 * d2))
                    
                    det_z = (a1 * (b2 * d3 - b3 * d2) - 
                             b1 * (a2 * d3 - a3 * d2) + 
                             d1 * (a2 * b3 - a3 * b2))
                    
                    x = det_x / det
                    y = det_y / det
                    z = det_z / det
                    result = f"x = {x:.4f}, y = {y:.4f}, z = {z:.4f}"
                else:
                    # Check if the system is consistent
                    # This is a simplified check - in a real app, you'd need more robust methods
                    if (a1 * d2 == a2 * d1 and b1 * d2 == b2 * d1 and c1 * d2 == c2 * d1 and
                        a1 * d3 == a3 * d1 and b1 * d3 == b3 * d1 and c1 * d3 == c3 * d1):
                        result = "Infinite solutions"
                    else:
                        result = "No solution"
        
        except Exception as e:
            result = "Error solving system"
            print(e)
        
        self.dialog.dismiss()
        self.root.ids.display.text = result
        self.history.append(f"{system_type} System => {result}")
    
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
