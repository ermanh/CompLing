### Introduction to the Natural Language Toolkit (NLTK)
### UC Berkeley, Computational methods in linguistics group
### Herman Leung
### 4/6/2015

### http://www.nltk.org
### http://www.nltk.org/book/ (Natural Language Processing with Python)

###    Many of the examples in this file come from or are adapted
###    from the NLTK book.

''' 
NOTE: The code in this file runs on Python 2.7 and some NLTK functions may also be older.
      Alternative Python 3/NLTK 3.0 code is provided immediately below the relevant parts 
      and are commented out.
'''

################
### CONTENTS ###
################
###
### 0. Downloading NLTK packages
### 1. Accessing corpora
### 2. Tokenization
### 3. Stemming
### 4. Lemmatization
### 5. Tagging
###       5.1. Regex tagger
###       5.2. Lookup tagger
###       5.3. Training (unigram) taggers
###       5.4. N-gram taggers
###       5.5. Storing taggers
###       5.6. Inspecting tagger performance
### 6. Mini-examples of NLTK application
###       6.1. Extracting noun-noun compounds
###       6.2. Extracting [N that V N N] phrases
###       6.3. Extracting the rhyme of a word
###       6.4. Poetry generation (using POS tags and bigrams)
### 7. Creating an NLTK-friendly corpus
###
################

import nltk, re

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### 0. Downloading NLTK packages ###
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###

nltk.download()  # a window will pop up

## for the purposes of this tutorial, download the following only:
# brown
# gutenberg
# cmudict

from nltk.corpus import brown, gutenberg, cmudict


### ~~~~~~~~~~~~~~~ ###
### 1. NLTK Corpora ###
### ~~~~~~~~~~~~~~~ ###


##-- Untagged corpus example: gutenberg --##

## A selection of 18 texts from Project Gutenberg
## 2.6 million words

gutenberg.fileids() # names of text files in the corpus
gutenberg.raw()[:100] # first 100 chars of the entire corpus in raw format
gutenberg.raw(fileids='shakespeare-macbeth.txt')[:100] # first 100 chars of Macbeth

gutenberg.sents('shakespeare-macbeth.txt')[0] # first sentence of Macbeth
     # Note: sentences here are actually a list of words
     # gutenberg.sents() would be a list of lists of words

gutenberg.words('shakespeare-macbeth.txt')[:10] # first ten words of Macbeth
     # gutenberg.words() is just one giant list of all words in the corpus


##-- Tagged corpus example: brown --##

## A selection of 500 texts from the Brown Corpus
## 1.2 million words

brown.fileids()[:10] # first 10 file names, not very descriptive
brown.categories() # the categories of texts in the corpus
brown.fileids(categories="hobbies") # text files in the category of "hobbies"

brown.raw()[:100] # the raw text of the brown corpus (note tags)
brown.sents()[0] # first sentence in the corpus
brown.words()[:10] # first ten words in the corpus
brown.tagged_sents()[0] # first sentence, each word tagged with part-of-speech info
brown.tagged_words()[:50] # first fifty words, all tagged


##-- Specialized corpus: cmudict --##

##     The Carnegie Mellon University Pronouncing Dictionary
##     over 130,000 words, includes stress and variant pronunciations

cmudict.dict()['idiosyncratic']
cmudict.dict()['caravan']


### ~~~~~~~~~~~~~~~~~~~~~~~ ###
### 2. Tokenizing Sentences ###
### ~~~~~~~~~~~~~~~~~~~~~~~ ###
###
### - Breaking a sentence string into tokens (words, etc.)
###
### - A few common issues:
###     Punctuation
###     Contractions (e.g., can't)
###     Non-alphabetical words

sent = "I don't want a blueberry cake... I want a vanilla-almond cake!!!"

sent.split(' ') # This doesn't separate the punctuation from the words
nltk.wordpunct_tokenize(sent) # A smarter but still not great tokenizer (e.g., splits up "don't")
nltk.word_tokenize(sent) # Better - takes care of contractions...

text = 'That U.S.A. poster-print costs $12.40...'
nltk.word_tokenize(text) # ... but still not necessarily perfect (e.g., split up the $ from the amount)


##-- Customizing your own tokenizer: nltk.regexp_tokenizer() -- ##

text = 'That U.S.A. poster-print costs $12.40...'
pattern = r'''(?x)                # set flag to allow verbose regexps (strip out embedded whitespace and comments)
              ([A-Z]\.)+          # abbreviations, e.g. U.S.A.
            | \w+(-\w+)*          # words with optional internal hyphens
            | \$?\d+(\.\d+)?%?    # currency and percentages, e.g. $12.40, 82%
            | \.\.\.              # ellipsis
            | [][.,;"'?():-_`]''' # punctuation marks, etc. as separate tokens

nltk.regexp_tokenize(text, pattern)


### ~~~~~~~~~~~ ###
### 3. Stemming ###
### ~~~~~~~~~~~ ###
###
### - obtaining the stem of a word
### - sometimes we don't want to deal with/care about affixes, e.g.
###      - dictionaries don't neccessarily contain all possible inflected/derived forms
###      - in search engine queries one would probably not want to exclude inflectional differences

## Using regex

re.findall(r'^(.*?)(ing|ly|ed|ious|ies|ive|es|s|ment)$', 'processes') # from NLTK book
# Returns: [('process', 'es')]
# But of course this is still a very weak stemmer:

re.findall(r'^(.*?)(ing|ly|ed|ious|ies|ive|es|s|ment)$', 'basis') # Returns 'basi' as the stem
re.findall(r'^(.*?)(ing|ly|ed|ious|ies|ive|es|s|ment)$', 'lying') # Returns 'ly' as the stem

## NLTK's stemmers (for English)

porter = nltk.PorterStemmer()
lancaster = nltk.LancasterStemmer()

text2 = brown.sents()[2004]
[porter.stem(t) for t in text2]
[lancaster.stem(t) for t in text2]

# Neither is anywhere near perfect, but using one stemmer consistently on several texts may
# still allow you to compare and extract semantically similar words across those texts.
# For example, you could find all forms of "increas" ("increase", "increasing", "increased",
# "increasingly", etc.) and create a concordance list.


### ~~~~~~~~~~~~~~~~ ###
### 4. Lemmatization ###
### ~~~~~~~~~~~~~~~~ ###
### - essentially stemming but only if the "stem" is in a dictionary

wnl = nltk.WordNetLemmatizer()
[wnl.lemmatize(t) for t in text2]


### ~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### 5. Tagging (Part of Speech) ###
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###

nltk.pos_tag(text2) # NLTK's own pretty robust tagger
nltk.help.brown_tagset('CD') # check what a particular tag represents
nltk.help.upenn_tagset('CD') # different corpora may use different tags/definitions


## - - - - - - - - - ##
## 5.1. Regex tagger ##
## - - - - - - - - - ##

patterns = [
    (r'.*ing$', 'VBG'),              # gerunds
    (r'.*ed$', 'VBD'),               # simple past
    (r'.*es$', 'VBZ'),               # 3rd singular present
    (r'.*ould$', 'MD'),              # modals
    (r'.*\'s$', 'NN$'),              # possessive nouns
    (r'.*e?s$', 'NNS'),              # plural nouns
    (r'^-?[0-9]+(.[0-9]+)?$', 'CD'), # cardinal numbers
    (r'.*', 'NN')                    # nouns (default)
]

re_tagger = nltk.RegexpTagger(patterns)
re_tagger.tag(brown.sents()[3])
re_tagger.evaluate(brown.tagged_sents()[-1000:])
# only about 17.7% accuracy


## - - - - - - - - -  ##
## 5.2. Lookup tagger ##
## - - - - - - - - -  ##
#
#   - store some of the most frequently occurring words and their tags
#   - the size of this lookup tagger doesn't have to be that big

fd = nltk.FreqDist(brown.words(categories='news'))
cfd = nltk.ConditionalFreqDist(brown.tagged_words(categories='news'))

most_freq_words = fd.keys()[:100]
# for Python 3:
# most_freq_words = fd.most_common(100)

likely_tags = dict((word, cfd[word].max()) for word in most_freq_words)
# for Python3:
# likely_tags = dict((word[0], cfd[word[0]].max()) for word in most_freq_words)

baseline_tagger = nltk.UnigramTagger(model=likely_tags)
baseline_tagger.tag(brown.sents()[3]) # Note: a lot of 'None' tags
baseline_tagger.evaluate(brown.tagged_sents()[-1000:])
# a lot better at 49.1% accuracy


## - - - - - -  ##
## 5.3. Backoff ##
## - - - - - -  ##
#
#   - if a tagger can't tag something (gives 'None'), we can tell it to
#     try a second tagger that might be able to tag it
#   - i.e., the backoff tagger comes to the rescue only when the main
#     tagger fails

baseline_tagger = nltk.UnigramTagger(model=likely_tags,
                                     backoff=nltk.DefaultTagger('NN'))
baseline_tagger.tag(brown.sents()[3]) # The 'None' tags are now 'NN'
baseline_tagger.evaluate(brown.tagged_sents()[-1000:])
# improved to 60.6% accuracy (nouns are the most common)

### Training a (unigram) tagger
#   - we basically just use nltk.UnigramTagger() over tagged data
#     (in [[(word, tag), (word, tag), ...], [...], ...] format)

# Training (90% of data) and testing (10% of data)
# - that way we can actually check the performance of the tagger on unseen data

news = brown.tagged_sents(categories="news")
cutoff = int(len(news) * 0.9)
cutoff # 4160
news_train = news[:cutoff]
news_test = news[cutoff:]
unigram_tagger = nltk.UnigramTagger(news_train) # training on first 90%
unigram_tagger.evaluate(news_test) # evaluate on last 10%
# 81.3% accuracy


## - - - - - - - - - - ##
## 5.4. N-gram taggers ##
## - - - - - - - - - - ##
#
#   - nltk.BigramTagger()
#   - nltk.TrigramTagger()
#   - these look at the preceding context
#   - consider 'tutor' in 'to tutor' (TO VB) vs. 'the tutor' (AT NN)
#   - if preceding word is TO, assign VB; if it's AT, assign NN

# However, the performance of an n-gram tagger by itself is not that great

bigram_tagger = nltk.BigramTagger(news_train)
bigram_tagger.evaluate(news_test)
# 10.3% accuracy

trigram_tagger = nltk.TrigramTagger(news_train)
trigram_tagger.evaluate(news_test)
# 6.3% accuracy

# The reason is because you would need an incredibly large training dataset
# for the tagger to be able to capture as many n-gram patterns as possible,
# but there are just too many possible patterns.
# That's too costly in terms of both memory and runtime.

# Solution: we combine taggers using a series of backoffs

t0 = nltk.DefaultTagger('NN')
t1 = nltk.UnigramTagger(news_train, backoff=t0)
t2 = nltk.BigramTagger(news_train, backoff=t1)
t3 = nltk.TrigramTagger(news_train, backoff=t2)
t3.evaluate(news_test)
# 84.4% accuracy (compared to 81.3% using just nltk.UnigramTagger())


## - - - - - - - - - -  ##
## 5.5. Storing Taggers ##
## - - - - - - - - - -  ##
#
#   - training a tagger on a large corpus can take up a lot of time
#   - instead of starting from scratch every time you start a new Python
#     process, you can store the tagger 

from pickle import dump
with open('t3.pkl', 'wb') as output:
    dump(t3, output, -1)

# In a different Python session, load the tagger back in

from pickle import load
with open('t3.pkl', 'rb') as input:
    t3 = load(input)


## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ##
## 5.6. Inspecting tagger performance - nltk.ConfusionMatrix() ##
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ##

test_tags = [tag for sent in brown.sents(categories="news") for (word, tag) in t3.tag(sent)]
gold_tags = [tag for (word, tag) in brown.tagged_words(categories="news")]

test_tags = [tag for sent in brown.sents() for (word, tag) in t3.tag(sent)]
gold_tags = [tag for (word, tag) in brown.tagged_words()]

cm = nltk.ConfusionMatrix(gold_tags, test_tags)
print(cm.pp(sort_by_count=True, truncate=10))
print(cm.pp(sort_by_count=True, show_percents=True, truncate=10))

# for Python 3:
# print(cm.pretty_format(sort_by_count=True, truncate=10))
# print(cm.pretty_format(sort_by_count=True, show_percents=True, truncate=10))


### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### 6. Mini-examples of NLTK application ###
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###

## - - - - - - - - - - - - - - - - - - ##
## 6.1. Extracting noun-noun compounds ##
## - - - - - - - - - - - - - - - - - - ##

compound_nouns = []

def process2(sentence):
    global compound_nouns
    for (w1, t1), (w2, t2) in nltk.bigrams(sentence):
        if (t1 in ['NN', 'NNS'] and t2 in ['NN', 'NNS']):
            compound_nouns.append((w1, w2))

for tagged_sent in brown.tagged_sents():
    process2(tagged_sent)

len(compound_nouns)
for c in compound_nouns[:20]:
    print(c)


## - - - - - - - - - - - - - - - - - - -  ##
## 6.2. Extracting [N that V N N] phrases ##
## - - - - - - - - - - - - - - - - - - -  ##

def process5(sentence):
    for (w1, t1), (w2, t2), (w3, t3), (w4, t4), (w5, t5) in nltk.ngrams(sentence, 5):
        if (t1.startswith('N') 
        and w2 == 'that'
        and t3.startswith('V')
        and t4.startswith('N')
        and t5.startswith('N')):
            print(w1, w2, w3, w4, w5)

for tagged_sent in brown.tagged_sents():
    process5(tagged_sent)

# committee that included James A.
# force that enabled President Balaguer
# things that make Newport's afternoon
# rain that disrupted Wednesday night's
# language that enlightened men today
# trouble that plagued Bill Ruger
# hope that come spring cleaning
# face-lifting that replaced Mike Fink
# requirement that United States flag
# capitals that simulate window lettering
# flower that smiles today tomorrow
# hands that circled Matsuo's wrist


## - - - - - - - - - - - - - - - - - - - - - - - - -  ##
## 6.3. Extracting the rhyme of a word (with cmudict) ##
## - - - - - - - - - - - - - - - - - - - - - - - - -  ##

cmuwords = cmudict.words()

def get_perfect_rhyme(word):
    if word in cmuwords:
        pronun_list = cmudict.dict()[word][0]
        if '1' in str(pronun_list):
            for i in range(len(pronun_list)):
                if '1' in pronun_list[i]:
                    stressed_pos = i
            rhyme_list = [pronun_list[stressed_pos]]
            for j in range(len(pronun_list) - stressed_pos -1):
                stressed_pos += 1
                rhyme_list.append(pronun_list[stressed_pos])
            return rhyme_list
        else:
            print(str(word) + ' not rhymable')
            return None
    else:
        print(str(word) + ' not in cmudict')
        return None

get_perfect_rhyme('caravan')
get_perfect_rhyme('winnebago')


## - - - - - - - - - - - - - - - - - - - - - - - - - ##
## 6.4. Poetry generation using POS tags and bigrams ##
## - - - - - - - - - - - - - - - - - - - - - - - - - ##
# (Separate file/demo not included here)


### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### 7. Creating an NLTK-friendly corpus ###
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###

# Full original code and files as well as details can be found at:
# https://github.com/ermanh/courses/tree/master/AppliedNLP

from nltk.corpus import CategorizedTaggedCorpusReader as CTCR

## The following is a corpus of 19th century American poetry webscraped from
## http://famouspoetsandpoems.com in Fall 2013. The data was curated and tagged using nltk.pos_tag(),
## then formatted and written into individual files for NLTK corpus reader access.

corpus_dir = 'C:/Python27/Poetry/' # <-- CHANGE (to where you place the unzipped Poetry folder; 
                                   #             visit link above to obtain zipped file)

##-- CorpusReader Creation --##

poetry = CTCR(corpus_dir, r'.*\.txt', cat_pattern=r'(.*?)\_.*')

# All the common NLTK corpus reading functions are available: 

poetry.categories() # returns all author names (76 total)
len(poetry.fileids())# 5645 poems
poetry.sents()[1000]
# ['115:', 'Bright', 'Spirit', ',', 'whose', 'illuminings', 'I', 'sought', ',']

poetry.tagged_sents()[1000] # Note untagged first item (where tag value is None)
poetry.paras()[1] # poetry.paras() returns all the poems, each a list of lines

poetry.raw()[:100]
poetry.words()[:50]
