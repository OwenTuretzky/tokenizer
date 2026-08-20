"""
A BPE tokenizer based off Sennrich's paper and SentencePiece. Takes some corpus and creates a list of tokens based on the most common pairs of characters in that corpus.
"""

import collections

class Tokenizer:
    def __init__(self):
        self.symbols = ["[UNKNOWN]", "[BOS]", "[EOS]", "[PAD]"]            #list of all the characters
        self.merges = {}                        #maps what has been merged together
        self.token_to_string = {0: "[UNKNOWN]",1: "[BOS]",2: "[EOS]",3: "[PAD]"} #maps a token back to the string it represents

    def train(self, corpus: list[str], num_merges: int) -> None:
        """
        Using the algorithm in Sennrich's paper and modifications in the SentencePiece paper, perform BPE on each sentence in the corpus.
        """

        #stores each sequence in the corpus in a dict, allowing duplicate sequences to be counted instead of both stored.
        corpus_dict = collections.defaultdict(int)

        #dictionary storing characters to make lookups faster
        symbols_to_id= {char: id for id, char in enumerate(self.symbols)}

        #loads each character and sentence
        for sentence in corpus:
            new_sentence = []
            for char in sentence:
                if char not in symbols_to_id:
                    symbols_to_id[char] = len(self.symbols)
                    self.symbols.append(char)
                new_sentence.append(symbols_to_id[char])
            key = tuple(new_sentence)
            corpus_dict[key] += 1

        initial_symbols = len(self.symbols)

        #maps out the initial symbols
        for i, char in enumerate(self.symbols):
            self.token_to_string[i] = char

        #merge everything num_merges times
        for i in range(num_merges):
            count = self._pair_counter(corpus_dict)
            most_frequent = max(count, key=count.get)

            new_token = initial_symbols + i

            print(f"Merge {i+1}/{num_merges} | Merging pair: {most_frequent} (Frequency: {count[most_frequent]})")

            self.merges[most_frequent] = new_token

            self.token_to_string[new_token] = self.token_to_string[most_frequent[0]] + self.token_to_string[most_frequent[1]]

            corpus_dict = self._merge_best(corpus_dict, most_frequent, new_token)

    def _pair_counter(self, corpus: dict[tuple[int, ...], int]) -> dict[tuple[int,int], int] :
        """
        A helper function to get the number of times each pair of tokens appears.
        """
        pairs = collections.defaultdict(int)
        for sequence, count in corpus.items():
            for i in range(len(sequence) - 1):
                pairs[(sequence[i], sequence[i+1])] += count
        return pairs

    def _merge_best(self, corpus: dict[tuple[int, ...], int], most_frequent: tuple[int, int], new_token: int) -> dict[tuple[int, ...], int]:
        """
        goes through the corpus and merges all instances of the most frequent pair into a new token
        """
        modified_corpus = collections.defaultdict(int)
        for sequence, count in corpus.items():
            new_sequence = []
            i = 0
            while i < len(sequence):
                #if the pair is in this sequence, replace the two tokens with the new one. otherwise, just copy the old token.
                if i < len(sequence) -1 and sequence[i] == most_frequent[0] and sequence[i+1] == most_frequent[1]:
                    new_sequence.append(new_token)
                    i += 2
                else:
                    new_sequence.append(sequence[i])
                    i += 1
            modified_corpus[tuple(new_sequence)] += count
        return modified_corpus


    def encode(self, text: str) -> list[int]:
        """
        Takes a given string of text and tokenizes it
        """
        #uses the list of symbols to map each symbol in the string to its token, and skips it if its a new symbol.
        tokens = []
        for char in text:
            if char in self.symbols:
                tokens.append(self.symbols.index(char))
            else:
                tokens.append(0) #if it gets here, there must be an unknown character

        #merge tokens while there are tokens left to merge
        while len(tokens) >= 2:
            pairs = collections.defaultdict(int)
            for i in range(len(tokens) - 1):
                pairs[(tokens[i], tokens[i+1])] += 1
            best_pair = None
            lowest_token_id = 10000000000000000 #really big number
            for pair in pairs.keys():
                if pair in self.merges:
                    token_id = self.merges[pair]

                    if token_id < lowest_token_id:
                        lowest_token_id = token_id
                        best_pair = pair

            if best_pair is None:
                break            

            i = 0
            new_tokens = []
            while i < len(tokens):
                if i < len(tokens) - 1 and (tokens[i], tokens[i+1]) == best_pair:
                    new_tokens.append(self.merges[best_pair])
                    i += 2
                else:
                    new_tokens.append(tokens[i])
                    i += 1
            tokens = new_tokens

        return tokens



    def decode(self, tokens: list[int]) -> str:
        """
        Takes a list of tokens and reassembles it back into a string
        """
        return "".join(self.token_to_string.get(t, "[UNKNOWN]") for t in tokens)

    
    #CODE BELOW HERE WAS WRITTEN BY LLMS

    def save(self, path: str) -> None:
        """
        THIS FUNCTION WAS WRITTEN FOR ME BY AN LLM
        saves the relavent lists and dicts, so you dont have to train every time.
        """
        import json
        data = {
            "symbols": self.symbols,
            "merges": {f"{a},{b}": c for (a, b), c in self.merges.items()},
            "token_to_string": {str(token): string for token, string in self.token_to_string.items()}
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

    def load(self, path: str) -> None:
        """
        THIS FUNCTION WAS WRITTEN FOR ME BY AN LLM
        loads the relavent lists and dicts, so you dont have to train every time.
        """
        import json
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.symbols = data["symbols"]
        self.merges = {
            (int(a), int(b)): c
            for key, c in data["merges"].items()
            for a, b in [key.split(",")]
        }
        self.token_to_string = {int(token): string for token, string in data["token_to_string"].items()}