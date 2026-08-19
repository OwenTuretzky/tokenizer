import collections

class Tokenizer:
    def __init__(self):
        self.symbols = ["[UNKNOWN]"] #list of all the characters
        self.merges = {} #maps what merges into what
        self.token_to_string = {0: "[UNKNOWN]"} #maps a token back to the string it represents

    def train(self, corpus: list[str], num_merges: int) -> None:
        """
        Using the algorithm in Sennrich's paper and modifications in the SentencePiece paper, perform BPE on each sentence in the corpus until len(tokens) = num_merges + len(symbols)
        """
        #get a list of every character, add them all as tokens
        #look through each sentence in the data and count the pairs of characters
        #take the most common pair and create a tuple, add it to the end of tokens
        #go back and replace all the smaller tokens in the training data with the new token
        #repeat num_merges times

        #counts the number of unique characters, and replaces every sentence with a list of characters (represented as their index in the list of vocab)
        modified_corpus = []
        for sentence in corpus:
            new_sentence = []
            for char in sentence:
                if char not in self.symbols:
                    self.symbols.append(char)
                new_sentence.append(self.symbols.index(char))
            modified_corpus.append(new_sentence)
        corpus = modified_corpus

        initial_symbols = len(self.symbols)

        #maps out the initial symbols
        for i, char in enumerate(self.symbols):
            self.token_to_string[i] = char

        #merge everything num_merges times
        for i in range(num_merges):
            count = self._pair_counter(corpus)
            most_frequent = max(count, key=count.get)

            print(f"Merge {i+1}/{num_merges} | Merging pair: {most_frequent} (Frequency: {count[most_frequent]})")

            new_token = initial_symbols + i

            self.merges[most_frequent] = new_token

            self.token_to_string[new_token] = self.token_to_string[most_frequent[0]] + self.token_to_string[most_frequent[1]]

            corpus = self._merge_best(corpus, most_frequent, new_token)

    def _pair_counter(self, corpus: list[list[int]]) -> dict[tuple[int,int], int] :
        """
        A helper function to get the number of times each pair of tokens appears.
        Takes the corpus as a list of ints instead of strings or characters, and returns a mapping of tuples to the number of times they appear.
        """
        pairs = collections.defaultdict(int)
        for sentence in corpus:
            for i in range(len(sentence) - 1):
                pair = (sentence[i], sentence[i+1])
                pairs[pair] += 1
        return pairs

    def _merge_best(self, corpus: list[list[int]], most_frequent: tuple[int, int], new_token: int) -> list[list[int]]:
        """
        goes through the corpus and merges all instances of the most frequent pair into their new pair
        """
        modified_corpus = []
        for sentence in corpus:
            new_sentence = []
            i = 0
            while i < len(sentence):
                #if the pair is in this sentence, replace the two tokens with the new one. otherwise, just copy the old token.
                if i < len(sentence) -1 and sentence[i] == most_frequent[0] and sentence[i+1] == most_frequent[1]:
                    new_sentence.append(new_token)
                    i += 2
                else:
                    new_sentence.append(sentence[i])
                    i += 1
            modified_corpus.append(new_sentence)
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
            pairs = self._pair_counter([tokens])
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

            tokens = self._merge_best([tokens], best_pair, self.merges[best_pair])[0]

        return tokens



    def decode(self, tokens: list[int]) -> str:
        """
        Takes a list of tokens and reassembles it back into a string
        """
        return "".join(self.token_to_string.get(t) for t in tokens)