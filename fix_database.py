import psycopg2

# Database connection parameters
db_params = {
    'dbname': 'rmhs_dashboard',
    'user': 'postgres',
    'password': 'sreyansh@45',
    'host': 'localhost',
    'port': '5432'
}

# Connect to the database
print("Connecting to the database...")
conn = psycopg2.connect(**db_params)
conn.autocommit = True

# Create a cursor
cursor = conn.cursor()

# Check if tonnage column exists
cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='dashboard_operation' AND column_name='tonnage';")
has_tonnage = cursor.fetchone() is not None

print(f"Tonnage column exists: {has_tonnage}")

# Check if quantity column exists
cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='dashboard_operation' AND column_name='quantity';")
has_quantity = cursor.fetchone() is not None

print(f"Quantity column exists: {has_quantity}")

# Execute the rename if needed
if has_tonnage and not has_quantity:
    print("Renaming column tonnage to quantity...")
    cursor.execute('ALTER TABLE dashboard_operation RENAME COLUMN tonnage TO quantity;')
    print("Column renamed successfully.")
elif not has_tonnage and has_quantity:
    print("Column is already renamed to quantity.")
else:
    print("Unexpected database state. Please check schema manually.")

# Close the cursor and connection
cursor.close()
conn.close() 