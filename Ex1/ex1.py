
def main():
    number = input("Please enter a 5 digit number\n")
    print("You entered the number: " + number)
    print("The digits of this number are: ", end="")
    sumNum = int(number[4])
    for i in range(0, 4, 1):
        print(number[i], end=",")
        sumNum += int(number[i])
    print(number[4])
    print("The sum of the digits is: " + str(sumNum), end="")


if __name__ == '__main__':
    main()

