from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.utils import platform
from kivymd.app import MDApp

if platform == "android":
	from android.permissions import Permission, request_permissions
	request_permissions([Permission.INTERNET, Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])


# CLASS ################################################################################################################

class VocabularyTrainer(MDApp):
	input = ObjectProperty(defaultvalue="")
	label_home = StringProperty(defaultvalue="")
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		# Theme
		self.theme_cls.primary_palette = "DeepPurple"
		self.theme_cls.primary_hue = "900"
		self.theme_cls.secondary_palette = "Teal"
		self.theme_cls.secondary_hue = "200"
		self.theme_cls.theme_style = "Light"
		# Builder
		self.screen = Builder.load_file("main.kv")
		# Variables
		self.label_home = "hi"

	# BUILD ------------------------------------------------------------------------------------------------------------

	def build(self):
		return self.screen


# MAIN #################################################################################################################

if __name__ == '__main__':
	VocabularyTrainer().run()
	
