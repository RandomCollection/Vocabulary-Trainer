# MODULE:       cfg.py
# VERSION:      0.3
# DIRECTORY:    <masked>
# DATE:         2023-02-26
# AUTHOR:       RandomCollection
# DESCRIPTION:  See https://github.com/RandomCollection/Vocabulary-Trainer.

# CONSTANTS ############################################################################################################

# DICTIONARIES ---------------------------------------------------------------------------------------------------------

DICT_LANGUAGE = {
	"Random": "arrow-left-right",
	"ES -> DE": "arrow-right",
	"ES <- DE": "arrow-left",
}

DICT_TEXT = {
	"HOME": "Welcome\n\nto the\n\nVocabulary Trainer!",
	"HOME_INITIAL": "\n\nHappy Learning!",
	"HOME_DAY_0": "\n\n[color=238823]Nice that you are back again today![/color]",
	"HOME_DAY_1": "\n\n[color=238823]Nice to see you again after\n\n{0}\n\nday![/color]",
	"HOME_DAY_>7": (
		"\n\n[color=D2222D]You need to come back more often.\n\nYour last visit was\n\n{0}\n\ndays ago![/color]"
	),
	"HOME_DAY_ELSE": "\n\n[color=238823]Nice to see you again after\n\n{0}\n\ndays![/color]",
	"NO_WORDS": "There are no more words with the current configuration. Back to [i]All[/i] and [i]ES -> DE[/i]."
}

# LABELS ---------------------------------------------------------------------------------------------------------------

LABEL_BUTTON_CHECK = "CHECK"
LABEL_ENTER_TRANSLATION = "Please enter a translation into the text field"
LABEL_EXPORT_0 = "Export not successful! Error:\n'{e}'"
LABEL_EXPORT_1 = "Export successful!"
LABEL_IMPORT_0 = "Import not successful! Error:\n'{e}'"
LABEL_IMPORT_1 = "Import successful!"
LABEL_HOW_TO = """\
Start the vocabulary trainer by selecting [b]Start[/b] in the menu.\n\n\
Press the [b]START[/b] button to start with a new word.\n\n\
Press the [b]CHECK[/b] button to verify whether the translation is correct.\n\n\
The [b]SOLVE[/b] button can be used to show the correct translation.\n\n\
Choose whether you want to translate from Spanish to German or vice versa via the [b]+[/b] button in the right bottom \
corner. There is also a random language option available. The default setting is from Spanish to German. Choose \
whether you want to practise a specific category of words via the [b]CATEGORY[/b] button. The default setting is \
[b]All[/b].\n\n\
Choose whether you want to practise a specific level of words via the [b]LEVEL[/b] button. The default setting is \
[b]All[/b].\n\n\
Initially, every word is assigned a level of zero. The level of a word decreases by one if it is solved incorrectly \
and increases by one if it is solved correctly. The probability of the words to show up are based on their weights, \
which are calculated as [b]sensitivity ** ((-1) * level of word)[/b]. Hence, the probability of seeing the \
corresponding word again decreases or increases exponentially with the number of correct or incorrect translations, \
respectively. The sensitivity has a default value of 10, but it can be adjusted using the [b]SENSITIVITY[/b] button in \
the [b]Settings[/b] section.\n\n\
The levels can be reset by pressing the [b]RESET[/b] button in the [b]Statistics[/b] section. Depending on the \
category and level selection of the [b]Start[/b] screen, it is possible to only reset the levels of a subsection.\
"""
LABEL_RESET = "Reset successful!"
LABEL_SETTINGS = "tbd"
LABEL_SOLUTION_CORRECT = "[color=238823]Correct =)[/color]"
LABEL_SOLUTION_INCORRECT = "[color=D2222D]Incorrect =([/color]"
LABEL_START = "Please click the [i]START[/i] button to start"
LABEL_TEXT = "Enter translation here"
LABEL_TRANSLATE = "Please translate"
LABEL_UPDATE = """\
In order to update the underlying vocabulary list, the database [b]data.db[/b] can be exported by pressing the \
[b]EXPORT[/b] button. The file will be stored in the Android [b]Download[/b] folder from which it can be further \
adjusted. Currently, this feature requires manual steps which can only be executed by RandomCollection. An updated \
version of the vocabulary list can then be imported py pressing the [b]IMPORT[/b] button. The updated [b]data.db[/b] \
file is currently retrieved from GitHub.\
"""
LABEL_WORD_IN = "Please click the [i]START[/i] button to start"

# NAMES ----------------------------------------------------------------------------------------------------------------

NAME_DATABASE = r"data.db"
NAME_DATABASE_OLD = r"old.db"
NAME_VOCABULARY_DIRTY = r"vocabulary.xlsx"
NAME_VOCABULARY_CLEAN = r"vocabulary_clean.xlsx"

# PATHS ----------------------------------------------------------------------------------------------------------------

PATH_ROOT = r"projects\vocabulary_trainer"

# SETTINGS -------------------------------------------------------------------------------------------------------------

SETTING_COUNTER_ON = 1
SETTING_COUNTER_ON_VALUES = ["On", "Off"]
SETTING_SENSITIVITY = 10
SETTING_SENSITIVITY_VALUES = [1, 2, 10, 50, 250]
SETTING_SLEEPER = 1
SETTING_SLEEPER_VALUES = [0, 1, 2, 5]

# STATISTICS -----------------------------------------------------------------------------------------------------------

STATISTIC_LAST_DATE = ""
STATISTIC_STREAK_BEST = 0
STATISTIC_WORDS_TOTAL = 0

# URLS -----------------------------------------------------------------------------------------------------------------

URL_DATABASE = r"http://raw.github.com/RandomCollection/Vocabulary-Trainer/main/data.db"

# END ##################################################################################################################
