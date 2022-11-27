# MODULE:       create_database.py
# VERSION:      1.0
# DIRECTORY:    <masked>
# DATE:         2022-11-27
# AUTHOR:       RandomCollection
# DESCRIPTION:  See https://github.com/RandomCollection/Vocabulary-Trainer.

# LIBRARIES ############################################################################################################

import pandas as pd
import sqlite3


# MAIN FUNCTION ########################################################################################################

def create_database():
	# Import vocabulary and transform to pandas DataFrame
	vocabulary = (
		pd.read_excel(io=r"projects\vocabulary-trainer\vocabulary.xlsx", engine="openpyxl", keep_default_na=False)
		.assign(
			ES_SINGULAR=lambda df: df.apply(
				lambda row: f"{row['SPANISH_SINGULAR_ARTICLE']} {row['SPANISH_SINGULAR_WORD']}".strip(), axis=1
			),
			DE_SINGULAR=lambda df: df.apply(
				lambda row: f"{row['GERMAN_SINGULAR_ARTICLE']} {row['GERMAN_SINGULAR_WORD']}".strip(), axis=1
			),
			ES_PLURAL=lambda df: df.apply(
				lambda row: f"{row['SPANISH_PLURAL_ARTICLE']} {row['SPANISH_PLURARL_WORD']}".strip(), axis=1
			),
			DE_PLURAL=lambda df: df.apply(
				lambda row: f"{row['GERMAN_PLURAL_ARTICLE']} {row['GERMAN_PLURAL_WORD']}".strip(), axis=1
			),
		)
		.filter(items=["ES_SINGULAR", "DE_SINGULAR", "ES_PLURAL", "DE_PLURAL", "CATEGORY"])
	)
	vocabulary = (
		pd.concat(
			[
				(
					vocabulary
					.filter(items=["ES_SINGULAR", "DE_SINGULAR", "CATEGORY"])
					.rename(
						columns={
							"ES_SINGULAR": "ES",
							"DE_SINGULAR": "DE",
						}
					)
				),
				(
					vocabulary
					.filter(items=["ES_PLURAL", "DE_PLURAL", "CATEGORY"])
					.rename(
						columns={
							"ES_PLURAL": "ES",
							"DE_PLURAL": "DE",
						}
					)
				)
			]
		)
		.loc[lambda df: df["ES"] != ""]
		.reset_index(drop=True)
	)
	vocabulary = (
		pd.concat(
			[
				(
					vocabulary
					.rename(columns={"ES": "WORD", "DE": "TRANSLATION"})
					.assign(
						LANGUAGE="ES",
						LEVEL=0,
					)
				),
				(
					vocabulary
					.rename(columns={"DE": "WORD", "ES": "TRANSLATION"})
					.assign(
						LANGUAGE="DE",
						LEVEL=0,
					)
				)
			]
		)
	)

	# Create SQLite3 database
	con = sqlite3.connect(database=r"projects\vocabulary-trainer\data.db")
	vocabulary.to_sql(name="vocabulary", con=con, if_exists="append", index=False)
	con.commit()
	con.close()


# MAIN #################################################################################################################

if __name__ == "__main__":
	create_database()

# END ##################################################################################################################
