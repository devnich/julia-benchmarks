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

# Files to tokenize
files = ["pettigrew_letters_ORIGINAL.txt", "moby_dick.txt", "war_and_peace.txt"]

# The Julia `ispunct` function matches all Unicode punctuation, whereas Python's
# `string.punctuation` only matches ASCII punctuation. We create a custom
# Unicode pattern matcher here:
chrs = (chr(i) for i in range(sys.maxunicode + 1))
punctuation = ''.join([c for c in chrs if category(c).startswith("P")])

# Alternatively, you could just add a few key Unicoed punctuation characters to
# the base ASCII:
# punctuation = ''.join([string.punctuation, '—', '”', '“'])

# -------------------------
# Main function
# -------------------------
def tokenize(infile):
    """Clean and tokenize a text file."""

    # Pre-work timestamp
    t1 = time.time()

    # Get a list of files lines; each line is a string
    with open('/'.join(["data", infile]), 'r') as f:
        text = f.readlines()

    # Segment tokens, do cleanup, and count them
    tokens = defaultdict(int)

    for line in text:
        line_tokens = [token.strip(punctuation) for token in
                       line.strip().lower().split()]
        for token in line_tokens:
            tokens[token] += 1

    # Delete zero-width spaces from our count
    del tokens['']

    # Sort tokens by count
    sorted_tokens = sorted(tokens.items(), key=itemgetter(1), reverse=True)

    # Post-work timestamp
    t2 = time.time()

    # Print output to screen
    print(infile)
    print("Wall clock time:", round(t2 - t1, 3))
    print("Entries:", len(sorted_tokens))
    print("Top 20 tokens")
    pprint(sorted_tokens[:20])
    print()

    return sorted_tokens

# -------------------------
# Profile and collect stats
# -------------------------
for infile in files:
    if profile:
        # Create and enable profiler
        pr = cProfile.Profile()
        pr.enable()

        # Run target function
        tokens = tokenize(infile)

        # Display stats
        pr.disable()
        pr.print_stats(sort="time")
    else:
        sorted_tokens = tokenize(infile)
