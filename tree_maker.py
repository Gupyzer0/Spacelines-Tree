# Gets the work done for now

import csv
import re

class KspTechTreeNode:
    def __init__(self, id, title, description, cost, hideEmpty, nodeName, anyToUnlock, icon, pos, parents, scale = 0.6):
        self.id = id
        self.title = title
        self.description = description
        self.cost = cost
        self.hideEmpty = hideEmpty
        self.nodeName = nodeName
        self.anyToUnlock = anyToUnlock
        self.icon = icon
        self.pos = pos
        self.scale = scale
        self.parents = parents

current_x_pos = -2300
current_y_pos = 2220

tech_node_objects = []

with open('tech_tree.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0

    for row in csv_reader:
        for col in row:
            if len(col):

                # Split the tech node so we get the id and erxtra parents and the title
                col = col.split('|')
                tech_and_title = col[0]
                if len(col) > 1:
                    title = col[1]
                else:
                    title = ''

                
                # Split the tech node so we get the id and the extra parents
                tech_node = tech_and_title.split('/')
                tech_node_id = tech_node[0]

                # If we have extra parents we add em in the tech_node_extra_parents list
                if len(tech_node) > 1:
                    tech_node_parents = tech_node[1:]
                else:
                    tech_node_parents = []
                
                # Now we check the id of the tech node for including the "expected" parent, for example
                # capsules3 "expected parent" is capsules4. So we use a regular expression for getting
                # the column number in the id string and the letters

                tech_node_column_id = re.findall(r'\d+', tech_node_id)
                tech_node_letters = re.findall(r'[a-zA-Z]',tech_node_id)

                # If we get a number check if it's one and if there are no previous tech node parents included
                # If the previous tech node is required and there are tech_node_parents just include it manually
                if len(tech_node_column_id):
                    tech_node_column_id = int(tech_node_column_id[0])
                else:
                    tech_node_column_id = 0

                if tech_node_column_id != 1 and len(tech_node_parents) < 1:
                    previous_column_id = tech_node_column_id - 1
                    parent_id = "".join(tech_node_letters) + str(previous_column_id)
                    tech_node_parents.append(parent_id)
                
                if title == '':
                    title = tech_node_id

                # fix science cost
                node = KspTechTreeNode(tech_node_id, title, tech_node_id, tech_node_column_id * 5, "False", "ct_"+tech_node_id, "True", tech_node_id, str(current_x_pos)+","+str(current_y_pos)+",-1",tech_node_parents, 0.6 )
                tech_node_objects.append(node)

            #current_x_pos += 200
            current_x_pos += 100
        
        current_x_pos = -2300 # reset x pos
        #current_y_pos -= 80 # move y post -80
        current_y_pos -= 50 # move y post -80

# Writing cfg file
f = open("../Tree/Tree.cfg","w")
f.write("@TechTree\n{\n")

for node in tech_node_objects:
    
    f.write("\tRDNode\n\t{\n")

    # id = debug
    f.write("\t\tid = "+node.id+"\n")
    # title = Debug
    f.write("\t\ttitle = "+node.title+"\n")
    # description = You shouldn't be seeing this...
    f.write("\t\tdescription = "+node.description+"\n")
    # cost = 781
    f.write("\t\tcost = "+str(node.cost)+"\n")
    # hideEmpty = False
    f.write("\t\thideEmpty = "+node.hideEmpty+"\n")
    # nodeName = debug
    f.write("\t\tnodeName = "+node.nodeName+"\n")
    # anyToUnlock = False
    f.write("\t\tanyToUnlock = "+node.anyToUnlock+"\n")
    # icon = RDicon_start
    f.write("\t\ticon = spacelines_tree/icons/"+node.icon+"\n")
    # pos = -2675,1340,0
    f.write("\t\tpos = "+node.pos+"\n")
    # scale = 0.6
    f.write("\t\tscale = "+str(node.scale)+"\n")

    # writing parents
    if node.id != "start":
        for parent in node.parents:
            f.write("\t\tParent\n\t\t{\n")
            f.write("\t\t\tparentID = "+parent+"\n")
            f.write("\t\t\tlineFrom = RIGHT\n")
            f.write("\t\t\tlineTo = LEFT\n")
            f.write("\t\t}\n")

    # closing nodes
    f.write("\t}\n")

# Closing file

f.write(''' 
    RDNode
    {
        id = debug
        title = Debug
        description = Debug for parts without a place
        cost = 0
        hideEmpty = False
        nodeName = debug
        anyToUnlock = False
        icon = RDicon_start
        pos = -2300,800,-1
        scale = 0.6
        Parent
        {
            parentID = start
            lineFrom = LEFT
            lineTo = RIGHT
        }
    }
''')

f.write('}')
f.close()
