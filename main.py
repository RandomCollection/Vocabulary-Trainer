# MODULE:       main.py
# VERSION:      1.0
# DIRECTORY:    <masked>
# DATE:         2022-08-21
# AUTHOR:       RandomCollection
# DESCRIPTION:  See https://github.com/RandomCollection/Vocabulary-Trainer.

# LIBRARIES ############################################################################################################

import random
import sqlite3
import webbrowser

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu

if platform == "android":
	from android.permissions import Permission, request_permissions
	request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

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
                    valign: "center"

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
                    markup: True
                    font_style: "H6"
                    halign: "center"
                    pos_hint: {"center_y": 0.75}

                MDTextField:
                    hint_text: "Enter translation here"
                    id: text
                    pos_hint: {"center_x": 0.5, "center_y": 0.65}
                    size_hint_x: None
                    mode: "rectangle"
                    width: 750

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
                    size_hint: None, None
                    width: dp(100) + (self.ids.lbl_txt.texture_size[0] - self.ids.lbl_txt.texture_size[0])
                    on_press: app.check()

                MDFillRoundFlatButton:
                    text: "Next"
                    font_style: "Button"
                    pos_hint: {"center_x": 0.7, "center_y": 0.45}
                    size_hint: None, None
                    width: dp(100) + (self.ids.lbl_txt.texture_size[0] - self.ids.lbl_txt.texture_size[0])
                    on_press: app.next()

                MDFillRoundFlatButton:
                    text: "Solve"
                    font_style: "Button"
                    pos_hint: {"center_x": 0.5, "center_y": 0.3}
                    size_hint: None, None
                    width: dp(100) + (self.ids.lbl_txt.texture_size[0] - self.ids.lbl_txt.texture_size[0])
                    on_press: app.solve()

                MDLabel:
                    text: "All"
                    id: label_category
                    font_style: "Body1"
                    pos_hint: {"center_x": 0.7, "center_y": 0.2}

                MDRaisedButton:
                    text: "Category"
                    id: button_category
                    font_style: "Button"
                    pos_hint: {"center_x": 0.1, "center_y": 0.2}
                    theme_text_color: "Custom"
                    md_bg_color: (100/255,255/255,218/255,1)
                    text_color: (0.1/255,0.1/255,0.1/255,1)
                    size_hint: None, None
                    width: dp(100) + (self.ids.lbl_txt.texture_size[0] - self.ids.lbl_txt.texture_size[0])
                    on_release: app.menu_category.open()

                MDLabel:
                    text: "All"
                    id: label_level
                    font_style: "Body1"
                    pos_hint: {"center_x": 0.7, "center_y": 0.1}

                MDRaisedButton:
                    text: "Level"
                    id: button_level
                    font_style: "Button"
                    pos_hint: {"center_x": 0.1, "center_y": 0.1}
                    theme_text_color: "Custom"
                    md_bg_color: (100/255,255/255,218/255,1)
                    text_color: (0.1/255,0.1/255,0.1/255,1)
                    size_hint: None, None
                    width: dp(100) + (self.ids.lbl_txt.texture_size[0] - self.ids.lbl_txt.texture_size[0])
                    on_release: app.menu_level.open()

                MDFloatingActionButtonSpeedDial:
                    callback: app.language_setting_callback
                    data: app.dict_language_setting
                    root_button_anim: True
                    label_text_color: 1,1,1,1
                    label_bg_color: 100/255,255/255,218/255,1
                    bg_color_stack_button: 100/255,255/255,218/255,1
                    bg_color_root_button: 100/255,255/255,218/255,1
                    color_icon_root_button: 0.1/255,0.1/255,0.1/255,1
                    color_icon_stack_button: 0.1/255,0.1/255,0.1/255,1

            Screen:

                name: "statistics"

                MDLabel:
                    text: app.label_statistics
                    id: statistics
                    font_style: "Body1"
                    markup: True
                    halign: "left"
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
                    size_hint: 0.8, 0.8

                MDFillRoundFlatButton:
                    text: "Reset"
                    font_style: "Button"
                    pos_hint: {"center_x": 0.5, "center_y": 0.15}
                    size_hint: None, None
                    width: dp(100) + (self.ids.lbl_txt.texture_size[0] - self.ids.lbl_txt.texture_size[0])
                    on_press: app.reset()

            Screen:

                name: "how_to"

                MDLabel:
                    text:
                        "\
                        Start the vocabulary trainer by selecting [b]Start[/b] in the menu.\n\n\

                        Click the [b]NEXT[/b] button to start with a new word.\n\n\

                        Click the [b]CHECK[/b] button to verify whether the translation is correct or incorrect.\n\n\

                        The [b]SOLVE[/b] button can be used to show the correct translation.\n\n\

                        Initially, every word is assigned a level of zero. The level of a word increases by one if \
                        it is solved incorrectly and decreases by one if it is solved correctly. The probability of \
                        the words to show up are based on their weights, which are calculated as 'sensitivity ** \
                        level of word'. Hence, the probability of seeing the corresponding word again increases or \
                        decreases exponentially with the number of incorrect or correct translations, respectively. \
                        The sensitivity has a default value of two, but it can be adjusted using the below \
                        [b]SENSITIVITY[/b] button. The levels can be reset by pressing the [b]RESET[/b] button in the \
                        [b]Statistics[/b] section. Depending on the category and level selection of the [b]Start[/b] \
                        screen, it is possible to only reset the levels of a subsection.\n\n\

                        Choose whether you want to translate from Spanish to German or vice versa via the [b]+[/b] \
                        button in the right bottom corner. There is also a random language option available. The \
                        default setting is from Spanish to German.\n\n\

                        Choose whether you want to practise a specific category of words via the [b]CATEGORY[/b] \
                        button. The default setting is [b]All[/b].\n\n\

                        Choose whether you want to practise a specific level of words via the [b]LEVEL[/b] button. \
                        The default setting is [b]All[/b].\
                        "
                    font_style: "Body2"
                    halign: "left"
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
                    markup: True
                    size_hint: 0.8, 0.8

                MDLabel:
                    text: "2"
                    id: label_sensitivity
                    font_style: "Body1"
                    pos_hint: {"center_x": 0.7, "center_y": 0.1}

                MDRaisedButton:
                    text: "Sensitivity"
                    id: button_sensitivity
                    font_style: "Button"
                    pos_hint: {"center_x": 0.1, "center_y": 0.1}
                    theme_text_color: "Custom"
                    md_bg_color: (100/255,255/255,218/255,1)
                    text_color: (0.1/255,0.1/255,0.1/255,1)
                    size_hint: None, None
                    width: dp(100) + (self.ids.lbl_txt.texture_size[0] - self.ids.lbl_txt.texture_size[0])
                    on_release: app.menu_sensitivity.open()

            Screen:

                name: "about"

                MDLabel:
                    text: "This is a [b]RandomCollection[/b] production."
                    font_style: "Body1"
                    markup: True
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

# GLOBAL VARIABLES #####################################################################################################

db = Database()


# FUNCTIONS ############################################################################################################

def calc_statistics() -> str:
	pass


def create_str_from_list(char: list) -> str:
	pass


def language_setting(mode: str) -> (str, str):
	pass


# CLASS ################################################################################################################

class VocabularyTrainer(MDApp):

	in_class = ObjectProperty(None)
	dict_language_setting = DICT_LANGUAGE_SETTING.copy()

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		# Theme
		self.theme_cls.primary_palette = "DeepPurple"
		self.theme_cls.primary_hue = "900"
		self.theme_cls.secondary_palette = "Teal"
		self.theme_cls.secondary_hue = "200"
		self.theme_cls.theme_style = "Light"
		# Builder
		self.screen = Builder.load_string(KV)
		# Variables
		self.language_in = None
		self.language_out = None
		self.language_setting = list(DICT_LANGUAGE_SETTING.keys())[1]
		self.words_in = None
		self.words_out = None
		self.z = None
		self.category_distinct = "k"
		self.level_distinct = "k"
		self.levels_in = None
		self.level_current = None
		self.sensitivity = 2
		# Dropdowns
		self.menu_category = "k"
		self.menu_level = "l"
		self.menu_sensitivity = "l"

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

	def callback_sensitivity(self, instance):
		pass

	def language_setting_callback(self, instance):
		pass

	# SCREEN "STATISTICS" ----------------------------------------------------------------------------------------------

	label_statistics = "s"

	def reset(self):
		pass

	# SCREEN "ABOUT" ---------------------------------------------------------------------------------------------------

	def open_link(self, link: str):
		pass

	# OTHER ------------------------------------------------------------------------------------------------------------

	def update_category(self):
		pass

	def update_level(self):
		pass

	def update_sensitivity(self):
		pass
	# BUILD ------------------------------------------------------------------------------------------------------------

	def build(self):
		return self.screen


VocabularyTrainer().run()
