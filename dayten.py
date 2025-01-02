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

# Get a sum of how many unique trailhead -> summit pairs can be found on the topographic map
def get_trail_score_sum(filename):
    map = [[int(x) for x in row] for row in file_lines_to_list(filename)]

    # First, parse out all the trailheads (0s) and trailtails (aka summits, 9s) from the map
    trailhead_locs = [(r, c) for r in range(len(map)) for c in range(len(map[r])) if map[r][c] == 0]
    trailtail_locs = [(r, c) for r in range(len(map)) for c in range(len(map[r])) if map[r][c] == 9]

    #          ^       >       v       <
    dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))

    # This helper function takes a trailhead -> trailtail pair, and determines whether it's possible to move between them step by step
    def can_go_to(trailhead, trailtail):
        curr_r, curr_c = trailhead[0], trailhead[1]

        # To save some processing, here we check whether the trailtail is too far, even if we beeline for it
        # [trailtail elevation] - [current elevation] must be greater than or equal to the difference between [current position] and [trailtail position]
        if map[trailtail[0]][trailtail[1]] - map[curr_r][curr_c] < abs((curr_r + curr_c) - (trailtail[0] + trailtail[1])):
            return 0
        
        # For every direction possible to move
        for dir in dirs:
            next_r, next_c = curr_r + dir[0], curr_c + dir[1]

            # If the direction takes us off the map, skip it
            if not ((0 <= next_r < len(map)) and (0 <= next_c < len(map[0]))):
                continue

            # If the direction takes us too high (or low) to climb from our current position, skip it
            if map[next_r][next_c] - map[curr_r][curr_c] != 1:
                continue

            # If the direction takes us to the trailtail, we found one!
            if (next_r, next_c) == trailtail:
                return 1
            
            # If all the above conditions failed, we CAN move, but it won't take us to the trailtail
            # See if we can see the trailtail after moving
            if can_go_to((next_r, next_c), trailtail):
                return 1

        # If all else fails, we can't get to this trailtail from this trailhead
        return 0

    # Check every combo of trailhead -> trailtail, and sum whether they're possible
    trailhead_score_sum = 0
    for trailhead in trailhead_locs:
        for trailtail in trailtail_locs:
            trailhead_score_sum += can_go_to(trailhead, trailtail)
        
    return trailhead_score_sum


# Get a sum of how many unique trailhead -> summit TRAILS can be found on the topographic map
def get_trail_rating_sum(filename):
    map = [[int(x) for x in row] for row in file_lines_to_list(filename)]

    # First, parse out all the trailheads (0s) from the map
    trailhead_locs = [(r, c) for r in range(len(map)) for c in range(len(map[r])) if map[r][c] == 0]
    
    #          ^       >       v       <
    dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))

    # This helper function takes one movement and sums all the trails that can be found from then on
    def explore(curr_r, curr_c, dir):
        next_r, next_c = curr_r + dirs[dir][0], curr_c + dirs[dir][1]
        
        # If this movement takes us off the map, stop
        if not ((0 <= next_r < len(map)) and (0 <= next_c < len(map[0]))):
            return 0
        
        # If this movement is into a wall (num too high) or off a cliff (num too low), stop
        elif map[next_r][next_c] - map[curr_r][curr_c] != 1:
            return 0
        
        # If this movement is to a summit, we've found a good trail. Return 1
        elif map[next_r][next_c] == 9:
            return 1
        
        # If this movement is valid, but not to a summit, let's see how many good trails we can find after moving
        # These calls to explore represent making the move, then seeing how many trails we can find from subsequently going the other three directions
        else:
            return sum([explore(next_r, next_c, dir_to_go) for dir_to_go in [d for d in range(len(dirs)) if d != (dir + 2) % 4]])

    # Find how many trails we can visit from every individual trailhead
    trailhead_rating_sum = 0
    for trailhead in trailhead_locs:
        trailhead_rating_sum += sum([explore(trailhead[0], trailhead[1], dir) for dir in range(len(dirs))])

    return trailhead_rating_sum

print(get_trail_score_sum("input.txt"))
print(get_trail_rating_sum("input.txt"))
