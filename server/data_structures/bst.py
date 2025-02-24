from typing import List
class Node:
    '''
    Classe that models a dinamic node of a binary tree.
    '''
    def __init__(self,data:object):
        '''
        Constructor that initializes a node with a data and
        without children.'''
        self.__data = data
        self.__left = None
        self.__right = None

    @property
    def data(self)->object:
        return self.__data

    @data.setter
    def data(self, newData:object):
        self.__data = newData

    @property
    def left(self)->'Node':
        return self.__left

    @left.setter
    def left(self, newleft:object):
        self.__left = newleft

    @property
    def right(self)->'Node':
        return self.__right

    @right.setter
    def right(self, newRightChild:'Node'):
        self.__right = newRightChild

    def addLeft(self, data:object):
        if self.__left == None:
            self.__left = Node(data)	

    def hasLeftChild(self)->bool:
        return self.__left != None

    def hasRightChild(self)->bool:
        return self.__right != None

    def addRight(self,data:object):
        if self.__right == None:
            self.__right = Node(data)

    def __str__(self):
        return f'{self.__data}'


        
class BinarySearchTree:
    '''
    Class that models a binary search tree data structure.
    Author: Alex Cunha  
    Date of last modification: 31/10/2023
    Attributes
    ----------
    root (Node): reference to the root node.
    '''
    preorder  = 0
    inorder   = 1
    postorder = 2
    def __init__(self):
        '''
        Initializes the tree with a root node.
        '''
        self.__root = None

    def getRoot(self)->any:
        '''
        Gets the data stored in the root node.
        '''
        return self.__root.data if self.__root is not None else None

    def isEmpty(self)->bool:
        '''
        Checks if the tree is empty.
        '''
        return self.__root == None

    def height(self)->int:
        '''
        Returns the height of the tree.
        -1 if the tree is empty. The root node has height 0.
        '''
        return self.__height(self.__root)
    
    def __height(self, root:Node)->int:
        if root is None:
            return -1
        else:
            return 1 + max(self.__height(root.left), self.__height(root.right))

    def add(self, data:any):
        '''
        Adds a new node to the tree.
        A new node is inserted in the right place according to BST properties.
        The left subtree of a node contains only nodes with keys lesser than 
        the node's key. The right subtree of a node contains only nodes 
        with keys greater than the node's key.

        Parameters
        ----------
        data (any): the data to be stored in the new node.
        '''
        if(self.__root == None):
            self.__root = Node(data)
        else:
            self.__add(data,self.__root)

    def __add(self, data:any, node:'Node'):
        if ( data < node.data):
            if( node.left != None):
                self.__add(data, node.left)
            else:
                node.addLeft(data)
        else:
            if( node.right != None):
                self.__add(data, node.right)
            else:
                node.addRight(data)
    
    def search(self, key:any )->any:
        '''
        Perform a search in the tree for a node with the given key
        Returns
        -------
        data (any): the data stored in the node corresponding the key.
        None: if the key is not found in the tree.
        '''
        if( self.__root != None ):
            node = self.__searchData(key, self.__root)
            return node.data if node is not None else None
        else:
            return None
    
    def __searchData(self, key:any, node:'Node'):
        if ( key == node.data):
            return node
        elif ( key < node.data and node.left != None):
            return self.__searchData( key, node.left)
        elif ( key > node.data and node.right != None):
            return self.__searchData( key, node.right)
        else:
            return None

    # Returns the number of nodes of the tree
    def __len__(self)->int:
        '''
        Counts the number of nodes in the tree.
        '''
        return self.__count(self.__root)

    def __count(self, node:'Node'):
        if ( node == None):
            return 0
        else:
            return 1 + self.__count(node.left) + self.__count(node.right)

    def traversal(self, order:int = None):
        '''
        Print the nodes of the in pre-order, in-order or post-order traversal.
        Arguments
        ---------
        order (int): the order of traversal. The possible values are:
        preorder, inorder, postorder. If no order is given, the traversal
        is performed in pre-order.
        '''
        if order == None:
            self.__preorder(self.__root)
        elif order == self.__class__.preorder:
            self.__preorder(self.__root)
        elif order == self.__class__.inorder:
            self.__inorder(self.__root)
        elif order == self.__class__.postorder:
            self.__postorder(self.__root)
        else:
            raise ValueError('Invalid order value')
        print()


    def __preorder(self, node):
        if( node != None):
            print(f'{node.data} ',end='')
            self.__preorder(node.left)
            self.__preorder(node.right)

    def __inorder(self, node):
        if( node != None):
            self.__inorder(node.left)
            print(f'{node.data} ',end='')
            self.__inorder(node.right)

    def __postorder(self, node):
        if( node != None):
            self.__postorder(node.left)
            self.__postorder(node.right)
            print(f'{node.data} ',end='')

    def clear(self):
        '''
        Deletes all nodes of the tree.
        '''
        # garbage collector will do the work of removing the nodes automatically.
        self.__root = None

 
    def delete(self, key:any)->'Node':
        '''
        Deletes a node with the given key and returns its data.
        Arguments
        ---------
        key (any): the key used to find the node to be deleted.
        Returns
        -------
        data (any): the data corresponding to the key node. If the key is not found
        return None.
        '''
        if self.__root is None:
            return None
        node = self.__searchData(key,self.__root)
        if node is not None:
            self.__root = self.__deleteNode(self.__root, key)
            return node.data
        else:
            return None
        
    
    def __deleteNode(self,root:'Node', key:any):
        '''
        Deletes a node with the given key and returns the new root node.
        Arguments
        ---------
        root (Node): the node that is the root of the search.
        key (any): the key used to find the node to be deleted.
        '''
        # Primary case: there is no root
        if root is None: 
            return root
  
        # If the key to be deleted is smaller than the root's key
        # then it lies in left subtree
        if key < root.data:
            root.left = self.__deleteNode(root.left, key) 

        # If the key to be deleted is greater than the root's key,
        # then it lies in right subtree
        elif(key > root.data):
            root.right = self.__deleteNode(root.right, key) 
  
        # If key is same as root's key, then this is the node to be deleted
        else:
            # (1) Node with only one child or no child
            if root.left is None : 
                temp = root.right  
                root = None 
                return temp

            elif root.right is None :
                temp = root.left  
                root = None
                return temp 
  
            # (2) Node with two children: Get the inorder successor
            # (smallest in the right subtree)
            temp = self.__minValueNode(root.right) 
  
            # Copy the inorder successor's content to this node
            root.data = temp.data 
  
            # Delete the inorder successor
            root.right = self.__deleteNode(root.right , temp.data)

        return root


    def __minValueNode(self, node:'Node')->'Node':
        '''
        Returns the node with the minimum key value found in the tree.
        Note that the entire tree does not need to be searched.
        Arguments
        ---------
        node (Node): the node that is the root of the search.   
        '''
        current = node 
  
        # Loop down to find the leftmost leaf
        while(current.left is not None): 
            current = current.left  
  
        return current

    def __maxValueNode(self, node:'Node')->'Node':
        '''
        Returns the node with the maximum key value found in the tree.
        Note that the entire tree does not need to be searched.
        Arguments
        ---------
        node (Node): the node that is the root of the search.
        '''
        current = node 
  
         # loop down to find the rightmost leaf
        while(current.right is not None): 
            current = current.right
  
        return current

    def __str__(self)->str:
        '''
        Returns a string representation of the tree in preorder traversal.
        '''
        return self.__preorderToStr(self.__root)[:-2]

    def __preorderToStr(self, root)->str:
        '''
        Returns a string representation of the tree in preorder traversal.
        Arguments
        ---------
        root (Node): the node that is the root of the traverse.
        '''
        if (root is None):
            return ''
    
        result = f'{root.data} | '
        result += self.__preorderToStr(root.left)
        result += self.__preorderToStr(root.right)
        return result

    
    def build(self,values:List[any]):
        '''
        Builds a binary search tree in the order the values appear in
        the list.        
        Precondition: the tree must be empty

        Arguments
        ---------
        values (List[any]): the list of values to be inserted in 
        the tree.
        '''
        if not values or self.__root != None:
            return None 

        for element in values:
            self.add(element)
    
    def balance(self):
        '''
        Balances the tree.
        '''
        nodes = []
        self.__saveToArray(self.__root, nodes)
        self.__root =  self.__rebuild(nodes, 0, len(nodes) - 1)

    def __saveToArray(self, root:Node,nodes:List[Node]):   
        '''
        A recursive method to get an array of nodes in inorder
        traversal of a given binary tree.
        Arguments
        ---------
        root (Node): the node of the tree.
        nodes (List[Node]): the list that stores the nodes visited
        in inorder traversal.
        Note
        ----
        Method of suport to the method __rebuild().
        '''         
        if not root:  # Base case
            return
        
        # Store nodes in Inorder traversal
        self.__saveToArray(root.left,nodes)
        nodes.append(root)
        self.__saveToArray(root.right,nodes)          


    def __iter__(self):
        '''
        Allow the tree to be iterated in preorder traversal.
        '''
        self.__stack = [self.__root]
        return self

    def __next__(self):
        '''
        Returns the next node in the iteration.
        '''
        if not self.__stack:
            raise StopIteration
        node = self.__stack.pop()
        if node.right:
            self.__stack.append(node.right)
        if node.left:
            self.__stack.append(node.left)
        return node.data
    
    def __contains__(self, key:any)->bool:
        '''
        Verifies if a key is present in the tree.
        Method is called when the operator "in" is used.
        '''
        value = self.search(key)
        return True if value else None

    