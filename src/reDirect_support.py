# Gets the work done for now

import csv

with open('reDirect_support.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0

    f = open("../support/Benjee10_reDIRECT.cfg","w")
    f.write("//reDIRECT Support\n\n")

    current_tech_node = 0

    for row in csv_reader:
        cont = 0
        for col in row:
            if len(col):
                if cont == 0:
                    current_tech_node = col
                    f.write("// --------------------------------------------------------\n")
                    f.write("// " + col + "\n")
                    f.write("// --------------------------------------------------------\n\n")
                else:
                    if(col.startswith("**")): # is a part upgrade
                        upgrade_name = col[2:]
                        f.write("@PARTUPGRADE["+ upgrade_name +"]:AFTER[Bluedog_DB]\n{\n\t@TechRequired = "+ current_tech_node +"\n}\n\n")
                    else:
                        f.write("@PART["+ col +"]:AFTER[Bluedog_DB]\n{\n\t@TechRequired = "+ current_tech_node +"\n}\n\n")

                cont+=1

    f.close()            