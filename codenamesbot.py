import json
import itertools
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class CodenamesBot:
    GROUP_WEIGHTS = {
        "good": +1.0,
        "bad": -0.5
    }
    
    def __init__(self, game, playing_as, repr_path):
        self.game = game
        self.all_game_words = set(self.game["gray"] + self.game["red"] + self.game["blue"] + self.game["black"])
        self.playing_as = playing_as
        self.other_team = "red" if playing_as == "blue" else "blue"
        self.repr_path = repr_path

    def initialize(self):
        with open(self.repr_path, "r") as f:
            self.model = json.load(f)
            self.all_words = list(self.model.keys())

    def get_repr(self, w):
        return self.model[w] if w in self.model else np.random.uniform(0, 1, (100))

    def find_similar(self, groups, group_weights):
        group_repr = { key: [self.get_repr(w) for w in values] for key, values in groups.items() }

        best_word = None
        best_score = float("-inf")
        for word in self.all_words:
            if word in self.all_game_words: continue
            word_repr = self.get_repr(word)

            score = 0
            for key in groups.keys():
                similarity = cosine_similarity(group_repr[key], [word_repr])
                score += group_weights[key] * np.mean(similarity)

            if score > best_score:
                best_score = score
                best_word = word

        return best_word, best_score

    def find_relational_word(self, target):
        groups = {
            "good": target,
            "bad": self.game[self.other_team] + self.game["gray"] + self.game["black"]
        }

        return self.find_similar(groups, CodenamesBot.GROUP_WEIGHTS)

    def find_best_with_n(self, n):
        best_word = (None, None, float("-inf"))
        options = [subset for subset in itertools.combinations(self.game[self.playing_as], n)]
        for subset in options:
            word, score = self.find_relational_word(subset)
            if score > best_word[2]:
                best_word = (subset, word, score)

        return best_word

    def print_best_guesses(self):
        for n_words in [2, 3]:
            best_word_n = self.find_best_with_n(n_words)
            print(f"Best choice with {n_words}: {best_word_n}")