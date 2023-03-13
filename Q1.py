from collections import deque

"""
Class: CISC 235
Author: Simon McNeely
Date: March 3rd, 2021
"""

class Node:
    def __init__ (self, data):
        #create node objects for the BST
        self.rchild = None
        self.lchild = None
        self.value = data


class BinarySearchTree:
    def __init__ (self):
        #initialize BST
        self.root = None
        self.size = 0
    

    def insert(self, x):
        #This function inserts new nodes into the BST and sorts the values
        new = Node(x)
        done = True
        self.size += 1

        if self.root == None:
            self.root = new
        else:
            current = self.root
            curVal = current.value
            done = False
        
        #loop until the nodes are properly sorted
        while not done:
            #if the new node is greater than the current node
            if x.value > curVal.value:

                #set it as the right child
                if curVal.rchild == None:
                    curVal.rchild = new
                    done = True
                else:
                    curVal = curVal.rchild.value
                    
            #if the new node is less than the current node
            else:

                #set it as the left child
                if curVal.lchild == None:
                    curVal.lchild = new
                    done = True
                else:
                    curVal = curVal.lchild.value


    def getHeight(self,node):
        #this function gets the height of a specific node recursively

        #if the node does not exist return 0
        if node is None:
            return 0
        #if the node is a leaf return 0
        elif node.value.rchild is None and node.value.lchild is None:
            return 0
        #otherwise get the maximum value of its children nodes' heights
        return max(self.getHeight(node.value.lchild), self.getHeight(node.value.rchild)) + 1


    def getTotalHeight(self,node):
        #this function gets the total height of the BST by recursively getting the heights of every child along with the current node
        if node is None:
            return 0
        return self.getTotalHeight(node.value.lchild) + self.getHeight(node) + self.getTotalHeight(node.value.rchild)


    def getWeightBalanceFactor(self, root):
        #This function gets the weight balance factor of the BST

        #if the root is empty, and its children are empty, return 0
        if root is None:
            return 0
        elif root.value.lchild is None and root.value.rchild is None:
            return 0
        #get the weight balance factor of the right child
        elif root.value.lchild is None and root.value.rchild is not None:
            return self.getWeightBalanceFactor(root.value.rchild) + 1
        #get the weight balance factor of the left child
        elif root.value.rchild is None and root.value.lchild is not None:
            return self.getWeightBalanceFactor(root.value.lchild) + 1
        #get the maximum weight balance factor of either the left side - the right side or the right side - the left side
        return max(self.getWeightBalanceFactor(root.value.lchild) - self.getWeightBalanceFactor(root.value.rchild), self.getWeightBalanceFactor(root.value.rchild) -self.getWeightBalanceFactor(root.value.lchild)) 


    def inOrder(self,node):
        #this function loops through the binary search tree in order
        if node is not None:
            self.inOrder(node.value.lchild)
            print (node.value.value)
            self.inOrder(node.value.rchild)


    
if __name__ == "__main__":
    #test code for the binary search tree
    test = BinarySearchTree()
    node1 = Node(5)
    node2 = Node(3)
    node3 = Node(6)
    node4 = Node(8)
    node5 = Node(9)
    node6 = Node(2)
    node7 = Node(7)
    node8 = Node(4)

    test.insert(node1)
    print("The size of the tree is:",test.size) #prints 1
    test.insert(node2)
    test.insert(node3)
    test.insert(node5)
    test.insert(node4)
    print("The Weight Balance Factor is: ",test.getWeightBalanceFactor(test.root)) #prints 2
    
    test.insert(node6)
    test.insert(node7)
    test.inOrder(test.root) #prints 2, 3, 5, 6, 7, 8, 9
    print("The total height is: ", test.getTotalHeight(test.root)) #prints 11
    print("The height of the root is: ", test.getHeight(test.root)) #prints 4
    print("The Weight Balance Factor is: ",test.getWeightBalanceFactor(test.root)) #prints 2
    test.insert(node8)

    test.inOrder(test.root) #prints 2, 3, 4, 5, 6, 7, 8, 9
    print("The total height is: ", test.getTotalHeight(test.root)) #prints 11
    print("The Weight Balance Factor is: ",test.getWeightBalanceFactor(test.root)) #prints 3
    

