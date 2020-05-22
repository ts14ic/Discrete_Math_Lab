# UTM-DiscreteMath

Something, something, developed long ago to complete some discrete math tasks
in university.
Graph notation transformations, BFS/DPS searching, Spanning trees, Ford's search, Bellman-Kalaba's search, 
node power calculation and whatnot.

## Notation transformations
Supports 4 kinds of inputs: incidence matrix, adjacency matrix, adjacency list & weighted matrix.
The first three can be transformed between each other.  
The weighted matrix can only be transformed into a weighted list.  

*Incidence matrix*

A matrix describing a directed graph, where columns are vertices/nodes and rows are for edges.
Numbers can be separated by anything except these `-012`.  
Example:
 
    -1 1  0 0
     1 0 -1 0
     0 0  0 2
     0 0 -1 1

First row describes an edge from vertice 1 to vertice 2
Second row describes an edge from vertice 3 to vertice 1
Third row describes a cycle from vertice 4 to itself
Fourth row describes an ege from vertice 3 to vertice 4

*Adjacency matrix*   

A matrix describing a directed graph, where each row is a vertice, and each 1 in the row
represents an edge to a different edge (so columns are also vertices).
Example:  

    0 1 0 0
    0 0 0 0
    1 0 0 1
    0 0 0 1

First row describes an edge going from first vertice to second vertice.  
Second row describes no edges outgoing from second vertice.
Third row describes two edges going from third vertice to first and fourth vertices.
Fourth row describes a cyclic edge to fourth vertice. 

*Adjacency list*  

Just like adjacency matrix, but in a zero-terminated list form, where zero means just end of list.  
Example:
  
    1:2,0
    2:,0
    3:1,4,0
    4:4,0 

Same description as adjacency matrix example.

*Weighted matrix*  
Like an adjacency matrix but the numbers can be different than 1 and represent the weight of the path. 
Example:  

    0 4 0 0
    0 0 0 0
    2 0 0 1
    0 0 0 5

Gets transformed into:

    0: 1{4}
    1: 
    2: 0{2}, 3{1}
    3: 3{5}

The numbering goes from 0, and the lists are not zero terminated. The `{}` contain the weight of the edge.

## Spanning tree output
Takes the starting node and outputs the spanning tree (a graph including all nodes with minimum number of edges)
using the adjacency list notation.

## DFS & BFS searches
Prints the shortest path from first node to last node according to depth-first and breadth-first search algorithms.
Works on incidence and adjacency matrices only.

## Ford's search
Prints the shortest path from first node to last node, but works only on weighted matrix.
Uses the Ford's algorithm.  

## Bellman-Kalaba's search
Prints the shortest path from first node to last node, but works only on weighted matrix.
Uses the Bellman-Kalaba's algorithm (good luck finding who Kalaba is, that's what we were taught).

## Node power
Outputs the number of outgoing edges for a node.
