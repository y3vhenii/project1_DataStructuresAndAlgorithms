#
# Created by Yevhenii Ganusich
#
def getSortedArray(n):
    tempVal = n
    sortedArray = []
    for i in range(n):
        sortedArray.append(tempVal)
        tempVal -= 1
    return sortedArray

print(getSortedArray(10))
