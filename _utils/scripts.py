import json
from pprint import pprint


def extract_grammer():
    while True:
        data = input()
        if data == "exit":
            break

        left = data.split("->")[0]
        rights = data.split("->")[1].split("|")
        for right in rights:
            print(
                left.replace("-", "_"),
                right.replace("-", "_") if right.strip() != "-" else right
            )



def run_command():
    header = input().strip().split("\t")
    print("\n")
    print(header)
    first_sets = dict()
    while True:
        text = input().strip()
        if text == "q":
            break
        parts = text.split("\t")
        first_set = [header[i] for i in range(len(header)) if parts[i + 1] == "+"]
        if "┤" in first_set:
            first_set.remove("┤")
            first_set.append("$")
        first_sets[parts[0]] = first_set
    with open("../static/first_sets.json", "w") as file:
        file.write(json.dumps(first_sets, indent=2))


run_command()
