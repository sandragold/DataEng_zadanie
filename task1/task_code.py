"""
Task 1 code
"""
import json

PATH = "./genes.json"


def json_from_path(filepath):
    """ Reads json from path """
    with open(filepath) as file:
        json_data = json.load(file)
    return json_data


def is_continuous(amplifications):
    """  `True` if amplifications are continuous """
    exons = []
    length=None
    for el in amplifications:
        try:
            seq, length = el.split("/")
            exons.extend([n for n in range(int(seq.split("-")[0]), int(seq.split("-")[-1])+1)])
        except ValueError:
            length = 0
    baseline = [n for n in range(1, int(length)+1)]
    return sorted(list(set(exons))) == baseline  and len(baseline) > 0


def analyze_multi(data):
    """ Analyzes data from multiple genes"""
    output = dict()
    for gene in data:
        output[gene] = is_continuous(data[gene])
    return output


def main():
    """ Main script module """
    data = json_from_path(PATH)
    output = analyze_multi(data)
    print(output)


if __name__ == "__main__":
    main()
