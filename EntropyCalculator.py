import math
import TreeTableMaker

aGenomes = 0
tGenomes = 0
cGenomes = 0
gGenomes = 0

def visit(currentNode):
    childNum = len(currentNode.children)
    if childNum == 0:
        if currentNode.name in aGenomes:
            currentNode.data = 'A'
        elif currentNode.name in tGenomes:
            currentNode.data = 'T'
        elif currentNode.name in cGenomes:
            currentNode.data = 'C'
        elif currentNode.name in gGenomes:
            currentNode.data = 'G'
        else:
            print(currentNode.name)
        return
    else:
        for i in range(childNum):
            visit(currentNode.children[i])
        currentData = currentNode.children[0].data
        for j in range(childNum):
            if currentNode.children[j].data == 'X':
                continue
            elif currentNode.children[j].data != currentData \
                    and currentNode.children[j].data != 'X':
                currentNode.data = 'X'    
                break
            else:
                currentNode.data = currentNode.children[j].data
        

def incrementGroups(currentNode):
    global groups
    global a_group
    global c_group
    global t_group
    global g_group
    groups+=1
    if currentNode.data == 'A':
        a_group += 1
    elif currentNode.data == 'T':
        t_group += 1
    elif currentNode.data == 'C':
        c_group += 1
    elif currentNode.data == 'G':
        g_group += 1

#Calculate Value determines the entropy value
def CalculateValue(treeTable, currentNode):
    global groups
    global a_group
    global c_group
    global t_group
    global g_group

    childCharacter = []
    childNum = len(currentNode.children)
    #print("\n\tCurrent: " + str(currentNode.data) + "\t NumChildren: " + \
    #        str(childNum))
    if childNum == 0:
        pass
    elif currentNode.data == 'X' and currentNode != treeTable.get_root():
        childCharacter.append(currentNode.get_parent().data)
    elif currentNode == treeTable.get_root() and currentNode.data != 'X':
        print(currentNode.data)
        childCharacter.append(currentNode.data)
        incrementGroups(currentNode)

    else:
        childCharacter.append(currentNode.data)
    if childNum != 0:
        for i in range(childNum):
            if currentNode.children[i].data in childCharacter or \
                    currentNode.children[i].data == 'X':
                pass
            else:
                childCharacter.append(currentNode.children[i].data)
                print(currentNode.data)
                incrementGroups(currentNode.children[i])

            CalculateValue(treeTable,currentNode.children[i])

def BFS(currentNode):
    print("\t" + currentNode.data)
    childNum = len(currentNode.children)
    for i in range(childNum):
        BFS(currentNode.children[i])


def CalculateEntropy():
    global groups
    global a_group
    global t_group
    global c_group
    global g_group
    p_a = 0
    p_t = 0
    p_c = 0
    p_g = 0
    if a_group != 0:
        p_a = long(a_group) / groups
        p_a *= math.log10(p_a)
    if t_group != 0:
        p_t = long(t_group) / groups
        p_t *= math.log10(p_t)
    if c_group != 0:
        p_c = long(c_group) / groups
        p_c *= math.log10(p_c)
    if g_group != 0:
        p_g = long(g_group) / groups
        p_g *= math.log10(p_g)

    entropy = -1 * (p_a + p_t + p_c + p_g)
    print(entropy)

def main(treeTable, aSet, tSet, cSet, gSet):
    global aGenomes 
    aGenomes = aSet
    global tGenomes
    tGenomes = tSet
    global cGenomes 
    cGenomes = cSet 
    global gGenomes 
    gGenomes = gSet
    visit(treeTable.get_root())
    #treeTable.get_root().data = 'X'
    print("NEW TABLE")
    BFS(treeTable.get_root())
    global groups
    global a_group
    global t_group
    global c_group
    global g_group
    groups = 0
    a_group = 0
    t_group = 0
    c_group = 0
    g_group = 0
    CalculateValue(treeTable, treeTable.get_root())
    print(groups)
    print(a_group)
    print(t_group)
    print(c_group)
    print(g_group)
    CalculateEntropy()
    return treeTable
