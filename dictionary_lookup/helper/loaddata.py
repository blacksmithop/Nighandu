import pandas as pd
from tqdm import tqdm
from io import BytesIO
import requests as rq
from os import environ

environ["PYTHONWARNINGS"] = "ignore:Unverified HTTPS request"


class Data:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def load(self):

        # read from url
        if "githubusercontent" in self.file_path:

            print("Loading dataset hosted on Github")

            data = rq.get(self.file_path).content
            return pd.read_csv(BytesIO(data))

        # read file from disk in chunks
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
