from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.app import MDApp


KV = r"""
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
                    pos_hint: {"center_y": 0.4}
                    font_style: "Body1"

                MDFillRoundFlatButton:
                    text: "Next"
                    pos_hint: {"center_x": 0.3, "center_y": 0.2}
                    font_style: "Button"

                MDFillRoundFlatButton:
                    text: "Check"
                    pos_hint: {"center_x": 0.7, "center_y": 0.2}
                    font_style: "Button"

                MDFillRoundFlatButton:
                    text: "Solve"
                    pos_hint: {"center_x": 0.5, "center_y": 0.1}
                    font_style: "Button"
                    md_bg_color: app.theme_cls.primary_light

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


class MainApp(MDApp):

	in_class = ObjectProperty(None)

	def build(self):
		self.theme_cls.primary_palette = "Teal"
		self.theme_cls.primary_hue = "700"
		self.theme_cls.theme_style = "Light"
		return Builder.load_string(KV)


MainApp().run()
