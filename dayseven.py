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
    
def sum_valid_calibrations(filename):
    # Parse input into list of calibration results and list of lists of the components that can equate to them
    calibrations = file_lines_to_list(filename)
    results = [int(line.split(": ")[0]) for line in calibrations]
    operationless_equations = [[int(x) for x in y] for y in [z.split(" ") for z in [line.split(": ")[1] for line in calibrations]]]

    valid_result_sum = 0

    # Loop through every result / components pair
    for result, components in zip(results, operationless_equations):
        num_ops = len(components) - 1

        # use binary to calculate all the possible combinations of operators. I.e.
        # 1 == 0001 == ["+", "+", "+", "*"]
        # 5 == 0101 == ["+", "*", "+", "*"]
        
        # the amount of combinations we could have is 2^<number of operations required>
        for op_dec in range(2 ** num_ops):
            component_result = components[0]

            # Get the binary string representing the operations we'll use - formatted with leading zeroes
            bin_str = f"{op_dec:0{num_ops}b}"
            for op_ind in range(len(bin_str)):
                if int(bin_str[op_ind]) == 0:
                    component_result += components[op_ind + 1]
                elif int(bin_str[op_ind]) == 1:
                    component_result *= components[op_ind + 1]

            if component_result == result:
                valid_result_sum += result
                break

    return valid_result_sum


# This will get you to the right answer, but it takes a while. See below for a better-optimized solution.

def sum_valid_calibrations_with_concats(filename):

    # Parse input into list of calibration results and list of lists of the components that can equate to them
    calibrations = file_lines_to_list(filename)
    results = [int(line.split(": ")[0]) for line in calibrations]
    operationless_equations = [[int(x) for x in y] for y in [z.split(" ") for z in [line.split(": ")[1] for line in calibrations]]]

    valid_result_sum = 0

    def dec_to_trinary(n, digits):
        if n == 0:
            return "0" * digits
    
        base3 = ""
        while n > 0:
            base3 = str(n % 3) + base3
            n //= 3

        return base3.zfill(digits)


    # Loop through every result / components pair
    for result, components in zip(results, operationless_equations):
        num_ops = len(components) - 1

        # use trinary to calculate all the possible combinations of operators. I.e.
        # 7 == 0021 == +, +, ||, *
        
        # the amount of combinations we could have is 3^<number of operations required>
        for op_dec in range(3 ** num_ops):
            component_result = components[0]

            # Get the trinary string representing the operations we'll use - formatted with leading zeroes
            trn_str = dec_to_trinary(op_dec, num_ops)
            for op_ind in range(len(trn_str)):
                if int(trn_str[op_ind]) == 0:
                    component_result += components[op_ind + 1]
                elif int(trn_str[op_ind]) == 1:
                    component_result *= components[op_ind + 1]
                elif int(trn_str[op_ind]) == 2:
                    component_result = int(str(component_result) + str(components[op_ind + 1]))

            if component_result == result:
                valid_result_sum += result
                break

    return valid_result_sum


# Though the above function brought me to the right answer and is the more "obvious" solution,
# it took longer than I would have liked to execute - so this is my trying to solve it more efficiently.

def sum_valid_calibrations_optimized(filename):
    # Parse input into list of calibration results and list of lists of the components that can equate to them
    calibrations = file_lines_to_list(filename)
    results = [int(line.split(": ")[0]) for line in calibrations]
    equations = [[int(x) for x in y] for y in [z.split(" ") for z in [line.split(": ")[1] for line in calibrations]]]

    # This helper function is called recursively to determine whether the result is possible to be
    # achieved based on the last component in the equation
    def is_result_possible(result, components):
        
        # Base cases - if length <= 1, we can't recurse
        if len(components) == 1:
            return result == components[0]
        elif len(components) == 0:
            return False
        
        # If the last element can be concatted to the result, take that concatenation off the result,
        # and see if the rest of the equation is possible.
        # i.e. "486: 6 8 6" -> "48: 6 8"
        if str(result)[-1 * len(str(components[-1])):] == str(components[-1]):
            if (len(str(result)) > len(str(components[-1]))
                and is_result_possible(int(str(result)[:-1 * len(str(components[-1]))]), components[:-1])):
                return True
        
        # If the result divides by the last component into a whole number, see if the rest of 
        # the equation is possible.
        # i.e. "36: 8 4 3" -> "12: 8 4"
        if result / components[-1] - result // components[-1] == 0:
            if is_result_possible(result // components[-1], components[:-1]):
                return True
        
        # As a last resort, since it's such an easy condition to meet, see if the result can have
        # the last element subtracted from it, then see if the rest of the equation is possible.
        # i.e. "133: 3 4 8 5" -> "128: 3 4 8"
        if result > components[-1]:
            if is_result_possible(result - components[-1], components[:-1]):
                return True
    
        return False

    calibration_sum = 0

    for result, equation in zip(results, equations):
        if is_result_possible(result, equation):
            calibration_sum += result

    return calibration_sum



print(sum_valid_calibrations("input.txt"))
print(sum_valid_calibrations_with_concats("input.txt"))

print(sum_valid_calibrations_optimized("input.txt"))

