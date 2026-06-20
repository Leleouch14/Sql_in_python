import mysql.connector

# Connect to MySQL server
conn = mysql.connector.connect(
    host="localhost", #change host if needed
    user="root", #or anyother user that is
    password="Password"  # change to your real password
)

cursor = conn.cursor()

# Ask which database to use
db_name = input("Which database do you want to use? ").strip()

# Select the database
try:
    cursor.execute(f"USE {db_name};")
except Exception as e:
    print("Failed to use database:", e)
    exit()

# Create the table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS Money_spent_games (
    Sr_no INT AUTO_INCREMENT PRIMARY KEY,
    Game_name VARCHAR(100),
    Item_bought VARCHAR(100),
    Amount_spent DECIMAL(10, 2)
);
"""
cursor.execute(create_table_query)
conn.commit()

# Ask what the user wants to do
choice = input("Do you want to 'add' a new entry or 'check' the table? ").strip().lower()

if choice == "add":
    while True:
        game = input("Enter the name of the game: ").strip()
        item = input("What item did you buy? ").strip()
        amount = float(input("How much money was spent? ₹"))

        insert_query = """
        INSERT INTO Money_spent_games (Game_name, Item_bought, Amount_spent)
        VALUES (%s, %s, %s);
        """
        values = (game, item, amount)

        try:
            cursor.execute(insert_query, values)
            conn.commit()
            print("Item added successfully! ")
        except Exception as e:
            print("Error adding item:", e)
            conn.rollback()

        cont = input("Do you want to add another item? (yes/no): ").strip().lower()
        if cont != "yes":
            break

elif choice == "check":
    try:
        cursor.execute("SELECT * FROM Money_spent_games;")
        results = cursor.fetchall()
        if results:
            print("\n--- Money Spent on Games ---")
            total = 0
            for row in results:
                print(f"#{row[0]} | Game: {row[1]} | Item: {row[2]} | ₹{row[3]}")
                total += float(row[3])
            print(f"\n Total Money Spent: ₹{total:.2f}")
        else:
            print("No entries found.")
    except Exception as e:
        print("Error retrieving data:", e)
else:
    print("Invalid choice. Please type 'add' or 'check'.")

# Clean up
cursor.close()
conn.close()
