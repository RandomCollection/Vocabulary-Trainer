# Vocabulary Trainer

<img src="vocabulary_trainer.gif" width="200">

Start the vocabulary trainer by selecting [b]Start[/b] in the menu.\n\n\

Press the [b]NEXT[/b] button to start with a new word.\n\n\

Press the [b]CHECK[/b] button to verify whether the translation is correct.\n\n\

The [b]SOLVE[/b] button can be used to show the correct translation.\n\n\

Choose whether you want to translate from Spanish to German or vice versa via the [b]+[/b] \
button in the right bottom corner. There is also a random language option available. The \
default setting is from Spanish to German.\n\n\

Choose whether you want to practise a specific category of words via the [b]CATEGORY[/b] \
button. The default setting is [b]All[/b].\n\n\

Choose whether you want to practise a specific level of words via the [b]LEVEL[/b] button. \
The default setting is [b]All[/b].\n\n\

Initially, every word is assigned a level of zero. The level of a word decreases by one if \
it is solved incorrectly and increases by one if it is solved correctly. The probability \
of the words to show up are based on their weights, which are calculated as [b]sensitivity \
** ((-1) * level of word)[/b]. Hence, the probability of seeing the corresponding word again \
decreases or increases exponentially with the number of correct or incorrect translations, \
respectively. The sensitivity has a default value of 2, but it can be adjusted using the \
below [b]SENSITIVITY[/b] button.\n\n\

The levels can be reset by pressing the [b]RESET[/b] button in the [b]Statistics[/b] \
section. Depending on the category and level selection of the [b]Start[/b] screen, it is \
possible to only reset the levels of a subsection.\

## License

[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)
