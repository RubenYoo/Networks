import sys


def open_file_to_read(name_file):
    """
    @param name_file: is a string
    @return: the name_file file if it exist in a read access
    """
    try:
        file = open(name_file, 'r')
    except IOError:
        return 0
    else:
        return file


def open_file_to_write(name_file):
    """
    @param name_file: is a string
    @return: the name_file file if it exist in a write access
    """
    try:
        file = open(name_file, 'r+')
        file.truncate(0)
    except IOError:
        return 0
    else:
        return file


def are_nums(x, y):
    """
    @param x: is a string
    @param y: is a string
    @return: true if x,y are nums, else return false
    """
    if x.isdigit() and y.isdigit():
        return True
    else:
        return False


def is_operator(op):
    """
    @param op: is a string
    @return: if op is one of -,+,/,* operator or not
    """
    if op == '+' or op == '-' or op == '/' or op == '*':
        return True
    return False


def two_spaces_check(st):
    """
    @param st: is a string
    @return: if the string contains 2 spaces or not
    """
    if st.count(' ') == 2:
        return True
    return False


def calc_solution(num1, op, num2):
    """
    @param num1: is a num
    @param op: is a char that contain an operator
    @param num2: is a num
    @return: num1 (op) num2
    """
    expression = num1 + op + num2
    return eval(expression)


def add_solution(file, result, words):
    """
    @param file: is a file
    @param result: is a num
    @param words: is a list
    @return: in the file the result of words[0](num) words[1](op) words[2](num)
    """
    if words:
        file.write(words[0] + ' ' + words[1] + ' ' + words[2] + " = " + str(result) + '\n')
    else:
        file.write(str(result) + '\n')


def main():
    run_assert()

    """case the user don't passed arguments in the terminal"""
    if len(sys.argv) < 3:
        file_name1 = input("Please enter your homework file name\n")
        file_name2 = input("Please enter your solution file name\n")
    else:
        file_name1 = sys.argv[1]
        file_name2 = sys.argv[2]

    homework_file = open_file_to_read(file_name1)

    while homework_file == 0:
        file_name1 = input("Error \nPlease enter once again your homework file name\n")
        homework_file = open_file_to_read(file_name1)

    solution_file = open_file_to_write(file_name2)

    while solution_file == 0:
        file_name2 = input("Error \nPlease enter once again your solution file name\n")
        solution_file = open_file_to_write(file_name2)

    for line in homework_file:
        words = line.split()
        if len(words) == 3 and are_nums(words[0], words[2]) and is_operator(words[1]) and two_spaces_check(line):
            if words[1] == "/" and int(words[2]) == 0:
                add_solution(solution_file, "Cannot divide by zero", [])
            else:
                result = calc_solution(words[0], words[1], words[2])
                add_solution(solution_file, result, words)
        else:
            add_solution(solution_file, "This line isn't in the correct format", [])

    solution_file.close()
    homework_file.close()


def run_assert():
    assert open_file_to_read("test_file") == 0
    assert open_file_to_write("test_file") == 0
    assert are_nums("3", "6") is True
    assert are_nums("aaa", "3") is False
    assert is_operator("/") is True
    assert is_operator("_") is False
    assert two_spaces_check("aa aa aa") is True
    assert two_spaces_check("aa aa") is False


if __name__ == '__main__':
    main()
