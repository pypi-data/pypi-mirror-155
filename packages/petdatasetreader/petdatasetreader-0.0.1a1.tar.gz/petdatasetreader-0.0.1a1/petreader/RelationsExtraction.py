from typing import Union
from datasets import load_dataset
import random

from petreader.labels import *

class RelationsExtraction:
    """

    RelationsExtraction
    --------------------

    This class provides a convenient interface to PET-dataset data.
    It allows you to get structured representation of the data.


    Please look at https://pdi.fbk.eu/pet-dataset/ for more information about the PET dataset.

    """

    def __init__(self):
        self.dataset = load_dataset("patriziobellan/PET", name='relations-extraction')

    def __len__(self):
        """the length of a RelationsExtraction instance is equal to the number of documents of the dataset

        Returns:
            the number of document of the PET dataset.

        """
        return len(self.dataset['test']['document name'])

    @staticmethod
    def _remove_B_I_prefix(tag_label):
        #  remove the prefix B/I from tag label
        if len(tag_label) == 1:
            return tag_label
        else:
            return tag_label[2:]

    def GetDocument(self, document_identifier: Union[int, str]) -> str:
        """Get the document's text of a given text identifier.

        Example::

            Get the document text providing document number.

            >>> pet = RelationsExtraction()

            >>> text1 = pet.GetDocument(1)

            >>> print(text1)

            Get the document text providing document name.

            >>> text1 = pet.GetDocument('doc-1.1')

            >>> print(text1)

        Args

            document_identifier (int): the number of the document you want the text.
            document_identifier (str): the name of the document you want the text.

        Returns:

            str: the document text.

        """
        if type(document_identifier) == int:

            return ' '.join(self.dataset['test']['tokens'][document_identifier]).strip()

        elif type(document_identifier) == str:
            document_identifier = self.GetDocumentNumber(document_identifier)

            return ' '.join(self.dataset['test']['tokens'][document_identifier]).strip()

    def GetDocumentName(self, document_number: int) -> str:
        """Get the document name of a given numeric identifier document_number.

        Args:
            document_number (int): the document number.

        Returns:
            the document name of a given document_number.

        """

        return self.dataset['test']['document name'][document_number]

    def GetDocumentNumber(self, document_name: str) -> int:
        """Get the document id of a given document name.

        Args:
            document_name (str): the name of the document.

        Returns (str):
            the document number (a.k.a. Id).

        """

        docs = {self.dataset['test'][n_]['document name']: n_ for n_ in range(len(self.dataset['test']))}

        return docs[document_name]

    def GetDocumentNames(self) -> list:
        """Get the list of documents' name.

        Returns:
            list of documents name

        """

        return list(set(self.dataset['test']['document name']))

    def GetRandomizedSampleNumbers(self) -> list:
        """Randomize sample identifiers list.
        The seed is set every call to make this list reproducible.

        Returns:
            A list of document names randomized

        """

        #  set random seed for reproducibility
        random.seed(23)

        ids = [x for x in range(len(self))]
        randomized_ids = random.sample(ids, len(self))
        return randomized_ids

    def GetSentenceIDs(self, sample_number: int):
        #  return the sentence IDs of a given document_number
        return self.dataset['test']['sentence-IDs'][sample_number]

    def GetTokens(self, sample_number: int):
        #  return the tokens of a given document_number
        return self.dataset['test']['tokens'][sample_number]

    def GetTokenIDs(self, sample_number: int):
        #  return the tokens of a given document_number
        return self.dataset['test']['tokens-IDs'][sample_number]

    #  TESTARE DA QUI
    def GetNerLabels(self, sample_number: int):
        #  return the ner-tags ids of a given document_number
        return self.dataset['test']['ner_tags'][sample_number]

    def GetSentencesWithIdsAndNerTagLabels(self, sample_number: int):
        #  return a list of sentences
        # each sentence has token IDs amd ner_tags

        tokens = self.GetTokens(sample_number)
        tokens_ids = self.GetTokenIDs(sample_number)
        sentence_ids = self.GetSentenceIDs(sample_number)
        ner_tags = self.GetNerLabels(sample_number)
        sentences = list()
        #  used to track changes in sentence id
        sentence_index = sentence_ids[0]
        temp_sentence = list()
        for token, token_id, sentence_id, ner_label in zip(tokens,
                                                           tokens_ids,
                                                           sentence_ids,
                                                           ner_tags):
            #  check if sentence id is changed
            if sentence_index != sentence_id:
                #  add sentence to sentences
                sentences.append(temp_sentence)
                #  clear var
                temp_sentence = list()
                sentence_index = sentence_id
            temp_sentence.append(tuple([token, token_id, ner_label]))

        #  add last sentence
        sentences.append(temp_sentence)

        return sentences

    def GetSentencesTokens(self, sample_number: int):
        #  return a list of tokens for each sentence

        sentences = self.GetSentencesWithIdsAndNerTagLabels(sample_number)
        token_sentences = [[x[0] for x in sent] for sent in sentences]
        return token_sentences

    def GetPrefixAndLabel(self, tag_label):
        #  return the prefix and the label for a give ner_label
        label = self._remove_B_I_prefix(tag_label)
        prefix = tag_label[0]

        return prefix, label

    def GetRelationsRaw(self, sample_number: int):
        #  return a list of raw relation of a given sample

        relations_raw = list()

        relations_raw_list = self.dataset['test'][sample_number]['relations']
        source_head_sentence_ids = relations_raw_list[SOURCE_SENTENCE_ID]
        source_head_token_ids = relations_raw_list[SOURCE_HEAD_TOKEN_ID]
        relation_types = relations_raw_list['relation-type']
        target_head_sentence_ids = relations_raw_list[TARGET_SENTENCE_ID]
        target_head_token_ids = relations_raw_list[TARGET_HEAD_TOKEN_ID]

        for source_head_sentence_id, \
            source_head_token_id, \
            relation_type, \
            target_head_sentence_id, \
            target_head_token_id in zip(source_head_sentence_ids,
                                        source_head_token_ids,
                                        relation_types,
                                        target_head_sentence_ids,
                                        target_head_token_ids):
            relations_raw.append(tuple([source_head_sentence_id,
                                        source_head_token_id,
                                        relation_type,
                                        target_head_sentence_id,
                                        target_head_token_id]))

        return relations_raw

    def GetEntityWithTokenIdFromId(self,
                                   sample_number,
                                   sentence_id,
                                   head_token_id):
        #  given a document_number, a head token and sentence ids it returns the span of words
        # and its type

        doc_entities = self.GetSentencesWithIdsAndNerTagLabels(sample_number)
        sentence_entities = doc_entities[sentence_id]

        #  get head element
        #  sentence_entities[head_token_id]
        #  >>>('reports', 3, 'B-Activity') | (token, token_id, ner_label
        head = sentence_entities[head_token_id]

        entity = [tuple([sentence_entities[head_token_id][0],
                         sentence_entities[head_token_id][1]])]
        prefix, label = self.GetPrefixAndLabel(sentence_entities[head_token_id][2])
        entity_type = label

        for token, token_id, ner_label in sentence_entities[head_token_id + 1:]:
            prefix, label = self.GetPrefixAndLabel(ner_label)
            if prefix != 'I':
                break
            entity.append(tuple([token, token_id]))

        return entity, entity_type

    def GetEntityFromId(self,
                        sample_number,
                        sentence_id,
                        head_token_id):

        entity, entity_type = self.GetEntityWithTokenIdFromId(sample_number,
                                                              sentence_id,
                                                              head_token_id)
        cleaned_entity = [x[0] for x in entity]

        return cleaned_entity, entity_type

    def GetRelations(self, document_number: int) -> dict:
        """Get a list of relations of a given document.

        Args:
            document_number (int): the document id.

        Returns:
            list of relations.

        """

        #  get raw relations
        raw_relations = self.GetRelationsRaw(document_number)

        #  create relations object
        relations = {k: list() for k in RELATIONS_EXTRACTION_LABELS}

        #  refactoring raw relations into structured relations
        for relation in raw_relations:
            source_sentence_id, source_head_token_id, rel_type, target_sentence_id, target_hard_token_id = relation

            source_entity, source_entity_type = self.GetEntityFromId(document_number,
                                                                     source_sentence_id,
                                                                     source_head_token_id)
            target_entity, target_entity_type = self.GetEntityFromId(document_number,
                                                                     target_sentence_id,
                                                                     target_hard_token_id)
            if rel_type not in RELATIONS_EXTRACTION_LABELS:
                doc_name = self.GetDocumentName(document_number)
                raise ValueError('{}|relation type {} not recognized. include it!'.format(doc_name,
                                                                                          rel_type))

            relations[rel_type].append({SOURCE_SENTENCE_ID:   source_sentence_id,
                                        SOURCE_HEAD_TOKEN_ID: source_head_token_id,

                                        SOURCE_ENTITY_TYPE:   source_entity_type,
                                        SOURCE_ENTITY:        source_entity,

                                        TARGET_SENTENCE_ID:   target_sentence_id,
                                        TARGET_HEAD_TOKEN_ID: target_hard_token_id,

                                        TARGET_ENTITY_TYPE:   target_entity_type,
                                        TARGET_ENTITY:        target_entity})

        return relations
