# -------------------------
# Setup
# -------------------------
# Import libraries
import cProfile
import string
import sys
from collections import defaultdict
from operator import itemgetter
from pprint import pprint
from timeit import time
from unicodedata import category

# Should we run the full profiler?
profile = False

# Should we strip all Unicode punctuation?
utf8_punctuation = True

if utf8_punctuation:
    # the julia `ispunct` function matches all unicode punctuation. to get the
    # equivalent functionality in python, we have to manually collect the
    # unicode punctuation characters (798 characters):
    chrs = (chr(i) for i in range(sys.maxunicode + 1))
    punctuation = ''.join([c for c in chrs if category(c).startswith("p")])
else:
    # use the built-in ascii punctuation collection (32 characters)
    punctuation = string.punctuation

    # an alternative approach would be to augment the base ascii set with a few
    # critical unicode characters, e.g.:
    # punctuation = ''.join([string.punctuation, '—', '”', '“'])

# files to tokenize
files = ["pettigrew_letters_original.txt", "moby_dick.txt", "war_and_peace.txt"]

# -------------------------
# main function
# -------------------------
def tokenize(infile):
    """clean and tokenize a text file."""

    # pre-work timestamp
    t1 = time.time()

    # get a list of files lines; each line is a string
    with open('/'.join(["data", infile]), 'r') as f:
        text = f.readlines()

    # segment tokens, do cleanup, and count them
    tokens = defaultdict(int)

    for line in text:
        line_tokens = [token.strip(punctuation) for token in
                       line.strip().lower().split()]
        for token in line_tokens:
            tokens[token] += 1

    # delete zero-width spaces from our count
    try:
        del tokens['']
    except KeyError:
        pass

    # sort tokens by count
    sorted_tokens = sorted(tokens.items(), key=itemgetter(1), reverse=True)

    # post-work timestamp
    t2 = time.time()

    # print output to screen
    print(infile)
    print("wall clock time:", round(t2 - t1, 3))
    print("entries:", len(sorted_tokens))
    print("top 20 tokens")
    pprint(sorted_tokens[:20])
    print()

    return sorted_tokens

# -------------------------
# profile and collect stats
# -------------------------
for infile in files:
    if profile:
        # create and enable profiler
        pr = cprofile.profile()
        pr.enable()

        # run target function
        tokens = tokenize(infile)

        # display stats
        pr.disable()
        pr.print_stats(sort="time")
    else:
        sorted_tokens = tokenize(infile)
