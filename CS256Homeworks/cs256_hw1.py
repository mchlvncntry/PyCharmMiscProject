import csv

def print_three_letter_streets(filename, column_name):
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                street_name = row[column_name].strip()
                if len(street_name) == 3:  # check for exactly 3 letters
                    print(street_name)
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except KeyError:
        print(f"Column '{column_name}' not found in CSV file.")


# Example usage
print_three_letter_streets("Street_Names_20250909.csv", column_name="StreetName")