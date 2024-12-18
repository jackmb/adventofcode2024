import re

def file_lines(filename):
    with open(filename) as file:
        return file.readlines()

# Regex-match all "mul(xxx,yyy)"s in the file, and return the sum of their results
def sum_all_valid_muls(filename):
    lines = file_lines(filename)
    sum = 0
    for line in lines:
        mults = re.findall("mul\((\d{1,3}),(\d{1,3})\)", line)
        for mult in mults:
            sum += int(mult[0]) * int(mult[1])
    return sum

# Regex-match all "mul(xxx,yyy)"s in the file, and ignore ones that are "disabled"
def sum_all_valid_enabled_muls(filename):
    text = "".join(file_lines(filename))
    sum = 0

    # Split the text into chunks that start enabled, and don't contain any more enables within them
    for do_block in text.split("do()"):

        # Take the text that appears before the first "don't"
        before_dont = do_block.split("don't()")[0]
        
        # Regex match that text to find mul(xxx,yyy)s, and sum their results.
        mults = re.findall("mul\((\d{1,3}),(\d{1,3})\)", before_dont)
        for mult in mults:
            sum += int(mult[0]) * int(mult[1])
    return sum

print(sum_all_valid_muls("input.txt"))
print(sum_all_valid_enabled_muls("input.txt"))
