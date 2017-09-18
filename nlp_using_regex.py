import nltk as n
import re
from nltk.corpus import stopwords
from nltk.stem import *
from nltk.tokenize import RegexpTokenizer
from collections import Counter

# problem 1
# a)
funny = 'colorless green ideas sleep furiously';
print(funny.split())

# b)
seq = '';
funny = funny.split()
for word in funny:
    seq += (word[1])
print(seq)

# c)
phrases = funny[0:3]
print(phrases)

# d)
new_phrases = ' '
print(new_phrases.join(phrases))

# e)
funny1 = sorted(funny)
for word in funny1:
    print(word)


# Problem 2

def split_sent(str1):
    counts = dict()
    words = str1.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    for key in sorted(counts):
        print("%s: %s" % (key, counts[key]))


var = input("Please enter a sentence: ")
split_sent(var.lower())

# Problem 3
# a) \b(an|a|the)\b
# b) (\d+)([+\-*/]\d+)*

# Problem 4
str = """
... austen-emma.txt:hart@vmd.cso.uiuc.edu (internet) hart@uiucvmd (bitnet)
... austen-emma.txt:Internet (72600.2026@compuserve.com); TEL: (212-254-5093) .
.. austen-persuasion.txt:Editing by Martin Ward (Martin.Ward@uk.ac.durham)
... blake-songs.txt:Prepared by David Price, email ccx074@coventry.ac.uk
... """

emails = n.re.findall(r'[\w\.-]+@[\w\.-]+', str)
for email in emails:
    # do something with each found email string
    print(email)

# Problem 5

test_str = open('books.txt', 'r').read()

def eliminate_duplicate(test_txt):
    regex = r"^(.*?)$\s+?^(?=.*^\1$)"
    subst = ""
    result = re.sub(regex, subst, test_str, 0, re.MULTILINE | re.DOTALL)
    return result


result = eliminate_duplicate(test_str)
out = open('books1.txt', 'w+')
out.write(result)
out.close()

# Problem 7 a)
OBAMA = []
ROMNEY = []
LEHRER = []

LEHRER.append('LEHRER:')
OBAMA.append('OBAMA:')
ROMNEY.append('ROMNEY:')

test_str = open('debate.txt', 'r').read()
out = open('debate11.txt', 'w')

# Regex to remove Crosstalk and audience behavior
regex_remove = r"\(CROSSTALK\)|\(APPLAUSE\)|\(inaudible\)|\(LAUGHTER\)"
subst = ""
test_str = re.sub(regex_remove, subst, test_str, 0, re.MULTILINE | re.DOTALL)

# regex to identify sentences spoken by Rmoney
regex = r"(?<=LEHRER:)(.*?)(?=OBAMA:|ROMNEY:|LEHRER:|© COPYRIGHT)"

matches = re.finditer(regex, test_str, re.MULTILINE | re.DOTALL)

for matchNum, match in enumerate(matches):
    matchNum = matchNum + 1

    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        LEHRER.append(match.group(1))

# out.writelines("%s\n" % l for l in LEHRER)
out.writelines(LEHRER)
out.writelines("\n")

regex1 = r"(?<=OBAMA:)(.*?)(?=OBAMA:|ROMNEY:|LEHRER:)"

matches1 = re.finditer(regex1, test_str, re.MULTILINE | re.DOTALL)

for matchNum, match in enumerate(matches1):
    matchNum = matchNum + 1

    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        OBAMA.append(match.group(1))

out.writelines(OBAMA)
out.writelines("\n")

regex2 = r"(?<=ROMNEY:)(.*?)(?=OBAMA:|ROMNEY:|LEHRER:)"

matches2 = re.finditer(regex2, test_str, re.MULTILINE | re.DOTALL)

for matchNum, match in enumerate(matches2):
    matchNum = matchNum + 1

    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        ROMNEY.append(match.group(1))

out.writelines(ROMNEY)
out.close()

# Problem 7 b)

# for lehrer
test_str = ' '.join(LEHRER)

# remove punctuation
test_str = re.sub(r'[^\w\s]', '', test_str)

# remove capitalization
for f in re.findall("([A-Z]+)", test_str):
    test_str = test_str.replace(f, f.lower())

# remove stop words
pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
test_str = pattern.sub('', test_str)

# tokenize the words
tokenizer = RegexpTokenizer(r'\w+')
test_str = tokenizer.tokenize(test_str)

print("\nFor Lehrer:\n")
# apply porter stemmer
stemmer = PorterStemmer()
port_stem = [stemmer.stem(prt) for prt in test_str]

print("Porter Stemmer:", ' '.join(port_stem))

# apply snowball stemmer
stemmer = SnowballStemmer("english")
snow_stem = [stemmer.stem(snows) for snows in test_str]
print("Snowball Stemmer:", ' '.join(snow_stem))

# apply lancaster stemmer
stemmer = LancasterStemmer()
lanc_stem = [stemmer.stem(lanc) for lanc in test_str]
print("Lancaster Stemmer:", ' '.join(lanc_stem))

# for obama
test_str1 = ' '.join(OBAMA)

# remove punctuation
test_str1 = re.sub(r'[^\w\s]', '', test_str1)

# remove capitalization
for f in re.findall("([A-Z]+)", test_str1):
    test_str1 = test_str1.replace(f, f.lower())

# remove stop words
pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
test_str1 = pattern.sub('', test_str1)

# tokenize the words
tokenizer = RegexpTokenizer(r'\w+')
test_str1 = tokenizer.tokenize(test_str1)

print("\nFor Obama:\n")
# apply porter stemmer
stemmer = PorterStemmer()
port_stem1 = [stemmer.stem(prt) for prt in test_str1]
print("Porter Stemmer:", ' '.join(port_stem1))

# apply snowball stemmer
stemmer = SnowballStemmer("english")
snow_stem1 = [stemmer.stem(snows) for snows in test_str1]
print("Snowball Stemmer:", ' '.join(snow_stem1))

# apply lancaster stemmer
stemmer = LancasterStemmer()
lanc_stem1 = [stemmer.stem(lanc) for lanc in test_str1]
print("Lancaster Stemmer:", ' '.join(lanc_stem1))

# for romney
test_str2 = ' '.join(ROMNEY)

# remove punctuation
test_str2 = re.sub(r'[^\w\s]', '', test_str2)

# remove capitalization
for f in re.findall("([A-Z]+)", test_str2):
    test_str2 = test_str2.replace(f, f.lower())

# remove stop words
pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
test_str2 = pattern.sub('', test_str2)

# tokenize the words
tokenizer = RegexpTokenizer(r'\w+')
test_str2 = tokenizer.tokenize(test_str2)

print("\nFor Romney:\n")
# apply porter stemmer
stemmer = PorterStemmer()
port_stem2 = [stemmer.stem(prt) for prt in test_str2]
print("Porter Stemmer:", ' '.join(port_stem2))

# apply snowball stemmer
stemmer = SnowballStemmer("english")
snow_stem2 = [stemmer.stem(snows) for snows in test_str2]
print("Snowball Stemmer:", ' '.join(snow_stem2))

# apply lancaster stemmer
stemmer = LancasterStemmer()
lanc_stem2 = [stemmer.stem(lanc) for lanc in test_str2]
print("Lancaster Stemmer:", ' '.join(lanc_stem2))

# Problem 7 c)

# 10 most frequent words by lehrer
leh_port = []
leh_snow = []
leh_lanc = []
cap_words = [word.lower() for word in port_stem]
word_counts = Counter(cap_words)
count = 0
for key in sorted(word_counts, key=word_counts.get, reverse=True):
    if count < 10:
        leh_port.append(key)
    count += 1

cap_words = [word.lower() for word in snow_stem]
word_counts = Counter(cap_words)
count = 0
for key in sorted(word_counts, key=word_counts.get, reverse=True):
    if count < 10:
        leh_snow.append(key)
    count += 1

cap_words = [word.lower() for word in lanc_stem]
word_counts = Counter(cap_words)
count = 0
for key in sorted(word_counts, key=word_counts.get, reverse=True):
    if count < 10:
        leh_lanc.append(key)
    count += 1

print("\n10 most frequent words by Lehrer")
print("Porter stemmer:", leh_port)
print("Snowball stemmer:", leh_snow)
print("Lancaster stemmer:", leh_lanc)

# 10 most frequent words by obama
oba_port = []
oba_snow = []
oba_lanc = []
cap_words = [word.lower() for word in port_stem1]
word_counts = Counter(cap_words)
count = 0
for key in sorted(word_counts, key=word_counts.get, reverse=True):
    if count < 10:
        oba_port.append(key)
    count += 1

cap_words = [word.lower() for word in snow_stem1]
word_counts = Counter(cap_words)
count = 0
for key in sorted(word_counts, key=word_counts.get, reverse=True):
    if count < 10:
        oba_snow.append(key)
    count += 1

cap_words = [word.lower() for word in lanc_stem1]
word_counts = Counter(cap_words)
count = 0
for key in sorted(word_counts, key=word_counts.get, reverse=True):
    if count < 10:
        oba_lanc.append(key)
    count += 1

print("\n10 most frequent words by Obama")
print("Porter stemmer:", oba_port)
print("Snowball stemmer:", oba_snow)
print("Lancaster stemmer:", oba_lanc)

# 10 most frequent words by romney
rom_port = []
rom_snow = []
rom_lanc = []
cap_words = [word.lower() for word in port_stem2]
word_counts = Counter(cap_words)
count = 0
for key in sorted(word_counts, key=word_counts.get, reverse=True):
    if count < 10:
        rom_port.append(key)
    count += 1

cap_words = [word.lower() for word in snow_stem2]
word_counts = Counter(cap_words)
count = 0
for key in sorted(word_counts, key=word_counts.get, reverse=True):
    if count < 10:
        rom_snow.append(key)
    count += 1

cap_words = [word.lower() for word in lanc_stem2]
word_counts = Counter(cap_words)
count = 0
for key in sorted(word_counts, key=word_counts.get, reverse=True):
    if count < 10:
        rom_lanc.append(key)
    count += 1

print("\n10 most frequent words by Romney")
print("Porter stemmer:", rom_port)
print("Snowball stemmer:", rom_snow)
print("Lancaster stemmer:", rom_lanc)

# Problem 7 d)
print("\nPorter stemmer to stem positive words:")
positive_str = open('positive.txt', 'r').read()
stemmer = PorterStemmer()
post_stem = [stemmer.stem(prt) for prt in positive_str]
positive_stem = ''.join(post_stem)
print(positive_stem)

# Problem 7 e)

# For Lehrer
print("10 most positive words used by Lehrer:")
port_output = ' '.join(port_stem)
elem1 = [x for x in port_output.split()]
elem2 = [x for x in positive_stem.split()]

elem3 = []

for item in elem1:
    if item in elem2:
        elem3.append(item)

cap_words = [word.lower() for word in elem3]
word_counts = Counter(cap_words)
count = 0
elem6 = []
for key in sorted(word_counts, key=word_counts.get, reverse=True):
    # print(key, word_counts[key])
    if count < 10:
        elem6.append(key)
    count += 1

print(elem6)

# For Obama
print("10 most positive words used by Obama:")
port_output1 = ' '.join(port_stem1)
elem1 = [x for x in port_output1.split()]
elem2 = [x for x in positive_stem.split()]

elem4 = []

for item in elem1:
    if item in elem2:
        elem4.append(item)

cap_words = [word.lower() for word in elem4]
word_counts = Counter(cap_words)
count = 0
elem7 = []
for key in sorted(word_counts, key=word_counts.get, reverse=True):

    if count < 10:
       #print(key, word_counts[key])
        elem7.append(key)
    count += 1

print(elem7)

# For Romney

print("10 most positive words used by Romney:")
port_output2 = ' '.join(port_stem2)

elem1 = [x for x in port_output2.split()]
elem2 = [x for x in positive_stem.split()]

elem5 = []

for item in elem1:
    if item in elem2:
        elem5.append(item)

cap_words = [word.lower() for word in elem5]
word_counts = Counter(cap_words)
count = 0
elem8 = []
for key in sorted(word_counts, key=word_counts.get, reverse=True):

    if count < 10:
        #print(key, word_counts[key])
        elem8.append(key)
    count += 1

print(elem8)
