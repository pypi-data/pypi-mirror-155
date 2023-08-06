import re
import string

def remove_punctuatuion(text):
    return text.translate(str.maketrans('', '', string.punctuation))
