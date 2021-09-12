"""
Task 2 code
"""
import pandas as pd

INPUT = "./table.xlsx"
OUTPUT = "./result.xlsx"
QUERIES = "./table_filtering"
COLUMNS = "./columns_order"


def load_data(path):
    """ Loader of Excel or TSV files """
    if INPUT.split(".")[-1].lower() == "xlsx":
        data = pd.read_excel(INPUT)
    else:
        # .tsv
        data = pd.read_csv(INPUT, sep='\t')
    return data


def read_queries(path):
    """ Parser for table_filtering files """
    output = {}
    with open(path) as fp:
        for line in fp:
            query = {}
            sheet, rest = line.split(": ")
            for q in rest.split(")")[:-1]:
                operator = None
                if "and" in q:
                    operator = "and"
                    q = q.strip("and ")

                if "or" in q:
                    operator = "or"
                    q = q.strip("or ")

                q = q.strip("(")
                # TODO: if needed support more operations like lt, gt, etc...
                if "in" in q:
                    colname, values = q.split(" in ")
                else:
                    colname, values = q.split(" == ")
                values = values.strip("[").strip("]").strip(" ").strip("'").strip('"').split('", "')
                # numbers to ints
                values = [int(val) if val.isnumeric() else val for val in values]
                query[colname] = {
                    "values": values,
                    "operator": operator,
                }
            output[sheet] = query
        return output


def read_column_order(path):
    """ Parses column ordering"""
    ordered_cols, removed_cols = [], []
    with open(path) as fp:
        for line in fp:
            if line.startswith("#"):
                removed_cols.extend([line.strip("# ").strip("\n")])
            else:
                if "#" in line:
                    line, comments = line.strip("\n").split(" # ")
                    if not comments == "moved to the end":
                        ordered_cols.extend([line.strip("\n")])
                else:
                    ordered_cols.extend([line.strip("\n")])

    return ordered_cols, removed_cols


def save_excel(input_dict, outpath="./result.xlsx"):
    """ Saves pandas.DataFrames to excel file. Each key in dict is a new sheet. """
    writer = pd.ExcelWriter(outpath, engine='xlsxwriter')
    for sheet in input_dict:
        input_dict[sheet].to_excel(writer, sheet_name=sheet)
    writer.save()


def combine_query(data, query):
    """ Finds indexes of data satisfying all conditions in multiple queries from `query`"""
    indexes = pd.Series(data=[True] * len(data))
    for key in query:
        if query[key]["operator"] == "or":
            indexes = indexes | data[key].isin(query[key]["values"])
        else:
            indexes = indexes & data[key].isin(query[key]["values"])
    return indexes


def main():
    """ Main script module """
    output_sheet = dict()

    # Parse queries
    queries = read_queries(QUERIES)

    # Parse column order
    ordered_cols, removed_cols = read_column_order(COLUMNS)

    # Load data
    data = load_data(INPUT)

    # Query the data
    for sheet in queries:
        # Get queries for sheet
        query = queries[sheet]
        # Get combined indexes
        indexes = combine_query(data, query)
        # Sort columns
        move_to_end = list(set(data.columns.to_list()).difference(set(ordered_cols + removed_cols)))
        output_sheet[sheet] = data.loc[indexes, ordered_cols + move_to_end]

    # Save multi sheet excel
    save_excel(output_sheet, outpath=OUTPUT)


if __name__ == "__main__":
    main()
