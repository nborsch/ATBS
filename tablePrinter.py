# Solution to Practice Project "Table Printer"
# from "Automate The Boring Stuff", by Al Sweigart,
# Chapter 6.
# 
# Nadia Borsch      misc@nborsch.com        2018

tableData = [['apples', 'oranges', 'cherries', 'banana'],
             ['Alice', 'Bob', 'Carol', 'David'],
             ['dogs', 'cats', 'moose', 'goose']]

def printTable(inputList):

    # Creating list to store the longest string value for each list in inputList
    colWidths = [0] * len(inputList)

    # Iterating over each item to find longest string in each list
    for each in range(len(inputList)):
        for item in range(len(inputList[each])):
            if len(inputList[each][item]) > colWidths[each]:
                # Storing longest string value for each list
                colWidths[each] = len(inputList[each][item])

    # Iterating to print items
    for i in range(len(inputList)):
        for j in range(len(colWidths)):
            print(inputList[j][i].rjust(colWidths[j] + 3), end="")
        print("")
        

printTable(tableData)