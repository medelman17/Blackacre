from spacy.matcher import PhraseMatcher
from blackacre.constants import state_legal_reporters, federal_legal_reporters
from spacy.tokens import Span

class ReporterMatcher(object):
    name = "reporter_matcher"
    entity_match_rules = [{"ENT_TYPE": "REPORTER"}]

    def on_match(self, matcher, doc, i, matches):
        match_id, start, end = matches[i]
        entity = Span(doc, start, end, label="REPORTER")
        newEnts = ()

        i = 0
        while i < len(doc.ents):
            existingEntity = doc.ents[i]
            if existingEntity.start != start:
                newEnts += (existingEntity,)
            i += 1

        newEnts += (entity,)
        doc.ents = newEnts


    def __init__(self, nlp, attr="LOWER"):
        self.matcher = PhraseMatcher(nlp.vocab, attr)
        patterns = [nlp.make_doc(reporter) for reporter in state_legal_reporters + federal_legal_reporters]
        self.matcher.add("Reporter", self.on_match, *patterns)

    def __call__(self, doc):
        matches = self.matcher(doc)

        return doc