import pandas as pd
from tqdm import tqdm

# from io import BytesIO
import requests as rq
from requests.exceptions import SSLError
import os


class Data:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def load(self):

        # read from url
        if "githubusercontent" in self.file_path:

            print("Loading dataset hosted on Github")
            self._save_dataset()

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

    def _save_dataset(self):
        """
        Helper method handling downloading large files from `url` to `filename`. Returns a pointer to `filename`.
        """
        chunkSize = 1024

        try:
            r = rq.get(self.file_path, stream=True)
        except SSLError:  # handle SSL Cerificatte error for self signed certs
            r = rq.get(self.file_path, stream=True, verify=False)

        file_name = self.file_path.split("/")[-1]
        file_path = os.path.join("./dataset/", file_name)

        with open(file_path, "wb") as f:
            pbar = tqdm(
                total=14332536, ascii="░▒█", unit="KB", desc=f"Downloading {file_name}"
            )
            for chunk in r.iter_content(chunk_size=chunkSize):
                if chunk:  # filter out keep-alive new chunks
                    pbar.update(len(chunk))
                    f.write(chunk)

        return file_name
