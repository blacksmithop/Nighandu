from dataclasses import dataclass
from pprint import pprint
from collections import Counter
from .clean import ProcessText


@dataclass
class Definition:
    id: int
    english_word: str
    part_of_speech: str
    malayalam_definition: str

    @property
    def dict(self):
        pprint(self.__dict__)

    def analyze(self):
        pre_process = ProcessText()
        pre_process.text = self.english_word

        tokens = pre_process.clean_and_stem()
        self.term_frequencies = Counter(tokens)

    def term_frequency(self, term):
        return self.term_frequencies.get(term, 0)

if __name__ == "__main__":
    word_def = Definition(113885, "A bird in a golden cage", "n", "സുഖകരമെങ്കിലും സ്വാതന്ത്യ്രമില്ലാത്ത അവസ്ഥ")
    word_def.dict