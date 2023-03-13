from collections import deque
import heapq

"""
Class: CISC 235
Author: Simon McNeely
Date: March 3rd, 2021
"""

class Node:
    def __init__ (self, key, value):
        #initialize nodes for the AVL tree
        self.key = key
        self.value = value
        self.rchild = None
        self.lchild = None
        self.height = 1
    

class AVLTree:
    def __init__(self):
        #initialize AVL tree
        self.root = None


    def get(self, root, key):
        #this function returns the value of an item if the key exists in the tree

        #if there is no root, return none
        if root is None:
            return None

        #if the inputted node is equal to the inputted key, return the value of the node
        elif (root.key == key):
            return root.value

        #if the inputted key is greater than the nodes key, recursively call the function with the nodes right child
        elif (root.key < key):
            return self.get(root.rchild, key)

        #if the inputted key is smaller than the nodes key, recursively call the function with the nodes left child
        else:
            return self.get(root.lchild, key)
    

    def put(self, root, key, value):
        #This function puts a new node in the AVL tree, inspired by the lecture code

        #if tree is empty return new node
        if root is None:
            return Node(key, value)

        #if new node's key is less than root, move it left
        elif key < root.key:
            root.lchild = self.put(root.lchild, key, value)

        #if new node's key is greater than root, move it right
        else:
            root.rchild = self.put(root.rchild, key, value)
        
        #change the height of the tree
        root.height = max(self.getHeight(root.lchild), self.getHeight(root.lchild)) + 1

        #balance factor
        bal = self.getBalance(root)
        
        #make sure the node has children to edit
        if root.lchild is None or root.rchild is None:
            return root
        
        #Case 1 - Left-Left
        if bal < -1 and key < root.lchild.key:
            return self.rightRotate(root)
        #Case 2 - Right-Right
        if bal > 1 and key > root.rchild.key:
            return self.leftRotate(root)
        #Case 3 - Left-Right
        if bal < -1 and key > root.lchild.key:
            root.lchild = self.leftRotate(root.lchild)
            return self.rightRotate(root)
        #Case 4 - Right-Left
        if bal > 1 and key < root.rchild.key:
            root.rchild = self.rightRotate(root.rchild)
            return self.leftRotate(root)

        return root

        
    def rightRotate(self, B):
        #this function performs a right rotation on the nodes in the tree, inspired from lecture

        if B.lchild is None:
            return None

        #set necessary variables
        A = B.lchild
        beta = A.rchild

        #rotate
        A.rchild = B
        B.lchild = beta

        #height modifications
        B.height = 1 + max(self.getHeight(B.lchild), self.getHeight(B.rchild))
        A.height = 1 + max(self.getHeight(A.lchild), self.getHeight(A.rchild))

        return A


    def leftRotate(self, A):
        #this function does a left rotation on the nodes in the tree, inspired from lecture
        if A.rchild is None:
            return None
        
        #set variables
        B = A.rchild
        beta = B.lchild

        #rotation
        B.lchild = A
        A.rchild = beta

        #height update
        A.height = 1 + max(self.getHeight(A.lchild), self.getHeight(A.rchild))
        A.height = 1 + max(self.getHeight(B.lchild), self.getHeight(B.rchild))

        return B


    def getHeight(self, root):
        #find the height of the tree
        if not root:
            return 0
        return root.height


    def getBalance(self, root):
        #return the balance of the tree
        if not root:
            return 0
        return self.getHeight(root.lchild) - self.getHeight(root.rchild)


    def preOrder(self,root):
        #this function loops through the tree in pre-order
        if not root:
            return None

        print(root.key, root.value)
        self.preOrder(root.lchild)
        self.preOrder(root.rchild)


    
class WebPageIndex:
    def __init__(self,file):
        #initialize a web page index object

        #set variables to access later, file keeps track of file name and priority is used to count instances of a word
        self.file = file
        self.priority = 0

        #open, access, and set file data
        infile = open(file,'r')
        self.data = infile.read()
        self.data = self.data.lower()
        infile.close()

        #remove punctuation
        p = ",.?!():"
        textList = ""
        for c in self.data:
            if c in p:
                self.data = self.data.replace(c, "")
            self.data = self.data.replace("/", " ")
        

    def makeAVL(self):
        #this function makes an AVL tree from the webpage index and organizes it based on instances of words
        textList = self.data.split()

        #count the words in the text list based on occurrances
        wordCount = {}

        for word in textList:
            count = wordCount.get(word,0)
            wordCount[word] = count + 1
        
        #create an AVL tree with the key being a word and the value as the instances of that word
        avl = AVLTree()
        root = None

        for i in wordCount:
            root = avl.put(root, i, wordCount[i])

        avl.preOrder(root)    
    

    def getCount(self, s):
        #this function counts the number of times a specific word appears in a web page index

        textList = self.data.split()
        count = 0

        #if the inputted word is in the text list, increase the count
        for i in textList:
            if s == i:
                count += 1
        
        return count


    #these functions override the comparison operators to be used to compare the priority values of web page indexes
    def __lt__(self, other):
        return self.priority < other.priority
    

    def __gt__(self, other): 
        return self.priority > other.priority


    def __eq__(self, other):
        return self.priority == other.priority



class WebpagePriorityQueue:

    def __init__(self, query, indexSet):
        #initialize an instance of a webpage priority queue

        #create the list of queries to be used
        queryList = query.split()

        #create necessary variables
        self.heap = []
        self.size = 0
        self.indexSet = indexSet

        #loop through webpage indexes
        for i in indexSet:
            sum = 0

            #set the priority of each webpage index based on the occurances of queries in the file
            for j in queryList:
                sum += i.getCount(j)

            #change the priority values and create the max heap
            i.priority = sum
            self.heap.append(i)
            self.maxheapify(len(self.heap)-1)
            


    def peek(self):
        #this function returns the top of the heap without removing it
        return self.heap[0]


    def poll(self):
        #this function returns the top of the heap while removing it
        return self.heap.pop(0)


    def getParent(self, pos):
        #this function gets the parent of an item in the heap
        return int((pos-1)/2)


    def hasP(self,pos):
        #this function returns whether or not an item in the heap has a parent or not
        return self.getParent(pos) < len(self.heap)
    

    def maxheapify(self, pos):
        #this function sorts the array into a max heap

        #while an item in the heap has a parent and is greater than the size of it parent
        while(self.hasP(pos) and (self.heap[pos] > self.heap[self.getParent(pos)])):

            #swap the items
            self.heap[pos], self.heap[self.getParent(pos)] = self.heap[self.getParent(pos)], self.heap[pos]
            pos = self.getParent(pos)


    def reheap(self, newQuery):
        #this function reheaps the webpage priority queue based on a new query

        self.heap.clear()
        self.size = 0

        #recounts the occurrances of a query and refreshes the heap with new priorities
        for i in self.indexSet:
            sum = 0
            sum += i.getCount(newQuery)
            i.priority = sum
            self.heap.append(i)
            self.maxheapify(len(self.heap)-1)


    
if __name__ == "__main__":
    #test the AVL tree 
    test = AVLTree()
    root = None

    #testing the put function
    root = test.put(root,15, "bob")
    root = test.put(root,20,"anna")
    root = test.put(root,24,"tom")
    root = test.put(root,10,"david")
    root = test.put(root,13,"david")
    root = test.put(root,7,"ben")
    root = test.put(root,30,"karen")
    root = test.put(root,36,"erin")
    root = test.put(root,25,"david")

    #testing the get function, prints Key: 20 Value: anna
    print("Key: 20 Value: ",test.get(root, 20))

    #tests the preorder function
    test.preOrder(root)

    #tests the creation of a webpageindex from a file
    page = WebPageIndex("data\doc1-arraylist.txt")

    #tests the counting of occcurances of the word array in doc1, prints 3
    print("The count is: ",page.getCount("array"))

    #makes an avl tree from a webpageindex
    page.makeAVL()


    

