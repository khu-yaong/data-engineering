class Word :

    words = []

    def __init__(self, word, url) :
        self.word = word
        self.url = url
        self.description = ""
    
    def setDescription(self, tag) :
        description = tag.text.strip()
        self.description += f"{description}\n"

    def toDict(self) :
        return {
            "word" : self.word,
            "url" : self.url,
            "description" : self.description
        }

    def __str__(self) :
        return f"{self.word} : {self.description} ({self.url})"
    