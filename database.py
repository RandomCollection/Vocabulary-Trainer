# MODULE:       database.py
# VERSION:      1.0
# DIRECTORY:    <masked>
# DATE:         2023-02-26
# AUTHOR:       RandomCollection
# DESCRIPTION:  See https://github.com/RandomCollection/Vocabulary-Trainer.

# LIBRARIES ############################################################################################################

import sqlite3


# MAIN FUNCTION ########################################################################################################

class Database:
	def __init__(self):
		self.con = sqlite3.connect(database=r".\data.db")  # TODO: r"data.db"
		self.cursor = self.con.cursor()

	def get_count_of_words_per_level(self) -> list:
		return (
			self.cursor.execute(
				"""
				SELECT
					LEVEL,
					COUNT(WORD) AS CNT
				FROM VOCABULARY
				GROUP BY LEVEL
				ORDER BY LEVEL
				"""
			)
			.fetchall()
		)

	def get_data(self, language: str, category: str, level: str) -> (list, list, list):
		data = (
			self.cursor.execute(
				f"""
				SELECT
					WORD,
					TRANSLATION,
					LEVEL
				FROM VOCABULARY
				WHERE LANGUAGE == '{language}'
				AND CATEGORY IN {category}
				AND LEVEL IN {level}
				"""
			)
			.fetchall()
		)
		return [word[0] for word in data], [translation[1] for translation in data], [level[2] for level in data]

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

	def get_distinct_categories(self, level: str) -> list:
		categories = (
			self.cursor.execute(
				f"""
				SELECT DISTINCT
					CATEGORY
				FROM VOCABULARY
				WHERE LEVEL IN {level}
				ORDER BY CATEGORY
				"""
			)
			.fetchall()
		)
		return [category[0] for category in categories]

	def get_distinct_categories_all(self) -> list:
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

	def get_distinct_levels(self, category: str) -> list:
		levels = (
			self.cursor.execute(
				f"""
				SELECT DISTINCT
					LEVEL
				FROM VOCABULARY
				WHERE CATEGORY IN {category}
				ORDER BY LEVEL
				"""
			)
			.fetchall()
		)
		return [str(level[0]) for level in levels]

	def get_distinct_levels_all(self) -> list:
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

	def reset(self, category: str, level: str):
		self.cursor.execute(
			f"""
			UPDATE VOCABULARY
			SET
				LEVEL = 0
			WHERE CATEGORY IN {category}
			AND LEVEL IN {level}
			"""
		)
		self.con.commit()
