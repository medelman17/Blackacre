from spacy.matcher import PhraseMatcher
from blackacre.constants.courts import state_courts_of_appeal, federal_courts_of_appeal
from spacy.tokens import Span

class CourtMatcher(object):
    name = "court_matcher"
    entity_match_rules = [{"ENT_TYPE": "COURT"}]

    def on_match(self, matcher, doc, i, matches):
        match_id, start, end = matches[i]
        entity = Span(doc, start, end, label="COURT")

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
        patterns = [nlp.make_doc(court[0]) for court in federal_courts_of_appeal + state_courts_of_appeal]
        self.matcher.add("Court", self.on_match, *patterns)

    def __call__(self, doc):
        matches = self.matcher(doc)
        return doc