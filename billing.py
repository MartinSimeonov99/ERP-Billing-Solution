#!C:/Users/PC/AppData/Local/Programs/Python/Python310/python


import sqlite3
from calculating import calculate_total_usage

# Create database connection and table
db = sqlite3.connect('monthly_bills.db')
c = db.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS monthly_bills
             (customer_name text, customer_id text, daytime_usage real, nighttime_usage real)''')

# Iterate through customer usage dictionary and generate monthly bills
customer_usage = calculate_total_usage()

with open('lookup.txt', 'r') as lookup_file:

    for line in lookup_file:
        fields = line.strip().split(',')

        if fields[0] in customer_usage:
            customer_name = fields[1]
            usage = customer_usage[fields[0]]

            daytime_charge = usage['daytime'] * 0.14
            nighttime_charge = usage['nighttime'] * 0.05

    
            c.execute("INSERT INTO monthly_bills (customer_name, customer_id, daytime_usage, nighttime_usage) VALUES (?, ?, ?, ?)", (customer_name, fields[0], usage['daytime'], usage['nighttime']))


            with open(f'{fields[0]}_monthly_bill.txt', 'w') as bill_file:
                bill_file.write(f'Customer name: {customer_name}\n')
                bill_file.write(f'Daytime usage: {usage["daytime"]} kWh\n')
                bill_file.write(f'Nighttime usage: {usage["nighttime"]} kWh\n')
                bill_file.write(f'Daytime charge: ${daytime_charge:.2f}\n')
                bill_file.write(f'Nighttime charge: ${nighttime_charge:.2f}\n')
                bill_file.write(f'Total: ${daytime_charge+nighttime_charge:.2f}\n')
                
db.commit()
db.close()
