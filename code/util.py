import nltk

nltk.data.path.append('./my_nltk_data')

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
            elif char.isalpha():
                decrypted_text += "_"
            else:
                decrypted_text += char
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
                    break
        if freq != len(words):
            return f"元音单词百分比：{freq/len(words)*100:.2f}%"
        else:
            return "所有单词都包含元音字母"
    
    def seperate_letters(self, text):
        analyzer = FrequencyAnalyzer(text)
        single_freq = analyzer.single_letter_frequency()
        total_letters = sum(single_freq.values())
        freq_percent = {letter: (count / total_letters)  for letter, count in single_freq.items()}
        tier_1=[];tier_2=[];tier_3=[];tier_4=[]
        for letter, percent in freq_percent.items():
            if percent > 0.1:
                tier_1.append((letter,percent))
            elif percent > 0.05:
                tier_2.append((letter,percent))
            elif percent > 0.01:
                tier_3.append((letter,percent))
            else:
                tier_4.append((letter,percent))
        tier ={
            "tier_1": (tier_1,">10%"),
            "tier_2": (tier_2,">5%"),
            "tier_3": (tier_3,">1%"),
            "tier_4": (tier_4,"<1%")
        }
        return tier
    

from nltk.corpus import words
# 提取英文单词词典并转换为小写集合，提高查询效率
english_words = set(word.lower() for word in words.words())
def check_short_words_validity(cipher_text, key):
    """
    检查密文中的短词（1-3字母）在解密后是否为有效英文单词
    返回一个包含(原词, 解密词, 是否有效)的列表
    """
    decryptor_instance = decryptor(cipher_text, key)
    decrypted_text = decryptor_instance.decrypt()
    words_list = decrypted_text.split()
    total = 0
    count = 0
    result = []
    for i, word in enumerate(words_list):
        word = word.strip('.,!?;:"()[]{}')
        if 1 <= len(word) <= 4:
            total += 1
            is_valid = word.lower() in english_words
            count += is_valid
            if not is_valid:
                result.append((word, i))
    return result, total, count

def suggest_vowels(text,key):
    generator = suggestion_generator()
    decryptor_instance = decryptor(text, key)
    decrypted_text = decryptor_instance.decrypt()
    return generator.check_vowels(decrypted_text)

def suggest_by_word_frequency(text):
    suggest = suggestion_generator()
    return suggest.seperate_letters(text)
        
        
            
def encrypt(text, key):
    encryptor_instance = encryptor(text, key)
    return encryptor_instance.encrypt()

def decrypt(text, key):
    decryptor_instance = decryptor(text, key)
    return decryptor_instance.decrypt()

def contrast_decrypt(text, key):
    decryptor_instance = decryptor(text, key)
    return decryptor_instance.contrast_decrypt()

def letter_frequency(text):
    analyzer = FrequencyAnalyzer(text)
    freq = analyzer.single_letter_frequency()
    total_letters = sum(freq.values())
    freq_percent = {letter: (count / total_letters) for letter, count in freq.items()}
    return freq_percent
    
def bigram_frequency(text):
    analyzer = FrequencyAnalyzer(text)
    bi_freq = analyzer.bigram_frequency()
    return bi_freq

def trigram_frequency(text):
    analyzer = FrequencyAnalyzer(text)
    tri_freq = analyzer.trigram_frequency()
    return tri_freq

def word_frequency(text):   
    analyzer = FrequencyAnalyzer(text)
    w_freq = analyzer.word_frequency()
    return w_freq

def generate_assist_suggestions(text, key):
    return "haven't implemented yet"

    


    
    
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
    nltk.data.path.append('./my_nltk_data')  # 添加路径到查找列表
    nltk.download('words', download_dir='./my_nltk_data')  # 下载到指定位置