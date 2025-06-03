class FrequencyAnalyzer:
    def __init__(self, text):
        self.text = text.lower()
        self.frequency = {}
        self.bi_frequency = {}
        self.tri_frequency = {}
        self.w_frequency = {}

    def single_letter_frequency(self):
        self.frequency = {}
        for char in self.text:
            if char.isalpha():
                self.frequency[char] = self.frequency.get(char, 0) + 1
        return self.frequency
    
    def bigram_frequency(self):
        self.bi_frequency = {}
        for i in range(len(self.text) - 1):
            if self.text[i].isalpha() and self.text[i + 1].isalpha():
                bigram = self.text[i:i + 2]
                self.bi_frequency[bigram] = self.bi_frequency.get(bigram, 0) + 1
        return self.bi_frequency
    
    def trigram_frequency(self):
        self.tri_frequency = {}
        for i in range(len(self.text) - 2):
            if (self.text[i].isalpha() and 
                self.text[i + 1].isalpha() and 
                self.text[i + 2].isalpha()):
                trigram = self.text[i:i + 3]
                self.tri_frequency[trigram] = self.tri_frequency.get(trigram, 0) + 1
        return self.tri_frequency
    
    def word_frequency(self):
        self.w_frequency = {}
        words = self.text.split()
        for word in words:
            self.w_frequency[word] = self.w_frequency.get(word, 0) + 1
        return self.w_frequency
    
    def get_frequencies(self):
        self.single_letter_frequency()
        self.bigram_frequency()
        self.trigram_frequency()
        self.word_frequency()
        return self.frequency, self.bi_frequency, self.tri_frequency , self.w_frequency
    
    
class encryptor:
    def __init__(self, text="", key={}):
        self.text = text.lower()
        self.key = key
        self.encrypted_text = ""
        
    def encrypt(self):
        encrypted_text = ""
        for char in self.text:
            if char in self.key:
                encrypted_text += self.key[char]
            else:
                encrypted_text += char
        self.encrypted_text = encrypted_text
        return encrypted_text

class decryptor:
    def __init__(self, text="", key={}):
        self.key = key
        self.text = text.lower()
        self.decrypted_text = ""
        self.suggested_key = key
        
    def decrypt(self):
        decrypted_text = ""
        for char in self.text:
            if char in self.key:
                decrypted_text += self.key[char]
            else:
                decrypted_text += char
        self.decrypted_text = decrypted_text
        return decrypted_text
    
    def contrast_decrypt(self):
        decrypted_text = ""
        for char in self.text:
            if char in self.key:
                decrypted_text += self.key[char]
            else:
                decrypted_text += " "
        return decrypted_text
    
    def get_suggestions(self, key={}):
        self.suggested_key = key
        
    def add_suggestion(self, key, value):
        self.suggested_key[key] = value
        
    def accept_suggestion(self):
        for key in self.suggested_key:
            self.key[key] = self.suggested_key[key]
    
    def decrypt_with_suggestion(self):
        decrypted_text = ""
        for char in self.text:
            if char in self.key:
                decrypted_text += self.suggested_key[char]
            else:
                decrypted_text += char
        self.decrypted_text = decrypted_text
        return decrypted_text
    
    def transpose(self):
        transposed_key = {v: k for k, v in self.key.items()}
        self.key = transposed_key

class suggestion_generator:
    def __init__(self):
        self.suggestions = {}
        
    def check_vowels(self, text):
        vowels = "aeiouy"
        freq= 0
        words = text.split()
        for word in words:
            for char in word:
                if char in vowels:
                    freq += 1
        if freq != len(words):
            return freq / len(words)
        else:
            return 1
            
def encrypt(text, key):
    encryptor_instance = encryptor(text, key)
    return encryptor_instance.encrypt()

def decrypt(text, key):
    decryptor_instance = decryptor(text, key)
    return decryptor_instance.decrypt()

def contrast_decrypt(text, key):
    decryptor_instance = decryptor(text, key)
    return decryptor_instance.contrast_decrypt()
    
    
    
    
## test the functionality
if __name__ == "__main__":
    text = "Hello World! This is a test text for the frequency analysis."
    key = {
    'a': 'm', 'b': 'n', 'c': 'o', 'd': 'p', 'e': 'q',
    'f': 'r', 'g': 's', 'h': 't', 'i': 'u', 'j': 'v',
    'k': 'w', 'l': 'x', 'm': 'y', 'n': 'z', 'o': 'a',
    'p': 'b', 'q': 'c', 'r': 'd', 's': 'e', 't': 'f',
    'u': 'g', 'v': 'h', 'w': 'i', 'x': 'j', 'y': 'k',
    'z': 'l'
    }
    encryptor = encryptor(text, key)
    encrypted_text = encryptor.encrypt()
    print("Encrypted Text:", encrypted_text)
    decryptor = decryptor(encrypted_text, key)
    decryptor.transpose()
    decrypted_text = decryptor.decrypt()
    print("Decrypted Text:", decrypted_text)
    analyzer = FrequencyAnalyzer(text)
    frequency, bi_frequency, tri_frequency , word= analyzer.get_frequencies()
    print("Single Letter Frequency:", frequency)
    print("Bigram Frequency:", bi_frequency)    
    print("Trigram Frequency:", tri_frequency)
    print("Trigram Word Frequency:", word)