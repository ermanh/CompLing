### Intro to Regular Expressions in Python
### Herman Leung
### 2/9/2015 

################
### CONTENTS ###
################
### 1. Escaping characters
### 2. Regex / re module
###     2.1. Basic functions in the re module
###     2.2. Character classes (and re.U)
###     2.3. Groups and ranges (and re.I, re.S)
###     2.4. Quantifiers
###     2.5. Anchors
###     2.6. Assertions
###     2.7. re.compile()
### 3. References and tools
################


##### IMPORTS #####

import re       # regex module, this command is required every session you use regex
import string   # string module - may be useful for string.punctuation (see character classes)


##### >>>>> 1. ESCAPING CHARACTERS <<<<<

#>> Backslash <<
# Necessary for quotes and apostrophes occuring in the string in string assignments

text = "I thought the other day, \"I'm going to eat six spoons of fresh snow peas.\" " 
text2 = 'I thought the other day, "I\'m going to eat six spoons of fresh snow peas." '

text == text2
# Returns: True

# In string assignment, either the single quotes or the double quotes need to be escaped.
# In regex search strings, all characters that have a regex function need to be 
# escaped if you want to refer to the actual character and not the function

## These characters, however, are always escaped:

## \n = newline    \r = carriage return
## \t = tab       
## \u0000 = unicode characters [Python 2: requires u before string, e.g. u'\u4620']
## \x00 = hexadecimal characters

## Multi-line string assignment 
# Uses three quotes on both ends (can be single or double)
# In which case no escaping is necessary (unless your string actually includes 3 consecutive quotes)
text3 = '''I thought the other day,
            "I'm going to eat six spoons of fresh snow peas." '''

### Note: text3 will have extra white spaces and newline 

text3
# Returns: 
# I thought the other day,
#             "I'm going to eat six spoons of fresh snow peas." 


##### >>>>> 2. REGEX <<<<<

### >>> 2.1. Some Basic Functions in the re module <<<

# re.search() - find first pattern encountered
# re.match() - find pattern only at the beginning of a string
# re.findall() - find and return all matches of pattern in list format
# re.sub() - substitute a pattern for another throughout the string

## >> 2.1.1. re.search(pattern, string) <<

re.search('a', text)
# If successful, returns something like: <_sre.SRE_Match object at 0x0000000002D4EF38>
# means a match is found and a match object is created
# NOTE: it finds the first match (and stops searching)

# To print out what is found:
re.search('a', text).group()
# Returns: 'a'


## >> 2.1.2. re.match(pattern, string) <<
# *Only looks at the beginning of a string*

re.match('I', text)
# If successful, returns something like: <_sre.SRE_Match object at 0x0000000002B06F38>
re.match('a', text)
# Returns nothing, because 'a' is not the first character in text


## >> 2.1.3. re.findall(pattern, string) <<

re.findall('a', text)
# Returns: ['a', 'a', 'a']
# Even if there is only one or zero items found, it still returns a list


## >> re.sub(pattern, replacement, string) <<

re.sub('a', 'z', text)
# Returns: 'I thought the other dzy, "I\'m going to ezt six spoons of fresh snow pezs." '
# All 'a's are replaced by 'z's.


### >>> 2.2. Character Classes <<<

# \d = numerical    \D = non-numerical
# \w = word         \W = non-word           ('word' here means alphanumeric)
# \s = white space  \S = not white space

# re.U - flag for including unicode in the above classes (particularly \w and \W)
# string.punctuation - non-word and non-whitespace characters

re.findall('\d', 'They have 2 sheep and 5 deer.')
# Returns: ['2', '5']

re.findall('\D', 'They have 2 sheep and 5 deer.')
# Returns: ['T', 'h', 'e', 'y', ' ', 'h', 'a', 'v', 'e', ' ', ' ', 's', 'h', 'e', 'e', 'p', ' ', 'a', 'n', 'd', ' ', ' ', 'd', 'e', 'e', 'r', '.']

re.sub('\s', '_', text3)
# Returns: 'I_thought_the_other_day,_____________"I\'m_going_to_eat_six_spoons_of_fresh_snow_peas."_'

re.sub('\S', '_', text3)
# Returns: '_ _______ ___ _____ ____\n            ____ _____ __ ___ ___ ______ __ _____ ____ ______ '

re.search('\w', 'a2!').group()
# Returns: 'a'

re.search('\W', 'a2!').group()
# Returns: '!'

## Unicode characters can be included in the \w and \W classes by using the re.U flag

print(u'\u1620')  # note the letter u before the string [not needed in Python 3]

foo = re.search('\w', u'\u1620 is a funny symbol', re.U).group()  # with re.U
print(foo)
# Returns: the unicode character

foo = re.search('\w', u'\u1620 is a funny symbol').group()  # without re.U
print(foo)
# Returns: 'i'

string.punctuation
# Returns: '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'


### >>> 2.3. Groups and Ranges (and some flags) <<<

# [] - range specification
# [^ ] - range specification (not)
# [a-z] - all letters of the alphabet (lowercase)
# re.I - flag for ignoring case
# . - everything except newline
# re.S - flag for making . everything including newline
# | - or
# () - group


## >> 2.3.1. [] [range] <<
## Customize your own class of characters

re.findall('[aei]', text)   # finds all characters that are one of these three
# Returns: ['e', 'e', 'a', 'i', 'e', 'a', 'i', 'e', 'e', 'a']

## >> [^ ] <<
## NOT version of []

re.findall('[^aei]', text)   # finds all characters that are NOT one of these three
# Returns: ['I', ' ', 't', 'h', 'o', 'u', 'g', 'h', 't', ' ', 't', 'h', ' ', 'o', 't', 'h', 'r', ' ', 'd', 'y', ',', ' ', '"', 'I', "'", 'm', ' ', 'g', 'o', 'n', 'g', ' ', 't', 'o', ' ', 't', ' ', 's', 'x', ' ', 's', 'p', 'o', 'o', 'n', 's', ' ', 'o', 'f', ' ', 'f', 'r', 's', 'h', ' ', 's', 'n', 'o', 'w', ' ', 'p', 's', '.', '"', ' ']

## >> 2.3.2. using [] with - <<

re.findall('[a-z]', 'abcABC')      # Returns: ['a', 'b', 'c']
re.findall('[A-Z]', 'abcABC')      # Returns: ['A', 'B', 'C']
re.findall('[0-5]', '1234567890')  # Returns: ['0', '1', '2', '3', '4', '5']

## >> 2.3.3. re.I [flag: ignore case] <<

re.findall('[a-z]', 'abcABC', re.I)
# Returns: ['a', 'b', 'c', 'A', 'B', 'C']

## >> 2.3.4. . [everything except newline] <<

re.findall('.', 'a\nb')  # Returns: ['a', 'b']

## >> 2.3.5. . with re.S [everything including newline] <<

# For the dot to represent anything at all, use the re.S flag:
re.findall('.', 'a\nb', re.S)  # Returns: ['a', '\n', 'b']

## >> 2.3.6. this|that [or] <<
# or function -- searches for "this" or "that" [NOT individual characters]

re.findall('this|that', 'this, that, these, those')
# Returns: ['this', 'that']

## Parentheses may be needed:

re.findall('(go|walk)ing', "I'm going and I'm walking")
# Returns: ['go', 'walk']

## >> 2.3.7. () [group] <<
## Parentheses in regex tells it to return the item(s) found in them
## Depending on the function, the default output can vary:

re.findall('b([aeiou])t', 'bit, bet, bat, bot') # Returns item inside () only
# Returns: ['i', 'e', 'a', 'o']

re.search('b([aeiou])t', 'bit, bet, bat, bot').group()  # Returns entire search string
# Returns: 'bit'

re.search('b([aeiou])t', 'bit, bet, bat, bot').group(1)  # Index for item inside ()
# Returns: 'i'

## If there are more than 2 sets of parentheses:

re.findall('b([aeiou])([aeiou])t', 'beat, bait')
# Returns: [('e', 'a'), ('a', 'i')]

re.search('b([aeiou])([aeiou])t', 'beat, bait').group()
# Returns: 'beat'

re.search('b([aeiou])([aeiou])t', 'beat, bait').group(1)
# Returns: 'e'

re.search('b([aeiou])([aeiou])t', 'beat, bait').group(2)
# Returns: 'a'

## NOTE: even if () is used for another reason (like the OR function),
## the group function still operates (exception: (? )) :

re.findall('b(ea|ai)t', 'beat, bait')
# Returns: ['ea', 'ai']
# Does NOT return: ['beat', 'bait']


### >>> 2.4. Quantifiers <<<

# {4} = exactly 4
# {4,6} = 4-6
# * = 0 or more         
# + = 1 or more         
# ? = 0 or 1
# when ? follows other quantifiers = non-greedy (the lowest number)

## >> 2.4.1. {} [specifying exact number of consecutive sequences] <<

re.findall('[aeiou]{2}', text) # finds all sequences of two vowels
# Returns: ['ou', 'oi']

## >> 2.4.2. {1,3} [specifying range of number of consecutive sequences] <<

re.findall('\w{4,6}', text) # finds sequences of 4-6 word characters
# Returns: ['though', 'other', 'going', 'spoons', 'fresh', 'snow', 'peas']
# Note: 'though' is extracted but the actual full word is 'thought'

re.findall('[bcdfghjklmnpqrstvwxz]{2,}', text) # finds sequences of 2+ consonants
# Returns: ['th', 'ght', 'th', 'th', 'ng', 'sp', 'ns', 'fr', 'sh', 'sn']

## >> 2.4.3. * [0 or more] <<

re.search('.*', text3).group()  # Finds the first and longest sequence of non-newline characters
# Returns: 'I thought the other day,'

## >> 2.4.4. + [1 or more] <<

re.findall('\w+', 'a pizza pie') # Finds all consecutive sequences of alphanumeric characters
# Returns: ['a', 'pizza', 'pie']

re.findall('(\w+)ing', "She's going, he's playing, they're laughing.")
# Returns: ['go', 'play', 'laugh']

## >> 2.4.5. ? [0 or 1] <<

re.findall('days?', "One day, two days, three days") # Finds "day" with optional final s
# Returns: ['day', 'days', 'days']

## NOTE: These quantifiers only scope over 1 character slot (unless you use parentheses):

re.findall('([md]a)+', 'mama, dada')
# Returns: ['ma', 'da']

# But remember () can also have a group function, so to get the disyllabic words:
re.findall('(([md]a)+)', 'mama, mana, dada, tati')
# Returns: [('mama', 'ma'), ('ma', 'ma'), ('dada', 'da')]

## >> 2.4.6. Taming the greedy with ? after a quantifier <<

# Here's a GREEDY example:
re.search('.+"', text).group()
# Returns: 'I thought the other day, "I\'m going to eat six spoons of fresh snow peas."'
# The + is "greedy" because it will go for the maximum, until the very last double quote is hit

# UNGREEDY example:
re.search('.+?"', text).group()
# Returns: 'I thought the other day, "'
# The +? is "ungreedy" because as soon as a double quote is hit, the search stops


### >>> 2.5. Anchors <<<

# ^ - start of string
# $ - end of string
# \b - word boundary [NOTE: requires r before string]

## >> 2.5.1. ^ [start of string] <<

re.search('^.', text).group()  # Returns first character of the string
# Returns: 'I'
# Functionally equivalent to re.match('.', text).group()

## >> 2.5.2. $ [end of string] <<

re.search('.$', text).group()  # Returns last character of the string
# Returns: ' ' (character space)

## >> 2.5.3. \b [word boundary, requires r''] <<
# NOTE: "word" here means alphanumeric characters, and
# "word boundary" doesn't mean \b stands in for a non-alphanumeric character.

re.findall(r'\bs\w+s\b', 'Five spoons of chooped salsify')  # Returns words beginning and ending in s
# Returns: ['spoons']


### >>> 2.6. Assertions <<<
## * Parentheses used in assertions do not trigger the group function
# These assertions look for patterns before or after the desired pattern
# Patterns inside the assertions are not returned

#   Lookahead     Negative lookahead
#   (?= )         (?! )

#   Lookbehind    Negative lookbehind
#   (?<= )        (?<! )

## >> 2.6.1. (?= ) [lookahead] <<

re.findall('\w+(?=[,.!?:;])', text) # Returns words immediately preceding a punctuation mark
# Returns: ['day', 'peas']

## >> 2.6.2. (?! ) [negative lookahead] <<

re.findall('\w+(?![,.!?:;])', text) # Returns "words" NOT preceding a punctuation mark
# Returns: ['I', 'thought', 'the', 'other', 'da', 'I', 'm', 'going', 'to', 'eat', 'six', 'spoons', 'of', 'fresh', 'snow', 'pea']
# Hm, some items are word segments instead

# BETTER:
re.findall(r'[\w\']+\b(?![,.!?:;])', text)
# Returns: ['I', 'thought', 'the', 'other', "I'm", 'going', 'to', 'eat', 'six', 'spoons', 'of', 'fresh', 'snow']

## >> 2.6.3. (?<= ) [lookbehind] <<

re.findall(r'(?<=six )\w+', text) # Returns words following "six "
# Returns: ['spoons']

## >> 2.6.4. (?<! ) [negative lookbehind] <<

re.findall('(?<!six )\w+', text)
# Returns: ['I', 'thought', 'the', 'other', 'day', 'I', 'm', 'going', 'to', 'eat', 'six', 'poons', 'of', 'fresh', 'snow', 'peas']
# Hm, "poons" is still returned and "I'm" is split

# BETTER:
re.findall(r'(?<!six )\b\w+', text)
# Returns: ['I', 'thought', 'the', 'other', 'day', 'I', 'm', 'going', 'to', 'eat', 'six', 'of', 'fresh', 'snow', 'peas']
# No 'poons' or 'spoons'

# A CUSTOM XML/HTML EXAMPLE:
re.search('(?<=\<word\>).*(?=\<\/word\>)', "<word>ko'mak</word>").group()
# Returns: "ko'mak"


### >>> 2.7. re.compile() <<<
# re.compile() enables you to assign a regex search string to a variable

SEARCH = re.compile('(?<=\<word\>).*(?=\<\/word\>)')  # See above XML/HTML example
re.search(SEARCH, "<word>ko'mak</word>").group()
# Returns: "ko'mak"

# Besides saving time retyping (if you have to reuse some long search string in
# multiple places), it also allows for customization when, for example, you are
# embedding a re function in a loop and a subpart of your search string varies
# after each loop:

motion_verbs = ["walk", "mosey", "scurry"]
text4 = "Mice were scurrying everywhere as he walked -- nay, moseyed -- down the street."

inflected_verbs = []
for verb in motion_verbs:
    RE = re.compile(r'\b' + verb + r'\w+\b')
    inflected_verbs += re.findall(RE, text4)

inflected_verbs
# Returns: ['walked', 'moseyed', 'scurrying']


##### >>>>> 3. REFERENCES AND TOOLS <<<<<

### Official Python Manual ###
# https://docs.python.org/2/library/re.html [Python 2]
# https://docs.python.org/3.4/library/re.html [Python 3.4]

### Python regex editor/tester ###
# http://pythex.org/

### Regex cheatsheet
# Use (image) search on a search engine of your choice
# NOTE: Not all regex functions are incorported into Python's re module;
# different programming languages have different implementations and their
# syntax can be slightly different.