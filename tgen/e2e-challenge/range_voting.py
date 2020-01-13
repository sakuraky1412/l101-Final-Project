import sys

BEAM_SIZE = 2

def process_output(output_filename):
    with open(output_filename) as f:
        content = f.readlines()
    text_file = open("split_output.txt", "w")
    large_set = []
    for line in content:
        split_lines = line.split("In city is ")
        small_set = []
        for split_line in split_lines:
            if split_line == ".\n":
                split_line = ""
            split_line += "\n"
            if split_line != "\n":
                small_set.append(split_line)
            text_file.write(split_line)
        large_set.append(small_set)
    text_file.close()
    return large_set

def range_voting(prob_filename, lstm_filename, large_set):
    with open(prob_filename) as f:
        probs = f.readlines()
    with open(lstm_filename) as f:
        lstms = f.readlines()

    assert len(large_set) == len(lstms)
    lstm_text_file = open("lstm_res.txt", "w")
    for i in range(len(lstms)):
        assert int(lstms[i]) < len(large_set)
        if len(large_set[i])<=int(lstms[i]):
            lstm_text_file.write(large_set[i][0])
        else:
            lstm_text_file.write(large_set[i][int(lstms[i])])
    lstm_text_file.close()

    large_prob_set = []
    small_prob_set = []
    for prob in probs:
        if prob != "\n":
            small_prob_set.append(prob)
        else:
            large_prob_set.append(small_prob_set)

    assert len(large_set) == len(large_prob_set)
    precision_text_file = open("precision_res.txt", "w")
    overlap_text_file = open("overlap_res.txt", "w")
    for i in range(len(large_set)):
        cur_output_set = large_set[i]
        cur_prob_set = large_prob_set[i]
        if len(cur_output_set) != BEAM_SIZE:
            precision_text_file.write(cur_output_set[0])
            overlap_text_file.write(cur_output_set[0])
            continue
        precision_scores = []
        overlap_scores = []
        for j in range(len(cur_output_set)):
            cur_output = cur_output_set[j].strip()
            precision_score = 0
            overlap_score = 0
            for k in range(len(cur_output_set)):
                other_output = cur_output_set[k].strip()
                other_prob = cur_prob_set[k].strip()
                precision_score += float(other_prob) * precision(other_output, cur_output)
                overlap_score += float(other_prob) * overlap(other_output, cur_output)
            precision_scores.append([precision_score, cur_output])
            overlap_scores.append([overlap_score, cur_output])

        precision_scores.sort(key=lambda tup: tup[0])
        overlap_scores.sort(key=lambda tup: tup[0])
        precision_text_file.write(precision_scores[0][1] + "\n")
        overlap_text_file.write(overlap_scores[0][1] + "\n")
    precision_text_file.close()
    overlap_text_file.close()

def precision(s, t):
    bag_s = bag(s)
    bag_t = bag(t)
    return len(set(bag_s).intersection(bag_t)) / len(bag_s)

def overlap(s, t):
    set_s = set(bag(s))
    set_t = set(bag(t))
    return len(set_s.intersection(set_t)) / len(set_s)

def bag(s):
    bag = s.split(" ")
    bag.remove(".")
    return bag

if __name__ == '__main__':
    output_filename = sys.argv[1]
    prob_filename = sys.argv[2]
    lstm_filename = sys.argv[3]
    large_set = process_output(output_filename)
    range_voting(prob_filename, lstm_filename, large_set)

