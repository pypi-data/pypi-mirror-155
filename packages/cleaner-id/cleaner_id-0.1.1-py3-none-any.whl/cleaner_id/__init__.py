import re
import string
from json import load
from os import getcwd
from . import slang_list

def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))

def remove_number(text):
    return re.sub(r'[0-9]', '', text)

def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  
        u"\U0001F300-\U0001F5FF"  
        u"\U0001F680-\U0001F6FF"  
        u"\U0001F1E0-\U0001F1FF"  
        u"\U00002500-\U00002BEF"  
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)

def remove_mention(text):
    return re.sub('@[^\s]+', '', text)

def remove_hashtag(text):
    return re.sub('#[^\s]+', '', text)

def remove_url(text):
    return re.sub(r'http\S+', '', text)

def remove_slang(text):
    slang_words = slang_list.slang_words
    return ' '.join([(slang_words[t] if t in slang_words.keys() else t) for t in text.split()])
