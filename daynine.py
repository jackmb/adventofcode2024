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

def get_fragmented_checksum(filename):
    fs_map = file_lines_to_list(filename)[0]

    # Parse the mapped filesystem into two discrete lists of file sizes and open space sizes
    file_sizes, space_sizes = [], []
    for i in range(0, len(fs_map)):
        if i % 2 == 0:
            file_sizes.append(fs_map[i])
        else:
            space_sizes.append(fs_map[i])

    # Parse the two lists we've created into a "visual" filesystem layout, e.g. "00..111...2...333..." etc
    block_map = []
    for i in range(len(file_sizes)):
        for _ in range(int(file_sizes[i])):
            block_map.append(str(i))
        if i < len(space_sizes):
            for _ in range(int(space_sizes[i])):
                block_map.append(".")

    # Keep a list of positions that aren't "."s
    # Traverse through the block map in order. When we see a file already in place,
    # we add it to the checksum. When we see a ".", we take the furthest file piece,
    # put it in the "."'s place, then add it to the checksum.
    checksum = 0
    ids = list(reversed([x for x in range(len(block_map)) if block_map[x] != "."]))
    for spot in range(len(block_map)):
        
        # If we're now checking locations further than our furthest file piece, we're done.
        if spot > ids[0]:
            break

        # If we're at an open space, we can take the furthest piece of file and move it here
        if block_map[spot] == ".":
            last_id_spot = ids.pop(0)
            block_map[spot] = block_map[last_id_spot]

            # Can't forget to replace the freshly-moved piece with open space
            block_map[last_id_spot] = "."

        checksum += spot * int(block_map[spot])

    return checksum


def get_unfragmented_checksum(filename):
    fs_map = file_lines_to_list(filename)[0]
    
    # Parse the mapped filesystem into two discrete lists of file sizes and open space sizes
    file_sizes, space_sizes = [], []
    for i in range(0, len(fs_map)):
        if i % 2 == 0:
            file_sizes.append(int(fs_map[i]))
        else:
            space_sizes.append(int(fs_map[i]))

    # Parse the two lists we've created into a "visual" filesystem layout, e.g. "00..111...2...333..." etc
    # At the same time, note the starting positions of the open spaces. They'll come in handy
    block_map, space_starts = [], []
    for i in range(len(file_sizes)):
        for _ in range(int(file_sizes[i])):
            block_map.append(str(i))
        if i < len(space_sizes):
            space_starts.append(len(block_map))
            for _ in range(int(space_sizes[i])):
                block_map.append(".")

    # Loop backwards through files, and loop forwards through spaces for each to find one that fits
    for fromfile_i in range(len(file_sizes) - 1, -1, -1):
        for tospace_i in range(0, fromfile_i):

            # If the space fits, insert the file and clear its old position
            if space_sizes[tospace_i] >= file_sizes[fromfile_i]:

                # Figure out the start and end positions of the files old and new positions
                to_start = space_starts[tospace_i]
                to_end = space_starts[tospace_i] + file_sizes[fromfile_i]
                from_start = block_map.index(str(fromfile_i))
                from_end = from_start + file_sizes[fromfile_i]

                # Move file indices into the space we found, and clear out its old spot
                block_map[to_start:to_end] = block_map[from_start:from_end]
                block_map[from_start:from_end] = ["." for _ in range(file_sizes[fromfile_i])]

                # Update our list of space sizes to account for the room we just took out
                # No need to update the room freed up from moving the file...
                # it can't be filled later with the current constraints.
                space_sizes[tospace_i] -= file_sizes[fromfile_i]

                # If there's still a little space left here, update the space start location
                # so we can use it later
                if space_sizes[tospace_i] != 0:
                    space_starts[tospace_i] = space_starts[tospace_i] + file_sizes[fromfile_i]

                break

    checksum = 0
    for i in range(len(block_map)):
        if block_map[i] != ".":
            checksum += i * int(block_map[i])

    return checksum

print(get_fragmented_checksum("input.txt"))
print(get_unfragmented_checksum("input.txt"))
