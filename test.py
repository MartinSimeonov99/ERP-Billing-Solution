import sqlite3
from datetime import date
from fpdf import FPDF

# import calculate_total_usage function from calculating.py
from calculating import calculate_total_usage


# Define a function to generate a PDF file with customer details and usage information
def generate_invoice(customer_name, customer_id, daytime_usage, nighttime_usage):
    # Create a new PDF document with portrait orientation
    pdf = FPDF()
    pdf.add_page()

    # Add a title for the invoice
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Monthly Usage Report', 0, 1, 'C')

    # Add customer details
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Customer Name: {customer_name}', 0, 1)
    pdf.cell(0, 10, f'Customer ID: {customer_id}', 0, 1)

    # Add usage information
    pdf.cell(0, 10, 'Usage Information:', 0, 1)
    pdf.cell(0, 5, '', 0, 1)
    pdf.cell(0, 5, 'Daytime Usage: ' + str(daytime_usage), 0, 1)
    pdf.cell(0, 5, 'Nighttime Usage: ' + str(nighttime_usage), 0, 1)

    # Save the PDF file with a name based on the customer ID and the current date
    file_name = f'{customer_id}_{date.today().strftime("%Y-%m-%d")}.pdf'
    pdf.output(file_name)


# Calculate the total usage for each customer
customer_usage = calculate_total_usage()

# Connect to the database
conn = sqlite3.connect('billing.db')
c = conn.cursor()

# Create a table for the monthly bills if it does not exist
c.execute('''CREATE TABLE IF NOT EXISTS monthly_bills
             (customer_name text, customer_id text, daytime_usage int, nighttime_usage int)''')

# Insert the monthly bills into the table
for fields in customer_usage:
    if fields is None:
        continue

    if fields[0] in customer_usage:
        usage = customer_usage[fields[0]]
        customer_name = fields[1]
        c.execute("INSERT INTO monthly_bills VALUES (?, ?, ?, ?)", (customer_name, fields[0], usage['daytime'], usage['nighttime']))
        
        # Generate a PDF invoice for the customer
        generate_invoice(customer_name, fields[0], usage['daytime'], usage['nighttime'])

# Commit the changes and close the connection
conn.commit()
conn.close()
