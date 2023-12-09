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

        print(fuzzified_values)

        print("Fuzzification => done")
        # Inference
        aggregated_rules = []
        for rule in self.rules:
            inputs = []
            for i in range(0, len(rule["inputs"]), 2):
                input_var = rule["inputs"][i]
                input_set = rule["inputs"][i + 1]
                not_flag = False
                if input_var.lower() == "not":
                    not_flag = True
                    input_var = rule["inputs"][i + 1]
                    input_set = rule["inputs"][i + 2]

                membership = fuzzified_values[input_var][input_set]
                inputs.append(not membership if not_flag else membership)

            operators = rule["operators"]

            # Apply precedence of operators
            while "and" in operators:
                index = operators.index("and")
                inputs[index] = min(inputs[index], inputs[index + 1])
                inputs.pop(index + 1)
                operators.pop(index)

            while "or" in operators:
                index = operators.index("or")
                inputs[index] = max(inputs[index], inputs[index + 1])
                inputs.pop(index + 1)
                operators.pop(index)

            min_activation = min(inputs)
            output = (rule["output"][0], rule["output"][1], min_activation)
            aggregated_rules.append(output)

        print("Inference => done")

        # Defuzzification
        weighted_sum = 0
        total_activation = 0

        for output_variable, output_set in self.rules["output"][0]:
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


def get_user_input_fuzzy_set(var_name):
    fuzzy_sets = {}
    print(f"Enter fuzzy sets for variable '{var_name}': (Press 'x' to finish)")
    while True:
        set_name = input("Set name: ")
        if set_name.lower() == "x":
            break
        ftype = input("Set type (TRI/TRAP): ")
        values = [float(val) for val in input("Set values: ").split()]
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
                "inputs": rule_parts,
                "output": (rule_parts[-2], rule_parts[-1]),
            }
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
                var_type = input("Enter the variable type (IN/OUT): ")
                var_range = [
                    float(val)
                    for val in input("Enter the variable range (lower upper): ").split()
                ]
                variable = FuzzyVariable(var_name, var_type, var_range)

                fuzzy_system.add_variable(variable)

        if choice == "2":
            var_name = input("Enter the variable's name: ")

            fuzzy_sets = get_user_input_fuzzy_set(var_name)
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
