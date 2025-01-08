def file_lines_to_list(filename):
    with open(filename) as file:
        lines = file.readlines()
        trimmed_lines = []
        for line in lines:
            if line[-1] == "\n":
                trimmed_lines.append(line[:-1])
            elif line.strip() == "":
                trimmed_lines.append(line)
        return trimmed_lines
    

# Get the cost of the fence for a field of crops using the formula (fence cost) = (fence length) * (area fenced)
def get_fence_cost(filename):
    field = file_lines_to_list(filename)
    dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))
    seen = [[False for _ in range(len(row))] for row in field]
    plots = []

    # This recursive function finds all the contiguous coordinates that have a certain crop
    # growing on them and adds them to plot
    def get_plot(crop, curr_pos, plot):

        # If we've already accounted for a position, or if it's out of bounds, skip it
        for new_pos in [(curr_pos[0] + dir[0], curr_pos[1] + dir[1]) for dir in dirs]:
            if (new_pos in plot 
                or not (0 <= new_pos[0] < len(field))
                or not (0 <= new_pos[1] < len(field[0]))
                or seen[new_pos[0]][new_pos[1]]):

                continue

            # If this space we're looking at is a neighbor, and has the same crop growing on it,
            # it's part of the same plot, so mark it seen and go from its neighbors to keep looking
            if field[new_pos[0]][new_pos[1]] == crop:
                plot.add(new_pos)
                seen[new_pos[0]][new_pos[1]] = True
                get_plot(crop, new_pos, plot)

    total_fence_cost = 0

    # Go through every cell we haven't yet added to a plot, and find and map its plot
    for pos in [(r, c) for r in range(len(field)) for c in range(len(field[r]))]:
        if seen[pos[0]][pos[1]]:
            continue

        plot_fence_len = 0

        seen[pos[0]][pos[1]] = True
        plot = {pos}
        get_plot(field[pos[0]][pos[1]], pos, plot)
        plots.append(plot)

        # For the plot we just mapped out, go through all of each cell's neighbors.
        # For every cell with a different neighbor, we know a fence must go there
        for plot_pos in plot:
            for neigh_pos in [(plot_pos[0] + dir[0], plot_pos[1] + dir[1]) for dir in dirs]:
                if (not 0 <= neigh_pos[0] < len(field)
                    or not 0 <= neigh_pos[1] < len(field[0])
                    or neigh_pos not in plot):
                    
                    plot_fence_len += 1

        # Now that we know how many fences this plot needs, multiply that by the area to find the cost of this plot's fence.
        total_fence_cost += (plot_fence_len * len(plot))
                

    return total_fence_cost


# We've qualified for a bulk discount! Find the cost of the fence where every contiguous stretch of fence
# is only the price of one fence cell. I.e. (fence cost) = (number of fence sides) * (fenced area)
def get_discounted_fence_cost(filename):
    field = file_lines_to_list(filename)
    dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))
    seen = [[False for _ in range(len(row))] for row in field]
    plots = []

    # Unchanged from the undiscounted function, this recursive helper function maps out a plot of a certain crop
    def get_plot(crop, curr_pos, plot):
        for new_pos in [(curr_pos[0] + dir[0], curr_pos[1] + dir[1]) for dir in dirs]:
            if (new_pos in plot 
                or not (0 <= new_pos[0] < len(field))
                or not (0 <= new_pos[1] < len(field[0]))
                or seen[new_pos[0]][new_pos[1]]):

                continue

            if field[new_pos[0]][new_pos[1]] == crop:
                plot.add(new_pos)
                seen[new_pos[0]][new_pos[1]] = True
                get_plot(crop, new_pos, plot)

    total_fence_cost = 0

    # Go through every unseen cell and map out its crop plot
    for pos in [(r, c) for r in range(len(field)) for c in range(len(field[r]))]:
        if seen[pos[0]][pos[1]]:
            continue

        seen[pos[0]][pos[1]] = True
        plot = {pos}
        get_plot(field[pos[0]][pos[1]], pos, plot)
        plots.append(plot)

        # Build a set of fence locations and travel directions.
        # If a cell has a different crop to its neighbor, we say they have a fence travelling in the direction of the neighbor + 90 degrees clockwise
        fences = set()
        for plot_pos in plot:
            for neigh_pos, neigh_dir in [((plot_pos[0] + dir[0], plot_pos[1] + dir[1]), dir) for dir in dirs]:

                # If the neighbor is out of bounds or doesn't have the same crop as this cell,
                # add ((fence_row, fence_col), fence_travel_direction) to the fences set
                if (not 0 <= neigh_pos[0] < len(field)
                    or not 0 <= neigh_pos[1] < len(field[0])
                    or neigh_pos not in plot):
                    
                    fences.add((neigh_pos, dirs[(dirs.index(neigh_dir) + 1) % 4]))

        # To count fence sides, we count the amount of times travelling along 
        # the fence takes us to a fence that's changed direction (i.e. a corner)
        fence_sides = len([1 for fence, fence_dir in fences if ((fence[0] + fence_dir[0], fence[1] + fence_dir[1]), fence_dir) not in fences])

        total_fence_cost += (fence_sides * len(plot))
                

    return total_fence_cost    



print(get_fence_cost("input.txt"))
print(get_discounted_fence_cost("input.txt"))