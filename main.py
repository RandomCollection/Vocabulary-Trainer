
import os
# import pandas as pd
import random
import shutil
import webbrowser

from datetime import date, datetime
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import DictProperty, ObjectProperty, StringProperty
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.menu import MDDropdownMenu

if platform == "android":
	from android.permissions import Permission, request_permissions
	from android.storage import primary_external_storage_path
	request_permissions([Permission.INTERNET, Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

# CLASS ################################################################################################################

class VocabularyTrainer(MDApp):
	input = ObjectProperty(defaultvalue=None)
	
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
	
