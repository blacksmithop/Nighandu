import pandas as pd
from tqdm import tqdm


class Data:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def load(self):
        return pd.concat(
            [
                chunk
                for chunk in tqdm(
                    pd.read_csv(self.file_path, chunksize=1000),
                    desc="Loading dataset",
                    total=218,
                    ascii="░▒█",
                )
            ]
        )
