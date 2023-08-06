from datasets import load_dataset
import random

from petreader.labels import *


class TokenClassification:
    """
    Dataset structure:
    ------------------
        DatasetDict({
            test: Dataset({
                features: ['document name', 'sentence-ID', 'tokens', 'ner-tags'],
                num_rows: 417
            })
        })


    """
    _NER_TAGS = ["O",
                 "B-Actor",
                 "I-Actor",
                 "B-Activity",
                 "I-Activity",
                 "B-Activity Data",
                 "I-Activity Data",
                 "B-Further Specification",
                 "I-Further Specification",
                 "B-XOR Gateway",
                 "I-XOR Gateway",
                 "B-Condition Specification",
                 "I-Condition Specification",
                 "B-AND Gateway",
                 "I-AND Gateway"]

    #  convenient ner tags maps
    _NER_TAGS_ID_TO_LABEL_MAP = {n_: label for n_, label in enumerate(_NER_TAGS)}
    _NER_TAGS_LABEL_TO_ID_MAP = {label: n_ for n_, label in enumerate(_NER_TAGS)}

    def __init__(self):
        self.dataset = load_dataset("patriziobellan/PET", name='token-classification')

        self._create_process_element_list()
        self._create_process_element_indexes_list()
        self.__create_n_sample_document_ids()

    def __len__(self):
        #  return the number of samples available
        return len(self.dataset['test']['document name'])

    @staticmethod
    def _remove_B_I_prefix(tag_label):
        #  remove the prefix B/I from tag label
        if len(tag_label) == 1:
            return tag_label
        else:
            return tag_label[2:]

    def GetDocumentName(self, sample_number: int):
        #  return the document name of a given document_number
        return self.dataset['test']['document name'][sample_number]

    def GetSentenceID(self, sample_number: int):
        #  return the sentence ID of a given document_number
        return self.dataset['test']['sentence-ID'][sample_number]

    def GetTokens(self, sample_number: int):
        #  return the tokens of a given document_number
        return self.dataset['test']['tokens'][sample_number]

    def GetNerTagIDs(self, sample_number: int):
        #  return the ner-tags ids of a given document_number
        return self.dataset['test']['ner-tags'][sample_number]

    def GetNerTagLabels(self, sample_number: int):
        #  return the ner tag labels of a given document_number
        return [self.GetNerTagLabel(tag_id) for tag_id in self.dataset['test']['ner-tags'][sample_number]]

    def GetPrefixAndLabel(self, ner_tag_id):
        #  return the prefix and the label for a give ner_id
        tag_label = self.GetNerTagLabel(ner_tag_id)
        label = self._remove_B_I_prefix(tag_label)
        prefix = tag_label[0]

        return prefix, label

    def GetNerTagLabel(self, tag_id):
        #  return the ner tag name of a given ner tag id
        return self._NER_TAGS_ID_TO_LABEL_MAP[tag_id]

    def GetNerTagId(self, ner_label):
        #  return the ner tag id of a given ner label
        return self._NER_TAGS_LABEL_TO_ID_MAP[ner_label]

    def GetDocumentNames(self):
        #  return the unique names of the dataset documents
        return list(set(self.dataset['test']['document name']))

    def GetSampleDict(self, sample_number: int):
        #  return a dict of the sample
        return {'document name': self.dataset['test']['document name'][sample_number],
                'sentence-ID':   self.dataset['test']['sentence-ID'][sample_number],
                'tokens':        self.dataset['test']['tokens'][sample_number],
                'ner-tags':      self.dataset['test']['ner-tags'][sample_number]
                }

    def GetSampleDictWithNerLabels(self, sample_number: int):
        #  return a dict of the sample with the ner tags mapped to their labels
        return {'document name': self.dataset['test']['document name'][sample_number],
                'sentence-ID':   self.dataset['test']['sentence-ID'][sample_number],
                'tokens':        self.dataset['test']['tokens'][sample_number],
                'ner-tags':      [self.GetNerTagLabel(ner_id) for ner_id in
                                  self.dataset['test']['ner-tags'][sample_number]]
                }

    def GetSampleListOfEntities(self, sample_number: int):
        #  return a list of annotated entities
        ner_id_sentence = self.dataset['test']['ner-tags'][sample_number]
        ner_labels = [self._remove_B_I_prefix(self.GetNerTagLabel(tag_id)) for tag_id in ner_id_sentence]
        ner_labels = set(ner_labels)
        ner_labels.remove('O')
        return list(ner_labels)

    def GetSampleEntitiesWithTokenIds(self, sample_number: int):
        # return a dict of list of entities mentioned in the sample
        #  the method return for element of the list a tuple of word, token position

        sentence_tokens = self.dataset['test']['tokens'][sample_number]
        sentence_ner_ids = self.dataset['test']['ner-tags'][sample_number]
        entities = {k: list() for k in self.GetSampleListOfEntities(sample_number)}

        #  memorize tokens span
        temp_entity = list()
        #  memorize entity type
        temp_entity_type = 'O'

        for n_token, (token, ner_tag_id) in enumerate(zip(sentence_tokens,
                                                          sentence_ner_ids)):
            prefix, label = self.GetPrefixAndLabel(ner_tag_id)
            if prefix == 'B':
                #  flush previous val, if any
                if temp_entity_type and temp_entity:
                    entities[temp_entity_type].append(temp_entity)
                #  reset var
                temp_entity = list()
                #  start collecting the new span
                temp_entity.append(tuple([token, n_token]))
                temp_entity_type = label
            elif prefix == 'I':
                temp_entity.append(tuple([token, n_token]))
            # else:
            #  prefix is 'O'
            # this case is not handled since
            #  it is rendondant to flush it. it is already done when another 'B' is found
            #  flush
        #  flush last entity, if it is not an 'O
        if temp_entity_type != 'O':
            entities[temp_entity_type].append(temp_entity)

        return entities

    def GetSampleEntitiesIndexes(self, sample_number: int) -> dict:
        """return a dict of list of entities mentioned in the sample
          the method return the indexes (a.k.a.)  token position.

        Args:
            sample_number (int):
                the number of the sentence
        Returns:
            dict of list
        """

        entities = self.GetSampleEntitiesWithTokenIds(sample_number)
        entities_cleanned = {k: list() for k in PROCESS_ELEMENT_LABELS}

        for k, item_list in entities.items():
            for item in item_list:
                indexes = [x[1] for x in item]
                entities_cleanned[k].append(indexes)

        return entities_cleanned

    def GetSampleEntities(self, sample_number: int):
        #  return a dict of list of entities mentioned in the sample
        #  the method return the words, NOT the token position
        entities = self.GetSampleEntitiesWithTokenIds(sample_number)
        entities_cleanned = {k: list() for k in PROCESS_ELEMENT_LABELS}

        for k, item_list in entities.items():
            for item in item_list:
                tokens = [x[0] for x in item]
                entities_cleanned[k].append(tokens)

        return entities_cleanned

    def GetRandomizedSampleNumbers(self):
        #  return a list of sample numbers randomized
        #  since the seed is set, the list is reproducible

        #  set random seed for reproducibility
        random.seed(23)

        ids = [x for x in range(len(self))]
        randomized_ids = random.sample(ids, len(self))
        return randomized_ids

    def _create_process_element_list(self) -> list:
        #  return a list
        #  each item correspond to a dataset sample and contains the list of token target element
        self._process_element_list = [self.GetSampleEntities(n_sample) for n_sample in range(len(self))]

    def _create_process_element_indexes_list(self) -> list:
        #  return a list
        #  each item correspond to a dataset sample and contains the list of index target element
        self._process_element_indexes_list = [self.GetSampleEntitiesIndexes(n_sample) for n_sample in range(len(self))]

    def _get_process_element_list(self,
                                  target_element: str,
                                  start_index: int,
                                  end_index: int) -> list:
        #  return a list
        #  each item correspond to a dataset sample and contains the list of token target element

        return [self._process_element_list[n_sample][target_element] for n_sample in range(start_index, end_index+1)]

    def _get_process_element_indexes_list(self,
                                          target_element: str,
                                          start_index: int,
                                          end_index: int) -> list:
        #  return a list
        #  each item correspond to a dataset sample and contains the list of index target element
        return [self._process_element_indexes_list[n_sample][target_element] for n_sample in
                range(start_index, end_index+1)]

    def GetActivities(self) -> list:
        return self._get_process_element_list(ACTIVITY, 0, len(self)-1)

    def GetActivityData(self) -> list:
        return self._get_process_element_list(ACTIVITY_DATA, 0, len(self)-1)

    def GetActors(self) -> list:
        return self._get_process_element_list(ACTOR, 0, len(self)-1)

    def GetFurtherSpecifications(self) -> list:
        return self._get_process_element_list(FURTHER_SPECIFICATION, 0, len(self)-1)

    def GetXORGateways(self) -> list:
        return self._get_process_element_list(XOR_GATEWAY, 0, len(self)-1)

    def GetANDGateways(self) -> list:
        return self._get_process_element_list(AND_GATEWAY, 0, len(self)-1)

    def GetConditionSpecifications(self) -> list:
        return self._get_process_element_list(CONDITION_SPECIFICATION, 0, len(self)-1)

    # TO FIX
    def __create_n_sample_document_ids(self) :
        """create document ids for fast look up
        """
        def get_ids(doc_name):
            ids = list()
            for n_ in range(len(self)):
                if self.GetDocumentName(n_) == doc_name:
                    ids.append(n_)
            return sorted(ids)

        self.__documents_ids = dict()
        for doc_name in self.GetDocumentNames():
            self.__documents_ids[doc_name] = get_ids(doc_name)

    def get_n_sample_of_a_document(self,
                                   document_name: str) -> list:
        return self.__documents_ids[document_name]
        # """Get the list of sample ids of a document
        #
        # Args:
        #     document_name (str):
        #         the name of the document
        # Returns:
        #     list of sample ids of a document
        # """
        # ids = list()
        # for n_ in range(len(self)):
        #     if self.GetDocumentName(n_) == document_name:
        #         ids.append(n_)
        #
        # return sorted(ids)


    def GetDocumentText(self,
                        document_name: str) -> str:
        """Get the text of a document

        Args:
            document_name (str):
                the name of the document.

        Returns:
            the text of the document
        """
        sentences = list()

        #  retrieve ids of a document
        doc_ids = self.get_n_sample_of_a_document(document_name)
        #  collect sentence's text
        for n_id in doc_ids:
            sentence = self.GetTokens(n_id)
            sentence = ' '.join(sentence).strip()
            sentences.append(sentence)

        #  compose the text
        text = '\n'.join(sentences).strip()

        return text

    #################################
    #  ENTITIIES IN TOKENS OF A DOCUMENT
    #################################
    def GetDocumentActivities(self,
                              document_name: str) -> list:

        #  retrieve ids of a document
        doc_ids = self.get_n_sample_of_a_document(document_name)
        return self._get_process_element_list(ACTIVITY, doc_ids[0], doc_ids[-1])

    def GetDocumentActivityData(self,
                                document_name: str) -> list:

        #  retrieve ids of a document
        doc_ids = self.get_n_sample_of_a_document(document_name)

        return self._get_process_element_list(ACTIVITY_DATA, doc_ids[0], doc_ids[-1])

    def GetDocumentActors(self,
                          document_name: str) -> list:

        #  retrieve ids of a document
        doc_ids = self.get_n_sample_of_a_document(document_name)

        return self._get_process_element_list(ACTOR, doc_ids[0], doc_ids[-1])

    def GetDocumentFurtherSpecifications(self,
                                         document_name: str) -> list:

        #  retrieve ids of a document
        doc_ids = self.get_n_sample_of_a_document(document_name)

        return self._get_process_element_list(FURTHER_SPECIFICATION, doc_ids[0], doc_ids[-1])

    def GetDocumentXORGateways(self,
                               document_name: str) -> list:

        #  retrieve ids of a document
        doc_ids = self.get_n_sample_of_a_document(document_name)

        return self._get_process_element_list(XOR_GATEWAY, doc_ids[0], doc_ids[-1])

    def GetDocumentANDGateways(self,
                               document_name: str) -> list:

        #  retrieve ids of a document
        doc_ids = self.get_n_sample_of_a_document(document_name)

        return self._get_process_element_list(AND_GATEWAY, doc_ids[0], doc_ids[-1])

    def GetDocumentConditionSpecifications(self,
                                           document_name: str) -> list:

        #  retrieve ids of a document
        doc_ids = self.get_n_sample_of_a_document(document_name)

        return self._get_process_element_list(CONDITION_SPECIFICATION, doc_ids[0], doc_ids[-1])

    #################################
    #  ENTITIES INDEXES OF A DOCUMENT
    #################################
    def GetDocumentActivitiesIndexes(self,
                                     document_name: str) -> list:

        #  retrieve ids of a document
        doc_ids = self.get_n_sample_of_a_document(document_name)
        #  get elements
        # activities = self._get_process_element_list(ACTIVITY)
        # #  trim list to document of interest
        # activities = activities[doc_ids[0]: doc_ids[-1]]
        return self._get_process_element_indexes_list(ACTIVITY, doc_ids[0], doc_ids[-1])

    def GetDocumentActivityDataIndexes(self,
                                       document_name: str) -> list:

        #  retrieve ids of a document
        doc_ids = self.get_n_sample_of_a_document(document_name)

        return self._get_process_element_indexes_list(ACTIVITY_DATA, doc_ids[0], doc_ids[-1])

    def GetDocumentActorsIndexes(self,
                                 document_name: str) -> list:

        #  retrieve ids of a document
        doc_ids = self.get_n_sample_of_a_document(document_name)

        return self._get_process_element_indexes_list(ACTOR, doc_ids[0], doc_ids[-1])

    def GetDocumentFurtherSpecificationsIndexes(self,
                                                document_name: str) -> list:

        #  retrieve ids of a document
        doc_ids = self.get_n_sample_of_a_document(document_name)

        return self._get_process_element_indexes_list(FURTHER_SPECIFICATION, doc_ids[0], doc_ids[-1])

    def GetDocumentXORGatewaysIndexes(self,
                                      document_name: str) -> list:

        #  retrieve ids of a document
        doc_ids = self.get_n_sample_of_a_document(document_name)

        return self._get_process_element_indexes_list(XOR_GATEWAY, doc_ids[0], doc_ids[-1])

    def GetDocumentANDGatewaysIndexes(self,
                                      document_name: str) -> list:

        #  retrieve ids of a document
        doc_ids = self.get_n_sample_of_a_document(document_name)

        return self._get_process_element_indexes_list(AND_GATEWAY, doc_ids[0], doc_ids[-1])

    def GetDocumentConditionSpecificationsIndexes(self,
                                                  document_name: str) -> list:

        #  retrieve ids of a document
        doc_ids = self.get_n_sample_of_a_document(document_name)

        return self._get_process_element_indexes_list(CONDITION_SPECIFICATION, doc_ids[0], doc_ids[-1])


if __name__ == '__main__':
    tc = TokenClassification()
    doc_name = 'doc-1.1'
    print(tc.GetDocumentText(doc_name))
    print(tc.GetDocumentActivities(doc_name))
    print(tc.GetDocumentActivitiesIndexes(doc_name))
    print(tc.GetDocumentActivityData(doc_name))
    print(tc.GetDocumentActors(doc_name))
    print(tc.GetDocumentFurtherSpecifications(doc_name))
    print(tc.GetDocumentConditionSpecifications(doc_name))
    print(tc.GetDocumentXORGateways(doc_name))
    print(tc.GetDocumentANDGateways(doc_name))

    tc.GetSampleEntitiesIndexes(67)

    for doc_name in tc.GetDocumentNames():
        print(tc.GetDocumentText(doc_name))
        print(tc.GetDocumentActivities(doc_name))
        print()
