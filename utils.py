import json
import re
import string
from indicTrans.inference.engine import Model
from ai4bharat.transliteration import XlitEngine
from flair.models import TextClassifier
from flair.data import Sentence

with open('./eng_words_dictionary.json','r') as f:
    eng_dic = json.load(f)
    
class Hindi2English():
    def __init__(self):
        self.model = Model(expdir='./en-indic/indic-en')
    
    def translate(self,sent):
        return self.model.translate_paragraph(sent, 'hi', 'en')

class English2Hindi():
    def __init__(self):
        self.model = Model(expdir='./indic-en/en-indic')
    
    def translate(self,sent):
        return self.model.translate_paragraph(sent, 'en', 'hi')

hin_translator = English2Hindi()
en_translator = Hindi2English()
eng_to_hin_translit = XlitEngine("hi", beam_width=10)

def calc_eng_percent(sent):
    sent = sent.split(' ')
    num_word = len(sent)
    num_eng = 0
    for word in sent:
        if word in eng_dic.keys():
            num_eng += 1
    return num_eng*100/num_word

def translit_sentence(x):
    try:
        return eng_to_hin_translit.translit_sentence(x)['hi']
    except:
        return None
    
def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True
    
def calc_hindi_percent(sent):
    sent = sent.split(' ')
    num_word = len(sent)
    num_hin = 0
    for word in sent:
        if not isEnglish(word):
            num_hin += 1
    return num_hin*100/num_word

def translate_sentence(sent):
    try :
        return en_translator.translate(sent)
    except:
        return sent
    
def clean_sentences(sentences):
    sentences = re.sub(r'http\S+', '', sentences)
    sentences = re.sub(r'@\w+ ', '', sentences)
    new_sentences = []
    for x in re.split('[\n.|]',sentences):
        # strip whitespace
        x = x.strip()
        # remove punctuations
        x = x.translate(str.maketrans('', '',string.punctuation))
        # remove multiple white spaces
        x = re.sub("\s+"," ",x)
        if len(x)>0:
            new_sentences.append(x)
    return "\n".join(new_sentences).lower()

language_threshold = 80
def final_transliteration(sentence):
    clean_sent = clean_sentences(sentence)
    this_eng_percent = []
    this_hindi_percent = []
    this_transliteration = []
    this_translation = []
    for sent in clean_sent.split('\n'):
        hin_per = calc_hindi_percent(sent)
        en_per = calc_eng_percent(sent)
        this_eng_percent.append(en_per)
        this_hindi_percent.append(hin_per)
        if en_per >= language_threshold:
            this_transliteration.append(translit_sentence(sent))
            this_translation.append(sent)
        elif  hin_per >= language_threshold:
            this_transliteration.append(sent)
            this_translation.append(sent)
        else:
            trans = translit_sentence(sent)
            this_transliteration.append(trans)
            this_translation.append(translate_sentence(trans))
    
    dic = {
        "translation" : "\n".join(this_translation),
        "transliteration" : "\n".join(this_transliteration),
        "eng_percent" : sum(this_eng_percent)/len(this_eng_percent),
        "hindi_percent" : sum(this_hindi_percent)/len(this_hindi_percent)
    }
    return dic

def flair_prediction(x):
    sia = TextClassifier.load('en-sentiment')
    prediction = {}
    sentence = Sentence(x)
    sia.predict(sentence)
    score = sentence.labels[0]
    score = str(score).split('→')[-1]
    val = float(score.split('(')[-1].split(')')[0])
    prediction["score"] = val
    if "POSITIVE" in str(score):
        prediction["sentiment"] = "positive"
    elif "NEGATIVE" in str(score):
        prediction["sentiment"] = "negative"
    else:
        prediction["sentiment"] = "neutral"
    return prediction
