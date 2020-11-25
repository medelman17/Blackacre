import spacy
from blackacre.components import SentenceSegmenter
from blackacre.components.matchers import ReporterMatcher, CourtMatcher

class SentencePipeline(object):

    def __init__(self, base_model="en_core_web_md", court_matcher=CourtMatcher, reporter_matcher=ReporterMatcher, rules=[]):
        self.nlp = spacy.load(base_model)
        self.segmenter = SentenceSegmenter(self.nlp)

        for rule in rules:
            label = rule["label"]
            pattern = rule["pattern"]
            self.segmenter.add_rule(label, pattern)

        court_matcher = court_matcher(self.nlp)
        reporter_matcher = reporter_matcher(self.nlp)

        self.segmenter.add_rule(court_matcher.name, court_matcher.entity_match_rules)
        self.segmenter.add_rule(reporter_matcher.name, reporter_matcher.entity_match_rules)

        self.nlp.add_pipe(self.segmenter, before="parser")
        self.nlp.add_pipe(court_matcher, before=self.segmenter.name)
        self.nlp.add_pipe(reporter_matcher, before=self.segmenter.name)

    def get_sentences(self, text):
        doc = self.nlp(text)

        return doc.sents

