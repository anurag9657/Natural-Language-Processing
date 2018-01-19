import gensim
import logging
import pprint
from gensim.scripts.glove2word2vec import glove2word2vec


glove_input_file = 'glove.6B.50d.txt'
word2vec_output_file = 'glove.6B.50d.txt.word2vec'
glove2word2vec(glove_input_file, word2vec_output_file)


model = gensim.models.KeyedVectors.load_word2vec_format('glove.6B.50d.txt.word2vec', binary=False)
# for logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
print(' \n')

model.accuracy('test1.txt')
print(' \n')

print('Top 10 most similar words for: open \n')
pprint.pprint(model.wv.similar_by_word('open',topn=10))
print(' \n')

print('Top 10 most similar words for: unable \n')
pprint.pprint(model.wv.similar_by_word('unable',topn=10))
print(' \n')

print('Top 10 most similar words for: above \n')
pprint.pprint(model.wv.similar_by_word('above',topn=10))
print(' \n')

print('Top 10 most similar words for: close \n')
pprint.pprint(model.wv.similar_by_word('close',topn=10))
print(' \n')

print('Top 10 most similar words for: able \n')
pprint.pprint(model.wv.similar_by_word('able',topn=10))
print(' \n')

print('Top 10 most similar words for: below \n')
pprint.pprint(model.wv.similar_by_word('below',topn=10))
print(' \n')

model.accuracy('relation.txt')
print(' \n')


print('\n\n\n')
glove_input_file = 'glove.twitter.27B.50d.txt'
word2vec_output_file = 'glove.twitter.27B.50d.txt.word2vec'
glove2word2vec(glove_input_file, word2vec_output_file)

model = gensim.models.KeyedVectors.load_word2vec_format('glove.twitter.27B.50d.txt.word2vec', binary=False)

# for logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
print(' \n')

model.accuracy('test1.txt')
print(' \n')

print('Top 10 most similar words for: open \n')
pprint.pprint(model.wv.similar_by_word('open',topn=10))
print(' \n')

print('Top 10 most similar words for: unable \n')
pprint.pprint(model.wv.similar_by_word('unable',topn=10))
print('\n')

print('Top 10 most similar words for: above \n')
pprint.pprint(model.wv.similar_by_word('above',topn=10))
print('\n')

print('Top 10 most similar words for: close \n')
pprint.pprint(model.wv.similar_by_word('close',topn=10))
print(' \n')

print('Top 10 most similar words for: able \n')
pprint.pprint(model.wv.similar_by_word('able',topn=10))
print('\n')

print('Top 10 most similar words for: below \n')
pprint.pprint(model.wv.similar_by_word('below',topn=10))
print('\n')

model.accuracy('relation.txt')

