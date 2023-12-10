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

            print(rule)
            min_activation = rule["inputs"][0]
            output = (rule["output"][0], rule["output"][1], min_activation)
            aggregated_rules.append(output)

        print("Inference => done")

        # Defuzzification
        weighted_sum = 0

        for output_variable, output_set, value in aggregated_rules:
            for var_name, sets in fuzzified_values.items():
                membership = sets[output_set]
                centroid = self.calculate_centroid(
                    self.variables[var_name].fuzzy_sets[output_set]["values"]
                )
                weighted_sum += membership * centroid
                total_membership += membership

        predicted_output = (
            weighted_sum / total_membership if total_membership != 0 else 0
        )

        print("Defuzzification => done")
        return output_variable + " " + predicted_output

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
        set_name = input("Set name: ")
        if set_name.lower() == "x":
            break
        ftype = input("Set type (TRI/TRAP): ")
        if ftype.upper() != "TRI" or ftype.upper() != "TRAP":
            print("Type must be either TRI or TRAP")
        else:
            values = [float(val) for val in input("Set values: ").split()]
            var = variables[var_name]
            valid = True
            for value in values:
                if value > var.range[1] or value < var.range[0]:
                    valid = False
            if valid == True:
                fuzzy_sets[set_name] = {"type": ftype, "values": values}
            else:
                print("fuzzy values must be between range")
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
        outputPart = False
        valid = True
        for part in rule_parts:
            if outputPart == True:
                names = []
                for i in variables:
                    names.append(i[name])
                if (
                    part not in names
                    and part != "and"
                    and part != "or"
                    and part != "not"
                ):
                    print("rewrite the fuzzy rule, variables must be stored in the app")
                    valid = False
                if part in names and part != "and" and part != "or" and part != "not":
                    if variables[part].type != "OUT":
                        print("variable after => must be OUT variable")
                        valid = False
                if part == "=>":
                    print("then part must appear once")
                    valid = False
            else:
                if part == "=>":
                    outputPart = True
                names = []
                for i in variables:
                    names.append(i[name])
                if (
                    part not in names
                    and part != "and"
                    and part != "or"
                    and part != "not"
                ):
                    print("rewrite the fuzzy rule, variables must be stored in the app")
                    valid = False
                if part in names and part != "and" and part != "or" and part != "not":
                    if variables[part].type != "IN":
                        print("variable before => must be IN variable")
                        valid = False
        if valid == True:
            if len(rule_parts) >= 8 and (len(rule_parts) - 2) % 3 == 0:
                rule = {
                    "inputs": rule_parts[:-3],
                    "output": (rule_parts[-2], rule_parts[-1]),
                }
                print(rule)
                rules.append(rule)
            else:
                print("Invalid input. Please check the format and variable names.")
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
                var_type = input("Enter the variable type (IN/OUT): ")
                var_range = [
                    float(val)
                    for val in input("Enter the variable range (lower upper): ").split()
                ]
                variable = FuzzyVariable(var_name, var_type, var_range)

                fuzzy_system.add_variable(variable)

        if choice == "2":
            var_name = input("Enter the variable's name: ")

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
                crisp_values[var_name] = value

            print("Running the simulation...")
            predicted_output = fuzzy_system.run_simulation(crisp_values)

            print(f"The predicted output is: {predicted_output}")
            break
