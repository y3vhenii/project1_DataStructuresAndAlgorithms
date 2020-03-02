#
# Created by Yevhenii Ganusich
#
class Node:
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

    newNode = Node(val)     # make a new node with new value inserted
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
    elif parentNode.val < newNode.val:
        parentNode.rightChild = newNode
    else:
        parentNode.leftChild = newNode

    # Re-balancing happens here...
    # Iterate through parents array in reverse order
    for node in reversed(parents):
        # Re-balance the tree if necessary
        if not checkIfBalanced(node):
            node = balanceAVLTree(node)
        # Update height of the node
        updateHeight(node)

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

    # Iterate through the tree
    while currentNode.val != valueToFind:
        parentNode = currentNode
        if valueToFind > currentNode.val:
            currentNode = currentNode.rightChild
            isLeft = False
        else:
            currentNode = currentNode.leftChild
            isLeft = True

    # Case 1: Found node with no children
    if currentNode.rightChild == None and currentNode.leftChild == None:
        if currentNode != root:
            # If the node is the left child, remove the pointer from parent to the left child
            if isLeft == True:
                parentNode.leftChild = None
            # If the node is the right child, remove the pointer from parent to the right child
            else:
                parentNode.rightChild = None
        else:
            root = None

    # Case 2: Node with one child
    if (currentNode.rightChild == None and currentNode.leftChild != None) or (currentNode.rightChild != None and currentNode.leftChild == None):
        if currentNode.rightChild != None:  # If the right child is present
            if currentNode != root:
                if isLeft == True:
                    parentNode.leftChild = currentNode.rightChild
                else:
                    parentNode.rightChild = currentNode.rightChild
            else:
                root = currentNode.rightChild

        else:   # If the left child is present
            if currentNode != root:
                if isLeft == True:
                    parentNode.leftChild = currentNode.leftChild
                else:
                    parentNode.rightChild = currentNode.leftChild
            else:
                root = currentNode.leftChild

    # Case 3: Node with two children
    if (currentNode.rightChild != None and currentNode.leftChild != None):
        # Retrieving the list of next successor and its parent
        successorList = findNextIter(currentNode, currentNode.val)
        parentOfSuccessor = successorList[0]
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
        # if successor is a leaf
        else:
            if parentOfSuccessor.leftChild == successor:
                parentOfSuccessor.leftChild = None
            elif parentOfSuccessor.rightChild == successor:
                parentOfSuccessor.rightChild = None
    return root


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


# Inorder traversal of the tree and printing it out
def Inorder(root):
    if (root == None):
        return
    else:
        Inorder(root.leftChild)
        print(str(root.val) + " ")
        Inorder(root.rightChild)


# Main method starts here
if __name__ == '__main__':
    root = None
    root = insertIter(root, 60)
    insertIter(root, 35)
    insertIter(root, 15)
    insertIter(root, 10)
    # insertIter(root, 70)
    # insertIter(root, 60)
    # insertIter(root, 80)
    # Printing inOrder
    print ("InOrder traversal of the tree in main:")
    Inorder(root)

    # Deleting leaf node
    # root = deleteIter(root, 20)
    # print ("InOrder traversal of the tree:")
    # Inorder(root)

    # Deleting root node
    # root = deleteIter(root, 50)
    # print ("InOrder traversal of the tree:")
    # Inorder(root)

    # Deleting node with 1 child
    # root = deleteIter(root, 70)
    # print ("InOrder traversal of the tree:")
    # Inorder(root)


