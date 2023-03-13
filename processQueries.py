import Q2
import os

"""
Class: CISC 235
Author: Simon McNeely
Date: March 3rd, 2021
"""

def readFiles(path):
    #this function takes a folder path and returns a list of webpage indexes

    fileList = os.listdir(path)
    webPageList = []

    #loop through the file list and add webpageindexes for each file in the folder
    for i in fileList:
        webPageList.append(Q2.WebPageIndex(path + "/" + i))

    return webPageList

    
def openFile(file):
    #simple file opening function
    infile = open(file,'r')

    #read and format
    data = infile.read()
    data = data.lower()

    #close and return
    infile.close()  
    return data



if __name__ == "__main__":
    #test the functions and implement the search engine

    data = readFiles("data")

    #create a webpage priority queue
    q = Q2.WebpagePriorityQueue("tree", data)

    #get the queries and format them
    queries = openFile("queries.txt")
    queries = queries.replace("\n","/")
    queries = queries.split("/")

    #user specified limit on when to stop searching files
    stop = 5

    #loop through the queries and reheap for every new query
    for query in queries:
        print("\n We are searching for:",query)
        q.reheap(query)

        #for every file in the heap, print the file name and occurances of the query if 
        #it is within the specified parameters
        for i in q.heap:
            if i.priority > 0 and i.priority < stop:        
                print("File:",i.file," Occurrances:",i.priority)

    #test the peek and poll functions
    print("\n")
    print("Peek:",q.peek().file)
    print("Poll:",q.poll().file)
    print("Peek Again:",q.peek().file)

    

    
