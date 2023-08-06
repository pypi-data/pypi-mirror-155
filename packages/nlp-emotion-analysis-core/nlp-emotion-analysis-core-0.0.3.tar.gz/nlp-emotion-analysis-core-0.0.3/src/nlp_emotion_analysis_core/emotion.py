"""
Date: 3/4/2020 11:55 AM
Author: Achini
"""

import pickle, os
from .core.emotions import emotion_extractor as emotion_extractor
from .utils import text_processor as text_utils
from .core.summary import keyphrase_extractor as keyphrase_extractor
from .core.clinical_info import clinical_info_extractor as clinical_info_extractor


def load_emotion_dictionaries():
    with open(os.path.dirname(__file__)+'/models/emotions/emotions_plutchik.pkl', 'rb') as f:
        EMOTION_MAP = pickle.load(f)
    with open(os.path.dirname(__file__)+'/models/emotions/intensifier_vocab_v2.pkl', 'rb') as f:
        INTENSIFIER_MAP = pickle.load(f)
    with open(os.path.dirname(__file__)+'/models/emotions/negation_vocab_v2.pkl', 'rb') as f:
        NEGATION_MAP = pickle.load(f)
    with open(os.path.dirname(__file__)+'/models/clinical_info/physical.pkl', 'rb') as f:
        PHYSICAL = pickle.load(f)

    EMO_RESOURCES = {'EMOTIONS': EMOTION_MAP,
                     'NEGATION': NEGATION_MAP,
                     'INTENSIFIERS': INTENSIFIER_MAP,
                     'PHYSICAL': PHYSICAL}

    return EMO_RESOURCES


EMO_RESOURCES = load_emotion_dictionaries()
if __name__ == '__main__':
    text_1 = 'still i feel very sad about the unexpected incident. hopefully the pain will be less, and i am grateful for..'
    clean_text_1 = text_utils.clean_text(text_1)
    emotion_profile, emo_seq = emotion_extractor.get_emotion_profile_per_post(clean_text_1, EMO_RESOURCES)
    clinical_info = clinical_info_extractor.get_physical_sym_profile(clean_text_1, EMO_RESOURCES)
    keyphrases = keyphrase_extractor.analyze_keyphrases(clean_text_1)

    print(keyphrases)
    print(clinical_info)
    print(emotion_profile)

def get_emotion_profile_per_post(post):
    return emotion_extractor.get_emotion_profile_per_post(text_utils.clean_text(post), EMO_RESOURCES)
def get_physical_sym_profile(post):
    return clinical_info_extractor.get_physical_sym_profile(text_utils.clean_text(post), EMO_RESOURCES)
def analyze_keyphrases(post):
    return keyphrase_extractor.analyze_keyphrases(text_utils.clean_text(post))
