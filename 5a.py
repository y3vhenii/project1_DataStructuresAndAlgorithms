#
# Created by Yevhenii Ganusich
#
import random
# -----------------------------------------------------------
# The following code implements recursive Binary Search Tree
# -----------------------------------------------------------


class Node:
    def __init__(self, val):
        self.val = val
        self.leftChild = None
        self.rightChild = None


# This function is used to insert nodes in the tree
def insertRec(root, newNode):
    # If the tree is empty
    if root is None:
        root = newNode
    # If the tree is not empty
    else:
        # If the parent node is less than new node
        if root.val < newNode.val:
            # and root doesn't have right child
            if root.rightChild is None:
                root.rightChild = newNode
            # if root has a right child, continue the recursion
            else:
                insertRec(root.rightChild, newNode)
        else:
            if root.leftChild is None:
                root.leftChild = newNode
            else:
                insertRec(root.leftChild, newNode)


# This function is used to delete nodes from the tree
def deleteRec(root, val):
    parentNode = None
    currentNode = root
    # Searching for the node with value val
    while currentNode != None and currentNode.val != val:
        # Keep track of parent node
        parentNode = currentNode
        # If value is less than root, jump to left child
        if val < currentNode.val:
            currentNode = currentNode.leftChild
        # If value is greater than root, jump to right child
        else:
            currentNode = currentNode.rightChild
    # If the node wasn't found in the tree
    if currentNode == None:
        return None

    # Case 1: the node has no children
    if currentNode.rightChild == None and currentNode.leftChild == None:
        if currentNode != root:
            if parentNode.leftChild == currentNode:
                parentNode.leftChild = None
            else:
                parentNode.rightChild = None
        else:
            root = None

    # Case 2: the node has 1 child
    elif (currentNode.rightChild != None and currentNode.leftChild == None) or (currentNode.rightChild == None and currentNode.leftChild != None):
        # If the right child is present
        if currentNode.rightChild != None:
            # If the node is not root
            if currentNode != root:
                # If current node is equal to parents left child
                if currentNode == parentNode.leftChild:
                    parentNode.leftChild = currentNode.rightChild
                else:
                    parentNode.rightChild = currentNode.rightChild
            # If the node is root
            else:
                root = currentNode.rightChild
                currentNode = None
        # If the left child is present
        elif currentNode.leftChild != None:
            # If the node is not root
            if currentNode != root:
                if currentNode == parentNode.leftChild:
                    parentNode.leftChild = currentNode.leftChild
                else:
                    parentNode.rightChild = currentNode.leftChild
            # If the node is root
            else:
                root = currentNode.leftChild
                currentNode = None

    # Case 3: the node has 2 children
    else:
        successor = findNextRec(currentNode, None, currentNode.val)
        successorVal = successor.val
        # Recursive call here
        deleteRec(root, successor.val)
        currentNode.val = successorVal
    return root


# Find minimum value in the tree recursively
# Finds the node, not the value
def findMinRec(root):
    if root.leftChild == None:
        return root
    return findMinRec(root.leftChild)


# Find maximum value in the tree recursively
def findMaxRec(root):
    if root.rightChild == None:
        return root
    return findMaxRec(root.rightChild)


# Find successor of the value recursively
# Returns the node, not the value
def findNextRec(root, successor, val):
    if root == None:
        return None
    # If the value is found
    if root.val == val:
        # If there is a right child in the root
        if root.rightChild != None:
            # Check if current node has children
            return findMinRec(root.rightChild)
    # If the value we are looking for is less than root value
    elif val<root.val:
        successor = root
        return findNextRec(root.leftChild, successor, val)
    else:
        return findNextRec(root.rightChild, successor, val)
    return successor


# Find the predecessor of the value recursively
# Returns the node, not the value
def findPrevRec(root, predecessor, val):
    if root == None:
        return None
    # If the value is found
    if root.val == val:
        # If there is a left child in the root
        if root.leftChild != None:
            # Check if current node has children
            return findMaxRec(root.leftChild)
    # If the value we are looking for is less than root value
    elif val<root.val:
        return findPrevRec(root.leftChild, predecessor, val)
    else:
        predecessor = root
        return findPrevRec(root.rightChild, predecessor, val)
    return predecessor


# This function is used to print out tree in order
def Inorder(root):
    if (root == None):
        return
    else:
        Inorder(root.leftChild)
        print(str(root.val) + " ")
        Inorder(root.rightChild)


# -----------------------------------------------------------
# The following code implements iterative AVL Tree
# -----------------------------------------------------------

class avlNode:
    # Node class constructor
    def __init__(self, val):
        self.val = val
        self.leftChild = None
        self.rightChild = None
        self.height = 0


# This function rotates the tree to the left
def rotateLeft(currentNode):
    # The new parent of the subtree becomes the right child of the currentNode
    temporaryNode = currentNode.rightChild
    # Set right child of the currentNode equal to left child of new parent
    currentNode.rightChild = temporaryNode.leftChild
    # Set new root node's left child equal to currentNode
    temporaryNode.leftChild = currentNode

    # Update heights
    updateHeight(currentNode)
    updateHeight(temporaryNode)
    return temporaryNode


# This function rotates the tree to the right
def rotateRight(currentNode):
    # The new parent of the subtree becomes the left child of the currentNode
    temporaryNode = currentNode.leftChild
    # Set left child of the currentNode equal to right child of new parent
    currentNode.leftChild = temporaryNode.rightChild
    # Set new root node's right child equal to currentNode
    temporaryNode.rightChild = currentNode

    # Update heights and return
    updateHeight(currentNode)
    updateHeight(temporaryNode)
    return temporaryNode


# This function checks if the current node is balanced
def checkIfBalanced(currentNode):
    if currentNode == None:
        return True
    else:
        # print("Balance factor of this node is: " + str(abs(getBalanceFactor(currentNode))))
        return abs(getBalanceFactor(currentNode)) <= 1


# This function returns balance factor of the current node
def getBalanceFactor(currentNode):
    heightOfLeftSubtree = getHeightOfNode(currentNode.leftChild)
    heightOfRightSubtree = getHeightOfNode(currentNode.rightChild)
    balanceFactor = heightOfLeftSubtree - heightOfRightSubtree
    return balanceFactor


# This function takes care of re-balancing the tree after insert or delete operations
# This function is only reached if insert or remove function notices dis-balance
def balanceAVLTree(root):
    currentBalanceFactor = getBalanceFactor(root)
    # If balance factor is > 1, the tree is left heavy
    if currentBalanceFactor > 1:
        leftChildBalance = getBalanceFactor(root.leftChild)
        # Left-right unbalanced tree
        if leftChildBalance < 0:
            root.leftChild = rotateLeft(root.leftChild)
        root = rotateRight(root)
        return root
    else:
        rightChildBalance = getBalanceFactor(root.rightChild)
        # Right-left unbalanced tree
        if rightChildBalance > 0:
            root.rightChild = rotateRight(root.rightChild)
        root = rotateLeft(root)
        return root


# This function updates height of the current node
def updateHeight(currentNode):
    if currentNode != None:
        currentNode.height = 1 + max(getHeightOfNode(currentNode.leftChild), getHeightOfNode(currentNode.rightChild))


# This function returns the height of the currentNode, otherwise it returns -1
def getHeightOfNode(currentNode):
    if currentNode != None:
        return currentNode.height
    else:
        return -1


# Iteratively insert the value in the tree
def insertIter(root, val):

    newNode = avlNode(val)     # make a new node with new value inserted
    currentNode = root      # create a pointer to the root node to start iteration
    parentNode = None       # keep track of parent node

    # This list will contain all the parents that will be traced back to the root
    parents = []
    # Iterate all the way to the leaf node
    while currentNode != None:
        # Keeping track of the parent node
        parentNode = currentNode
        # Appending current node to the array
        parents.append(parentNode)
        # If new value is greater than current node value, jump to the right child
        if newNode.val > currentNode.val:
            currentNode = currentNode.rightChild
        # otherwise jump to the left child
        else:
            currentNode = currentNode.leftChild

    # After we hit the last node, we retrieve parent value and assign it a new child based on whether the new node is
    # greater than or less than the parent
    if parentNode == None:
        parentNode = newNode
        return parentNode
    elif parentNode.val < newNode.val:
        parentNode.rightChild = newNode
    else:
        parentNode.leftChild = newNode

    # Re-balancing happens here...
    # Iterate through parents array in reverse order
    iterator = len(parents)-1
    for node in range(len(parents)):
        currentNode = parents[iterator]
        if not checkIfBalanced(currentNode):
            currentNode = balanceAVLTree(currentNode)
            # The node that possibly points to the subtree we are rotating
            possibleIndex = iterator - 1
            # If possible index is in bounds of the array
            if possibleIndex >= 0 and possibleIndex < len(parents):
                if currentNode.val < parents[possibleIndex].val:
                    updateHeight(currentNode)
                    parents[possibleIndex].leftChild = currentNode
                else:
                    updateHeight(currentNode)
                    parents[possibleIndex].rightChild = currentNode
            # If possible index is out of bounds of the array
            else:
                parentNode = currentNode
        else:
            updateHeight(currentNode)
            parentNode = currentNode
        iterator = iterator - 1

    return parentNode


# Iterative function to delete a node from the tree
def deleteIter(root, val):
    # In order to properly delete the node, we need to assume 3 cases.
    # 1-case: The node we are trying to delete has no children
    # 2-case: The node has one child
    # 3-case: The node has left and right child
    # Step 1: Search for the node with this value
    valueToFind = val
    currentNode = root
    parentNode = None
    isLeft = False

    # This list will contain all the parents that will be traced back to the root
    parents = []

    # Iterate through the tree
    while currentNode.val != valueToFind:
        parentNode = currentNode
        parents.append(parentNode)
        if valueToFind > currentNode.val:
            currentNode = currentNode.rightChild
            isLeft = False
        else:
            currentNode = currentNode.leftChild
            isLeft = True

    # CASE 1: Found node with no children
    if currentNode.rightChild == None and currentNode.leftChild == None:
        # If the node that gets deleted is not root
        if currentNode != root:
            # If the node is the left child, remove the pointer from parent to the left child
            if isLeft == True:
                parentNode.leftChild = None
                updateHeight(parentNode)
            # If the node is the right child, remove the pointer from parent to the right child
            else:
                parentNode.rightChild = None
                updateHeight(parentNode)

            # From here, we take care of balancing the tree if necessary
            iterator = len(parents) - 1     # Keep track of nodes from rightmost to leftmost nodes in the array
            # Iterating through array of traversed nodes
            for node in range(len(parents)):
                currentNode = parents[iterator]
                # Check if current node is unbalanced
                if not checkIfBalanced(currentNode):
                    # Return the balanced subtree
                    currentNode = balanceAVLTree(currentNode)
                    # The node that possibly points to the subtree we have rotated
                    possibleIndex = iterator - 1
                    # If possible index is in bounds of the array
                    if possibleIndex >= 0 and possibleIndex < len(parents):
                        # If rotated subtree root is less than its parent, assign it as a left child of its parent
                        if currentNode.val < parents[possibleIndex]:
                            updateHeight(currentNode)
                            parents[possibleIndex].leftChild = currentNode
                        # If rotated subtree root is greater than its parent, assign it as a right child of its parent
                        else:
                            updateHeight(currentNode)
                            parents[possibleIndex].rightChild = currentNode
                    # If possible index is out of bounds of the array, we are dealing with root node
                    else:
                        parentNode = currentNode
                # If current node is balanced, continue
                else:
                    updateHeight(currentNode)
                    parentNode = currentNode
                # Decrement the iterator
                iterator = iterator - 1

        # If the value we delete is a root, return None
        else:
            parentNode = None


    # CASE 2: Node with one child
    elif (currentNode.rightChild == None and currentNode.leftChild != None) or (currentNode.rightChild != None and currentNode.leftChild == None):
        # If the right child is present
        if currentNode.rightChild != None:
            if currentNode != root:
                if isLeft == True:
                    parentNode.leftChild = currentNode.rightChild
                    updateHeight(parentNode)
                else:
                    parentNode.rightChild = currentNode.rightChild
                    updateHeight(parentNode)
                # From here, we take care of balancing the tree if necessary
                iterator = len(parents) - 1  # Keep track of nodes from rightmost to leftmost nodes in the array
                # Iterating through array of traversed nodes
                for node in range(len(parents)):
                    currentNode = parents[iterator]
                    # Check if current node is unbalanced
                    if not checkIfBalanced(currentNode):
                        # Return the balanced subtree
                        currentNode = balanceAVLTree(currentNode)
                        # The node that possibly points to the subtree we have rotated
                        possibleIndex = iterator - 1
                        # If possible index is in bounds of the array
                        if possibleIndex >= 0 and possibleIndex < len(parents):
                            # If rotated subtree root is less than its parent, assign it as a left child of its parent
                            if currentNode.val < parents[possibleIndex]:
                                updateHeight(currentNode)
                                parents[possibleIndex].leftChild = currentNode
                            # If rotated subtree root is greater than its parent, assign it as a right child of its parent
                            else:
                                updateHeight(currentNode)
                                parents[possibleIndex].rightChild = currentNode
                        # If possible index is out of bounds of the array, we are dealing with root node
                        else:
                            parentNode = currentNode
                    # If current node is balanced, continue
                    else:
                        updateHeight(currentNode)
                        parentNode = currentNode
                    # Decrement the iterator
                    iterator = iterator - 1
            else:
                parentNode = currentNode.rightChild

        # If the left child is present
        else:
            if currentNode != root:
                if isLeft == True:
                    parentNode.leftChild = currentNode.leftChild
                    updateHeight(parentNode)
                else:
                    parentNode.rightChild = currentNode.leftChild
                    updateHeight(parentNode)
                iterator = len(parents) - 1  # Keep track of nodes from rightmost to leftmost nodes in the array
                # Iterating through array of traversed nodes
                for node in range(len(parents)):
                    currentNode = parents[iterator]
                    # Check if current node is unbalanced
                    if not checkIfBalanced(currentNode):
                        # Return the balanced subtree
                        currentNode = balanceAVLTree(currentNode)
                        # The node that possibly points to the subtree we have rotated
                        possibleIndex = iterator - 1
                        # If possible index is in bounds of the array
                        if possibleIndex >= 0 and possibleIndex < len(parents):
                            # If rotated subtree root is less than its parent, assign it as a left child of its parent
                            if currentNode.val < parents[possibleIndex]:
                                updateHeight(currentNode)
                                parents[possibleIndex].leftChild = currentNode
                            # If rotated subtree root is greater than its parent, assign it as a right child of its parent
                            else:
                                updateHeight(currentNode)
                                parents[possibleIndex].rightChild = currentNode
                        # If possible index is out of bounds of the array, we are dealing with root node
                        else:
                            parentNode = currentNode
                    # If current node is balanced, continue
                    else:
                        updateHeight(currentNode)
                        parentNode = currentNode
                    # Decrement the iterator
                    iterator = iterator - 1
            else:
                parentNode = currentNode.leftChild

    # Case 3: Node with two children
    elif (currentNode.rightChild != None and currentNode.leftChild != None):
        # Retrieving the list of next successor and its parent
        successorList = findNextIter(currentNode, currentNode.val)
        # Storing parent of successor
        parentOfSuccessor = successorList[0]
        # Storing the successor node here
        successor = successorList[1]

        # Swap the values of successor and current node
        if successor != None:
            currentNode.val = successor.val
        # if successor is the right child of current node
        if currentNode.rightChild == successor:
            # if successor has no children
            if successor.leftChild == None and successor.rightChild == None:
                currentNode.rightChild = None
            # if successor has right child
            elif successor.rightChild != None and successor.leftChild == None:
                currentNode.rightChild = successor.rightChild
            # if successor has left child
            elif successor.leftChild != None and successor.rightChild == None:
                currentNode.rightChild = successor.leftChild
            updateHeight(successor)
            updateHeight(currentNode)
        # If successor is a leaf
        else:
            if parentOfSuccessor.leftChild == successor:
                parentOfSuccessor.leftChild = None
            elif parentOfSuccessor.rightChild == successor:
                parentOfSuccessor.rightChild = None
            updateHeight(parentOfSuccessor)
        if currentNode != root:
            # Re-balancing the tree
            iterator = len(parents) - 1  # Keep track of nodes from rightmost to leftmost nodes in the array
            # Iterating through array of traversed nodes
            for node in range(len(parents)):
                currentNode = parents[iterator]
                # Check if current node is unbalanced
                if not checkIfBalanced(currentNode):
                    # Return the balanced subtree
                    currentNode = balanceAVLTree(currentNode)
                    # The node that possibly points to the subtree we have rotated
                    possibleIndex = iterator - 1
                    # If possible index is in bounds of the array
                    if possibleIndex >= 0 and possibleIndex < len(parents):
                        # If rotated subtree root is less than its parent, assign it as a left child of its parent
                        if currentNode.val < parents[possibleIndex]:
                            updateHeight(currentNode)
                            parents[possibleIndex].leftChild = currentNode
                        # If rotated subtree root is greater than its parent, assign it as a right child of its parent
                        else:
                            updateHeight(currentNode)
                            parents[possibleIndex].rightChild = currentNode
                    # If possible index is out of bounds of the array, we are dealing with root node
                    else:
                        parentNode = currentNode
                # If current node is balanced, continue
                else:
                    updateHeight(currentNode)
                    parentNode = currentNode
                # Decrement the iterator
                iterator = iterator - 1
        else:
            parentNode = currentNode

    return parentNode


# Find the successor of a certain node
def findNextIter(root, value):
    successor = None
    parentOfSuccessor = None
    returnList = []
    while True:                     # Continue until we hit the null
        if value<root.val:          # If value is less than root, traverse left child
            successor = root
            root = root.leftChild
        elif value>root.val:        # If value is greater than root, traverse right child
            root = root.rightChild
        else:                       # If we find value, its successor will be the smallest value in the right subtree
            if root.rightChild != None:
                successorList = findMinIter(root.rightChild)
                parentOfSuccessor = successorList[0]
                successor = successorList[1]
            break
        if root == None:
            return None
    if successor != None and parentOfSuccessor != None:
        returnList.append(parentOfSuccessor)
        returnList.append(successor)
        return successorList
    else:
        return None


# Find predecessor of the value
def findPrevIter(root, value):
    predecessor = None
    while True:  # Continue until we hit the null
        if value < root.val:  # If value is less than root, traverse left child
            root = root.leftChild
        elif value > root.val:  # If value is greater than root, traverse right child
            predecessor = root
            root = root.rightChild
        else:  # If we find value, its predecessor will be the greatest value in the left subtree
            if root.leftChild != None:
                predecessor = findMaxIter(root.leftChild)
            break
        if root == None:
            return None
    if predecessor == None:
        return None
    else:
        return predecessor


# Find minimum value in the tree
def findMinIter(root):
    returnList = []
    currentNode = root
    parentNode = root
    while currentNode.leftChild != None:        # Iterate to the leftmost node
        parentNode = currentNode                    # Store the parent node
        currentNode = currentNode.leftChild         # Set left child as current node
    returnList.append(parentNode)       # We are using these values in remove() in order to find parent of a child that
    returnList.append(currentNode)      # we are trying to delete
    return returnList


# Find maximum value in the tree
def findMaxIter(root):
    currentNode = root
    parentNode = None
    while currentNode.rightChild != None:       # Iterate to the rightmost node
        parentNode = currentNode                # Store the parent node
        currentNode = currentNode.rightChild    # Set right child as current node
    return currentNode


# Function to  print level order traversal of tree
def printLevelOrder(root):
    h = height(root)
    for i in range(1, h + 1):
        printGivenLevel(root, i)


def printGivenLevel(root, level):
    if root is None:
        return
    if level == 1:
        print "%d" % (root.val),
    elif level > 1:
        printGivenLevel(root.leftChild, level - 1)
        printGivenLevel(root.rightChild, level - 1)


# *** This function is borrowed from geeksForGeeks for printing the tree ***
def height(node):
    if node is None:
        return 0
    else:
        # Compute the height of each subtree
        lheight = height(node.leftChild)
        rheight = height(node.rightChild)

        # Use the larger one
        if lheight > rheight:
            return lheight + 1
        else:
            return rheight + 1


# This function generates random array
def getRandomArray(n):
    arr = []
    while len(arr) != n:
        randomNum = random.randint(0, n)
        if randomNum not in arr:
            arr.append(randomNum)
    return arr


if __name__ == '__main__':
    avlRoot = None
    bstRoot = None
    inputArray = getRandomArray(10000)
    print("Input array is generated successfully")
    # Inserting values in the iterative AVL Tree
    for index in range(len(inputArray)):
        avlRoot = insertIter(avlRoot, inputArray[index])
    print("Done inserting into AVL tree...")

    # Inserting values in the recursive BST
    for index in range(len(inputArray)):
        if index == 0:
            bstRoot = Node(inputArray[index])
        else:
            insertRec(bstRoot, Node(inputArray[index]))

    print("Done inserting into recursive BST...")

    # Both should output the same during in-order traversal
    print("Inorder traversal of AVL Tree...")
    Inorder(avlRoot)
    print("Inorder traversal of BST Tree...")
    Inorder(bstRoot)

