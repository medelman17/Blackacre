import spacy
from spacy.matcher import Matcher

class SentenceSegmenter(object):
    name = "sentence_segmenter"

    def __init__(self, nlp):
        self.matcher = Matcher(nlp.vocab)

    def __call__(self, doc):
        matches = self.matcher(doc)
        for i, token in enumerate(doc[:-2]):
            if token_in_match_range(token, matches):
                token.is_sent_start = False
            if token.text == "v.":
                doc[i + 1].is_sent_start = False
            if token.text == "al" and doc[i + 1].is_punct:
                doc[i + 2].is_sent_start = False
            if token.is_digit and str(doc[i + 1]) == "(":
                doc[i + 1].is_sent_start = False
            if token.text == "," and doc[i+1].is_digit:
                doc[i + 1].is_sent_start = False
            if token.text == "No" and doc[i + 1].is_punct and token.is_sent_start != True:
                # print(token, doc[i+1].text, doc[i+2].text, doc[i+3].text, doc[i+4].text,)
                doc[i + 2].is_sent_start = False
            if token.text == "—":
                doc[i + 1].is_sent_start = False
            if token.text == ")" and doc[i+1].is_punct != True:
                doc[i + 1].is_sent_start = False
            if token.text == ")" and doc[i + 1].text == "(":
                doc[i + 1].is_sent_start = False
        return doc

    def add_rule(self, label, pattern, on_match=None):
        self.matcher.add(label, on_match, pattern)




def token_in_match_range(token, matches):
    for _, start, end in matches:
        if token.i >= start and token.i <= end:
            return True
    return False
