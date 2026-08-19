class Tokenizer:
    def __init__(self):
        self.tokens = []

    def train(self, corpus, num_tokens) -> None:
        """
        Using the algorithm in Sennrich's paper and modifications in the SentencePiece paper, perform BPE on each sentence in the corpus until len(tokens) = num_tokens
        """

    def encode(self, text) -> list[str]:
        """
        Takes a given string of text and tokenizes it
        """

    def decode(self, tokens) -> str:
        """
        Takes a list of tokens and reassembles it back into a string
        """