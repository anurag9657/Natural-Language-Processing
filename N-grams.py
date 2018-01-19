import operator
import string
import functools
import nltk
from nltk.corpus import udhr
from nltk import collections, ngrams
from nltk.tokenize import RegexpTokenizer

import re

def remove_nonwords(string):
    string = re.sub(u"[ùúûü]", 'u', string)
    string = re.sub(u"[àáâãäå]", 'a', string)
    string = re.sub(u"[ýÿ]", 'y', string)
    string = re.sub(u"[ìíîï]", 'i', string)
    string = re.sub(u"[òóôõö]", 'o', string)
    string = re.sub(u"[èéêë]", 'e', string)
    return string

english = remove_nonwords(udhr.raw('English-Latin1').lower())
french = remove_nonwords(udhr.raw('French_Francais-Latin1').lower())
italian = remove_nonwords(udhr.raw('Italian_Italiano-Latin1').lower())
spanish = remove_nonwords(udhr.raw('Spanish_Espanol-Latin1').lower())

english_train = english[0:1000]
english_dev = english[1000:1100]
english_test = remove_nonwords(udhr.raw('English-Latin1')).lower()[0:1000]
french_train = french[0:1000]
french_dev = french[1000:1100]
french_test = remove_nonwords(udhr.raw('French_Francais-Latin1')).lower()[0:1000]
italian_train = italian[0:1000]
italian_dev = italian[1000:1100]
italian_test = remove_nonwords(udhr.raw('Italian_Italiano-Latin1')).lower()[0:1000]
spanish_train = spanish[0:1000]
spanish_dev = spanish[1000:1100]
spanish_test = remove_nonwords(udhr.raw('Spanish_Espanol-Latin1')).lower()[0:1000]

#tokanizing test set
tokenizer = nltk.RegexpTokenizer(r'\w+')
english_test_tokenized = tokenizer.tokenize(english_test)
french_test_tokenized = tokenizer.tokenize(french_test)
italian_test_tokenized = tokenizer.tokenize(italian_test)
spanish_test_tokenized = tokenizer.tokenize(spanish_test)

#calculate n-gram model. Specify n to find unigram/bigram/trigram

def word2ngrams(text, n, exact=True):
    return ["".join(j) for j in zip(*[text[i:] for i in range(n)])]

english_uni = word2ngrams(english_train,1)
english_bi = word2ngrams(english_train,2)
english_tri = word2ngrams(english_train,3)
print("Unigram for English:",english_uni)
print("Bigram for English:",english_bi)
print("Trigram for English:",english_tri)
print("\n")

french_uni = word2ngrams(french_train,1)
french_bi = word2ngrams(french_train,2)
french_tri = word2ngrams(french_train,3)
print("Unigram for French:",french_uni)
print("Bigram for French:",french_bi)
print("Trigram for French:",french_tri)
print("\n")

italian_uni = word2ngrams(italian_train,1)
italian_bi = word2ngrams(italian_train,2)
italian_tri = word2ngrams(italian_train,3)
print("Unigram for Italian:",italian_uni)
print("Bigram for Italian:",italian_bi)
print("Trigram for Italian:",italian_tri)
print("\n")

spanish_uni = word2ngrams(spanish_train,1)
spanish_bi = word2ngrams(spanish_train,2)
spanish_tri = word2ngrams(spanish_train,3)
print("Unigram for Spanish:",spanish_uni)
print("Bigram for Spanish:",spanish_bi)
print("Trigram for Spanish:",spanish_tri)
print("\n")

# Remove Punctuation
translator = str.maketrans('', '', string.punctuation)
english = re.sub('\s+',' ',english.translate(translator))
french = re.sub('\s+',' ',french.translate(translator))
italian = re.sub('\s+',' ',italian.translate(translator))
spanish = re.sub('\s+',' ',spanish.translate(translator))

# Calculate frequency for unigram model
eng_uni_freq = nltk.FreqDist(english_uni)
fre_uni_freq = nltk.FreqDist(french_uni)
ita_uni_freq = nltk.FreqDist(italian_uni)
spa_uni_freq = nltk.FreqDist(spanish_uni)

english_char = [ch for ch in english_train]
french_char = [ch for ch in french_train]
italian_char = [ch for ch in italian_train]
spanish_char = [ch for ch in spanish_train]

# Calculate frequency for bigram model
eng_bi_freq = nltk.FreqDist(nltk.bigrams([' '] + english_char))
fre_bi_freq = nltk.FreqDist(nltk.bigrams([' '] + french_char))
ita_bi_freq = nltk.FreqDist(nltk.bigrams([' '] + italian_char))
spa_bi_freq = nltk.FreqDist(nltk.bigrams([' '] + spanish_char))

# Calculate frequency for trigram model
eng_tri_freq = nltk.FreqDist(ngrams([' ', ' '] + english_char,3))
fre_tri_freq = nltk.FreqDist(ngrams([' ', ' '] + french_char,3))
ita_tri_freq = nltk.FreqDist(ngrams([' ', ' '] + italian_char,3))
spa_tri_freq = nltk.FreqDist(ngrams([' ', ' '] + spanish_char,3))


# Calculate Probability
def calc_prob(u_model, b_model, t_model, data):
    unigram_word_probs = collections.defaultdict(int)
    bigram_word_probs = collections.defaultdict(int)
    trigram_word_probs = collections.defaultdict(int)
    last_last_c = ' '
    for word in data:
        last_c = ' '
        u_word_prob = []
        b_word_prob = []
        t_word_prob = []
        b_model[(' ', ' ')] = len(data)
        for c in list(word):
            try:
                u_word_prob.append(u_model.get(c) / sum(u_model.values()))
            except:
                u_word_prob.append(0)
            try:
                b_word_prob.append(b_model.get((last_c, c)) / u_model.get(last_c))
            except:
                b_word_prob.append(0)
            try:
                t_word_prob.append(t_model.get((last_last_c, last_c, c)) / b_model.get((last_last_c, last_c)))
            except:
                t_word_prob.append(0)

            last_last_c = last_c
            last_c = c
        # end-for
        last_last_c = c

        # Calculating Perplexity
        unigram_word_probs[word] = (functools.reduce(operator.mul, u_word_prob, 1)) ** (1 / len(u_word_prob))
        bigram_word_probs[word] = (functools.reduce(operator.mul, b_word_prob, 1)) ** (1 / len(b_word_prob))
        trigram_word_probs[word] = (functools.reduce(operator.mul, t_word_prob, 1)) ** (1 / len(t_word_prob))
        # end-for
    return (unigram_word_probs, bigram_word_probs, trigram_word_probs)


# Word prediction
def compare_models(model1, model2):
    compared = ['m1' if m1 > m2 else 'm2' for m1, m2 in zip(model1.values(), model2.values())]
    comp_freq = nltk.FreqDist(compared)
    return comp_freq.get('m1') / sum(comp_freq.values()) * 100

print("English Vs French Model")
eng_uni_model, eng_bi_model, eng_tri_model = calc_prob(eng_uni_freq, eng_bi_freq, eng_tri_freq, english_test_tokenized)
fre_uni_model, fre_bi_model, fre_tri_model = calc_prob(fre_uni_freq, fre_bi_freq, fre_tri_freq, english_test_tokenized)

print("English Unigram Model Accuracy :", compare_models(eng_uni_model, fre_uni_model))
print("English Bigram Model Accuracy :", compare_models(eng_bi_model, fre_bi_model))
print("English Trigram Model Accuracy :", compare_models(eng_tri_model, fre_tri_model), "\n")

print("\n")
print("Spanish Vs Italian")
spa_uni_prob, spa_bi_prob, spa_tri_prob = calc_prob(spa_uni_freq, spa_bi_freq, spa_tri_freq, spanish_test_tokenized)
ita_uni_prob, ita_bi_prob, ita_tri_prob = calc_prob(ita_uni_freq, ita_bi_freq, ita_tri_freq, spanish_test_tokenized)

print("Spanish Unigram Model Accuracy :", compare_models(spa_uni_prob, ita_uni_prob))
print("Spanish Bigram Model Accuracy :", compare_models(spa_bi_prob, ita_bi_prob))
print("Spanish Trigram Model Accuracy :", compare_models(spa_tri_prob, ita_tri_prob), "\n")
