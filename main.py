def create_fuzzy_system():
    print("1- Create a new fuzzy system\n")
    print("2- Quit\n")

    choice = input()

    if choice == "2":
        return
    while True:
        print("""
Main Menu:
==========
1- Add variables.
2- Add fuzzy sets to an existing variable.
3- Add rules.
4- Run the simulation on crisp values.\n""")

        choice = input()

        if choice == "1":
            print("""
Enter the variable’s name, type (IN/OUT), and range ([lower, upper]):
(Press x to finish)\n""")
            variables = []
            inp = input()
            while inp != "x":
                variables.append(inp)
                inp = input()

        elif choice == "2":
            print("Enter the variable’s name:\n")
            variable_name = input()

            print("Enter the fuzzy set name, type (TRI/TRAP), and values: (Press x to finish)\n")
            fuzzy_sets = []
            inp = input()
            while inp != "x":
                fuzzy_sets.append(inp)
                inp = input()

        elif choice == "3":
            print("Enter the rules in this format: (Press x to finish)\n")
            print("IN_variable set operator IN_variable set => OUT_variable set\n")
            rules = []
            inp = input()
            while inp != "x":
                rules.append(inp)
                inp = input()

        elif choice == "4":
            print("Enter the crisp value:\n")
            crisp_values = []
            inp = input()
            while inp != "x":
                crisp_values.append(inp)
                inp = input()

        else:
            return

create_fuzzy_system()
