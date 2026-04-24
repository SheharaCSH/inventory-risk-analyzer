import csv

def read_inventory_and_find_reorder_items(filename='inventory_data.csv'):
    """
    Reads inventory data from CSV and identifies products that need reordering.
    
    Handles "Out of Stock" as 0 and finds items where stock_level < reorder_threshold.
    
    Args:
        filename (str): Path to the inventory CSV file
    """
    reorder_items = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Validate that required columns exist
            if reader.fieldnames is None:
                print("Error: CSV file is empty")
                return
            
            required_columns = {'product_id', 'stock_level', 'reorder_threshold', 'category'}
            if not required_columns.issubset(set(reader.fieldnames)):
                missing = required_columns - set(reader.fieldnames)
                print(f"Error: Missing required columns: {missing}")
                return
            
            # Process each row
            for row_num, row in enumerate(reader, start=2):  # start=2 to account for header
                try:
                    product_id = row['product_id'].strip()
                    category = row['category'].strip()
                    
                    # Handle stock_level - convert "Out of Stock" to 0
                    stock_level_str = row['stock_level'].strip()
                    if stock_level_str.lower() == "out of stock":
                        stock_level = 0
                    else:
                        stock_level = int(stock_level_str)
                    
                    # Convert reorder_threshold to int
                    reorder_threshold = int(row['reorder_threshold'].strip())
                    
                    # Check if reordering is needed
                    if stock_level < reorder_threshold:
                        reorder_items.append({
                            'product_id': product_id,
                            'category': category,
                            'stock_level': stock_level,
                            'reorder_threshold': reorder_threshold
                        })
                
                except ValueError as e:
                    print(f"Warning: Row {row_num} has invalid data - {e}")
                    continue
        
        # Print results
        if reorder_items:
            print(f"Found {len(reorder_items)} product(s) that need reordering:\n")
            print(f"{'Product ID':<15} {'Category':<20} {'Stock Level':<12} {'Threshold':<10}")
            print("-" * 57)
            for item in reorder_items:
                print(f"{item['product_id']:<15} {item['category']:<20} {item['stock_level']:<12} {item['reorder_threshold']:<10}")
        else:
            print("No products need reordering at this time.")
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    read_inventory_and_find_reorder_items()
