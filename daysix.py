from collections import defaultdict
import time

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

# Given the guard's position, the direction they're facing, and the state of the map,
# return the guard's new position and direction after one move.
def move(guard_pos, guard_dir, map):
    # directions = ( ^       >       v       <   )
    directions = ((-1, 0), (0, 1), (1, 0), (0, -1))
    map_h = len(map)
    map_w = len(map[0]) if map_h > 0 else 0

    # Determine which cell the guard is looking at. If it's off the map, return False
    guard_looking_at = (guard_pos[0] + directions[guard_dir][0], guard_pos[1] + directions[guard_dir][1])
    if not (0 <= guard_looking_at[0] < map_h and 0 <= guard_looking_at[1] < map_w):
        return False
    
    # copy the guards direction, and modify the copy so we can compare it to the original later
    new_dir = guard_dir

    # while we're facing a wall (could be one wall, a corner, or a dead end), turn
    while map[guard_looking_at[0]][guard_looking_at[1]] == "#":
        new_dir = (new_dir + 1) % 4
        guard_looking_at = (guard_pos[0] + directions[new_dir][0], guard_pos[1] + directions[new_dir][1])

        # if we turned 4 times (should only happen if guard starts surrounded), return False
        if new_dir == guard_dir:
            return False
    
    # If we've turned all we need to and are still on the map, move the guard to the location in front of them
    guard_pos = (guard_pos[0] + directions[new_dir][0], guard_pos[1] + directions[new_dir][1])
    return (guard_pos, new_dir)

# Find the guard's path through the room. Returned as a list of coordinates
def find_guard_path(filename):
    map = file_lines_to_list(filename)

    # Find the guard's starting position (the "^" in the input file)
    guard_pos = [-1, -1]
    for row_i, row in enumerate(map):
        if "^" in row:
            guard_pos = [row_i, row.index("^")]
            break
   
    guard_dir = 0
    path = []

    # Move while we can move. If moving into an unvisited tile, add it to path
    while True:
        new_state = move(guard_pos, guard_dir, map)

        if not new_state:
            break

        guard_pos, guard_dir = new_state

        if guard_pos in [x[0] for x in path]:
            continue
        else:
            path.append((guard_pos, guard_dir))
            
    return path

# This will brute-force the solution by trying to sabotage all the tiles on the guard's path 
# and simulating the guard's movement until it detects she's making the same turns.

def find_sabotage_tiles(filename):
    map = file_lines_to_list(filename)

    # we do one extra loop through the map here to find the path, letting us skip
    # trying all the tiles the guard would never hit anyway
    guard_path = find_guard_path(filename)

    sabotage_tiles = []

    # Now that we know the path, try placing an obstacle in every location in it,
    # and start the guard from the location right behind the new obstacle
    for path_piece in range(1, len(guard_path)):
        guard_pos = guard_path[path_piece - 1][0]
        guard_dir = guard_path[path_piece - 1][1]

        obstacle = guard_path[path_piece][0]
        map[obstacle[0]] = map[obstacle[0]][:obstacle[1]] + "#" + map[obstacle[0]][obstacle[1] + 1:]

        # Move while we can move. Track the cells AND DIRECTIONS the guard has been in before.
        path = []
        while True:
            new_state = move(guard_pos, guard_dir, map)

            if not new_state:
                break

            # If the guard has been here before, facing the same way as before, she's stuck.
            # Add this obstacle as a good one to sabotage, and break to the next one
            if (guard_pos, guard_dir) in path:
                sabotage_tiles.append(obstacle)
                break

            path.append((guard_pos, guard_dir))

            guard_pos, guard_dir = new_state

        # As we finish up with this obstacle, remove it from the map
        map[obstacle[0]] = map[obstacle[0]][:obstacle[1]] + "." + map[obstacle[0]][obstacle[1] + 1:]

    return sabotage_tiles
                
print(len(find_guard_path("input.txt")))
print(len(find_sabotage_tiles("input.txt")))