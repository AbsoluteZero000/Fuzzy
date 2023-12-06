import Triangle
import Trapezoid


class FuzzyVariable:
    def __init__(self, name, vtype, vrange):
        self.name = name
        self.type = vtype
        self.range = vrange
        self.fuzzy_sets = {}

    def add_fuzzy_set(self, name, ftype, values):
        self.fuzzy_sets[name] = {"type": ftype, "values": values}


class FuzzySystem:
    def __init__(self, name, description):
        self.variables = {}
        self.rules = []

    def add_variable(self, variable):
        self.variables[variable.name] = variable

    def add_rule(self, rule):
        self.rules.append(rule)

    def add_fuzzy_set(self, variable_name, set_name, ftype, values):
        self.variables[variable_name].add_fuzzy_set(set_name, ftype, values)

    def fuzzification(variable, crisp_value):
        output = []
        if variable.type != "OUT":
            for fuzzy_set in variable.fuzzy_sets:
                x_points = []
                y_points = []
                if fuzzy_set.type == "TRI":
                    x_points.append(fuzzy_set.values["x1"])
                    x_points.append(fuzzy_set.values["x2"])
                    x_points.append(fuzzy_set.values["x3"])
                    if fuzzy_set.values["x1"] == fuzzy_set.values["x2"]:
                        y_points.append(1)
                        y_points.append(1)
                        y_points.append(0)
                    elif fuzzy_set.values["x2"] == fuzzy_set.values["x3"]:
                        y_points.append(0)
                        y_points.append(1)
                        y_points.append(1)
                    else:
                        y_points.append(0)
                        y_points.append(1)
                        y_points.append(0)
                    triangle = Triangle(x_points, y_points, crisp_value)
                    output.append(triangle.fuzzification())
                elif fuzzy_set.type == "TRAP":
                    x_points.append(fuzzy_set.values["x1"])
                    x_points.append(fuzzy_set.values["x2"])
                    x_points.append(fuzzy_set.values["x3"])
                    x_points.append(fuzzy_set.values["x4"])
                    if fuzzy_set.values["x1"] == fuzzy_set.values["x2"]:
                        y_points.append(1)
                        y_points.append(1)
                        y_points.append(1)
                        y_points.append(0)
                    elif fuzzy_set.values["x3"] == fuzzy_set.values["x4"]:
                        y_points.append(0)
                        y_points.append(1)
                        y_points.append(1)
                        y_points.append(1)
                    else:
                        y_points.append(0)
                        y_points.append(1)
                        y_points.append(1)
                        y_points.append(0)
                    trapezoid = Trapezoid(x_points, y_points, crisp_value)
                    output.append(trapezoid.fuzzification())
        return output

    def run_simulation(self, crisp_values):
        # Fuzzification
        # write code here
        for variable in self.variables:
            break
        print("Fuzzification => done")
        # Inference

        print("Inference => done")
        # Defuzzification
        weighted_sum = 0
        total_activation = 0
        # write code here

        predicted_output = weighted_sum / total_activation

        print("Defuzzification => done")
        return predicted_output

    def calculate_membership(self, value, set_values):
        if set_values[0] == set_values[1] == set_values[2]:
            return 1 if value == set_values[0] else 0
        else:
            return max(
                0,
                min(
                    (value - set_values[0]) / (set_values[1] - set_values[0]),
                    (set_values[2] - value) / (set_values[2] - set_values[1]),
                ),
            )


def get_user_input_fuzzy_set(var_name):
    fuzzy_sets = {}
    print(f"Enter fuzzy sets for variable '{var_name}': (Press 'x' to finish)")
    while True:
        set_name = input("Set name: ")
        if set_name.lower() == "x":
            break
        ftype = input("Set type (TRI/TRAP): ")
        values = [float(val) for val in input("Set values (comma-separated): ").split()]
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
        if (
            len(rule_parts) == 8
            and rule_parts[1] in variables
            and rule_parts[5] in variables
            and rule_parts[7] in variables
        ):
            rule = {
                "inputs": [
                    (rule_parts[1], rule_parts[2]),
                    (rule_parts[5], rule_parts[6]),
                ],
                "output": (rule_parts[7], rule_parts[8]),
            }
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

        # adding variables to the fuzzy system
        if choice == "1":
            var_name = input("Enter the variable's name (Press 'x' to finish): ")
            if var_name.lower() == "x":
                break
            var_type = input("Enter the variable type (IN/OUT): ")
            var_range = [
                float(val)
                for val in input("Enter the variable range (lower upper): ").split()
            ]
            variable = FuzzyVariable(var_name, var_type, var_range)
            fuzzy_sets = get_user_input_fuzzy_set(var_name)
            for set_name, set_data in fuzzy_sets.items():
                variable.add_fuzzy_set(set_name, set_data["type"], set_data["values"])
            fuzzy_system.add_variable(variable)

        # adding fuzzy sets to the fuzzy Variables
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
