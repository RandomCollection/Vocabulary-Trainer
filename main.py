import random

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.app import MDApp

kv = r"""
Screen:

    in_class: text

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
                    pos_hint: {"center_x": 0.8, "center_y": 0.8}

                MDTextField:
                    id: text
                    hint_text: "Enter translation here"
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
                    size_hint_x: None
                    mode: "rectangle"
                    width: 200

                MDFillRoundFlatButton:
                    text: "Next"
                    font_style: "Button"
                    pos_hint: {"center_x": 0.3, "center_y": 0.2}
                    on_press:
                        app.next()

                MDFillRoundFlatButton:
                    text: "Check"
                    font_style: "Button"
                    pos_hint: {"center_x": 0.7, "center_y": 0.2}
                    on_press:
                        app.check()

                MDLabel:
                    text: ""
                    id: word_in
                    pos_hint: {"center_x": 0.9, "center_y": 0.7}

                MDLabel:
                    text: ""
                    id: word_out
                    pos_hint: {"center_x": 0.9, "center_y": 0.4}

            Screen:

                name: "screen_3"

                MDLabel:
                    text: "This is a RandomCollection production.\nFor more information check out\nRandomCollection.github.io"
                    font_style: "Body2"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 0, 0, 0, 1

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
                text: "RandomCollection.github.io"
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

spanish = ['trabajar', 'todo', 'querer', 'volar', 'beber', 'gordo', 'yo', 'el perro', 'la gente', 'el cigarrillo', 'pero', 'el vaso', 'la vaca', 'el cuchillo', 'la luna', 'el bolígrafo', 'él', 'el chocolate', 'el chorizo', 'el vino', 'la harina']
german = ['arbeiten', 'alles', 'wollen', 'fliegen', 'trinken', 'dick', 'ich', 'der Hund', 'die Leute', 'die Zigarette', 'aber', 'das Glas', 'die Kuh', 'das Messer', 'der Mond', 'der Kugelschreiber', 'er ', 'die Schokolade', 'die Wurst', 'der Wein', 'das Mehl']


class MainApp(MDApp):

	in_class = ObjectProperty(None)

	def build(self):
		Window.size = [300, 600]
		return Builder.load_string(kv)

	def next(self):
		global n
		n = random.randint(0, len(spanish))
		label = self.root.ids.word_in
		label.text = german[n]

	def check(self):
		if self.root.in_class.text == spanish[n]:
			label = self.root.ids.word_out
			label.text = "True"
		else:
			label = self.root.ids.word_out
			label.text = "False"


MainApp().run()
