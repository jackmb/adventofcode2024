from collections import defaultdict

def file_lines_to_list(filename):
    with open(filename) as file:
        lines = file.readlines()
        trimmed_lines = []
        for line in lines:
            if line[-1] == "\n":
                trimmed_lines.append(line[:-1])
            else:
                trimmed_lines.append(line)
        return trimmed_lines
    
# Part one - sum the middle page number of all correctly-ordered groups of pages
def sum_ordered_middles(rules_file, sequences_file):
    rules = file_lines_to_list(rules_file)

    # Create a dictionary for tracking which pages MUST appear before a specific page
    must_precede_dict = defaultdict(lambda: [])

    # Populate the dictionary with precedent requirements
    for rule in rules:
        [before, after] = rule.split("|")
        before, after = int(before), int(after)
        must_precede_dict[before].append(after)

    # int-listify the list strings from the sequences file
    sequences = [[int(x) for x in y.split(",")] for y in file_lines_to_list(sequences_file)]

    summed_midpoints = 0

    # For every sequence, determine correctness
    for sequence in sequences:
        bad_sequence = False

        # Iterate through the sequence and check whether each element is correctly succeeded
        for predecessor in sequence:
            for successor in must_precede_dict[predecessor]:

                # If we find successor before predecessor, mark this a bad sequence and exit to the next one
                if successor in sequence and sequence.index(successor) < sequence.index(predecessor):
                    bad_sequence = True
                    break
            if bad_sequence:
                break

        # If we've checked all the rules and haven't broken any, sum the middle page number
        if not bad_sequence:
            summed_midpoints += sequence[len(sequence) // 2]

    return summed_midpoints

# Part two - sum the middle page number of all the originally-incorrect page sequences, once they're fixed
def sum_corrected_middles(rules_file, sequences_file):
    rules = file_lines_to_list(rules_file)

    sequences = [[int(x) for x in y.split(",")] for y in file_lines_to_list(sequences_file)]
    summed_midpoints = 0

    for sequence in sequences:
        good_sequence = True
        i = 0

        # Go through the list of rules and assert they hold up
        while i < len(rules):
            rule = rules[i]
            [before, after] = rule.split("|")
            before, after = int(before), int(after)

            # If one of the rule's pieces is missing, it can't invalidate this sequence
            if not (before in sequence and after in sequence):
                i += 1
                continue

            # If we break this rule, swap the before page with the after page, then start over to make sure we're still following all the rules
            before_i, after_i = sequence.index(before), sequence.index(after)
            if before_i > after_i:

                # Also, we mark this page sequence broken so we know to grab the middle page number once it's fixed
                good_sequence = False
                sequence[before_i], sequence[after_i] = sequence[after_i], sequence[before_i]
                i = 0
            else:
                i += 1

        if not good_sequence:
            summed_midpoints += sequence[len(sequence) // 2]

    return summed_midpoints


print(sum_ordered_middles("rules.txt", "seqs.txt"))
print(sum_corrected_middles("rules.txt", "seqs.txt"))
