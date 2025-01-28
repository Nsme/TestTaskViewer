import os
import pandas as pd
import pyreadstat
import matplotlib.pyplot as plt
from tabulate import tabulate

DATA_FOLDER = "Data"
SUPPORTED_FORMATS = ['.csv', '.xlsx', '.sas7bdat', '.xpt']


def read_data(file_path):

    ext = os.path.splitext(file_path)[-1].lower()

    if ext == '.csv':
        return pd.read_csv(file_path, sep="$")
    elif ext == '.xlsx':
        sheets = pd.ExcelFile(file_path).sheet_names
        return {sheet: pd.read_excel(file_path, sheet_name=sheet) for sheet in sheets}
    elif ext == '.sas7bdat':
        data, _ = pyreadstat.read_sas7bdat(file_path)
        return data
    elif ext == '.xpt':
        data, _ = pyreadstat.read_xport(file_path)
        return data

    return None


def list_files(data_folder):
    return [f for f in os.listdir(data_folder) if os.path.isfile(os.path.join(data_folder, f))]


def display_table(data):
    print(tabulate(data, headers="keys", tablefmt="grid"))


def sort_table(data):

    print("Available columns for sorting:")
    for i, col in enumerate(data.columns, 1):
        print(f"{i}. {col}")
    try:
        col_choice = int(input("Select the column number to sort by: ")) - 1
        if 0 <= col_choice < len(data.columns):
            ascending = input("Sort ascending? (y/n): ").lower() == 'y'
            sorted_data = data.sort_values(by=data.columns[col_choice], ascending=ascending)
            return sorted_data
    except (ValueError, IndexError):
        print("Error.")

    return data


def plot_graph(data):

    print("Available columns for plotting:")
    for i, col in enumerate(data.columns, 1):
        print(f"{i}. {col}")
    try:
        col_choice = int(input("Select a column number for the graph: ")) - 1
        if 0 <= col_choice < len(data.columns):
            column = data.columns[col_choice]
            if pd.api.types.is_numeric_dtype(data[column]):
                plt.figure(figsize=(8, 5))
                plt.hist(data[column].dropna(), bins=10, alpha=0.7, color='blue', edgecolor='black')
                plt.title(f"Histogram {column}")
                plt.xlabel(column)
                plt.show()
            else:
                plt.figure(figsize=(8, 5))
                data[column].dropna().value_counts().plot(kind='bar', alpha=0.7, color='orange')
                plt.title(f"Histogram {column}")
                plt.xlabel(column)
                plt.grid()
                plt.show()
    except (ValueError, IndexError):
        print("Error.")


def cli_interface(data_folder):

    files = list_files(data_folder)

    if not files:
        print("No File.")
        return

    print("Available files:")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")

    try:
        choice = int(input("Select file number to view: "))
        if 1 <= choice <= len(files):

            file_path = os.path.join(data_folder, files[choice - 1])
            data = read_data(file_path)

            if isinstance(data, pd.DataFrame):
                while True:
                    print("\n1. Show table\n"
                          "2. Sort data\n"
                          "3. Build a graph\n"
                          "4. Exit")
                    action = input("Select action (number): ")
                    if action == "1":
                        display_table(data)
                    elif action == "2":
                        data = sort_table(data)
                    elif action == "3":
                        plot_graph(data)
                    elif action == "4":
                        break
                    else:
                        print("Invalid number.")
            else:
                print("Data error.")
        else:
            print("НIncorrectly file selected.")
    except ValueError:
        print("Error.")


if __name__ == "__main__":
    cli_interface(DATA_FOLDER)
