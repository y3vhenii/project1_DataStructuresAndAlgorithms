#
# Created by Yevhenii Ganusich
#
import random
def getRandomArray(n):
    arr = []
    while len(arr) != n:
        randomNum = random.randint(0, n)
        if randomNum not in arr:
            arr.append(randomNum)
    return arr
print(getRandomArray(10))
