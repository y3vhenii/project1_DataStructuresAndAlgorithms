#
# Created by Yevhenii Ganusich
#
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
        deleteRec(root, successor.val)
        currentNode.val = successorVal
    return root

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

if __name__ == '__main__':
    # Inserting values in the tree
    root = Node(50)
    insertRec(root, Node(30))
    insertRec(root, Node(20))
    insertRec(root, Node(40))
    insertRec(root, Node(70))
    insertRec(root, Node(60))
    insertRec(root, Node(80))
    # Printing inOrder
    print ("InOrder traversal of the tree:")
    Inorder(root)
    # Deleting leaf node
    root = deleteRec(root, 20)
    print("Tree after deletion of 20:")
    Inorder(root)
    # Deleting a node with 1 child
    root = deleteRec(root, 30)
    print("Tree after deletion of 30:")
    Inorder(root)
    # Deleting a root node
    root = deleteRec(root, 50)
    print("Tree after deletion of 50:")
    Inorder(root)
    # Deleting a left child of root node
    root = deleteRec(root, 40)
    print("Tree after deletion of 40:")
    Inorder(root)
    # Deleting a root node again
    root = deleteRec(root, 60)
    print("Tree after deletion of 60:")
    Inorder(root)

