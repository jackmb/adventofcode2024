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
    
# Find antinodes - defined as points on the grid that are twice as far from
# a node of one frequency as they are from another node of the same frequency
def find_antinodes(filename):
    map = file_lines_to_list(filename)

    node_locs = defaultdict(lambda: [])
    antinode_locs = defaultdict(lambda: False)

    # First, collect a list of coordinates for the nodes that emit each frequency
    for r in range(len(map)):
        for c in range(len(map[r])):
            if map[r][c] != ".":
                node_locs[map[r][c]].append((r, c))

    # For each frequency emitted by one or more nodes...
    for frequency in node_locs:

        # Go through each possible pair of antennas
        for loc in range(len(node_locs[frequency])):
            for other_loc in range(loc + 1, len(node_locs[frequency])):

                # Parse the index of the pairs in the node_loc list to a [h]uman-readable ordered-pair coordinate
                loc_h = (node_locs[frequency][loc][0], node_locs[frequency][loc][1])
                other_loc_h = (node_locs[frequency][other_loc][0], node_locs[frequency][other_loc][1])

                # Points that are 2x as far from one antenna (a, b) as they are from another (i, j) of the same frequency can be found
                # using the equation (x1, y1) = (2i - a, 2j - b) 
                # and (x2, y2) = (2a - i, 2b - j)
                antinode_one_loc = (2 * other_loc_h[0] - loc_h[0], 2 * other_loc_h[1] - loc_h[1])
                antinode_two_loc = (2 * loc_h[0] - other_loc_h[0], 2 * loc_h[1] - other_loc_h[1])

                # If the two antinodes we found are still on the map, add them to the antinode_loc dictionary
                if 0 <= antinode_one_loc[0] < len(map) and 0 <= antinode_one_loc[1] < len(map[0]):
                    antinode_locs[antinode_one_loc] = frequency
                if 0 <= antinode_two_loc[0] < len(map) and 0 <= antinode_two_loc[1] < len(map[0]):
                    antinode_locs[antinode_two_loc] = frequency

    return antinode_locs

# Find all harmonically resonant antinodes - defined as locations on the grid that are
# "in line" with two antennas of the same frequency
def find_resonant_antinodes(filename):
    map = file_lines_to_list(filename)

    node_locs = defaultdict(lambda: [])
    res_antinode_locs = defaultdict(lambda: [])

    # First, collect list of coordinates for each antenna by frequency
    for r in range(len(map)):
        for c in range(len(map[r])):
            if map[r][c] != ".":
                node_locs[map[r][c]].append((r, c))

    # For every frequency possible,
    for frequency in node_locs:

        # If there's only one antenna with this frequency, it can't have harmonically resonant antinodes
        if len(node_locs[frequency]) <= 1:
            continue

        # Loop through every possible pair of antennas with the same frequency
        for loc in range(len(node_locs[frequency])):
            for other_loc in range(loc + 1, len(node_locs[frequency])):

                # Parse the index of the pairs in the node_loc list to a [h]uman-readable ordered-pair coordinate
                loc_h = (node_locs[frequency][loc][0], node_locs[frequency][loc][1])
                other_loc_h = (node_locs[frequency][other_loc][0], node_locs[frequency][other_loc][1])

                # Calculate the (x, y) offset between these two antennas
                node_diff = (other_loc_h[0] - loc_h[0], other_loc_h[1] - loc_h[1])

                # Loop through all the locations (including starting antenna) that harmonically resonate
                # with these antennas *in the positive direction*
                resonant_loc = loc_h
                while (0 <= resonant_loc[0] < len(map)
                       and 0 <=  resonant_loc[1] < len(map[0])):
                    res_antinode_locs[resonant_loc] = frequency
                    resonant_loc = (resonant_loc[0] + node_diff[0], resonant_loc[1] + node_diff[1])

                # Now do the same thing with the harmonic locations, but using a negative offset
                resonant_loc = (loc_h[0] - node_diff[0], loc_h[1] - node_diff[1])
                while (0 <= resonant_loc[0] < len(map)
                       and 0 <=  resonant_loc[1] < len(map[0])):
                    res_antinode_locs[resonant_loc] = frequency
                    resonant_loc = (resonant_loc[0] - node_diff[0], resonant_loc[1] - node_diff[1])

    return res_antinode_locs

print(len(find_antinodes("input.txt")))
print(len(find_resonant_antinodes("input.txt")))
