# MODULE:       vocabulary_process.py
# VERSION:      0.4
# DIRECTORY:    <masked>
# DATE:         2023-06-04
# AUTHOR:       RandomCollection
# DESCRIPTION:  See https://github.com/RandomCollection/Vocabulary-Trainer.

# LIBRARIES ############################################################################################################

import os
import pandas as pd

from projects.vocabulary_trainer import cfg


# FUNCTIONS ############################################################################################################

def unstack_vocabulary_languages(df: pd.DataFrame) -> pd.DataFrame:
	_df = (
		pd.concat(
			[
				(
					df
					.filter(items=["ID_ES", "WORD_DE", "CATEGORY"])
					.rename(columns={"ID_ES": "WORD", "WORD_DE": "TRANSLATION"})
					.assign(
						LANGUAGE="ES",
						LEVEL=0,
					)
				),
				(
					df
					.filter(items=["ID_DE", "WORD_ES", "CATEGORY"])
					.rename(columns={"ID_DE": "WORD", "WORD_ES": "TRANSLATION"})
					.assign(
						LANGUAGE="DE",
						LEVEL=0
					)
				)
			]
		)
		.reset_index(drop=True)
	)
	return _df


def unstack_vocabulary_singular_plural(df: pd.DataFrame) -> pd.DataFrame:
	cols_sin = [col for col in df.columns if "SINGULAR" in col]
	cols_plu = [col for col in df.columns if "PLURAL" in col]
	cols = [col.split("_", 1)[-1] for col in cols_sin]
	_df = (
		pd.concat(
			[
				(
					df
					.filter(items=cols_sin + ["CATEGORY"])
					.rename(columns=dict(zip(cols_sin, cols)))
				),
				(
					df
					.filter(items=cols_plu + ["CATEGORY"])
					.rename(columns=dict(zip(cols_plu, cols)))
				)
			]
		)
		.sort_values(by=["CATEGORY", "ID_ES"])
		.filter(items=["ID_ES", "ID_DE", "WORD_ES", "WORD_DE", "CATEGORY"])
		.loc[lambda _df: _df["ID_ES"] != ""]
		.reset_index(drop=True)
	)
	return _df


# MAIN FUNCTION ########################################################################################################

def vocabulary_process():
	(
		pd.read_excel(
			io=os.path.join(cfg.PATH_ROOT, cfg.NAME_VOCABULARY_DIRTY),
			engine="openpyxl",
			keep_default_na=False
		)
		.pipe(unstack_vocabulary_singular_plural)
		.pipe(unstack_vocabulary_languages)
		.to_excel(excel_writer=os.path.join(cfg.PATH_ROOT, cfg.NAME_VOCABULARY_CLEAN), index=False)
	)


# MAIN #################################################################################################################

if __name__ == "__main__":
	vocabulary_process()

# END ##################################################################################################################
