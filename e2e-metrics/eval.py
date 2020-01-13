import re
import sys
import numpy as np

# crude method to calculate output information for sign test of the difference in scores
def sign_test():
    leng = open("length_100", "r")
    o = open("outputt_100", "r")
    u = open("unigram_100", "r")
    b = open("bigram_100", "r")

    lc = leng.readlines()
    oc = o.readlines()
    uc = u.readlines()
    bc = b.readlines()

    leng.close()
    o.close()
    u.close()
    b.close()

    baseline = []
    precision = []
    overlap = []
    lstm = []

    for i in range(2520):
        if i <630:
            baseline.append(lc[i])
        elif i <1260:
            precision.append(lc[i])
        elif i < 1890:
            overlap.append(lc[i])
        else:
            lstm.append(lc[i])

    precision_score = 0
    overlap_score = 0
    lstm_score = 0
    pre_total = 630
    over_total = 630
    lstm_total = 630

    for j in range(630):
        if precision[j] > baseline[j]:
            precision_score += 1
        elif precision[j] == baseline[j]:
            pre_total -= 1
        if overlap[j] > baseline[j]:
            overlap_score += 1
        elif overlap[j] == baseline[j]:
            over_total -= 1
        if lstm[j] > baseline[j]:
            lstm_score += 1
        elif lstm[j] == baseline[j]:
            lstm_total -= 1

    print("length")
    print("p: %d / %d" % (precision_score, pre_total))
    print("o: %d / %d" % (overlap_score, over_total))
    print("l: %d / %d" % (lstm_score, lstm_total))

    baseline = []
    precision = []
    overlap = []
    lstm = []

    for i in range(2520):
        if i < 630:
            baseline.append(oc[i])
        elif i < 1260:
            precision.append(oc[i])
        elif i < 1890:
            overlap.append(oc[i])
        else:
            lstm.append(oc[i])

    precision_score = 0
    overlap_score = 0
    lstm_score = 0
    pre_total = 630
    over_total = 630
    lstm_total = 630

    for j in range(630):
        if precision[j] > baseline[j]:
            precision_score += 1
        elif precision[j] == baseline[j]:
            pre_total -= 1
        if overlap[j] > baseline[j]:
            overlap_score += 1
        elif overlap[j] == baseline[j]:
            over_total -= 1
        if lstm[j] > baseline[j]:
            lstm_score += 1
        elif lstm[j] == baseline[j]:
            lstm_total -= 1
    print("output")
    print("p: %d / %d" % (precision_score, pre_total))
    print("o: %d / %d" % (overlap_score, over_total))
    print("l: %d / %d" % (lstm_score, lstm_total))

    baseline = []
    precision = []
    overlap = []
    lstm = []

    for i in range(2520):
        if i < 630:
            baseline.append(uc[i])
        elif i < 1260:
            precision.append(uc[i])
        elif i < 1890:
            overlap.append(uc[i])
        else:
            lstm.append(uc[i])

    precision_score = 0
    overlap_score = 0
    lstm_score = 0
    pre_total = 630
    over_total = 630
    lstm_total = 630

    for j in range(630):
        if precision[j] > baseline[j]:
            precision_score += 1
        elif precision[j] == baseline[j]:
            pre_total -= 1
        if overlap[j] > baseline[j]:
            overlap_score += 1
        elif overlap[j] == baseline[j]:
            over_total -= 1
        if lstm[j] > baseline[j]:
            lstm_score += 1
        elif lstm[j] == baseline[j]:
            lstm_total -= 1
    print("unigram")
    print("p: %d / %d" % (precision_score, pre_total))
    print("o: %d / %d" % (overlap_score, over_total))
    print("l: %d / %d" % (lstm_score, lstm_total))

    baseline = []
    precision = []
    overlap = []
    lstm = []

    for i in range(2520):
        if i < 630:
            baseline.append(bc[i])
        elif i < 1260:
            precision.append(bc[i])
        elif i < 1890:
            overlap.append(bc[i])
        else:
            lstm.append(bc[i])

    precision_score = 0
    overlap_score = 0
    lstm_score = 0
    pre_total = 630
    over_total = 630
    lstm_total = 630

    for j in range(630):
        if precision[j] > baseline[j]:
            precision_score += 1
        elif precision[j] == baseline[j]:
            pre_total -= 1
        if overlap[j] > baseline[j]:
            overlap_score += 1
        elif overlap[j] == baseline[j]:
            over_total -= 1
        if lstm[j] > baseline[j]:
            lstm_score += 1
        elif lstm[j] == baseline[j]:
            lstm_total -= 1

    print("bigram")
    print("p: %d / %d" % (precision_score, pre_total))
    print("o: %d / %d" % (overlap_score, over_total))
    print("l: %d / %d" % (lstm_score, lstm_total))

def eval(filename, outputfilename):
    with open(filename) as f:
        content = f.readlines()
    lengths = []
    unigrams = []
    bigrams = []
    # process outputs for sign test
    # lines = []
    # leng = open("length", "a+")
    # o = open("outputt", "a+")
    # u = open("unigram", "a+")
    # b = open("bigram", "a+")
    for line in content:
        unigram = generate_ngrams(line, 1)
        bigram = generate_ngrams(line, 2)
        length = len(unigram)
        lengths.append(length)
        unigrams.extend(unigram)
        bigrams.extend(bigram)
        # leng.write(str(length) + "\n")
        # lines.append(line)
        # o.write(str(len(set(lines))) + "\n")
        # u.write(str(len(set(unigram))) + "\n")
        # b.write(str(len(set(bigram))) + "\n")
    # leng.close()
    # o.close()
    # u.close()
    # b.close()

    average_caption_length = np.average(np.array(lengths))
    caption_diversity = len(set(content))
    unigram_diversity = len(set(unigrams))
    bigram_diversity = len(set(bigrams))

    text_file = open(outputfilename, "a")
    text_file.write("LENGTH: " + str(average_caption_length) + "\n")
    text_file.write("CAPTION_DIVERSITY: " + str(caption_diversity) + "\n")
    text_file.write("UNIGRAM_DIVERSITY: " + str(unigram_diversity) + "\n")
    text_file.write("BIGRAM_DIVERSITY: " + str(bigram_diversity) + "\n")
    text_file.close()

# credit to http://www.albertauyeung.com/post/generating-ngrams-python/
def generate_ngrams(s, n):
    # Convert to lowercases
    s = s.lower()
    s = s.strip()
    # Replace all none alphanumeric characters with spaces
    s = re.sub(r'[^a-zA-Z0-9\s]', ' ', s)

    # Break sentence in the token, remove empty tokens
    tokens = [token for token in s.split(" ") if token != ""]

    # Use the zip function to help us generate n-grams
    # Concatentate the tokens into ngrams and return
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]

if __name__ == '__main__':
    for i in range(1, 9, 2):
        eval(sys.argv[i], sys.argv[i+1])
    # sign_test()
