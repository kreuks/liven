# -*- coding: utf-8 -*-

import codecs
import json
import re
import warnings
from itertools import groupby

from core import util


class TrainingData(object):
    def __init__(self, resource_name, backend, language_name):
        self.intent_examples = []
        self.entity_examples = []
        self.resource_name = resource_name
        self.files = util.recursively_find_files(resource_name)
        self.fformat = self.guess_format(self.files)
        self.tokenizer = None
        self.language_name = language_name
        self.min_examples_per_intent = 2
        self.min_examples_per_entity = 2

        if backend in ['mitie', 'mitie_sklearn']:
            from core.tokenizers.mitie_tokenizer import MITIETokenizer
            self.tokenizer = MITIETokenizer()
        elif backend in ['spacy_sklearn']:
            from core.tokenizers.spacy_tokenizer import SpacyTokenizer
            self.tokenizer = SpacyTokenizer(language_name)
        else:
            from core.tokenizers.whitespace_tokenizer import WhitespaceTokenizer
            self.tokenizer = WhitespaceTokenizer()
            warnings.warn(
                "backend not recognised by TrainingData : defaulting to tokenizing by splitting on whitespace")

        if self.fformat == 'luis':
            self.load_luis_data(self.files[0])
        elif self.fformat == 'wit':
            self.load_wit_data(self.files[0])
        elif self.fformat == 'api':
            self.load_api_data(self.files)
        elif self.fformat == 'rasa_nlu':
            self.load_data(self.files[0])
        else:
            raise ValueError("unknown training file format : {0}".format(self.fformat))

        self.validate()

    def as_json(self, **kwargs):
        return json.dumps({
            "rasa_nlu_data": {
                "intent_examples": self.intent_examples,
                "entity_examples": self.entity_examples
            }
        }, **kwargs)

    def guess_format(self, files):
        for filename in files:
            filedata = json.loads(codecs.open(filename, encoding='utf-8').read())
            if "data" in "data" and type(filedata.get("data")) is list:
                return 'wit'
            elif "luis_schema_version" in filedata:
                return 'luis'
            elif "userSays" in filedata:
                return 'api'
            elif "rasa_nlu_data" in filedata:
                return 'rasa_nlu'

        return 'unk'

    def load_wit_data(self, filename):
        data = json.loads(codecs.open(filename, encoding='utf-8').read())
        for s in data["data"]:
            entities = s.get("entities")
            if entities is None:
                continue
            text = s.get("text")

            intents = [e['entity'] for e in entities if e['value'] == '"true"' or e['value'] == '"True"']
            intent = intents[0] if intents else 'None'

            entities = [e for e in entities]
            for e in entities:
                e["value"] = e["value"][1:-1]

            self.intent_examples.append({"text": text, "intent": intent})
            self.entity_examples.append({"text": text, "intent": intent, "entities": entities})

    def load_luis_data(self, filename):
        warnings.warn(
            """LUIS data may not always be correctly imported because entity locations are specified by tokens.
            If you use a tokenizer which behaves differently from LUIS's your entities might not be correct""")
        data = json.loads(codecs.open(filename, encoding='utf-8').read())
        for s in data["utterances"]:
            text = s.get("text")
            tokens = [t for t in self.tokenizer.tokenize(text)]
            intent = s.get("intent")
            entities = []
            for e in s.get("entities") or []:
                i, ii = e["startPos"], e["endPos"] + 1
                _regex = u"\s*".join([re.escape(s) for s in tokens[i:ii]])
                expr = re.compile(_regex)
                m = expr.search(text)
                start, end = m.start(), m.end()
                val = text[start:end]
                entities.append({"entity": e["entity"], "value": val, "start": start, "end": end})

            self.intent_examples.append({"text": text, "intent": intent})
            self.entity_examples.append({"text": text, "intent": intent, "entities": entities})

    def load_api_data(self, files):
        for filename in files:
            data = json.loads(codecs.open(filename, encoding='utf-8').read())
            # get only intents, skip the rest. The property name is the target class
            if "userSays" not in data:
                continue

            intent = data.get("name")
            for s in data["userSays"]:
                text = "".join(map(lambda chunk: chunk["text"], s.get("data")))
                # add entities to each token, if available
                entities = []
                for e in filter(lambda chunk: "alias" in chunk or "meta" in chunk, s.get("data")):
                    start = text.find(e["text"])
                    end = start + len(e["text"])
                    val = text[start:end]
                    entities.append(
                        {"entity": e["alias"] if "alias" in e else e["meta"], "value": val, "start": start, "end": end})

                self.intent_examples.append({"text": text, "intent": intent})
                self.entity_examples.append({"text": text, "intent": intent, "entities": entities})

    def load_data(self, filename):
        data = json.loads(open(filename, 'rb').read())
        common = data['rasa_nlu_data'].get("common_examples", list())
        intent = data['rasa_nlu_data'].get("intent_examples", list())
        entity = data['rasa_nlu_data'].get("entity_examples", list())

        self.intent_examples = intent + common
        self.entity_examples = entity + common

    def validate(self):
        examples = sorted(self.intent_examples, key=lambda e: e["intent"])
        intentgroups = []
        for intent, group in groupby(examples, lambda e: e["intent"]):
            size = len(list(group))
            if size < self.min_examples_per_intent:
                template = "intent {0} has only {1} training examples! minimum is {2}, training may fail."
                warnings.warn(template.format(intent, size, self.min_examples_per_intent))

        entitygroups = []
        examples = sorted([e for ex in self.entity_examples for e in ex["entities"]], key=lambda e: e["entity"])
        for entity, group in groupby(examples, lambda e: e["entity"]):
            size = len(list(group))
            if size < self.min_examples_per_entity:
                template = "entity {0} has only {1} training examples! minimum is {2}, training may fail."
                warnings.warn(template.format(entity, size, self.min_examples_per_entity))
