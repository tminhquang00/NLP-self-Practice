from googletrans import Translator
from random import randrange


def translate(text, from_lang, to_lang):
    '''
    Translate text from some language to another using google trans api
    '''
    translator = Translator()
    tranlated = translator.translate(text,src=from_lang, dest=to_lang)
    return tranlated.text



def get_tranlated_text(text):
    '''
    Randomly translate another text to other languge and translate back to augment data
    '''
    lang_list = ['ja', 'vi', 'ar'] # japan, vietnamese, arabic
    lang = lang_list[randrange(3)]
    buf_text = translate(text, 'en', lang)
    return translate(buf_text, lang, 'en')


def augmented_data_using_translation(questions, labels, answers):
    '''
    agumented data  
    '''
    new_q = []
    new_l = []
    new_a = []
    for q, l, a in zip(questions, labels, answers):
        new_question = get_tranlated_text(q)
        new_q.append(new_question)
        new_l.append(l)
        new_a.append(a)
        
    questions = questions + new_q
    labels = labels + new_l
    answers = answers + new_a
    return questions, labels, answers