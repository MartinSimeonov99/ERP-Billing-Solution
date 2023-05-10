#!C:/Users/PC/AppData/Local/Programs/Python/Python310/python

def calculate_total_usage():

    customer_usage = {}

    with open('D:\pythonProject\ERP customer billing solution\input.txt', 'r') as input_file, open('A_records.txt', 'w') as a_file, open("EE_records.txt", "w") as e_file:

        for line in input_file:
            fields = line.strip().split(',')

            if len(fields) >= 7 and fields[6] == 'A' and all(int(x) > 0 for x in fields[2:6]):
                
                a_file.write(line)  # write the line to the A_records.txt file

                daytime_usage = int(fields[3]) + int(fields[4])
                nighttime_usage = int(fields[2]) + int(fields[5])
                customer_id = fields[0]

                if customer_id not in customer_usage:
                    customer_usage[customer_id] = {'daytime': 0, 'nighttime': 0}

                customer_usage[customer_id]['daytime'] += daytime_usage
                customer_usage[customer_id]['nighttime'] += nighttime_usage

            elif len(fields) >= 7 and fields[6] == 'E' and all(int(x) > 0 for x in fields[2:6]):
                e_file.write(line)

    return customer_usage
