from collections import defaultdict

def file_lines_to_list(filename):
    with open(filename) as file:
        return file.readlines()
    
def count_xmases(filename):
    wordsearch = file_lines_to_list(filename)

    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0,  -1),          (0,  1),
                  (1,  -1), (1,  0), (1,  1)]

    x_locs = [(x, y) for x, row in enumerate(wordsearch) for y, value in enumerate(row) if value == "X"]

    xmas_count = 0

    # Iterate through all the Xs
    for loc in x_locs:

        # Check the 8 directions around the Xs for "MAS"s
        for dir in directions:
            one_off = (loc[0] + dir[0], loc[1] + dir[1])
            two_off = (loc[0] + 2*dir[0], loc[1] + 2*dir[1])
            three_off = (loc[0] + 3*dir[0], loc[1] + 3*dir[1])

            # If we're out of bounds this direction, skip it
            if (three_off[0] < 0
                or three_off[0] >= len(wordsearch)
                or three_off[1] < 0
                or three_off[1] >= len(wordsearch[0])):
                    continue
            
            # If we can spell out "XMAS" in this direction, increment the count
            if (wordsearch[one_off[0]][one_off[1]] == "M"
                and wordsearch[two_off[0]][two_off[1]] == "A"
                and wordsearch[three_off[0]][three_off[1]] == "S"):
                    xmas_count += 1

    return xmas_count

def count_xed_mases(filename):
    wordsearch = file_lines_to_list(filename)

    # Check if a diagonal (either / or \) has ends that are M and S
    def check_diag(loc, is_up):
        # If is_up, the left is bottom and right is top, else vice versa
        left = (loc[0] + 1, loc[1] - 1) if is_up else (loc[0] - 1, loc[1] - 1)
        right = (loc[0] - 1, loc[1] + 1) if is_up else (loc[0] + 1, loc[1] + 1)

        # If the diagonals poke through the bounds of the wordsearch, return False
        if (left[1] < 0
            or min(left[0], right[0]) < 0
            or right[1] >= len(wordsearch[0])
            or max(left[0], right[0]) >= len(wordsearch)):
             return False

        # If opposite corners are M and S, return True
        if ((wordsearch[left[0]][left[1]] == "M"
            and wordsearch[right[0]][right[1]] == "S")
            or (wordsearch[left[0]][left[1]] == "S"
                and wordsearch[right[0]][right[1]] == "M")):
             return True
        return False

    # Get all the locations of As in the wordsearch
    a_locs = [(x, y) for x, row in enumerate(wordsearch) for y, value in enumerate(row) if value == "A"]

    xed_mas_count = 0


    for loc in a_locs:
        # If the / diagonal has an opposite M and S AND the \ diagonal does, increment xed_mas_count
        if check_diag(loc, True) and check_diag(loc, False):
             xed_mas_count += 1

    return xed_mas_count

print(f"Number of orthagonal \"XMAS\"s in the input file: {count_xmases("input.txt")}")
print(f"Number of X-crossed \"MAS\"s in the input fule: {count_xed_mases("input.txt")}")