#
# Created by Yevhenii Ganusich
#


class Node:
    def __init__(self, val):
        self.val = val
        self.leftChild = None
        self.rightChild = None
        self.height = 0     # AVL tree needs to store height of each node in the tree


# The next two functions take care of the rotations of the tree
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


# The next three functions take care of the balancing of the tree
# This function checks if the current node is balanced
def checkIfBalanced(currentNode):
    if currentNode == None:
        return True
    else:
        return abs(getBalanceFactor(currentNode)) <= 1


# This function returns balance factor of the current node by subtracting the height of right child from height of left child
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


# The next two functions take care of operations regarding the heights of nodes
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


# Next two functions take care of inserting and removing elements from the AVL tree
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
                root.rightChild = insertRec(root.rightChild, newNode)
        # If the parent node is greater than new node
        else:
            if root.leftChild is None:
                root.leftChild = newNode
            else:
                root.leftChild = insertRec(root.leftChild, newNode)
    # Re-balance the tree if necessary
    if not checkIfBalanced(root):
        root = balanceAVLTree(root)
    # Update the height of the root
    updateHeight(root)
    return root


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
        deleteRec(root, successor.val)
        currentNode.val = successorVal

    # Check if the tree is balanced and re-balance the tree if not
    if checkIfBalanced(root) == False:
        root = balanceAVLTree(root)
    # Update the height of the root
    updateHeight(root)
    return root


# Next two functions take care of finding the minimum and maximum values in the tree
# Find minimum value in the tree
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


# Next two functions take care of finding successor and predecessor values
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


def height(node):
    if node is None:
        return 0
    else:
        lheight = height(node.leftChild)
        rheight = height(node.rightChild)

        if lheight > rheight:
            return lheight + 1
        else:
            return rheight + 1


if __name__ == '__main__':
    # Inserting values in the tree
    root = None
    root = insertRec(root, Node(10))
    printLevelOrder(root)
    print(" :1")
    root = insertRec(root, Node(20))
    printLevelOrder(root)
    print(" :2")
    root = insertRec(root, Node(30))
    printLevelOrder(root)
    print(" :3")
    root = insertRec(root, Node(40))
    printLevelOrder(root)
    print(" :4")
    # Everything works fine until here
    root = insertRec(root, Node(50))
    printLevelOrder(root)
    print(" :5")
    root = insertRec(root, Node(60))
    printLevelOrder(root)
    print(" :6")
    root = insertRec(root, Node(80))
    printLevelOrder(root)
    print(" :7")

    # Test 1
    # Removing the nodes
    # root = deleteRec(root, 60)
    # printLevelOrder(root)
    # print(" : after removing 60")

    # root = deleteRec(root, 50)
    # printLevelOrder(root)
    # print(" : after removing 50")

    # root = deleteRec(root, 80)
    # printLevelOrder(root)
    # print(" : after removing 80")

    # Test 2
    # Removing the nodes
    root = deleteRec(root, 10)
    printLevelOrder(root)
    print(" : after removing 10")

    root = deleteRec(root, 30)
    printLevelOrder(root)
    print(" : after removing 30")

    root = deleteRec(root, 20)
    printLevelOrder(root)
    print(" : after removing 20")

    root = deleteRec(root, 50)
    printLevelOrder(root)
    print(" : after removing 50")

    root = deleteRec(root, 80)
    printLevelOrder(root)
    print(" : after removing 80")

    root = deleteRec(root, 40)
    printLevelOrder(root)
    print(" : after removing 40")

    root = deleteRec(root, 60)
    printLevelOrder(root)
    print(" : after removing 60")