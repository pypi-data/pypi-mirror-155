from pathlib import Path
from typing import List
from typing import Union

import logging
import pandas as pd  # noqa


logger = logging.getLogger(__name__)


class PdReadFlexibleCsv:
    def __init__(
        self,
        path: Union[str, Path],
        sep: str = None,
        expected_columns: List[str] = None,
        parse_dates: List[str] = False,
        source_is_github: bool = False,
    ):
        self.source_is_github = source_is_github
        self.path_str = self._get_path(path=path)
        self.date_columns = parse_dates
        self.separators = self._get_separators(sep=sep)
        self.expected_columns = expected_columns
        self.df = self._get_df()

    def _get_path(self, path: Union[str, Path]) -> str:
        if self.source_is_github:
            return str(path)
        if isinstance(path, Path):
            assert path.exists(), f"path {path} is not a file"
            return path.as_posix()
        assert isinstance(path, str)
        assert "http" in path, f"if path {path} not a pathlib.Path, then it must be an url"
        return path

    def _get_separators(self, sep: str = None) -> List[str]:
        if sep:
            assert isinstance(sep, str), f"sep {sep} must be of type string"
            return [sep]
        if self.date_columns:
            return [None, ";"]
        return [",", ";"]

    @staticmethod
    def _trim_all_string_columns(df):
        """Trim whitespace from ends of each value across all series in dataframe."""
        return df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    def _get_df(self) -> pd.DataFrame:
        for separator in self.separators:
            df = self._csv_to_df(separator=separator)
            if df.empty:
                continue
            if len(df.columns) == 1:
                continue
            if self.expected_columns:
                for expected_column in self.expected_columns:
                    assert (
                        expected_column in df.columns
                    ), f"expected_column {expected_column} must be in {df.columns}, file={self.path_str}"
            df = self._trim_all_string_columns(df=df)
            return df
        # raise since no success
        raise AssertionError(
            f"could not read csv {self.path_str} with separators={self.separators}, "
            f"expected columns={self.expected_columns}"
        )

    def _csv_to_df(self, separator: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(
                filepath_or_buffer=self.path_str, sep=separator, engine="python", parse_dates=self.date_columns
            )
            return df
        except pd.errors.ParserError:
            logger.debug(f"could not open csv {self.path_str} with separator {separator}")
        return pd.DataFrame(data=None)
