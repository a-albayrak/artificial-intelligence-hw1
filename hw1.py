import re
from itertools import permutations

class Subject:
    def __init__(self, attribute_list):
        self.attribute_list = attribute_list

class Attribute:
    def __init__(self, name, value):
        self.name = name
        self.value = value 

    def __repr__(self):
        return f"{self.name:<8} | " + " | ".join(f"{value:<8}" for value in self.value)
    
class Clue:
    def __init__(self, clue_string):
        self.clue_string = clue_string
        self.clue_type = None

    def __repr__(self):
        return f"Clue: {self.clue_string:<8} | Clue Type: {self.clue_type}\n"
    
def read_data_file(data_filename):
    with open(data_filename, 'r') as data_file:
        attribute_string_list = []
        value_string_matrix = []

        for line in data_file:
            string_list = line.rstrip().split(",")
            attribute_string_list.append(string_list[0])
            value_string_matrix.append(string_list[1:])
        
        return attribute_string_list, value_string_matrix
  
def read_clues_file(data_filename):
    clue_match_list = []

    with open(data_filename, 'r') as file:
        for line in file:
            line = line.strip()
            if re.match(r"if (\w+)=(\w+) then (\w+)=(\w+)", line):
                clue_match_list.append(("clue_1", line))
            elif re.match(r"if (\w+)=(\w+) then not (\w+)=(\w+)", line):
                clue_match_list.append(("clue_2", line))
            elif re.match(r"if (\w+)=(\w+) then either (\w+)=(\w+) or (\w+)=(\w+)", line):
                clue_match_list.append(("clue_3", line))
            elif re.match(r"n\((\w+)=(\w+)\) = n\((\w+)=(\w+)\)", line):
                clue_match_list.append(("clue_4", line))
            elif re.match(r"(\w+)\((\w+)=(\w+)\) = \1\((\w+)=(\w+)\) \+ (\d+)", line):
                clue_match_list.append(("clue_5", line))
            elif re.match(r"(\w+)\((\w+)=(\w+)\) = \1\((\w+)=(\w+)\) \- (\d+)", line):
                clue_match_list.append(("clue_6", line))
            elif re.match(r"\w+\((\w+)=(\w+)\) > \w+\((\w+)=(\w+)\)", line):
                clue_match_list.append(("clue_7", line))
            elif re.match(r"\w+\((\w+)=(\w+)\) < \w+\((\w+)=(\w+)\)", line):
                clue_match_list.append(("clue_8", line))
            elif re.match(r"one of \{(\w+)=(\w+),(\w+)=(\w+)\} corresponds to (\w+)=(\w+) other (\w+)=(\w+)", line):
                clue_match_list.append(("clue_9", line))
            elif re.match(r"\{(\w+)=(\w+),(\w+)=(\w+),(\w+)=(\w+)\} are all different", line):
                clue_match_list.append(("clue_10", line))

    return clue_match_list

def initialize_subject_list(attribute_string_list, value_string_matrix):
    subject_list = []
    
    for name, values in zip(attribute_string_list, value_string_matrix):
        subject_list.append(Attribute(name, values))
    
    return subject_list

def print_solution(subject_list):
    attribute_names = [attr.name for attr in subject_list[0].attribute_list]

    print(" | ".join(f"{name:<8}" for name in attribute_names))
    print("-" * (10 * len(attribute_names))) 

    for subject in subject_list:
        row = " | ".join(f"{attr.value[0]:<8}" for attr in subject.attribute_list)
        print(row)

# Generates set of subjects then checks if that set of subjects are consistent with the clues
def generate_matrices(attribute_string_list, value_string_matrix, clue_match_list):
    columns = list(permutations([1, 2, 3, 4]))
    count = 0
    subject_list = []

    for col1 in columns:
        for col2 in columns:
            for col3 in columns:
                for col4 in columns:
                    matrix = [list(col) for col in zip(col1, col2, col3, col4)]
                    subjects = []

                    for row in matrix:
                        attributes = [Attribute(name, [value_string_matrix[i][val - 1]]) for i, (name, val) in enumerate(zip(attribute_string_list, row))]
                        subjects.append(Subject(attributes))
                    
                    subject_list = subjects
                    count += 1

                    if (check_consistencies(subject_list, clue_match_list) == True):
                        return subject_list

# Checks if given subjects are consistent with clues(constraints)                    
def check_consistencies(subject_list, clue_match_list):
    while True:
        for i in range (len(clue_match_list)):
            clue_type = "consistent_with_" + clue_match_list[i][0]
            clue = clue_match_list[i][1]
            if (globals()[clue_type](subject_list, clue) == False):
                return False
        return True

# Checks Clue 1: if x=a then y=b
def consistent_with_clue_1(subject_list, clue):
    match = re.match(r"if (\w+)=(\w+) then (\w+)=(\w+)", clue)
    x, a, y, b = match.groups()

    for subject in subject_list:
        x_value = next(attr.value[0] for attr in subject.attribute_list if attr.name == x)
        y_value = next(attr.value[0] for attr in subject.attribute_list if attr.name == y)
        if x_value == a and y_value != b:
            return False
        
    return True

# Checks Clue 2: if x=a then not y=b
def consistent_with_clue_2(subject_list, clue):
    match = re.match(r"if (\w+)=(\w+) then not (\w+)=(\w+)", clue)
    x, a, y, b = match.groups()

    for subject in subject_list:
        x_value = next(attr.value[0] for attr in subject.attribute_list if attr.name == x)
        y_value = next(attr.value[0] for attr in subject.attribute_list if attr.name == y)
        if x_value == a and y_value == b:
            return False
        
    return True

# Checks Clue 3: if x=a then either y=b or z=c
def consistent_with_clue_3(subject_list, clue):
    match = re.match(r"if (\w+)=(\w+) then either (\w+)=(\w+) or (\w+)=(\w+)", clue)
    x, a, y, b, z, c = match.groups()

    for subject in subject_list:
        x_value = next(attr.value[0] for attr in subject.attribute_list if attr.name == x)
        y_value = next(attr.value[0] for attr in subject.attribute_list if attr.name == y)
        z_value = next(attr.value[0] for attr in subject.attribute_list if attr.name == z)
        if x_value == a and not ((y_value == b) ^ (z_value == c)):
            return False
        
    return True

# Checks Clue 4: n(x=a) = n(y=b)
def consistent_with_clue_4(subject_list, clue):
    pattern = r"(\w+)\((\w+)=(\w+)\) = (\w+)\((\w+)=(\w+)\)"
    match = re.match(pattern, clue.strip())
    n1, x, a, n2, y, b = match.groups()

    x_matches = [subject for subject in subject_list if any(attr.name == x and attr.value[0] == a for attr in subject.attribute_list)]
    y_matches = [subject for subject in subject_list if any(attr.name == y and attr.value[0] == b for attr in subject.attribute_list)]

    if len(x_matches) != 1 or len(y_matches) != 1:
        return False

    x_subject = x_matches[0]
    y_subject = y_matches[0]

    try:
        x_numeric_value = int(next(attr.value[0] for attr in x_subject.attribute_list if attr.name == n1))
        y_numeric_value = int(next(attr.value[0] for attr in y_subject.attribute_list if attr.name == n2))
    except (ValueError, StopIteration):
        return False

    return x_numeric_value == y_numeric_value

# Checks Clue 5: n(x=a) = n(y=b) + m
def consistent_with_clue_5(subject_list, clue):
    pattern = r"(\w+)\((\w+)=(\w+)\) = (\w+)\((\w+)=(\w+)\) \+ (\w+)"
    match = re.match(pattern, clue.strip())
    n1, x, a, n2, y, b, m = match.groups()

    try:
        m = int(m)
    except ValueError:
        return False

    x_matches = [subject for subject in subject_list if any(attr.name == x and attr.value[0] == a for attr in subject.attribute_list)]
    y_matches = [subject for subject in subject_list if any(attr.name == y and attr.value[0] == b for attr in subject.attribute_list)]

    if len(x_matches) != 1 or len(y_matches) != 1:
        return False

    x_subject = x_matches[0]
    y_subject = y_matches[0]

    try:
        x_numeric_value = int(next(attr.value[0] for attr in x_subject.attribute_list if attr.name == n1))
        y_numeric_value = int(next(attr.value[0] for attr in y_subject.attribute_list if attr.name == n2))
    except (ValueError, StopIteration):
        return False
    return x_numeric_value == y_numeric_value + m

# Checks Clue 6: n(x=a) = n(y=b) - m
def consistent_with_clue_6(subject_list, clue):
    pattern = r"(\w+)\((\w+)=(\w+)\) = (\w+)\((\w+)=(\w+)\) \- (\w+)"
    match = re.match(pattern, clue.strip())
    n1, x, a, n2, y, b, m = match.groups()

    try:
        m = int(m)
    except ValueError:
        return False

    x_matches = [subject for subject in subject_list if any(attr.name == x and attr.value[0] == a for attr in subject.attribute_list)]
    y_matches = [subject for subject in subject_list if any(attr.name == y and attr.value[0] == b for attr in subject.attribute_list)]

    if len(x_matches) != 1 or len(y_matches) != 1:
        return False

    x_subject = x_matches[0]
    y_subject = y_matches[0]

    try:
        x_numeric_value = int(next(attr.value[0] for attr in x_subject.attribute_list if attr.name == n1))
        y_numeric_value = int(next(attr.value[0] for attr in y_subject.attribute_list if attr.name == n2))
    except (ValueError, StopIteration):
        return False
    return x_numeric_value == y_numeric_value - m

# Checks Clue 7: n(x=a) > n(y=b)
def consistent_with_clue_7(subject_list, clue):
    pattern = r"(\w+)\((\w+)=(\w+)\) > (\w+)\((\w+)=(\w+)\)"
    match = re.match(pattern, clue.strip())
    n1, x, a, n2, y, b = match.groups()

    x_matches = [subject for subject in subject_list if any(attr.name == x and attr.value[0] == a for attr in subject.attribute_list)]
    y_matches = [subject for subject in subject_list if any(attr.name == y and attr.value[0] == b for attr in subject.attribute_list)]

    if len(x_matches) != 1 or len(y_matches) != 1:
        return False

    x_subject = x_matches[0]
    y_subject = y_matches[0]

    try:
        x_numeric_value = int(next(attr.value[0] for attr in x_subject.attribute_list if attr.name == n1))
        y_numeric_value = int(next(attr.value[0] for attr in y_subject.attribute_list if attr.name == n2))
    except (ValueError, StopIteration):
        return False  

    return x_numeric_value > y_numeric_value

# Checks Clue 8: n(x=a) < n(y=b)
def consistent_with_clue_8(subject_list, clue):
    pattern = r"(\w+)\((\w+)=(\w+)\) < (\w+)\((\w+)=(\w+)\)"
    match = re.match(pattern, clue.strip())
    n1, x, a, n2, y, b = match.groups()

    x_matches = [subject for subject in subject_list if any(attr.name == x and attr.value[0] == a for attr in subject.attribute_list)]
    y_matches = [subject for subject in subject_list if any(attr.name == y and attr.value[0] == b for attr in subject.attribute_list)]

    if len(x_matches) != 1 or len(y_matches) != 1:
        return False

    x_subject = x_matches[0]
    y_subject = y_matches[0]

    try:
        x_numeric_value = int(next(attr.value[0] for attr in x_subject.attribute_list if attr.name == n1))
        y_numeric_value = int(next(attr.value[0] for attr in y_subject.attribute_list if attr.name == n2))
    except (ValueError, StopIteration):
        return False 

    return x_numeric_value < y_numeric_value

# Checks Clue 9: one of {x=a, y=b} corresponds to z=c other t=d
def consistent_with_clue_9(subject_list, clue):
    pattern = r"one of \{(\w+)=(\w+),(\w+)=(\w+)\} corresponds to (\w+)=(\w+) other (\w+)=(\w+)"
    match = re.match(pattern, clue.strip())
    x, a, y, b, z, c, t, d = match.groups()

    x_matches = [subject for subject in subject_list if any(attr.name == x and attr.value[0] == a for attr in subject.attribute_list)]
    y_matches = [subject for subject in subject_list if any(attr.name == y and attr.value[0] == b for attr in subject.attribute_list)]

    if len(x_matches) != 1 or len(y_matches) != 1:
        return False

    x_subject = x_matches[0]
    y_subject = y_matches[0]

    if x_subject == y_subject:
        return False

    x_z_condition = any(attr.name == z and attr.value[0] == c for attr in x_subject.attribute_list)
    y_t_condition = any(attr.name == t and attr.value[0] == d for attr in y_subject.attribute_list)

    if x_z_condition and y_t_condition:
        return True

    y_z_condition = any(attr.name == z and attr.value[0] == c for attr in y_subject.attribute_list)
    x_t_condition = any(attr.name == t and attr.value[0] == d for attr in x_subject.attribute_list)

    if y_z_condition and x_t_condition:
        return True

    return False

# Checks Clue 10: {x=a,y=b,z=c} are all different
def consistent_with_clue_10(subject_list, clue):
    pattern = r"\{(\w+)=(\w+),(\w+)=(\w+),(\w+)=(\w+)\} are all different"
    match = re.match(pattern, clue.strip())
    x, a, y, b, z, c = match.groups()

    x_matches = [subject for subject in subject_list if any(attr.name == x and attr.value[0] == a for attr in subject.attribute_list)]
    y_matches = [subject for subject in subject_list if any(attr.name == y and attr.value[0] == b for attr in subject.attribute_list)]
    z_matches = [subject for subject in subject_list if any(attr.name == z and attr.value[0] == c for attr in subject.attribute_list)]

    if len(x_matches) != 1 or len(y_matches) != 1 or len(z_matches) != 1:
        return False

    x_subject = x_matches[0]
    y_subject = y_matches[0]
    z_subject = z_matches[0]

    if x_subject is not y_subject and x_subject is not z_subject and y_subject is not z_subject:
        return True

    return False

def main():
    available_problems = [1, 2, 3]
    print("The problems available in this directory:", " ".join(map(str, available_problems)))
    choice = input("Choose a problem: ").strip()
    if choice.isdigit() and int(choice) in available_problems:
        problem_number = int(choice)

        data_filename = f"data-{problem_number}.txt"
        clues_filename = f"clues-{problem_number}.txt"

        attribute_string_list, value_string_matrix = read_data_file(data_filename)
        clue_match_list = read_clues_file(clues_filename)
        subject_list = generate_matrices(attribute_string_list, value_string_matrix, clue_match_list)

        print(f"\nHere is the solution to the problem defined in data-{choice}.txt and clues-{choice}.txt.\n")
        print_solution(subject_list)

if __name__ == "__main__":
    main()