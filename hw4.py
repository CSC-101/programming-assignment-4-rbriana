import sys
import csv


def load_data(file_path):
    """Load the demographic's data."""
    try:
        with open(file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            data = [row for row in reader]
        return data
    except FileNotFoundError:
        print(f"Error: Could not open data file '{file_path}'")
        sys.exit(1)


def filter_state(data, state):
    """Filter counties by state."""
    filtered = [entry for entry in data if entry["State"] == state]
    print(f"Filter: state == {state} ({len(filtered)} entries)")
    return filtered


def filter_gt(data, field, value):
    """Filter counties where field > value."""
    filtered = [entry for entry in data if float(entry[field]) > float(value)]
    print(f"Filter: {field} gt {value} ({len(filtered)} entries)")
    return filtered


def filter_lt(data, field, value):
    """Filter counties where field < value."""
    filtered = [entry for entry in data if float(entry[field]) < float(value)]
    print(f"Filter: {field} lt {value} ({len(filtered)} entries)")
    return filtered


def population_total(data):
    """Calculate total 2014 population."""
    total_population = sum(int(entry["Population"]) for entry in data)
    print(f"2014 population: {total_population}")


def population_subfield(data, field):
    """Calculate total sub-population based on a percentage field."""
    total_population = sum(
        (float(entry[field]) / 100) * int(entry["Population"]) for entry in data
    )
    print(f"2014 {field} population: {total_population}")


def percent_field(data, field):
    """Calculate percentage of sub-population for a given field."""
    total_population = sum(int(entry["Population"]) for entry in data)
    sub_population = sum(
        (float(entry[field]) / 100) * int(entry["Population"]) for entry in data
    )
    percentage = (sub_population / total_population) * 100 if total_population else 0
    print(f"2014 {field} percentage: {percentage}")


def display(data):
    """Display county information."""
    print("Displaying county information:")
    for entry in data:
        print(entry)


def process_operations_file(data, operations_file):
    """Process each operation in the operations file."""
    try:
        with open(operations_file, 'r') as file:
            for line_num, line in enumerate(file, start=1):
                line = line.strip()
                if not line or line.startswith("#"):  # Skip blank lines or comments
                    continue

                try:
                    parts = line.split(":")
                    operation = parts[0]
                    if operation == "display":
                        display(data)
                    elif operation == "filter-state":
                        data = filter_state(data, parts[1])
                    elif operation == "filter-gt":
                        data = filter_gt(data, parts[1], float(parts[2]))
                    elif operation == "filter-lt":
                        data = filter_lt(data, parts[1], float(parts[2]))
                    elif operation == "population-total":
                        population_total(data)
                    elif operation == "population":
                        population_subfield(data, parts[1])
                    elif operation == "percent":
                        percent_field(data, parts[1])
                    else:
                        print(f"Error: Invalid operation on line {line_num}")
                except (IndexError, ValueError) as e:
                    print(f"Error: Malformed line {line_num} - {line.strip()}")
    except FileNotFoundError:
        print(f"Error: Could not open operations file '{operations_file}'")
        sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print("Usage: python program.py <operations_file>")
        sys.exit(1)

    operations_file = sys.argv[1]
    demographics_file = "demographics.csv"  # Change to the path of your data file

    # Load the full demographics dataset
    data = load_data(demographics_file)
    print(f"Loaded {len(data)} entries from the dataset.")

    # Process the operations file
    process_operations_file(data, operations_file)


if __name__ == "__main__":
    main()
