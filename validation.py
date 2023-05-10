#!C:/Users/PC/AppData/Local/Programs/Python/Python310/python

with open('D:\pythonProject\ERP customer billing solution\input.txt', 'r') as input_file, open('E_records.txt', 'w') as error_file:
    
    for line in input_file:
        fields = line.split(',')

        if len(fields) < 7:
            error_file.write(line)

        if fields[6] not in ['A', 'E'] or any(int(x) <= 0 for x in fields[2:6]):
            error_file.write(line)

        else:
            pass
            # Process valid record