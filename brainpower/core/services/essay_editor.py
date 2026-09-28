import nltk
nltk.download('punkt_tab')


class EssayEditor: 
    """This class displays the body of text,  
         calculates: word and sentence counts
    """

    def __init__(self, text):
        self.text = text

    def get_sentence_count(self):
        sentences = nltk.tokenize.sent_tokenize(self.text)
        sentence_count = len(sentences)
        return sentence_count  

    def get_text(self):
        return self.text
        
    def get_word_count(self):
        words= nltk.tokenize.word_tokenize(self.text)
        words = [word for word in words if word.isalnum()]
        word_count= len(words)
        return word_count
