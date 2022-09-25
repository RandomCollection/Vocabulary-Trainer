# MODULE:       main.py
# VERSION:      1.0
# DIRECTORY:    <masked>
# DATE:         2022-08-21
# AUTHOR:       RandomCollection
# DESCRIPTION:  See https://github.com/RandomCollection/Vocabulary-Trainer.a

# LIBRARIES ############################################################################################################

import random
import webbrowser

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu

from database import Database

KV = r"""
Screen:

    in_class: text

    BoxLayout:

        orientation: "vertical"

        MDToolbar:
            title: "Menu"
            left_action_items: [["menu", lambda x: navigation_drawer.set_state()]]

        Widget:

    MDNavigationLayout:

        ScreenManager:

            id: screen_manager

            Screen:

                name: "home"

                MDLabel:
                    text: "Welcome\n\nto\n\nthe\n\nVocabulary\n\nTrainer!"
                    font_style: "H4"
                    halign: "center"

            Screen:

                name: "start"

                MDLabel:
                    text: "Please translate"
                    font_style: "Body1"
                    halign: "center"
                    pos_hint: {"center_y": 0.85}

                MDLabel:
                    text: ""
                    id: label_word_in
                    font_style: "H6"
                    halign: "center"
                    pos_hint: {"center_y": 0.75}

                MDTextField:
                    hint_text: "Enter translation here"
                    id: text
                    pos_hint: {"center_x": 0.5, "center_y": 0.65}
                    size_hint_x: None
                    mode: "rectangle"
                    width: 700

                MDLabel:
                    text: ""
                    id: label_word_out
                    font_style: "H6"
                    halign: "center"
                    pos_hint: {"center_y": 0.55}
                    markup: True

                MDFillRoundFlatButton:
                    text: "Check"
                    font_style: "Button"
                    pos_hint: {"center_x": 0.3, "center_y": 0.45}
                    theme_icon_color: "Custom"
                    md_bg_color: "#6200EE"
                    on_press: app.check()

                MDFillRoundFlatButton:
                    text: "Next"
                    font_style: "Button"
                    pos_hint: {"center_x": 0.7, "center_y": 0.45}
                    theme_icon_color: "Custom"
                    md_bg_color: "#6200EE"
                    on_press: app.next()

                MDLabel:
                    text: "Category: All"
                    id: label_category
                    font_style: "Body1"
                    pos_hint: {"center_x": 0.55, "center_y": 0.2}

                MDRaisedButton:
                    text: "Category"
                    id: button_category
                    font_style: "Button"
                    pos_hint: {"center_x": 0.1, "center_y": 0.1}
                    md_bg_color: (0, 0.47, 0.42, 1)
                    on_release: app.menu_category.open()

                MDLabel:
                    text: "Level: All"
                    id: label_level
                    font_style: "Body1"
                    pos_hint: {"center_x": 0.75, "center_y": 0.2}

                MDRaisedButton:
                    text: "Level"
                    id: button_level
                    font_style: "Button"
                    pos_hint: {"center_x": 0.3, "center_y": 0.1}
                    md_bg_color: (0, 0.47, 0.42, 1)
                    on_release: app.menu_level.open()

                MDFillRoundFlatButton:
                    text: "Solve"
                    font_style: "Button"
                    pos_hint: {"center_x": 0.5, "center_y": 0.1}
                    theme_icon_color: "Custom"
                    md_bg_color: "#00796B"
                    on_press: app.solve()

                MDFloatingActionButtonSpeedDial:
                    callback: app.language_setting_callback
                    data: app.language_setting_dict
                    root_button_anim: True
                    label_text_color: 1,0,0,1
                    bg_color_stack_button: 1,0,0,1
                    bg_color_root_button: 1,0,0,1
                    color_icon_root_button: 1,0,0,1
                    color_icon_stack_button: 1,0,0,1

            Screen:

                name: "statistics"

                MDLabel:
                    text: app.text_statistics()
                    id: statistics
                    font_style: "Body1"
                    halign: "center"
                    pos_hint: {"center_y": 0.7}

                MDFillRoundFlatButton:
                    text: "Reset"
                    font_style: "Button"
                    pos_hint: {"center_x": 0.7, "center_y": 0.45}
                    on_press: app.reset_level()

            Screen:

                name: "how_to"

                MDLabel:
                    text:
                        "You can choose between categories and whether you want to translate from Spanish to German or\
                        vice versa. The initial probability weight of every word is one and doubles or halves when the\
                        correpsonding word has been solve correctly or incorrectly, respectively."
                    font_style: "Body1"
                    halign: "center"
                    pos_hint: {"center_y": 0.7}

            Screen:

                name: "about"

                MDLabel:
                    text: "This is a RandomCollection production."
                    font_style: "Body1"
                    halign: "center"
                    pos_hint: {"center_y": 0.7}

                MDLabel:
                    text: "For more information, visit"
                    font_style: "Body1"
                    halign: "center"
                    pos_hint: {"center_y": 0.6}

                MDLabel:
                    text: "[ref=randomcollection_github][u]RandomCollection GitHub[/u][/ref]"
                    font_style: "Body1"
                    halign: "center"
                    pos_hint: {"center_y": 0.5}
                    markup: True
                    theme_text_color: "Custom"
                    text_color: 5/255, 99/255, 193/255, 1
                    on_ref_press: app.open_link(link="https://github.com/RandomCollection")

                MDLabel:
                    text: "or"
                    font_style: "Body1"
                    halign: "center"
                    pos_hint: {"center_y": 0.4}

                MDLabel:
                    text: "[ref=randomcollection_github_page][u]RandomCollection GitHub Page[/u][/ref][color=000000].[/color]"
                    font_style: "Body1"
                    halign: "center"
                    pos_hint: {"center_y": 0.3}
                    markup: True
                    theme_text_color: "Custom"
                    text_color: 5/255, 99/255, 193/255, 1
                    on_ref_press: app.open_link(link="https://randomcollection.github.io/")

        MDNavigationDrawer:
            id: navigation_drawer
            orientation: "vertical"
            padding: "12dp", "12dp", "12dp", "0dp"
            spacing: "5dp"

            AnchorLayout:
                anchor_x: "left"
                size_hint_y: None
                height: img.height

                Image:
                    id: img
                    size_hint: None, None
                    size: "56dp", "56dp"
                    source: "img.png"

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
                            navigation_drawer.set_state("close")
                            screen_manager.current = "home"
                        IconLeftWidget:
                            icon: "home"

                    OneLineAvatarListItem:
                        text: "Start"
                        on_press:
                            navigation_drawer.set_state("close")
                            screen_manager.current = "start"
                        IconLeftWidget:
                            icon: "play"

                    OneLineAvatarListItem:
                        text: "Statistics"
                        on_press:
                            navigation_drawer.set_state("close")
                            screen_manager.current = "statistics"
                        IconLeftWidget:
                            icon: "chart-bar"

                    OneLineAvatarListItem:
                        text: "How To"
                        on_press:
                            navigation_drawer.set_state("close")
                            screen_manager.current = "how_to"
                        IconLeftWidget:
                            icon: "chat-question"

                    OneLineAvatarListItem:
                        text: "About"
                        on_press:
                            navigation_drawer.set_state("close")
                            screen_manager.current = "about"
                        IconLeftWidget:
                            icon: "information"
            Widget:
"""

# CONSTANTS ############################################################################################################

DICT_LANGUAGE_SETTING = {
	"Random": "arrow-left-right",
	"ES -> DE": "arrow-right",
	"ES <- DE": "arrow-left",
}

colors = {
	"Purple": {
		"200": "#673AB7",
		"500": "#512DA8",
		"700": "#311B92",
	},
	"Teal": {
		"200": "#009688",
		"500": "#00796B",
		"700": "#004D40",
	},
	"Red": {
		"200": "#C25554",
		"500": "#C25554",
		"A700": "#C25554",
		"700": "#C25554",
	},
	"Light": {
		"StatusBar": "E0E0E0",
		"AppBar": "#202020",
		"Background": "#FFFFFF",
		"CardsDialogs": "#FFFFFF",
		"FlatButtonDown": "#CCCCCC",
	},
}

# GLOBAL VARIABLES #####################################################################################################

db = Database()
# FUNCTIONS ############################################################################################################

def language_setting(mode: str) -> (str, str):
	if mode == list(DICT_LANGUAGE_SETTING.keys())[0]:
		if random.randint(0, 1) == 0:
			return "ES", "DE"
		else:
			return "DE", "ES"
	if mode == list(DICT_LANGUAGE_SETTING.keys())[1]:
		return "ES", "DE"
	if mode == list(DICT_LANGUAGE_SETTING.keys())[2]:
		return "DE", "ES"


# CLASS ################################################################################################################

class VocabularyTrainer(MDApp):
	# TODO: material design
	# TODO: context menu to change sensitivity of level adjustments
	# TODO: close database connection

	# TODO: make a statistics screen with, for example, number of words
	# TODO: So far the levels are changed globally, i.e. if I want to do category xxx it does not start with all level 1
	# TODO: but whatever the levels are
	# TODO: it is important that I press the 'next' button always before the 'check' button
	# con = sqlite3.connect(database=r"projects\vocabulary-trainer\data.db")
	# cursor = con.cursor()
	# con.close()

	in_class = ObjectProperty(None)
	language_setting_dict = DICT_LANGUAGE_SETTING.copy()

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		# Theme configuration
		self.theme_cls.colors = colors
		self.theme_cls.primary_palette = "Purple"
		self.theme_cls.primary_hue = "700"
		self.theme_cls.secondary_palette = "Teal"
		self.theme_cls.secondary_hue = "700"
		self.theme_cls.accent_palette = "Teal"
		self.theme_cls.theme_style = "Light"
		# Builder
		self.screen = Builder.load_string(KV)  # TODO: adjust this when copying to GitHub
		# Variables
		self.n = None
		self.words_in_used = None
		self.words_out_used = None
		self.language_in = None
		self.language_out = None
		self.language_setting_mode = list(DICT_LANGUAGE_SETTING.keys())[1]
		self.category_distinct = "f"
		self.level_current = None
		self.level_distinct = "l"
		# Dropdown menus
		self.menu_category = MDDropdownMenu(
			caller=self.screen.ids.button_category,
			items=[
				{
					"text": f"{category.capitalize()}",
					"viewclass": "OneLineListItem",
					"height": dp(56),
					"on_release": lambda x=f"{category}": self.callback_category(x),
				} for category in ["All"]
			],
			width_mult=3,
			max_height=dp(224),
			background_color=self.theme_cls.primary_light,
		)
		self.menu_level = MDDropdownMenu(
			caller=self.screen.ids.button_level,
			items=[
				{
					"text": f"{level}",
					"viewclass": "OneLineListItem",
					"height": dp(56),
					"on_release": lambda x=f"{level}": self.callback_level(x),
				} for level in ["All"]
			],
			width_mult=3,
			max_height=dp(224),
			background_color=self.theme_cls.primary_light,
		)

	# SCREEN "START" ---------------------------------------------------------------------------------------------------

	def check(self):
		pass
	
	def next(self):
		pass

	def solve(self):
		pass

	def callback_category(self, instance):
		pass

	def callback_level(self, instance):
		pass

	def language_setting_callback(self, instance):
		pass

	# SCREEN "STATISTICS" ----------------------------------------------------------------------------------------------

	def text_statistics(self):
		return "f"

	def reset_level(self):
		pass

	# SCREEN "ABOUT" ---------------------------------------------------------------------------------------------------

	def open_link(self, link: str):
		webbrowser.open(url=link)

	# BUILD ------------------------------------------------------------------------------------------------------------

	def build(self):
		return self.screen


VocabularyTrainer().run()
