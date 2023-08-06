import re

SPECIAL_CHARS = {'Ä': 'A', 'ä': 'a', 'Ë': 'E', 'ë': 'e', 'Ï': 'I', 'ï': 'i', 'Ö': 'O', 'ö': 'o', 'Ü': 'U', 'ü': 'u', 'ß': 'ss', 'À': 'A', 'à': 'a', 'Á': 'A', 'á': 'a', 'Â': 'A', 'â': 'a',
                 'Ç': 'C', 'ç': 'c', 'È': 'E', 'è': 'e', 'É': 'E', 'é': 'e', 'Ê': 'E', 'ê': 'e', 'Ñ': 'N', 'ñ': 'n', 'Ò': 'O', 'ò': 'o', 'Ó': 'O', 'ó': 'o', 'Ô': 'O', 'ô': 'o', 'õ': 'o', 'Ÿ': 'Y', 'ÿ': 'y'}

class cleaner:
    def __init__(self, text: str = ""):
        self.text = text
        self.text = self.text.strip()
        self.remove_blanks()
        self.remove_special_chars()

    def remove_blanks(self):
        self.text = re.sub('[ \t\n]+', ' ', self.text)

    def remove_special_chars(self):
        for s in self.text:
            if s in SPECIAL_CHARS:
                self.text = self.text.replace(s, SPECIAL_CHARS[s])