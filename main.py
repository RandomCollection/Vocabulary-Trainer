# MODULE:       main.py
# VERSION:      1.0
# DIRECTORY:    <masked>
# DATE:         2022-08-21
# AUTHOR:       RandomCollection
# DESCRIPTION:  See https://github.com/RandomCollection/Vocabulary-Trainer.

# LIBRARIES ############################################################################################################

import pandas as pd
import random
import webbrowser

from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu

KV = r"""
Screen:

    in_class: text

    canvas.before:
        Color:
            rgba: (0.5, 0.3, 0.2, 1)

    BoxLayout:

        orientation: "vertical"

        MDToolbar:
            title: "Menu"
            left_action_items: [["menu", lambda x: nav_draw.set_state()]]

        Widget:

    MDNavigationLayout:

        ScreenManager:

            id: screen_manager

            Screen:

                name: "screen_1"

                MDLabel:
                    text: "Welcome\nto\nthe\nVocabulary\nTrainer!"
                    font_style: "H4"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 0, 0, 0, 1
        
            Screen:

                name: "screen_2"

                MDLabel:
                    text: "Please translate"
                    halign: "center"
                    pos_hint: {"center_y": 0.8}

                MDLabel:
                    text: ""
                    id: word_in
                    halign: "center"
                    pos_hint: {"center_y": 0.7}
                    font_style: "Body1"

                MDTextField:
                    id: text
                    hint_text: "Enter translation here"
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
                    size_hint_x: None
                    mode: "rectangle"
                    width: 200

                MDLabel:
                    text: ""
                    id: word_out
                    halign: "center"
                    markup: True
                    pos_hint: {"center_y": 0.4}
                    font_style: "Body1"

                MDFillRoundFlatButton:
                    text: "Next"
                    pos_hint: {"center_x": 0.3, "center_y": 0.2}
                    font_style: "Button"
                    on_press: app.next()

                MDFillRoundFlatButton:
                    text: "Check"
                    pos_hint: {"center_x": 0.7, "center_y": 0.2}
                    font_style: "Button"
                    on_press: app.check()

                MDFillRoundFlatButton:
                    text: "Solve"
                    pos_hint: {"center_x": 0.5, "center_y": 0.1}
                    font_style: "Button"
                    md_bg_color: app.theme_cls.primary_light
                    on_press: app.solve()

                MDFloatingActionButtonSpeedDial:
                    callback: app.callback
                    data: app.data
                    bg_color_root_button: app.theme_cls.primary_light
                    root_button_anim: True

                MDRaisedButton:
                    id: menu_
                    pos_hint: {"center_x": 0.1, "center_y": 0.1}
                    font_style: "Button"
                    md_bg_color: app.theme_cls.primary_light
                    text: "Category"
                    on_release: app.dropdown()

            Screen:

                name: "screen_3"

                MDLabel:
                    text: "This is a RandomCollection production."
                    font_style: "Body2"
                    halign: "center"
                    pos_hint: {"center_y": 0.7}

                MDLabel:
                    text: "For more information, check out"
                    font_style: "Body2"
                    halign: "center"
                    pos_hint: {"center_y": 0.6}

                MDLabel:
                    text: "[ref=randomcollection_github]RandomCollection GitHub[/ref]"
                    font_style: "Body2"
                    halign: "center"
                    markup: True
                    pos_hint: {"center_y": 0.5}
                    text_color: 5/255, 99/255, 193/255, 1
                    theme_text_color: "Custom"
                    underline: True
                    on_ref_press: app.open_link_1()

                MDLabel:
                    text: "or"
                    font_style: "Body2"
                    halign: "center"
                    pos_hint: {"center_y": 0.4}

                MDLabel:
                    text: "[ref=randomcollection_github_page]RandomCollection GitHub Page[/ref]"
                    font_style: "Body2"
                    halign: "center"
                    markup: True
                    pos_hint: {"center_y": 0.3}
                    text_color: 0.0196, 0.3882, 0.7569, 1
                    theme_text_color: "Custom"
                    underline: True
                    on_ref_press: app.open_link_2()

        MDNavigationDrawer:
            id: nav_draw
            orientation: "vertical"
            padding: "12dp", "12dp", "12dp", "0dp"
            spacing: "5dp"

            AnchorLayout:
                anchor_x: "left"
                size_hint_y: None

            MDLabel:
                text: "Vocabulary Trainer"
                font_style: "Button"
                size_hint_y: None
                height: self.texture_size[1]

            MDLabel:
                text: "RandomCollection"
                font_style: "Caption"
                size_hint_y: None
                height: self.texture_size[1]

            ScrollView:

                MDList:

                    OneLineAvatarListItem:
                        text: "Home"
                        on_press:
                            nav_draw.set_state("close")
                            screen_manager.current = "screen_1"
                        IconLeftWidget:
                            icon: "home-circle"

                    OneLineAvatarListItem:
                        text: "Start"
                        on_press:
                            nav_draw.set_state("close")
                            screen_manager.current = "screen_2"
                        IconLeftWidget:
                            icon: "play-circle"

                    OneLineAvatarListItem:
                        text: "About"
                        on_press:
                            nav_draw.set_state("close")
                            screen_manager.current = "screen_3"
                        IconLeftWidget:
                            icon: "account-circle"
            Widget:
"""

# CONSTANTS ############################################################################################################

DICT_WORDS = {'SPANISH': {0: 'el animal', 1: 'el caballo', 2: 'el perro', 3: 'el pez', 4: 'la vaca', 5: 'adiós', 6: 'el alemán', 7: 'bienvenido', 8: 'el bolígrafo', 9: 'la botella', 10: 'buenas noches', 11: 'buenas tardes', 12: 'buenos días', 13: 'la casa', 14: 'el cepillo', 15: 'el cigarrillo', 16: 'la ciudad', 17: 'el coche', 18: 'cómo estás', 19: 'el cuaderno', 20: 'de nada', 21: 'la gente', 22: 'la gitana', 23: 'el gitano', 24: 'gracias', 25: 'la guerra', 26: 'hasta luego', 27: 'hasta mañana', 28: 'hasta pronto', 29: 'hola', 30: 'el hombre', 31: 'el imbécil', 32: 'el libro', 33: 'mucha suerte', 34: 'muchas gracias', 35: 'mucho gusto', 36: 'la niña', 37: 'el niño', 38: 'la pared', 39: 'pásalo bien', 40: 'por favor', 41: 'qué tal', 42: 'la razón', 43: 'la torre', 44: 'el diente', 45: 'la mano', 46: 'ayer', 47: 'el día', 48: 'domingo', 49: 'hoy', 50: 'jueves', 51: 'lunes', 52: 'mañana', 53: 'martes', 54: 'miércoles', 55: 'sábado', 56: 'la semana', 57: 'viernes', 58: 'la abuela', 59: 'el abuelo', 60: 'amar', 61: 'la amiga', 62: 'el amigo', 63: 'besar', 64: 'la boda', 65: 'casarse', 66: 'el cumpleaños', 67: 'el divorcio', 68: 'la familia', 69: 'la hermana', 70: 'el hermano', 71: 'la hija', 72: 'el hijo', 73: 'la madre', 74: 'el marido', 75: 'el matrimonio', 76: 'la mujer', 77: 'la nieta', 78: 'el nieto', 79: 'la novia', 80: 'el novio', 81: 'el padre', 82: 'querer', 83: 'te quiero', 84: 'la tía', 85: 'el tío', 86: 'la cebolla', 87: 'el chocolate', 88: 'el chorizo', 89: 'la harina', 90: 'el vino', 91: 'la zanahoria', 92: 'el baño', 93: 'la cocina', 94: 'la cuchara', 95: 'el cuchillo', 96: 'la mesa', 97: 'la silla', 98: 'el tenedor', 99: 'el vaso', 100: 'la luna', 101: 'catorce', 102: 'cero', 103: 'cien', 104: 'cinco', 105: 'cincuenta', 106: 'cuarenta', 107: 'cuatro', 108: 'diecinueve', 109: 'dieciocho', 110: 'dieciseis', 111: 'diecisiete', 112: 'diez', 113: 'doce', 114: 'dos', 115: 'mil', 116: 'noventa', 117: 'nueve', 118: 'ochenta', 119: 'ocho', 120: 'once', 121: 'quince', 122: 'seis', 123: 'sesenta', 124: 'setenta', 125: 'siete', 126: 'trece', 127: 'treinta', 128: 'tres', 129: 'uno', 130: 'veinte', 131: 'cómo', 132: 'cuándo', 133: 'cuánto', 134: 'dónde', 135: 'él', 136: 'gordo', 137: 'pero', 138: 'por qué', 139: 'qué', 140: 'quién', 141: 'todo', 142: 'yo', 143: 'beber', 144: 'querer', 145: 'trabajar', 146: 'volar', 147: 'los animales', 148: 'los caballos', 149: 'los perros', 150: 'los peces', 151: 'las vacas', 152: 'los alemanes', 153: 'los bolígrafos', 154: 'las botellas', 155: 'las casas', 156: 'las ciudades', 157: 'las coches', 158: 'los cuadernos', 159: 'los hombres', 160: 'los imbéciles', 161: 'los libros', 162: 'las paredes', 163: 'los razones', 164: 'las torres', 165: 'los dientes', 166: 'los manos', 167: 'los padres', 168: 'los hermanos', 169: 'las cebollas', 170: 'las zanahorias', 171: 'los baños', 172: 'las cocinas', 173: 'las cucharas', 174: 'los cuchillos', 175: 'las mesas', 176: 'las sillas', 177: 'los tenedores', 178: 'los vasos', 179: 'las lunas'}, 'GERMAN': {0: 'das Tier', 1: 'das Pferd', 2: 'der Hund', 3: 'der Fisch', 4: 'die Kuh', 5: 'auf Wiedersehen', 6: 'der Deutsche', 7: 'willkommen', 8: 'der Kugelschreiber', 9: 'die Flasche', 10: 'gute Nacht', 11: 'guten Tag', 12: 'guten Morgen', 13: 'das Haus', 14: 'die Bürste', 15: 'die Zigarette', 16: 'die Stadt', 17: 'das Auto', 18: 'wie geht es dir', 19: 'das Heft', 20: 'gern geschehen', 21: 'die Leute', 22: 'die Zigeunerin', 23: 'der Zigeuner', 24: 'danke', 25: 'der Krieg', 26: 'bis später', 27: 'bis morgen', 28: 'bis dann', 29: 'hallo', 30: 'der Mann', 31: 'der Idiot', 32: 'das Buch', 33: 'viel Glück', 34: 'vielen Dank', 35: 'sehr erfreut', 36: 'das Mädchen', 37: 'der Junge', 38: 'die Wand', 39: 'viel Spaß', 40: 'bitte', 41: "wie geht's", 42: 'der Grund', 43: 'der Turm', 44: 'der Zahn', 45: 'die Hand', 46: 'gestern', 47: 'der Tag', 48: 'Sonntag', 49: 'heute', 50: 'Donnerstag', 51: 'Montag', 52: 'morgen', 53: 'Dienstag', 54: 'Mittwoch', 55: 'Samstag', 56: 'die Woche', 57: 'Freitag', 58: 'die Oma', 59: 'der Opa', 60: 'lieben', 61: 'die Freundin', 62: 'der Freund', 63: 'küssen', 64: 'die Hochzeit', 65: 'heiraten', 66: 'der Geburtstag', 67: 'die Scheidung', 68: 'die Famillie', 69: 'die Schwester', 70: 'der Bruder', 71: 'die Tochter', 72: 'der Sohn', 73: 'die Mutter', 74: 'der Ehemann', 75: 'die Ehe', 76: 'die Frau', 77: 'die Enkelin', 78: 'der Enkel', 79: 'die Freundin', 80: 'der Freund', 81: 'der Vater', 82: 'mögen', 83: 'ich liebe Dich', 84: 'die Tante', 85: 'der Onkel', 86: 'die Zwiebel', 87: 'die Schokolade', 88: 'die Wurst', 89: 'das Mehl', 90: 'der Wein', 91: 'die Karotte', 92: 'das Bad', 93: 'die Küche', 94: 'der Löffel', 95: 'das Messer', 96: 'der Tisch', 97: 'der Stuhl', 98: 'die Gabel', 99: 'das Glas', 100: 'der Mond', 101: 'vierzehn', 102: 'null', 103: 'hundert', 104: 'fünf', 105: 'fünfzig', 106: 'vierzig', 107: 'vier', 108: 'neunzehn', 109: 'achtzehn', 110: 'sechzehn', 111: 'siebzehn', 112: 'zehn', 113: 'zwölf', 114: 'zwei', 115: 'tausend', 116: 'neunzig', 117: 'neun', 118: 'achtzig', 119: 'acht', 120: 'elf', 121: 'fünfzehn', 122: 'sechs', 123: 'sechzig', 124: 'siebzig', 125: 'sieben', 126: 'dreizehn', 127: 'dreißig', 128: 'drei', 129: 'eins', 130: 'zwanzig', 131: 'wie', 132: 'wann', 133: 'wie viel', 134: 'wo', 135: 'er', 136: 'dick', 137: 'aber', 138: 'warum', 139: 'was', 140: 'wer', 141: 'alles', 142: 'ich', 143: 'trinken', 144: 'wollen', 145: 'arbeiten', 146: 'fliegen', 147: 'die Tiere', 148: 'die Pferde', 149: 'die Hunde', 150: 'die Fische', 151: 'die Kühe', 152: 'die Deutschen', 153: 'die Kugelschreiber', 154: 'die Flaschen', 155: 'die Häuser', 156: 'die Städte', 157: 'die Autos', 158: 'die Hefte', 159: 'die Männer', 160: 'die Idioten', 161: 'die Bücher', 162: 'die Wände', 163: 'die Gründe', 164: 'die Türme', 165: 'die Zähne', 166: 'die Hände', 167: 'die Eltern', 168: 'die Geschwister', 169: 'die Zwiebeln', 170: 'die Karotten', 171: 'die Bäder', 172: 'die Küchen', 173: 'die Löffel', 174: 'die Messer', 175: 'die Tische', 176: 'die Stühle', 177: 'die Gabeln', 178: 'die Gläser', 179: 'die Monde'}, 'CATEGORY': {0: 'ANIMAL', 1: 'ANIMAL', 2: 'ANIMAL', 3: 'ANIMAL', 4: 'ANIMAL', 5: 'BASIS', 6: 'BASIS', 7: 'BASIS', 8: 'BASIS', 9: 'BASIS', 10: 'BASIS', 11: 'BASIS', 12: 'BASIS', 13: 'BASIS', 14: 'BASIS', 15: 'BASIS', 16: 'BASIS', 17: 'BASIS', 18: 'BASIS', 19: 'BASIS', 20: 'BASIS', 21: 'BASIS', 22: 'BASIS', 23: 'BASIS', 24: 'BASIS', 25: 'BASIS', 26: 'BASIS', 27: 'BASIS', 28: 'BASIS', 29: 'BASIS', 30: 'BASIS', 31: 'BASIS', 32: 'BASIS', 33: 'BASIS', 34: 'BASIS', 35: 'BASIS', 36: 'BASIS', 37: 'BASIS', 38: 'BASIS', 39: 'BASIS', 40: 'BASIS', 41: 'BASIS', 42: 'BASIS', 43: 'BASIS', 44: 'BODY', 45: 'BODY', 46: 'DATE', 47: 'DATE', 48: 'DATE', 49: 'DATE', 50: 'DATE', 51: 'DATE', 52: 'DATE', 53: 'DATE', 54: 'DATE', 55: 'DATE', 56: 'DATE', 57: 'DATE', 58: 'FAMILY', 59: 'FAMILY', 60: 'FAMILY', 61: 'FAMILY', 62: 'FAMILY', 63: 'FAMILY', 64: 'FAMILY', 65: 'FAMILY', 66: 'FAMILY', 67: 'FAMILY', 68: 'FAMILY', 69: 'FAMILY', 70: 'FAMILY', 71: 'FAMILY', 72: 'FAMILY', 73: 'FAMILY', 74: 'FAMILY', 75: 'FAMILY', 76: 'FAMILY', 77: 'FAMILY', 78: 'FAMILY', 79: 'FAMILY', 80: 'FAMILY', 81: 'FAMILY', 82: 'FAMILY', 83: 'FAMILY', 84: 'FAMILY', 85: 'FAMILY', 86: 'FOOD', 87: 'FOOD', 88: 'FOOD', 89: 'FOOD', 90: 'FOOD', 91: 'FOOD', 92: 'LIVING', 93: 'LIVING', 94: 'LIVING', 95: 'LIVING', 96: 'LIVING', 97: 'LIVING', 98: 'LIVING', 99: 'LIVING', 100: 'NATURE', 101: 'NUMBER', 102: 'NUMBER', 103: 'NUMBER', 104: 'NUMBER', 105: 'NUMBER', 106: 'NUMBER', 107: 'NUMBER', 108: 'NUMBER', 109: 'NUMBER', 110: 'NUMBER', 111: 'NUMBER', 112: 'NUMBER', 113: 'NUMBER', 114: 'NUMBER', 115: 'NUMBER', 116: 'NUMBER', 117: 'NUMBER', 118: 'NUMBER', 119: 'NUMBER', 120: 'NUMBER', 121: 'NUMBER', 122: 'NUMBER', 123: 'NUMBER', 124: 'NUMBER', 125: 'NUMBER', 126: 'NUMBER', 127: 'NUMBER', 128: 'NUMBER', 129: 'NUMBER', 130: 'NUMBER', 131: 'TBD', 132: 'TBD', 133: 'TBD', 134: 'TBD', 135: 'TBD', 136: 'TBD', 137: 'TBD', 138: 'TBD', 139: 'TBD', 140: 'TBD', 141: 'TBD', 142: 'TBD', 143: 'VERB', 144: 'VERB', 145: 'VERB', 146: 'VERB', 147: 'ANIMAL', 148: 'ANIMAL', 149: 'ANIMAL', 150: 'ANIMAL', 151: 'ANIMAL', 152: 'BASIS', 153: 'BASIS', 154: 'BASIS', 155: 'BASIS', 156: 'BASIS', 157: 'BASIS', 158: 'BASIS', 159: 'BASIS', 160: 'BASIS', 161: 'BASIS', 162: 'BASIS', 163: 'BASIS', 164: 'BASIS', 165: 'BODY', 166: 'BODY', 167: 'FAMILY', 168: 'FAMILY', 169: 'FOOD', 170: 'FOOD', 171: 'LIVING', 172: 'LIVING', 173: 'LIVING', 174: 'LIVING', 175: 'LIVING', 176: 'LIVING', 177: 'LIVING', 178: 'LIVING', 179: 'NATURE'}}
WORDS = pd.DataFrame.from_dict(DICT_WORDS)


# CLASS ################################################################################################################

class VocabularyTrainer(MDApp):
	in_class = ObjectProperty(None)
	global category_var
	category_var = ""

	data = {
		"Random": "account",
		"ES -> DE": "language-php",
		"ES <- DE": "language-python",
	}

	def build(self):
		self.theme_cls.primary_palette = "Teal"
		self.theme_cls.primary_hue = "700"
		self.theme_cls.theme_style = "Light"
		return Builder.load_string(KV)

	# SCREEN 2 - START -------------------------------------------------------------------------------------------------

	def next(self):
		if category_var != "":
			worda = WORDS[WORDS["CATEGORY"] == category_var]
		else:
			worda = WORDS.copy()
		global n
		n = random.randint(0, len(worda)-1)
		label = self.root.ids.word_in
		label.text = worda.iloc[n, 1]
		self.root.in_class.text = ""
		label = self.root.ids.word_out
		label.text = ""

	def check(self):
		if self.root.in_class.text == WORDS.iloc[n, 0]:
			label = self.root.ids.word_out
			label.text = "[color=238823]Correct =)[/color]"
		else:
			label = self.root.ids.word_out
			label.text = "[color=D2222D]Wrong =([/color]"

	def solve(self):
		label = self.root.ids.word_out
		label.text = WORDS.iloc[n, 0]


	def dropdown(self):
		# global category_var
		self.menu_list = [
			{
				"viewclass": "OneLineListItem",
				"text": "All",
				"on_release": lambda x="All": self.callback(x)
			},
			{
				"viewclass": "OneLineListItem",
				"text": "Animal",
				"on_release": lambda x="Animal": self.callback(x)
			},
			{
				"viewclass": "OneLineListItem",
				"text": "Basis",
				"on_release": lambda x="Basis": self.callback(x)
			},
			{
				"viewclass": "OneLineListItem",
				"text": "Body",
				"on_release": lambda x="Body": self.callback(x)
			},
			{
				"viewclass": "OneLineListItem",
				"text": "Date",
				"on_release": lambda x="Date": self.callback(x)
			},
			{
				"viewclass": "OneLineListItem",
				"text": "Family",
				"on_release": lambda x="Family": self.callback(x)
			},
			{
				"viewclass": "OneLineListItem",
				"text": "Food",
				"on_release": lambda x="Food": self.callback(x)
			},
			{
				"viewclass": "OneLineListItem",
				"text": "Living",
				"on_release": lambda x="Living": self.callback(x)
			},
			{
				"viewclass": "OneLineListItem",
				"text": "Nature",
				"on_release": lambda x="Nature": self.callback(x)
			},
			{
				"viewclass": "OneLineListItem",
				"text": "Number",
				"on_release": lambda x="Number": self.callback(x)
			},
			{
				"viewclass": "OneLineListItem",
				"text": "Verb",
				"on_release": lambda x="Verb": self.callback(x)
			},
		]
		self.menu = MDDropdownMenu(
			caller = self.root.ids.menu_,
			items = self.menu_list,
			width_mult = 4
		)
		self.menu.open()

	def callback(self, instance):
		global category_var
		if instance == "All":
			category_var = ""
		if instance == "Animal":
			category_var = "ANIMAL"
		if instance == "Basis":
			category_var = "BASIS"
		if instance == "Body":
			category_var = "BODY"
		if instance == "Date":
			category_var = "DATE"
		if instance == "Family":
			category_var = "FAMILY"
		if instance == "Food":
			category_var = "FOOD"
		if instance == "Living":
			category_var = "LIVING"
		if instance == "Nature":
			category_var = "NATURE"
		if instance == "Number":
			category_var = "NUMBER"
		if instance == "Verb":
			category_var = "VERB"

	# SCREEN 3 - ABOUT -------------------------------------------------------------------------------------------------

	def open_link_1(self):
		webbrowser.open("https://github.com/RandomCollection")

	def open_link_2(self):
		webbrowser.open("https://randomcollection.github.io/")


VocabularyTrainer().run()
