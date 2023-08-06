#  Matching strategy
WORD_BASED_STRATEGY = 'word-based'
INDEX_BASED_STRATEGY = 'index-based'

#  Relations Extraction task labels
SOURCE_SENTENCE_ID = 'source-head-sentence-ID'
SOURCE_HEAD_TOKEN_ID = 'source-head-word-ID'
SOURCE_ENTITY_TYPE = 'source-entity-type'
SOURCE_ENTITY = 'source-entity'

TARGET_SENTENCE_ID = 'target-head-sentence-ID'
TARGET_HEAD_TOKEN_ID = 'target-head-word-ID'
TARGET_ENTITY_TYPE = 'target-entity-type'
TARGET_ENTITY = 'target-entity'

#  Process Elements labels
ACTIVITY = 'Activity'
"""
Constant for labeling  ``Activity`` process element
"""
ACTIVITY_DATA = 'Activity Data'
"""
Constant for labeling  ``Activity Data'' process element
"""
ACTOR = 'Actor'
"""
Constant for labeling  ``Actor'' process element
"""
FURTHER_SPECIFICATION = 'Further Specification'
"""
Constant for labeling  ``Further Specification'' process element
"""
XOR_GATEWAY = 'XOR Gateway'
"""
Constant for labeling  ``Xor Gateway'' process element
"""
AND_GATEWAY = 'AND Gateway'
"""
Constant for labeling  ``And Gateway'' process element
"""
CONDITION_SPECIFICATION = 'Condition Specification'
"""
Constant for labeling  ``Condition Specification'' process element
"""

PROCESS_ELEMENT_LABELS = [ACTIVITY,
                          ACTIVITY_DATA,
                          ACTOR,
                          FURTHER_SPECIFICATION,
                          XOR_GATEWAY,
                          AND_GATEWAY,
                          CONDITION_SPECIFICATION]
"""
List of process element labels
"""

#  Relation labels
USES = 'uses'
"""
Constant for labeling  ``uses'' relation
"""
FURTHER_SPECIFICATION_RELATION = 'further specification'
"""
Constant for labeling  ``further specification'' relation
"""
ACTOR_PERFORMER = 'actor performer'
"""
Constant for labeling  ``actor performer'' relation
"""
ACTOR_RECIPIENT = 'actor recipient'
"""
Constant for labeling  ``actor recipient'' relation
"""
FLOW = 'flow'
"""
Constant for labeling  ``sequence flow'' relation
"""
SAME_GATEWAY = 'same gateway'
"""
Constant for labeling  ``same gateway'' relation
"""
RELATIONS_EXTRACTION_LABELS = [USES,
                               FURTHER_SPECIFICATION_RELATION,
                               ACTOR_PERFORMER,
                               ACTOR_RECIPIENT,
                               FLOW,
                               SAME_GATEWAY]
"""
List of process relations labels
"""
#  Statistics
PER_CLASS_STATISTICS = 'per-class-statistics'
OVERALL_STATISTICS = 'overall-statistics'

TRUE_POSITIVE = 'true-positive'
FALSE_POSITIVE = 'false-positive'
TRUE_NEGATIVE = 'true-negative'
FALSE_NEGATIVE = 'false-negative'

PRECISION = 'precision'
RECALL = 'recall'
F1SCORE = 'f1-score'
SUPPORT = 'supports'

MICRO_STATISTICS = 'micro-statistics'
MACRO_STATISTICS = 'macro-statistics'
AVERAGE_STATISTICS = 'average-statistics'

#  Macro statistics
MACRO_PRECISION = 'macro-precision'
MACRO_RECALL = 'macro-recall'
MACRO_F1SCORE = 'macro-f1'

#  Average statistics
AVERAGE_PRECISION = 'average-precision'
AVERAGE_RECALL = 'average-recall'
AVERAGE_F1SCORE = 'average-f1'

#  Micro statistics
MICRO_PRECISION = 'micro-precision'
MICRO_RECALL = 'micro-recall'
MICRO_F1SCORE = 'micro-f1'