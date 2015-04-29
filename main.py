from PyQt4 import QtGui
import sys
import re
from collections import deque


class Window(QtGui.QWidget):
    """
    Discrete Math program main window
    """

    # noinspection PyUnresolvedReferences
    def __init__(self):
        """
        Construct the main window
        :return:
        """
        super(Window, self).__init__()

        self.setWindowTitle("Discrete Math (Iazinsky Artyom TI-146)")

        # Setting the layout:
        # Gui is divided in 4 parts.
        # A horizontal toolbar + 2 vertical columns for input\output + status label for error reporting.
        box = QtGui.QGridLayout()
        self.setLayout(box)

        # Setting Input layout:
        label_input = QtGui.QLabel("Graph Input")
        box.addWidget(label_input, 0, 0)

        # Setting input combo box, which we want to remember
        self.combo_input = QtGui.QComboBox(self)
        self.combo_input.addItem("Incidence Matrix")
        self.combo_input.addItem("Adjacency Matrix")
        self.combo_input.addItem("Adjacency List")
        box.addWidget(self.combo_input, 1, 0)

        # Setting input text area
        self.text_input = QtGui.QTextEdit(self)
        box.addWidget(self.text_input, 3, 0)

        # Setting Output layout:
        label_output = QtGui.QLabel("Graph Output")
        box.addWidget(label_output, 0, 1)

        # Setting the output combo box to remember
        self.combo_output = QtGui.QComboBox(self)
        self.combo_output.addItem("Incidence Matrix")
        self.combo_output.addItem("Adjacency Matrix")
        self.combo_output.addItem("Adjacency List")
        box.addWidget(self.combo_output, 1, 1)

        # Setting the apply button and connect it to processing code
        button_process = QtGui.QPushButton("Process")
        button_process.clicked.connect(self.process_graph)
        box.addWidget(button_process, 2, 0)

        # Setting the node power button
        button_nodepower = QtGui.QPushButton("Node power")
        button_nodepower.clicked.connect(self.print_node_power)
        box.addWidget(button_nodepower, 2, 1)

        # Setting the output text area to remember
        self.text_output = QtGui.QTextBrowser(self)
        box.addWidget(self.text_output, 3, 1)

        # Setting the search buttons
        buttons_search = QtGui.QHBoxLayout()
        button_dfs = QtGui.QPushButton("Perform DFS")
        button_dfs.clicked.connect(self.perform_dfs)
        buttons_search.addWidget(button_dfs)

        # Setting BFS button
        button_bfs = QtGui.QPushButton("Perform BFS")
        button_bfs.clicked.connect(self.perform_bfs)
        buttons_search.addWidget(button_bfs)

        box.addLayout(buttons_search, 4, 0)

        # Setting the spanning tree button
        button_spantree = QtGui.QPushButton("Get spanning tree")
        button_spantree.clicked.connect(self.get_span_tree)
        box.addWidget(button_spantree, 4, 1)

        # Setting the status label for error reporting
        self.status = QtGui.QLabel("Status: Ok...")
        box.addWidget(self.status, 5, 0)

        # Creating a class-scope adjacency list and oriented toggle option
        self.al = list()
        self.dfs_result = str()
        self.bfs_result = str()

    def perform_dfs(self):
        """
        Performs a Depth First Search and prints the result in status bar
        :return:
        """
        if len(self.al) == 0:
            self.status.setText("Error: No adjacency list stored!")
            return

        self.dfs_result = ""
        unvisited = deque(x for x in range(len(self.al)))
        stack = []

        while len(unvisited) > 0:
            n = unvisited.popleft()         # If stack empty, get the leftmost element from unvisited
            self.dfs_result += str(n+1)       # Set ready for printing
            stack.append(n)                 # Add to the stack
            while len(stack) > 0:
                top = stack[len(stack) - 1]

                if top in unvisited:
                    self.dfs_result += str(top+1)
                    unvisited.remove(top)

                # Get all adjacent unvisited for top
                adj = [x for x in self.al[top] if (x in unvisited) and (x not in stack)]

                if len(adj) > 0:
                    stack.append(adj[0])
                else:
                    stack.remove(top)

        self.status.setText("DFS result: " + "->".join(self.dfs_result))

    def perform_bfs(self):
        """
        Performs Breadth-First search and sets the status
        :return:
        """
        if len(self.al) == 0:
            self.status.setText("Error: No adjacency list stored!")
            return

        self.bfs_result = ""
        unvisited = deque(x for x in range(len(self.al)))
        queue = []

        while len(unvisited) > 0:
            n = unvisited.popleft()         # Get lefmost unvisited node
            self.bfs_result += str(n+1)     # Set ready for printing
            queue.append(n)                 # Add the node to queue
            while len(queue) > 0:
                tip = queue[0]              # Remember the begining of queue

                if tip in unvisited:
                    self.bfs_result += str(tip+1)
                    unvisited.remove(tip)

                # Get all adjacent unvisited nodes and queue them
                adj = [x for x in self.al[tip] if (x in unvisited) and (x not in queue)]
                queue += adj

                queue.remove(tip)
        self.status.setText("BFS result: " + "->".join(self.bfs_result))

    def print_node_power(self):
        """
        Prints the node power for a node
        :return:
        """
        if len(self.al) == 0:
            self.status.setText("Error: No adjacency list stored!")
            return

        num, ok = QtGui.QInputDialog.getText(QtGui.QInputDialog(), "Node power", "Enter node number",
                                             QtGui.QLineEdit.Normal)
        if not ok:
            return

        node = re.search("[1-9][0-9]*", num)
        if not node:
            self.status.setText("Error: Can't get node number. Try again")
            return

        node = int(node.group()) - 1
        if node >= len(self.al) or node == -1:
            self.status.setText("Error: There is no {} node in adjacency list".format(node+1))
            return

        row = self.al[node][1:]
        power = 0
        for i in row:
            power += 1
            if i == node:
                power += 1

        self.status.setText("Status: Node {} power: {}".format(node+1, power))

    def get_span_tree(self):
        """
        Prints the spanning tree of our graph
        :return:
        """
        if len(self.al) == 0:
            self.status.setText("Error: No adjacency list stored!")
            return

        span_tree = [[] for _ in range(len(self.al))]
        unvisited = deque(x for x in range(len(self.al)))
        queue = []

        while len(unvisited) > 0:
            queue.append(unvisited[0])      # Add leftmost unvisited node to queue
            while len(queue) > 0:
                tip = queue[0]              # Remember the begining of queue

                if tip in unvisited:
                    unvisited.remove(tip)
                    span_tree[tip].append(tip)
                    span_tree[tip] += [x for x in self.al[tip] if (x in unvisited) and (x not in queue)]

                # Get all adjacent unvisited nodes and queue them
                queue += [x for x in self.al[tip] if (x in unvisited) and (x not in queue)]
                queue.remove(tip)

        span_tree = [[str(x+1) for x in row]for row in span_tree]
        for i in range(len(span_tree)):
            if len(span_tree[i]) != 1:
                span_tree[i] = span_tree[i][0] + ": " + ", ".join(span_tree[i][1:]) + ", 0"
            else:
                span_tree[i] = span_tree[i][0] + ": 0"
        # noinspection PyTypeChecker
        span_tree = "\n".join(span_tree)

        QtGui.QMessageBox.information(QtGui.QMessageBox(), "Spanning tree", str(span_tree), QtGui.QMessageBox.Ok)

    def process_graph(self):
        """
        Summon the processing code
        :return:
        """
        # store the graph
        if self.combo_input.currentIndex() == 0:
            self.get_im()
        elif self.combo_input.currentIndex() == 1:
            self.get_am()
        elif self.combo_input.currentIndex() == 2:
            self.get_al()

        if self.combo_output.currentIndex() == 0:
            self.print_im()
        if self.combo_output.currentIndex() == 1:
            self.print_am()
        if self.combo_output.currentIndex() == 2:
            self.print_al()

    def get_im(self):
        """
        Get the incidence matrix
        :return:
        """

        # Get all the lines of input
        im = self.text_input.toPlainText().split("\n")

        # Extract every digit, (with - sign, if one exists)
        for i in range(len(im)):
            im[i] = re.findall(r"-?1|0|2", im[i])

        # Delete empty rows
        im = [x for x in im if x != []]

        # Int-ify elements
        im = [[int(x) for x in im[i]] for i in range(len(im))]

        # Check for input errors
        for i in im:
            if len(i) != len(im[0]):
                self.status.setText("Status: IM size is not persistent!")
                return
        else:
            if len(im) == 0:
                self.status.setText("Status: IM is empty!")
                return
            else:
                self.status.setText("Status: Ok...")

        # Store the matrix in an adjacency list
        self.im2al(im)

    # store adjacency matrix
    def get_am(self):
        """
        Get the adjacency matrix
        :return:
        """

        # Get all the lines of input.
        am = self.text_input.toPlainText().split("\n")

        # Extract digits
        for i in range(len(am)):
            am[i] = re.findall(r"[01]", am[i])

        # Delete empty rows
        am = [x for x in am if x != []]

        # Int-ify elements
        am = [[int(x) for x in am[i]] for i in range(len(am))]

        # Check for input errors
        for i in am:
            if len(i) != len(am[0]):
                self.status.setText("Status: AM size is not persistent!")
                return
        else:
            if len(am) == 0:
                self.status.setText("Status: AM is empty!")
                return
            elif len(am[0]) != len(am):
                self.status.setText("Status: AM is not square")
                return
            else:
                self.status.setText("Status: Ok...")

        # Save the matrix in adjacency list
        self.am2al(am)

    # store adjacency list
    def get_al(self):
        """
        Get the adjacency list
        :return:
        """
        # Get the lines
        al = self.text_input.toPlainText().split("\n")

        # Extract digits.
        for i in range(len(al)):
            al[i] = re.findall(r"\d+", al[i])

        # Delete empty rows.
        al = [x for x in al if x != []]

        # Int-ify elements.
        al = [[int(x)-1 for x in al[i] if(int(x)) > 0] for i in range(len(al))]

        # Sort the lines excluding repetiions.
        for i in al:
            i[1:] = sorted(set(i[1:]))

        # Check for user-input errors.
        if len(al) == 0:
            self.status.setText("Status: AL is empty!")
            return
        else:
            self.status.setText("Status: Ok...")

        # Store the adjacency list
        self.al = al.copy()

    def im2al(self, im):
        """
        Convert incidence matrix to adjacency list
        :param im:
        :return:
        """
        if not im:
            return
        am = self.im2am(im)
        self.am2al(am)

    @staticmethod
    def im2am(im) -> list:
        """
        Convert incidence matrix to adjacency matrix
        :param im:
        :return list:
        """
        if not im:
            return

        vertices = len(im)
        nodes = len(im[0])
        am = [[0]*nodes for _ in range(nodes)]

        for v in range(vertices):
            if 2 in im[v]:
                c = im[v].index(2)
                am[c][c] = 1
            else:
                row = im[v].index(-1)
                col = im[v].index(1)
                am[row][col] = 1

        return am

    def am2al(self, am):
        """
        Convert adjacency matrix to adjacency list
        :param am:
        :return:
        """
        if not am:
            return

        al = []
        nodes = len(am)

        for n in range(nodes):
            al.append([n])
            for v in range(len(am[n])):
                if am[n][v] == 1:
                    al[n].append(v)

        self.al = al.copy()

    def print_im(self):
        """
        Display incidence matrix on the output textbox
        :return:
        """
        if not self.al:
            return

        im = self.al2im()

        im = [[repr(x) for x in im[i]] for i in range(len(im))]

        for i in range(len(im)):
            im[i] = ",".join(im[i])
        im = "\n".join(im.copy())

        self.text_output.setText(im)

    def print_am(self):
        """
        Display adjacency matrix on the output textbox
        :return:
        """
        if not self.al:
            return

        am = self.al2am()

        am = [[repr(x) for x in am[i]] for i in range(len(am))]

        for i in range(len(am)):
            am[i] = ",".join(am[i])
        am = "\n".join(am.copy())

        self.text_output.setText(am)

    def print_al(self):
        """
        Display adjacency matrix
        :return:
        """
        if not self.al:
            return

        # Get a copy of stored adjacency list
        al = self.al.copy()

        # Increment the stored digits and transform to chars
        al = [[repr(int(x)+1) for x in al[i]] for i in range(len(al))]

        # Format the rows for output
        for i in range(len(al)):
            al[i] = str(al[i][0]) + ":" + ",".join(al[i][1:]) + ",0"
        al = "\n".join(al.copy())

        self.text_output.setText(al)

    def al2im(self) -> list:
        """
        Convert adjacency list to incidence matrix and return it
        :return list:
        """
        am = self.al2am()
        return self.am2im(am)

    def al2am(self) -> list:
        """
        Convert adjacency list to adjacency matrix and return it
        :return list:
        """
        al = self.al.copy()
        nodes = len(al)
        am = [[0]*nodes for _ in range(nodes)]

        for n in range(nodes):
            row = al[n][1:]
            for v in range(len(row)):
                am[n][row[v]] = 1

        return am

    @staticmethod
    def am2im(am) -> list:
        """
        Convert adjacency matrix to incidence matrix
        :return list:
        """
        if not am:
            return

        nodes = len(am)
        im = []

        vertice = int(0)
        for n in range(nodes):
            for c in range(len(am[n])):
                if am[n][c] == 1:
                    im.append([0]*nodes)
                    if n == c:
                        im[vertice][n] = 2
                    else:
                        im[vertice][n] = -1
                        im[vertice][c] = 1
                    vertice += 1

        return im


def main():
    app = QtGui.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
