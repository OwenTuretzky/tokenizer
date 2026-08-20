# Custom Tokenizer
A custom from-scratch tokenizer meant to work for both Japanese and English. Written as a starting point for my larger translation project, but works by itself as well.

Implements Byte-Pair Encoding without any whitespace segmentation, allowing it to handle both japanese and english effectively.

## Usage
Install the package
```bash
pip install -e .
```
Train on some corpus (I tested with [small_parallel_enja](https://github.com/odashi/small_parallel_enja/tree/master), but any list of strings will work)

```python
from tokenizer import Tokenizer

t = Tokenizer()
t.train(corpus, num_merges=1000)
t.save("vocab.json")
```
You can also save and load and use it to encode/decode text:
```python
t = Tokenizer()
t.load("vocab.json")

tokens = t.encode("this is a test sentence.")
print(tokens)           # [4747, 7427, ...]
print(t.decode(tokens)) # this is a test sentence.
```

Unknown characters are mapped as a special token 0 "[UNKNOWN]"


## LLM Use
LLM's such as Anthropic's Claude and Google Gemini were used to help assist in finding relavent papers and notes for this project, as well as bugfixing at times. Any code written by an LLM is clearly labled as such in a comment.

## References

This implementation is based on the following papers:

- Sennrich, R., Haddow, B., & Birch, A. (2015). Neural Machine Translation of Rare Words with Subword Units. arXiv Preprint (Cs.CL). https://arxiv.org/abs/1508.07909v5
- Kudo, T., & Richardson, J. (2018). SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing. arXiv Preprint (Cs.CL). https://arxiv.org/abs/1808.06226v1