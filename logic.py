from collections import defaultdict
from translate import Translator

class TextAnalysis():   
    memory = defaultdict(list)
    
    questions = {
        'как тебя зовут': "Я супер-крутой-бот и мое предназначение помогать тебе!",
        'сколько тебе лет': "Это слишком философский вопрос",
        'привет': "Привет! Я бот-переводчик!",
        'hello': "Hello! I'm translation bot!",
        'что ты умеешь': "Перевожу текст с русского на английский и наоборот!",
        'what can you do': "I translate text from Russian to English and vice versa!"
    }
    
    def __init__(self, text, user_id):
        self.text = text
        
        if self.__is_russian(text):
            self.translation = self.__translate(text, "ru", "en")
        else:
            self.translation = self.__translate(text, "en", "ru")
        
        if self.text.lower() in self.questions.keys():
            self.response = self.questions[self.text.lower()]  #
        else:
            self.response = self.get_answer()  
        
        TextAnalysis.memory[user_id].append(self)
    
    def __is_russian(self, text):
        russian = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        text_lower = text.lower()
        for char in text_lower:
            if char in russian:
                return True
        return False
    
    def __translate(self, text, from_lang, to_lang):
        try:
            translator = Translator(from_lang=from_lang, to_lang=to_lang)
            return translator.translate(text)
        except:
            return "Ошибка перевода"
    
    def get_answer(self):
        return "Я пока не знаю что ответить на это. Попробуй спросить что-то другое!"