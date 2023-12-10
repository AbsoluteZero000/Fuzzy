class FuzzyVariable:
    def __init__(self, name, vtype, vrange):
        self.name = name
        self.type = vtype
        self.range = vrange
        self.fuzzy_sets = {}

    def add_fuzzy_set(self, name, ftype, values):
        self.fuzzy_sets[name] = {"type": ftype, "values": values}


class FuzzySystem:
    def __init__(self):
        self.variables = {}
        self.rules = []

    def add_variable(self, variable):
        self.variables[variable.name] = variable

    def add_rule(self, rule):
        self.rules.append(rule)

    def add_fuzzy_set(self, variable_name, set_name, ftype, values):
        self.variables[variable_name].add_fuzzy_set(set_name, ftype, values)

    def run_simulation(self, crisp_values):
        fuzzified_values = {}
        for var_name, value in crisp_values.items():
            fuzzified_values[var_name] = {}
            for set_name, fuzzy_set in self.variables[var_name].fuzzy_sets.items():
                print(fuzzy_set)
                fuzzified_values[var_name][set_name] = self.calculate_membership(
                    value, fuzzy_set
                )

        print("Fuzzification => done")
        # Inference
        aggregated_rules = []
        for rule in self.rules:
            for i in range(0, len(rule["inputs"]), 1):
                if i == len(rule["inputs"]):
                    break
                if rule["inputs"][i] in self.variables:
                    rule["inputs"][i] = fuzzified_values[rule["inputs"][i]][
                        rule["inputs"][i + 1]
                    ]
                    rule["inputs"].pop(i + 1)

            for i in range(0, len(rule["inputs"]), 1):
                if i >= len(rule["inputs"]):
                    break
                if rule["inputs"][i] == "not":
                    rule["inputs"][i] = 1 - rule["inputs"][i + 1]
                    rule["inputs"].pop(i + 1)

            # Apply precedence of operators
            for i in range(0, len(rule["inputs"]), 1):
                if i >= len(rule["inputs"]):
                    break
                if rule["inputs"][i] == "and":
                    rule["inputs"][i - 1] = min(
                        rule["inputs"][i - 1], rule["inputs"][i + 1]
                    )
                    rule["inputs"].pop(i)
                    rule["inputs"].pop(i)

            for i in range(0, len(rule["inputs"]), 1):
                if i >= len(rule["inputs"]):
                    break
                if rule["inputs"][i] == "or":
                    rule["inputs"][i - 1] = max(
                        rule["inputs"][i - 1], rule["inputs"][i + 1]
                    )
                    rule["inputs"].pop(i + 1)
                    rule["inputs"].pop(i + 1)

            min_activation = rule["inputs"][0]
            output = (rule["output"][0], rule["output"][1], min_activation)
            aggregated_rules.append(output)
        print("Inference => done")

        # Defuzzification
        weighted_sum = 0
        total_membership = 0
        for output_variable, output_set, value in aggregated_rules:
            for set_name, fuzzy_set in self.variables[
                output_variable
            ].fuzzy_sets.items():
                print(self.variables[output_variable].fuzzy_sets)
                membership = self.calculate_membership(
                    value, self.variables[output_variable].fuzzy_sets[output_set]
                )

            centroid = self.calculate_centroid(
                self.variables[output_variable].fuzzy_sets[output_set]["values"]
            )
            weighted_sum += membership * centroid
            total_membership += membership

        predicted_output = (
            weighted_sum / total_membership if total_membership != 0 else 0
        )

        print("Defuzzification => done")
        return str(output_variable) + " " + str(predicted_output)

    def calculate_membership(self, value, fuzzy_set):
        ftype = fuzzy_set["type"]
        if ftype == "TRI":
            return self.membership_triangle(value, fuzzy_set["values"])
        elif ftype == "TRAP":
            return self.membership_trapezoid(value, fuzzy_set["values"])
        else:
            raise ValueError("Invalid fuzzy set type")

    def membership_triangle(self, value, set_values):
        x_points = set_values
        y_points = []
        if x_points[0] == x_points[1]:
            y_points.append(1)
            y_points.append(1)
            y_points.append(0)
        elif x_points[1] == x_points[2]:
            y_points.append(0)
            y_points.append(1)
            y_points.append(1)
        else:
            y_points.append(0)
            y_points.append(1)
            y_points.append(0)
        slope = 0.0
        b = 0
        if value > x_points[0] and value <= x_points[1]:
            if x_points[0] == x_points[1]:
                slope = 1
            else:
                slope = (y_points[1] - y_points[0]) / (x_points[1] - x_points[0])
            b = y_points[0] - (slope * x_points[0])
            return (slope * value) + b
        elif value > x_points[1] and value <= x_points[2]:
            if x_points[1] == x_points[2]:
                slope = 1
            else:
                slope = (y_points[2] - y_points[1]) / (x_points[2] - x_points[1])
            b = y_points[1] - (slope * x_points[1])
            return (slope * value) + b
        else:
            return 0

    def membership_trapezoid(self, value, set_values):
        x_points = set_values
        y_points = []
        if x_points[0] == x_points[1]:
            y_points.append(1)
            y_points.append(1)
            y_points.append(1)
            y_points.append(0)
        elif x_points[1] == x_points[2]:
            y_points.append(0)
            y_points.append(1)
            y_points.append(1)
            y_points.append(1)
        else:
            y_points.append(0)
            y_points.append(1)
            y_points.append(1)
            y_points.append(0)
        slope = 0.0
        b = 0
        if value > x_points[0] and value <= x_points[1]:
            if x_points[0] == x_points[1]:
                slope = 1
            else:
                slope = (y_points[1] - y_points[0]) / (x_points[1] - x_points[0])
            b = y_points[0] - (slope * x_points[0])
            return (slope * value) + b
        elif value > x_points[1] and value <= x_points[2]:
            if x_points[1] == x_points[2]:
                slope = 1
            else:
                slope = (y_points[2] - y_points[1]) / (x_points[2] - x_points[1])
            b = y_points[1] - (slope * x_points[1])
            return (slope * value) + b
        elif value > x_points[2] and value <= x_points[3]:
            if x_points[2] == x_points[3]:
                slope = 1
            else:
                slope = (y_points[3] - y_points[2]) / (x_points[3] - x_points[2])
            b = y_points[2] - (slope * x_points[2])
            return (slope * value) + b
        else:
            return 0

    def calculate_centroid(self, set_values):
        return sum(set_values) / len(set_values)


def get_user_input_fuzzy_set(var_name, variables):
    fuzzy_sets = {}
    print(f"Enter fuzzy sets for variable '{var_name}': (Press 'x' to finish)")
    while True:
        valid = True
        set_name = input("Set name: ")
        if set_name.lower() == "x":
            break
        if set_name in fuzzy_sets:
            print("Set already exists. Please enter a different name.")
            continue
        ftype = input("Set type (TRI/TRAP): ")
        if ftype.lower() != "trap" and ftype.lower() != "tri":
            print("Set type must be either TRI or TRAP")
            continue
        values = [float(val) for val in input("Set values: ").split()]
        var = variables[var_name]
        for value in values:
            if value > var.range[1] or value < var.range[0]:
                valid = False
                break
        if valid == False:
            print("Set values must be within range")
            valid = True
            continue
        fuzzy_sets[set_name] = {"type": ftype, "values": values}
    return fuzzy_sets


def get_user_input_rule(variables):
    rules = []
    print("Enter rules: (Press 'x' to finish)")
    while True:
        rule_input = input(
            "Enter the rule in this format (IN_variable set operator IN_variable set => OUT_variable set): "
        )

        if rule_input.lower() == "x":
            break

        rule_parts = rule_input.split()

        if len(rule_parts) >= 8 and (len(rule_parts) - 2) % 3 == 0:
            rule = {
                "inputs": rule_parts[:-3],
                "output": (rule_parts[-2], rule_parts[-1]),
            }
            valid = True
            outputPart = False
            for i in range(0, len(rule_parts), 1):
                part = rule_parts[i]
                if (
                    i > 0
                    and (part == "and" or part == "or" or part == "not")
                    and rule_parts[i + 1] not in variables
                ):
                    valid = False
                    break
                if part == "=>" and outputPart == True:
                    valid = False
                    break
                if part == "=>" and outputPart == False:
                    outputPart = True
            if valid == False:
                print("Invalid rule format")
                continue
            print(rule)
            rules.append(rule)
        else:
            print("Invalid input. Please check the format and variable names.")

    return rules


if __name__ == "__main__":
    choice = input("Enter 1 to create a new fuzzy system or 2 to quit: ")

    if choice == "2":
        exit()

    fuzzy_system = FuzzySystem()

    while True:
        choice = input(
            "1- add variables\n2- add fuzzy sets\n3- add rules\n4- run simulation\n"
        )

        if choice == "1":
            while True:
                var_name = input("Enter the variable's name (Press 'x' to finish): ")
                if var_name.lower() == "x":
                    break
                if var_name in fuzzy_system.variables:
                    print("var name mustn't exist in the variables")
                    continue
                var_type = input("Enter the variable type (IN/OUT): ")
                if var_type.lower() != "in" and var_type.lower() != "out":
                    print("var type must be either in or out")
                    continue
                var_range = [
                    float(val)
                    for val in input("Enter the variable range (lower upper): ").split()
                ]
                if len(var_range) > 2 or var_range[0] > var_range[1]:
                    print("enter a valid ranges")
                    continue
                variable = FuzzyVariable(var_name, var_type, var_range)

                fuzzy_system.add_variable(variable)

        if choice == "2":
            var_name = input("Enter the variable's name: ")
            if var_name not in fuzzy_system.variables:
                print("var name must exist in the variables")
                continue
            fuzzy_sets = get_user_input_fuzzy_set(var_name, fuzzy_system.variables)
            for set_name, set_data in fuzzy_sets.items():
                fuzzy_system.add_fuzzy_set(
                    var_name, set_name, set_data["type"], set_data["values"]
                )

        # adding rules to the fuzzy system
        elif choice == "3":
            fuzzy_rules = get_user_input_rule(fuzzy_system.variables)
            for rule in fuzzy_rules:
                fuzzy_system.add_rule(rule)

        # running on crisp values
        elif choice == "4":
            crisp_values = {}
            for var_name in fuzzy_system.variables:
                value = float(input(f"Enter the crisp value for {var_name}: "))
                while (
                    fuzzy_system.variables[var_name].range[1] < value
                    or fuzzy_system.variables[var_name].range[0] > value
                ):
                    print("value must be in the range")
                    value = float(input(f"Enter the crisp value for {var_name}: "))
                crisp_values[var_name] = value

            print("Running the simulation...")
            try:
                predicted_output = fuzzy_system.run_simulation(crisp_values)

                print(f"The predicted output is: {predicted_output}")
                break
            except:
                print("make sure to add needed variables")
                continue
