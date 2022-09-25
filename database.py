# MODULE:       database.py
# VERSION:      1.0
# DIRECTORY:    <masked>
# DATE:         2022-08-21
# AUTHOR:       RandomCollection
# DESCRIPTION:  See https://github.com/RandomCollection/Vocabulary-Trainer.

# LIBRARIES ############################################################################################################

import sqlite3


# MAIN FUNCTION ########################################################################################################

class Database:
	def __init__(self):
		self.con = sqlite3.connect(database=r".\data.db")
		self.cursor = self.con.cursor()

	def close_connection(self):
		self.con.close()

	def decrease_level(self, level: int, word: str):
		self.cursor.execute(
			f"""
			UPDATE VOCABULARY
			SET
				LEVEL = {level - 1}
			WHERE WORD == '{word}'
			"""
		)
		self.con.commit()

	def get_distinct_categories(self) -> list:
		categories = (
			self.cursor.execute(
				"""
				SELECT DISTINCT
					CATEGORY
				FROM VOCABULARY
				ORDER BY CATEGORY
				"""
			)
			.fetchall()
		)
		return [category[0] for category in categories]

	def get_distinct_levels(self) -> list:
		levels = (
			self.cursor.execute(
				"""
				SELECT DISTINCT
					LEVEL
				FROM VOCABULARY
				ORDER BY LEVEL
				"""
			)
			.fetchall()
		)
		return [str(level[0]) for level in levels]

	def get_level(self, word: str) -> int:
		return (
			self.cursor.execute(
				f"""
				SELECT
					LEVEL
				FROM VOCABULARY
				WHERE WORD == '{word}'
				"""
			)
			.fetchall()[0][0]
		)

	def get_number_of_words(self, language: str) -> int:
		return (
			self.cursor.execute(
				f"""
				SELECT
					COUNT(WORD) AS CNT
				FROM VOCABULARY
				WHERE LANGUAGE == '{language}'
				"""
			)
			.fetchall()[0][0]
		)

	def get_words(self, language: str, category: str, level: str) -> list:
		words = (
			self.cursor.execute(
				f"""
				SELECT
					WORD
				FROM VOCABULARY
				WHERE LANGUAGE == '{language}'
				AND CATEGORY IN {category}
				AND LEVEL IN {level}
				"""
			)
			.fetchall()
		)
		return [word for word in words]

	def get_words_and_levels(self, words: str) -> (list, list):
		words_and_levels = (
			self.cursor.execute(
				f"""
				SELECT
					WORD,
					LEVEL
				FROM VOCABULARY
				WHERE WORD IN {words}
				"""
			)
			.fetchall()
		)
		return [word[0] for word in words_and_levels], [level[1] for level in words_and_levels]

	def get_words_by_language(self, language: str) -> list:
		return (
			self.cursor.execute(
				f"""
				SELECT
					WORD
				FROM VOCABULARY
				WHERE LANGUAGE == '{language}'
				"""
			)
			.fetchall()
		)

	def get_words_by_language_and_category(self, language: str, category: str) -> list:
		return (
			self.cursor.execute(
				f"""
				SELECT
					WORD
				FROM VOCABULARY
				WHERE LANGUAGE == '{language}'
				AND CATEGORY == {category}
				"""
			)
			.fetchall()
		)

	def increase_level(self, level: int, word: str):
		self.cursor.execute(
			f"""
			UPDATE VOCABULARY
			SET
				LEVEL = {level + 1}
			WHERE WORD == '{word}'
			"""
		)
		self.con.commit()

	def reset_level(self):
		self.cursor.execute(
			f"""
			UPDATE VOCABULARY
			SET
				LEVEL = 0
			"""
		)
		self.con.commit()
