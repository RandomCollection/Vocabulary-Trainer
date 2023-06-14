# MODULE:       database_initialise.py
# VERSION:      0.4
# DIRECTORY:    <masked>
# DATE:         2023-06-04
# AUTHOR:       RandomCollection
# DESCRIPTION:  See https://github.com/RandomCollection/Vocabulary-Trainer.

# LIBRARIES ############################################################################################################

import os
import pandas as pd
import sqlite3

from projects.vocabulary_trainer import cfg, vocabulary_process


# FUNCTIONS ############################################################################################################

def initialise_database_settings() -> pd.DataFrame:
	return pd.DataFrame(
		data={
			"SETTING_COUNTER_ON": [cfg.SETTING_COUNTER_ON],
			"SETTING_SENSITIVITY": [cfg.SETTING_SENSITIVITY],
			"SETTING_SLEEPER": [cfg.SETTING_SLEEPER],
		},
		index=["VALUE"]
	)


def initialise_database_statistics() -> pd.DataFrame:
	return pd.DataFrame(
		data={
			"STATISTIC_LAST_DATE": [cfg.STATISTIC_LAST_DATE],
			"STATISTIC_STREAK_BEST": [cfg.STATISTIC_STREAK_BEST],
			"STATISTIC_WORDS_TOTAL": [cfg.STATISTIC_WORDS_TOTAL],
		},
		index=["VALUE"]
	)


# MAIN FUNCTION ########################################################################################################

def database_initialise():
	# SETTINGS ---------------------------------------------------------------------------------------------------------

	settings = initialise_database_settings()

	# STATISTICS -------------------------------------------------------------------------------------------------------

	statistics = initialise_database_statistics()

	# VOCABULARY -------------------------------------------------------------------------------------------------------

	vocabulary = (
		pd.read_excel(
			io=os.path.join(cfg.PATH_ROOT, cfg.NAME_VOCABULARY_DIRTY),
			engine="openpyxl",
			keep_default_na=False
		)
		.pipe(vocabulary_process.unstack_vocabulary_singular_plural)
		.pipe(vocabulary_process.unstack_vocabulary_languages)
	)

	# CREATE SQLITE3 DATABASE ------------------------------------------------------------------------------------------

	con = sqlite3.connect(database=os.path.join(cfg.PATH_ROOT, cfg.NAME_DATABASE))
	settings.to_sql(name="SETTINGS", con=con, if_exists="replace", index=False)
	statistics.to_sql(name="STATISTICS", con=con, if_exists="replace", index=False)
	vocabulary.to_sql(name="VOCABULARY", con=con, if_exists="replace", index=False)
	con.commit()
	con.close()


# MAIN #################################################################################################################

if __name__ == "__main__":
	database_initialise()

# END ##################################################################################################################
