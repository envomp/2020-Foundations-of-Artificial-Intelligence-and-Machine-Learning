import os
import math
import re


class NativeBayesianModel:

    def __init__(self):
        self.ham_l = self.read_dir(os.path.join("enron6", "ham"))  # list mitte spam sõnadest
        self.spam_l = self.read_dir(os.path.join("enron6", "spam"))  # list spam sõnadest

        self.ham_l_repetitions = dict()  # mitte spam sõnade kordus
        self.spam_l_repetitions = dict()  # spam sõnade kordus

        for text in self.ham_l:
            for word in text:
                if self.ham_l_repetitions.get(word) is not None:
                    self.ham_l_repetitions[word] += 1
                else:
                    self.ham_l_repetitions[word] = 1

        for text in self.spam_l:
            for word in text:
                if self.spam_l_repetitions.get(word) is not None:
                    self.spam_l_repetitions[word] += 1
                else:
                    self.spam_l_repetitions[word] = 1

        self.ham_l_repetitions_keyset_size = len(self.ham_l_repetitions.keys())  # unikaalsed nmitte spam sõnad
        self.spam_l_repetitions_keyset_size = len(self.spam_l_repetitions.keys())  # unikaalsed spam sõnad

        self.total_l_repetitions_keyset = self.ham_l_repetitions.keys() | self.spam_l_repetitions.keys()  # unikaalsed sõnad
        self.total_l_repetitions_keyset_size = len(self.total_l_repetitions_keyset)  # unikaalsed sõnade arv

        self.ham_l_len = len(self.ham_l)  # Mitte spam'is olevate sõnade arv
        self.spam_l_len = len(self.spam_l)  # Spam'is olevate sõnade arv
        self.total_1_len = self.spam_l_len + self.ham_l_len  # Kõikide sõnade arv

        self.P_spam = len(self.spam_l) / self.total_1_len
        self.P_ham = len(self.ham_l) / self.total_1_len

    def read_dir(self, dirn):
        cont_l = []
        for fn in os.listdir(dirn):
            cont_l.append(self.read_file(os.path.join(dirn, fn)))
        return cont_l

    def read_file(self, fn):
        cont_l_f = []
        with open(fn, encoding="latin-1") as f:
            cont_l_f += [self.filter_word(w) for w in f.read().split() if self.filter_word(w)]
        return cont_l_f

    @staticmethod
    def filter_word(wstr):
        w = wstr.strip()
        pattern = re.compile("^[A-Za-z0-9]+$")

        if w.isdigit():
            return None

        concentration = 0
        for char in w:
            if pattern.match(char):
                concentration += 1
        concentration /= len(w)

        if concentration < 0.6 or len(w) < 4:
            return None

        return w

    @staticmethod
    def P_w_c(N_w_c, N_c, unique_words):
        return (N_w_c + 1) / (N_c + unique_words)

    @staticmethod
    def Nz(param):
        if param is None:
            return 0
        return param

    def classify_text(self, text):
        # Hspam = log P(spam) * log P(w1|spam) *... * P log(wn|spam)
        # Hham = log P(ham) * log P(w1|ham) * ... * log P(wn|ham)

        H_spam = math.log10(self.P_spam)
        H_ham = math.log10(self.P_ham)

        for word in text:
            if word in self.total_l_repetitions_keyset:
                H_ham += math.log10(self.P_w_c(self.Nz(self.ham_l_repetitions.get(word)), self.ham_l_len,
                                               self.ham_l_repetitions_keyset_size))
                H_spam += math.log10(self.P_w_c(self.Nz(self.spam_l_repetitions.get(word)), self.spam_l_len,
                                                self.spam_l_repetitions_keyset_size))

        return "SPAM" if H_spam >= H_ham else "NOT SPAM"


if __name__ == '__main__':
    model = NativeBayesianModel()
    print(model.classify_text(set(model.read_file("enron6/Letter1.txt"))))
    print(model.classify_text(set(model.read_file("enron6/Letter2.txt"))))
