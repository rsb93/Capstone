################################
#
#Treemaker converts a phylogenetic tree file into a tree data structure, 
#where each node in the tree contains:
#   data - used to store A T C or G, when a particular SNP is loaded      
#           into the tree using entropy calculator
#   name - stores the species name or branch number of the node depending  
#           on if the node is a leaf or not
#   children - stores the list of this nodes children
#   parent - stores this nodes parent
#
#The preprocess method removes unnecessary data from the tree file, and 
#creates a list containing "(", ")", and species names
#
#The branchfinder method reads through the processed list and builds the 
#initial tree
#
#the parentChildFinder method is used to generate the parents and 
#children for each branch
#
################################

# regular expression module
import re


# exception to demonstrate poorly formed Newick file
class NewickFileError(Exception):
    pass


class TreeTableNode:
    def __init__(self, name):
        self.data = ""
        self.name = str(name)
        self.children = []
        self.parent = []

    def add_child(self, obj):
        self.children.append(obj)

    def add_parent(self, obj):
        self.parent.append(obj)

    def printTree(self, level=0):
        print ('\t' * level + repr(level) + self.data + '-' + repr(len(self.children)) + ' ' +self.name)
        for child in self.children:
            child.printTree(level+1)


class TreeTable:

    def __init__(self, inFile):
        self.fo = open(inFile, "r")
        fs = self.fo.read();
        self.processed = self.preprocess(fs)
        self.branches = self.branchFinder(self.processed)
        self.parents, self.children = self.parentChildFinder(self.branches)
        self.fo.close()

    def get_root(self):
        return self.root

    def get_tree(self):
        return parents, children

    # this removes branch length values
    # returns a Newick formatted string
    def preprocess(self, fileString):
        fileString = fileString.replace("\n","")
        sre = re.compile(':0\.\d+')
        fileString = sre.sub("",fileString)
        stringList = []
        pos = 0
        for char in fileString:
            if char in ['(', ')']:
                stringList.append(char)
                pos += 1
            elif char == ',':
                pos += 1
                continue
            else:
                name = ''

                # pos will keep incrementing if an invalid character is present
                try:
                    while fileString[pos] not in ['(', ')', ',',';']:
                        name += fileString[pos]
                        pos += 1
                    if name != '':
                        stringList.append(name)
                except IndexError:
                    self.fo.close()
                    raise NewickFileError("Third argument must be a properly" +
                                          " formatted Newick file")

        return stringList

    def branchFinder(self, processedString):
        branches = []
        opens = []
        bpos = 0
        
        node_counter = 1
        self.root = TreeTableNode(0)
        current_node = self.root

        for i, char in enumerate(processedString):
            if i == 0 or i == len(processedString) - 1:
                continue
            if char == '(':
                opens.append(i)
                node = TreeTableNode(node_counter)
                node.add_parent(current_node)
                current_node.add_child(node)
                current_node = node
                node_counter += 1
                
            elif char == ')':
                branches.append([])
                for letter in processedString[opens.pop()+1:i]:
                    if letter in [',', '(', ')']:
                        continue
                    else:
                        branches[bpos].append(letter)
                        if current_node != self.root:
                            current_node = current_node.parent[0]
                bpos += 1
            elif char == ',':
                continue
            else:
                branches.append([char])
                n = TreeTableNode(char)
                current_node.add_child(n)
                bpos += 1
        self.root.printTree()
        return branches

    def parentChildFinder(self, branches):
        parents = []
        children = [[] for i in range(len(branches))]

        for i, branch in enumerate(branches):
            if i != len(branches) - 1:
                j = i + 1
                while not frozenset(branch) < frozenset(branches[j]):
                    if j == len(branches) - 1:
                        j = -1
                        break
                    j += 1
                parents.append(j)
                if j != -1:
                    children[j].append(i)
            else:
                parents.append(-1)
        return (parents, children)

    
