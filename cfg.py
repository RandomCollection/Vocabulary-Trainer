# MODULE:       cfg.py
# VERSION:      0.4
# DIRECTORY:    <masked>
# DATE:         2023-06-04
# AUTHOR:       RandomCollection
# DESCRIPTION:  See https://github.com/RandomCollection/Vocabulary-Trainer.

# CONSTANTS ############################################################################################################

# URLS -----------------------------------------------------------------------------------------------------------------

URL_DATABASE = r"https://github.com/RandomCollection/Vocabulary-Trainer/blob/main/vocabulary.xlsx?raw=true"
URL_GITHUB = r"https://github.com/RandomCollection/Vocabulary-Trainer"
URL_GITHUB_PAGE = r"https://randomcollection.github.io"

# DICTIONARIES ---------------------------------------------------------------------------------------------------------

DICT_LANGUAGE = {
	"Random": "arrow-left-right",
	"ES -> DE": "arrow-right",
	"ES <- DE": "arrow-left",
}

# LABELS ---------------------------------------------------------------------------------------------------------------

LABEL_ABOUT = f"""\
This is a [b]RandomCollection[/b] production.\n\n
For more information, visit\n\n
[ref={URL_GITHUB}][color=0563c1][u]RandomCollection GitHub[/u][/color][/ref]\n\n
or\n\n
[ref={URL_GITHUB_PAGE}][color=0563c1][u]RandomCollection GitHub Page[/u][/color][/ref].\
"""
LABEL_BUTTON_CHECK = "CHECK"
LABEL_COUNTER_STREAK_BEST = "Streak Best:"
LABEL_COUNTER_STREAK_CURRENT = "Streak:"
LABEL_COUNTER_WORDS_CURRENT = "Words:"
LABEL_COUNTER_WORDS_TOTAL = "Words Total:"
LABEL_ENTER_TRANSLATION = "Please enter a translation into the text field"
LABEL_EXPORT_START = "Export has started, please wait..."
LABEL_EXPORT_0 = "Export not successful!\n'{e}'"
LABEL_EXPORT_1 = "Export successful!"
LABEL_IMPORT_START = "Import has started, please wait..."
LABEL_IMPORT_0 = "Import not successful!\n'{e}'"
LABEL_IMPORT_1 = "Import successful!"
LABEL_HOME = {
	"HOME": "Welcome\n\nto the\n\n[b]Vocabulary Trainer[/b]!\n\n",
	"HOME_INITIAL": "\n\nHappy Learning!",
	"HOME_DAY_0": "\n\n[color=238823]Nice you are back again today![/color]",
	"HOME_DAY_1": "\n\n[color=238823]Nice to see you again after\n\n{days}\n\nday![/color]",
	"HOME_DAY_>7": "\n\n[color=D2222D]Come back more often.\n\nYour last visit was\n\n{days}\n\ndays ago![/color]",
	"HOME_DAY_ELSE": "\n\n[color=238823]Nice to see you again after\n\n{days}\n\ndays![/color]",
}
LABEL_HOW_TO = """\
Start the [b]Vocabulary Trainer[/b] by selecting [b]Start[/b] in the menu.\n
Press the [b]START[/b] button to start with a new word.\n
Press the [b]CHECK[/b] button to verify whether the translation is correct.\n
The [b]SOLVE[/b] button can be used to show the correct translation.\n
Choose whether you want to translate from Spanish to German or vice versa via the [b]+[/b] button in the right bottom \
corner. There is also a random language option available. The default setting is from Spanish to German.\n
Choose whether you want to practise a specific category of words via the [b]CATEGORY[/b] button. The default setting \
is [b]All[/b].\n
Choose whether you want to practise a specific level of words via the [b]LEVEL[/b] button. The default setting is \
[b]All[/b].\n
The levels can be reset by pressing the [b]RESET[/b] button in the [b]Statistics[/b] section. Depending on the \
category and level selection of the [b]Start[/b] screen, it is possible to only reset the levels of a subsection.\n
The [b]Settings[/b] section can be used to adjust several settings.\
"""
LABEL_NO_WORDS = "There are no more words with the current configuration. Back to [i]All[/i] and [i]ES -> DE[/i]."
LABEL_RESET = "Reset successful!"
LABEL_SETTINGS = """\
[b]SENSITIVITY[/b] - Initially, every word is assigned a level of zero. The level of a word decreases by one if it is \
solved incorrectly and increases by one if it is solved correctly. The probability of the words to show up are based \
on their weights, which are calculated as [b]sensitivity ** ((-1) * level of word)[/b]. Hence, the probability of \
seeing the corresponding word again decreases or increases exponentially with the number of correct or incorrect \
translations, respectively. The sensitivity has a default value of 10, but it can be adjusted via the \
[b]SENSITIVITY[/b] button.\n
[b]SLEEPER[/b] - The [b]SLEEPER[/b] button can be used to adjust the time it takes for a new word to appear in case \
the current word has been solved correctly.\n
[b]COUNTERS[/b] - Counters can be set [b]On[/b] or [b]Off[/b] to be displayed on the [b]Start[/b] screen. They can be \
reset by pressing the [b]RESET[/b] button.\
"""
LABEL_SOLUTION_CORRECT = "[color=238823]Correct =)[/color]"
LABEL_SOLUTION_INCORRECT = "[color=D2222D]Incorrect =([/color]"
LABEL_START = "Please click the [i]START[/i] button to start"
LABEL_STATISTICS = """\
The vocabulary trainer contains [b]{words} {words_adj}[/b] and [b]{categories} {categories_adj}[/b].\n
The table below gives an overview about the currently existing [b]levels[/b] and corresponding [b]number of words[/b] \
within. Please note that every word appears twice - once for the Spanish to German translation and once for the German \
to Spanish translation.\
"""
LABEL_TEXT = "Enter translation here"
LABEL_TRANSLATE = "Please translate"
LABEL_UPDATE = """\
In order to update the underlying vocabulary list, the [b]IMPORT[/b] button can be pressed, which downloads an updated \
vocabulary list from the corresponding [b]RandomCollection[/b] GitHub repository.\n
The underlying database [b]data.db[/b] of the [b]Vocabulary Trainer[/b] can be exported by pressing the [b]EXPORT[/b] \
button. The database will be stored in the Android [b]Download[/b] folder from which it can be further processed.\
"""

# NAMES ----------------------------------------------------------------------------------------------------------------

NAME_DATABASE = r"data.db"
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

# END ##################################################################################################################
