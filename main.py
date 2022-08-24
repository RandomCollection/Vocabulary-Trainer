# MODULE:       main.py
# VERSION:      1.0
# DIRECTORY:    <masked>
# DATE:         2022-08-21
# AUTHOR:       RandomCollection
# DESCRIPTION:  See https://github.com/RandomCollection/Vocabulary-Trainer.

# LIBRARIES ############################################################################################################

# import pandas as pd
import random

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
                height: avatar.height

                Image:
                    id: avatar
                    size_hint: None, None
                    size: "56dp", "56dp"
                    source: "app.png"

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

spanish = ['el animal', 'el caballo', 'el perro', 'el pez', 'la vaca', 'adiós', 'el alemán', 'bienvenido', 'el bolígrafo', 'la botella', 'buenas noches', 'buenas tardes', 'buenos días', 'la casa', 'el cepillo', 'el cigarrillo', 'la ciudad', 'el coche', 'cómo estás', 'el cuaderno', 'de nada', 'la gente', 'la gitana', 'el gitano', 'gracias', 'la guerra', 'hasta luego', 'hasta mañana', 'hasta pronto', 'hola', 'el hombre', 'el imbécil', 'el libro', 'mucha suerte', 'muchas gracias', 'mucho gusto', 'la niña', 'el niño', 'la pared', 'pásalo bien', 'por favor', 'qué tal', 'la razón', 'la torre', 'el diente', 'la mano', 'ayer', 'el día', 'domingo', 'hoy', 'jueves', 'lunes', 'mañana', 'martes', 'miércoles', 'sábado', 'la semana', 'viernes', 'la abuela', 'el abuelo', 'amar', 'la amiga', 'el amigo', 'besar', 'la boda', 'casarse', 'el cumpleaños', 'el divorcio', 'la familia', 'la hermana', 'el hermano', 'la hija', 'el hijo', 'la madre', 'el marido', 'el matrimonio', 'la mujer', 'la nieta', 'el nieto', 'la novia', 'el novio', 'el padre', 'querer', 'te quiero', 'la tía', 'el tío', 'la cebolla', 'el chocolate', 'el chorizo', 'la harina', 'el vino', 'la zanahoria', 'el baño', 'la cocina', 'la cuchara', 'el cuchillo', 'la mesa', 'la silla', 'el tenedor', 'el vaso', 'la luna', 'catorce', 'cero', 'cien', 'cinco', 'cincuenta', 'cuarenta', 'cuatro', 'diecinueve', 'dieciocho', 'dieciseis', 'diecisiete', 'diez', 'doce', 'dos', 'mil', 'noventa', 'nueve', 'ochenta', 'ocho', 'once', 'quince', 'seis', 'sesenta', 'setenta', 'siete', 'trece', 'treinta', 'tres', 'uno', 'veinte', 'cómo', 'cuándo', 'cuánto', 'dónde', 'él', 'gordo', 'pero', 'por qué', 'qué', 'quién', 'todo', 'yo', 'beber', 'querer', 'trabajar', 'volar', 'la oferta', 'agotado', 'la panadería', 'el banco', 'el importe', 'el pago', 'barato', 'el céntimo', 'la droguería', 'comprar', 'el mercadillo', 'la garantía', 'usado', 'el sueldo', 'el dinero', 'la caja', 'el dinero suelto', 'gratuito', 'el cliente', 'la clienta', 'el despegue', 'la salida', 'salir', 'llegar', 'la llegada', 'la estancia', 'el mirador', 'el bañador', 'bañarse', 'la estación', 'el andén', 'visitar', 'al autobús', 'la habitación doble', 'la habitación individual', 'la recepción', 'el pasajero', 'el billete', 'el horario', 'el vuelvo', 'el aeropuerte', 'el avión', 'el equipaje', 'el hotel', 'la maleta', 'el mapa', 'el pasaporte', 'el viaje', 'viajar', 'la vuelta', 'la sombra', 'nadar', 'la playa', 'bucear', 'el traje', 'el biquini', 'la blusa', 'el monedero', 'el guante', 'el bolso', 'la camisa', 'el sombrero', 'la chaqueta', 'el vestido', 'la corbata', 'el maquillaje', 'el abrigo', 'el perfume', 'el jersey', 'el paraguas', 'los animales', 'los caballos', 'los perros', 'los peces', 'las vacas', 'los alemanes', 'los bolígrafos', 'las botellas', 'las casas', 'las ciudades', 'las coches', 'los cuadernos', 'los hombres', 'los imbéciles', 'los libros', 'las paredes', 'los razones', 'las torres', 'los dientes', 'los manos', 'los padres', 'los hermanos', 'las cebollas', 'las zanahorias', 'los baños', 'las cocinas', 'las cucharas', 'los cuchillos', 'las mesas', 'las sillas', 'los tenedores', 'los vasos', 'las lunas', 'las vacaciones', 'las gafas', 'los pantalones', 'los vaqueros']
german = ['das Tier', 'das Pferd', 'der Hund', 'der Fisch', 'die Kuh', 'auf Wiedersehen', 'der Deutsche', 'willkommen', 'der Kugelschreiber', 'die Flasche', 'gute Nacht', 'guten Tag', 'guten Morgen', 'das Haus', 'die Bürste', 'die Zigarette', 'die Stadt', 'das Auto', 'wie geht es dir', 'das Heft', 'gern geschehen', 'die Leute', 'die Zigeunerin', 'der Zigeuner', 'danke', 'der Krieg', 'bis später', 'bis morgen', 'bis dann', 'hallo', 'der Mann', 'der Idiot', 'das Buch', 'viel Glück', 'vielen Dank', 'sehr erfreut', 'das Mädchen', 'der Junge', 'die Wand', 'viel Spaß', 'bitte', "wie geht's", 'der Grund', 'der Turm', 'der Zahn', 'die Hand', 'gestern', 'der Tag', 'Sonntag', 'heute', 'Donnerstag', 'Montag', 'morgen', 'Dienstag', 'Mittwoch', 'Samstag', 'die Woche', 'Freitag', 'die Oma', 'der Opa', 'lieben', 'die Freundin', 'der Freund', 'küssen', 'die Hochzeit', 'heiraten', 'der Geburtstag', 'die Scheidung', 'die Famillie', 'die Schwester', 'der Bruder', 'die Tochter', 'der Sohn', 'die Mutter', 'der Ehemann', 'die Ehe', 'die Frau', 'die Enkelin', 'der Enkel', 'die Freundin', 'der Freund', 'der Vater', 'mögen', 'ich liebe Dich', 'die Tante', 'der Onkel', 'die Zwiebel', 'die Schokolade', 'die Wurst', 'das Mehl', 'der Wein', 'die Karotte', 'das Bad', 'die Küche', 'der Löffel', 'das Messer', 'der Tisch', 'der Stuhl', 'die Gabel', 'das Glas', 'der Mond', 'vierzehn', 'null', 'hundert', 'fünf', 'fünfzig', 'vierzig', 'vier', 'neunzehn', 'achtzehn', 'sechzehn', 'siebzehn', 'zehn', 'zwölf', 'zwei', 'tausend', 'neunzig', 'neun', 'achtzig', 'acht', 'elf', 'fünfzehn', 'sechs', 'sechzig', 'siebzig', 'sieben', 'dreizehn', 'dreißig', 'drei', 'eins', 'zwanzig', 'wie', 'wann', 'wie viel', 'wo', 'er', 'dick', 'aber', 'warum', 'was', 'wer', 'alles', 'ich', 'trinken', 'wollen', 'arbeiten', 'fliegen', 'das Angebot', 'ausverkauft', 'die Bäckerei', 'die Bank', 'der Betrag', 'die Bezahlung', 'billig', 'der Cent', 'die Drogerie', 'einkaufen', 'der Flohmarkt', 'die Garantie', 'gebraucht', 'das Gehalt', 'das Geld', 'die Kasse', 'das Kleingeld', 'kostenlos', 'der Kunde', 'die Kundin', 'der Abflug', 'die Abreise', 'abreisen', 'ankommen', 'die Ankunft', 'der Aufenthalt', 'der Aussichtspunkt', 'die Badehose', 'baden', 'der Bahnhof', 'der Bahnsteig', 'besuchen', 'der Bus', 'das Doppelzimmer', 'das Einzelzimmer', 'die Rezeption', 'der Fahrgast', 'die Fahrkarte', 'der Fahrplan', 'der Flug', 'der Flughafen', 'das Flugzeug', 'das Gepäck', 'das Hotel', 'der Koffer', 'die Landkarte', 'der Pass', 'die Reise', 'reisen', 'die Rückfahrt', 'der Schatten', 'schwimmen', 'der Strand', 'tauchen', 'der Anzug', 'der Bikini', 'die Bluse', 'der Geldbeutel', 'der Handschuh', 'die Handtasche', 'das Hemd', 'der Hut', 'die Jacke', 'das Kleid', 'die Krawatte', 'das Make-up', 'der Mantel', 'das Parfüm', 'der Pullover', 'der Regenschirm', 'die Tiere', 'die Pferde', 'die Hunde', 'die Fische', 'die Kühe', 'die Deutschen', 'die Kugelschreiber', 'die Flaschen', 'die Häuser', 'die Städte', 'die Autos', 'die Hefte', 'die Männer', 'die Idioten', 'die Bücher', 'die Wände', 'die Gründe', 'die Türme', 'die Zähne', 'die Hände', 'die Eltern', 'die Geschwister', 'die Zwiebeln', 'die Karotten', 'die Bäder', 'die Küchen', 'die Löffel', 'die Messer', 'die Tische', 'die Stühle', 'die Gabeln', 'die Gläser', 'die Monde', 'der Urlaub', 'die Brille', 'die Hose', 'die Jeans']
category = ['ANIMAL', 'ANIMAL', 'ANIMAL', 'ANIMAL', 'ANIMAL', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BODY', 'BODY', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'LIVING', 'LIVING', 'LIVING', 'LIVING', 'LIVING', 'LIVING', 'LIVING', 'LIVING', 'NATURE', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'TBD', 'TBD', 'TBD', 'TBD', 'TBD', 'TBD', 'TBD', 'TBD', 'TBD', 'TBD', 'TBD', 'TBD', 'VERB', 'VERB', 'VERB', 'VERB', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'ANIMAL', 'ANIMAL', 'ANIMAL', 'ANIMAL', 'ANIMAL', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BODY', 'BODY', 'FAMILY', 'FAMILY', 'FOOD', 'FOOD', 'LIVING', 'LIVING', 'LIVING', 'LIVING', 'LIVING', 'LIVING', 'LIVING', 'LIVING', 'NATURE', '', '', '', '']


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
			# worda = WORDS[WORDS["CATEGORY"] == category_var]
			idxs = [i for i, e in enumerate(category) if e == category_var]
			spanish_in_use = [spanish[i] for i in idxs]
			german_in_use = [german[i] for i in idxs]
		else:
			# worda = WORDS.copy()
			spanish_in_use = spanish.copy()
			german_in_use = german.copy()
		global n
		n = random.randint(0, len(idxs) - 1)
		label = self.root.ids.word_in
		# label.text = worda.iloc[n, 1]
		label.text = spanish_in_use[n]
		self.root.in_class.text = ""
		label = self.root.ids.word_out
		label.text = ""

	def check(self):
		# if self.root.in_class.text == WORDS.iloc[n, 0]:
		if self.root.in_class.text == german[n]:
			label = self.root.ids.word_out
			label.text = "[color=238823]Correct =)[/color]"
		else:
			label = self.root.ids.word_out
			label.text = "[color=D2222D]Wrong =([/color]"

	def solve(self):
		label = self.root.ids.word_out
		# label.text = WORDS.iloc[n, 0]
		label.text = german[n]


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
		pass

	def open_link_2(self):
		pass


VocabularyTrainer().run()
