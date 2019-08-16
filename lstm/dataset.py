import numpy as np
import pandas as pd
import re


class TitleDataset:
    def __init__(self,
                 csv_file,
                 max_len=7,
                 step=1):

        self.max_len = max_len
        self.step = step

        self.csv_file = csv_file
        self.titles = self.load_csv_data()
        self.chars = self.build_chars()
        self.sentences, self.next_chars = self.build_dataset()

        self.char2idx = {c: i for i, c in enumerate(self.chars)}
        self.idx2char = {i: c for i, c in enumerate(self.chars)}

    def load_csv_data(self):
        df = pd.read_csv(self.csv_file)

        titles = set()
        for i, d in df.iterrows():
            title = d['title']
            title = re.sub(r'- ローリエプレス.*', '', title)
            titles.add(title.strip() + '\n')
        return list(titles)

    def build_chars(self):
        return sorted(list(set(''.join(list(self.titles)))))

    def build_dataset(self):
        sentences = []
        next_chars = []
        for title in self.titles:
            for i in range(0, len(title) - self.max_len, self.step):
                sentences.append(title[i: i + self.max_len])
                next_chars.append(title[i + self.max_len])
        return sentences, next_chars

    def vectorize(self, sentences):
        x = np.zeros((len(sentences), self.max_len, len(self.chars)), dtype=np.bool)
        y = np.zeros((len(sentences), len(self.chars)), dtype=np.bool)
        for i, sentence in enumerate(sentences):
            for t, char in enumerate(sentence):
                x[i, t, self.char2idx[char]] = 1
            y[i, self.char2idx[self.next_chars[i]]] = 1
        return x, y

    def __len__(self):
        return len(self.sentences)
