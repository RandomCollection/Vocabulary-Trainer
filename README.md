# Vocabulary Trainer

<p align="center">
<video src="vocabulary_trainer.mp4 width="200">
</p>

<p align="center">
<img src="vocabulary_trainer.gif" width="200">
</p>

- Start the vocabulary trainer by selecting **Start** in the menu.

- Press the **NEXT** button to start with a new word.

- Press the **CHECK** button to verify whether the translation is correct.

- The **SOLVE** button can be used to show the correct translation.

- Choose whether you want to translate from Spanish to German or vice versa via the **+** button in the right bottom corner. There is also a random language option available. The default setting is from Spanish to German.

- Choose whether you want to practise a specific category of words via the **CATEGORY** button. The default setting is **All**.

- Choose whether you want to practise a specific level of words via the **LEVEL** button. The default setting is **All**.

- Initially, every word is assigned a level of zero. The level of a word decreases by one if it is solved incorrectly and increases by one if it is solved correctly. The probability of the words to show up are based on their weights, which are calculated as **sensitivity \*\* ((-1) * level of word)**. Hence, the probability of seeing the corresponding word again decreases or increases exponentially with the number of correct or incorrect translations, respectively. The sensitivity has a default value of 2, but it can be adjusted using the below **SENSITIVITY** button.

- The levels can be reset by pressing the **RESET** button in the **Statistics** section. Depending on the category and level selection of the **Start** screen, it is
possible to only reset the levels of a subsection.

## License

[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)
