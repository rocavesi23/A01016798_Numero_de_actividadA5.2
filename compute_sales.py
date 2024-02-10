"""
compute_sales.py

This Python program computes the total cost of sales based on a price catalogue
and sales records.
It takes two JSON files as input parameters - one containing information about
the catalogue of product prices, and the other containing records of sales
within a company.

Usage:
    python compute_sales.py priceCatalogue.json salesRecord.json

The program processes the sales records, calculates the total cost for all
sales considering the cost of each item in the price catalogue, and prints
the results on the screen and in a file named SalesResults.txt.

The program handles invalid data in the files, displaying errors in the
console while continuing execution.

Requirements:
    - The name of the program is computeSales.py
    - The program manages files with hundreds to thousands of items.
    - The execution includes the time elapsed for the computation, and this
      information is included in the results file.

Author: Roberto Avelar
Date: February 5, 2024
"""
import json
import sys
import time


def load_price_catalogue(filename):
    """
    Load the price catalogue from a JSON file.

    Args:
        filename (str): The filename of the JSON file containing the
        price catalogue.

    Returns:
        dict: A dictionary mapping product IDs to their prices.
    """
    price_catalogue = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                product_id = item.get("title")
                price = item.get("price")
                if product_id and price is not None:
                    price_catalogue[product_id] = price
                else:
                    print("Error: Invalid item in the price catalogue.")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{filename}'.")

    return price_catalogue


def load_sales_record(filename):
    """
    Load the sales record from a JSON file.

    Args:
        filename (str): The filename of the JSON file containing
        the sales record.

    Returns:
        dict: A dictionary containing sales records.
    """
    sales_record = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                product_id = item.get("Product")
                quantity = item.get("Quantity")
                if product_id and quantity is not None:

                    if product_id not in sales_record:
                        sales_record[product_id] = 0

                    sales_record[product_id] += quantity

                else:
                    print("Error: Invalid item in the price catalogue.")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{filename}'.")

    return sales_record


def compute_total_cost(price_catalogue, sales_record):
    """
    Compute the total cost of all sales.

    Args:
        price_catalogue (dict): A dictionary containing product
                                IDs as keys and their prices as
                                values.
        sales_record (dict): A dictionary containing sales records.

    Returns:
        float: The total cost of all sales.
    """
    print(f"\n{'PRODUCT':{50}} {'QUANTITY':>{10}} {'COST':>{20}}")
    total_cost = 0
    for product in sales_record.keys():
        quantity = sales_record[product]
        if product in price_catalogue:
            total_cost += price_catalogue[product] * quantity
            print(f"{product:{50}} {quantity:10} "
                  f"{price_catalogue[product] * quantity:20.2f}")
        else:
            print(f"Error: Product '{product}' not found in "
                  "the price catalogue.")
    return total_cost


def main():
    """
    Main function of the program.
    """

    if len(sys.argv) != 3:
        print("Usage: python computeSales.py priceCatalogue.json "
              "salesRecord.json")
        return

    start_time = time.time()

    price_catalogue_file = sys.argv[1]
    sales_record_file = sys.argv[2]

    price_catalogue = load_price_catalogue(price_catalogue_file)
    sales_record = load_sales_record(sales_record_file)

    if not price_catalogue or not sales_record:
        print("Exiting due to errors.")
        return

    total_cost = compute_total_cost(price_catalogue, sales_record)

    end_time = time.time()
    execution_time = end_time - start_time

    print(f"\n{'TOTAL COST OF ALL SALES':>61} {round(total_cost, 2):20.2f}")

    with open("SalesResults.txt", 'w', encoding='utf-8') as results_file:
        results_file.write("Total cost of all sales: " +
                           str(round(total_cost, 2)) + "\n")
        results_file.write("Execution time: " + str(execution_time) +
                           " seconds\n")


if __name__ == "__main__":
    main()
