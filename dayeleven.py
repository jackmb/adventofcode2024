from collections import defaultdict
from functools import cache

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

# Return the updated stone(s) from one stone based on the three rules provided
def blink_at(stone):
    # If stone is engraved with a zero, blinking replaces the engraving with a one
    if stone == 0:
        return [1]
    
    # If stone is engraved with an even-digited number, blinking apparates a new stone that takes half that number
    elif len(str(stone)) % 2 == 0:
        return [int(str(stone)[:len(str(stone)) // 2]), int(str(stone)[len(str(stone)) // 2:])]
    
    # If the stone doesn't have engravings with the above rules, its engraving is multiplied by 2024
    else:
        return [stone * 2024]

# Take a row of stones, and blink once - modifying each in turn
def blink_at_stones(stones: list):
    for i in range(len(stones) - 1, -1, -1):

        # Store the stones before and after the one we're processing, so we can rebuild the list once it's done
        before_stones = stones[:i]
        after_stones = stones[i + 1:]

        # Recombine the stones once we've modified this one
        stones = before_stones + blink_at(stones[i]) + after_stones

    return stones

# Blink at a row of stones n times
# This was my initial approach. Passably fast for low n values, but struggles when going over 25
# This does no caching - it modifies the row of stones in place one by one, over and over until
# we've blinked at each individual stone n times.
def blink_n_times(filename, n):
    stones = [int(x) for x in file_lines_to_list(filename)[0].split(" ")]
    new_stones = []

    # Go one by one through the original stones, blinking at it n times
    for i in range(len(stones) - 1, -1, -1):
        ith_stone_blinked = [stones[i]]

        # Blink at the stone n times, potentially expanding it to many many more stones
        for _ in range(n):
            ith_stone_blinked = blink_at_stones(ith_stone_blinked)

        new_stones = ith_stone_blinked + new_stones

    return len(new_stones)


@cache
# This was my second approach. Using the functools cache decorator, we save loads of processing time.
# This will short-circuit the function call if we've tried this same-etched stone
# with this same amount of steps remaining.
def count_stones(stone, steps_remaining):
    
    # If we have no steps remaining, we're only looking at one unmodifyable stone. Return 1
    if steps_remaining == 0:
        return 1
    
    # As before, if the stone has a 0, etch it with a 1 instead and decrement the steps remaining
    elif stone == 0:
        return count_stones(1, steps_remaining - 1)
    
    # As before, split even-digited stones and decrement steps remaining
    elif len(str(stone)) % 2 == 0:
        return (count_stones(int(str(stone)[:len(str(stone)) // 2]), steps_remaining - 1) +
                count_stones(int(str(stone)[len(str(stone)) // 2:]), steps_remaining - 1))
    
    # As before, multiply stones that aren't 0s and aren't even-digited by 2024 and decrement steps remaining
    else:
        return count_stones(stone * 2024, steps_remaining - 1)


# Using the functools-cached count_stones function to speed up drastically, count the stones after n blinks
def blink_n_times_optimized(filename, n):
    stones = [int(x) for x in file_lines_to_list(filename)[0].split(" ")]
    return sum(count_stones(x, n) for x in stones)


print(blink_n_times_optimized("input.txt", 25))
print(blink_n_times_optimized("input.txt", 75))
