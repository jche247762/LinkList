import core

class UndoStack:
    """
    Undo Stack
    ----------
    Keeps track of the actions that were performed;
    When `pop()` is called, pops the last action off.
    """
    def __init__(self):
        self.stack = []

    def push(self, command, position):
        self.stack.append((command, position))

    def pop(self):
        # Empty List ;)
        try:
            return self.stack.pop()
        except IndexError:
            return None

class Node(core.Position):

    def __init__(self, element):
        self.element = element
        self.prev = None
        self.next = None

    def get_element(self):
        return self.element


class LinkedPositionalList(core.PositionalList):

    def __init__(self):
        # The header sentinel
        self._header = Node(None)
        # The trailer sentinel
        self._trailer = Node(None)

        # Setting the correct previous/next
        self._header.next = self._trailer
        self._trailer.prev = self._header

        # Initializing the undo stack
        self._undo_stack = UndoStack()

    def print_list(self):
        """
        Prints the current state of the list; Starting at the header and moving forwards.
        """
        current = self._header.next
        list_str = ""
        while True:
            if current == self._trailer:
                break
            list_str += "{} ".format(current.get_element())
            current = current.next

        return list_str

    def internal_insert(self, prev, next, new_node):
        # New node points to previous and next.
        new_node.next = next
        new_node.prev = prev

        # Position previous points to new node.
        next.prev = new_node

        # Old previous points to new node.
        prev.next = new_node

    def insert_first(self, element):
        # Make the new node
        new_node = Node(element)
        prev = self._header
        next = self._header.next

        self.internal_insert(prev, next, new_node)

        self._undo_stack.push("REMOVE", new_node)

        return new_node

    def insert_last(self, element):
        # Make the new node
        new_node = Node(element)
        prev = self._trailer.prev
        next = self._trailer

        self.internal_insert(prev, next, new_node)

        self._undo_stack.push("REMOVE", new_node)

        return new_node


    def insert_before(self, position, element):
        """
        Example:
        -A-B-
           ^- position=B
        INSERT: C
        -A-C-B-
        """

        new_node = Node(element)
        prev = position.prev
        next = position

        self.internal_insert(prev, next, new_node)

        # Add to undo stack
        self._undo_stack.push("REMOVE", new_node)

        return new_node

    def internal_remove(self, position):
        position.prev.next = position.next
        position.next.prev = position.prev

    def remove(self, position):
        self.internal_remove(position)

        self._undo_stack.push("INSERT", position)
        return position.element

    def undo(self):
        to_undo = self._undo_stack.pop()

        if to_undo is None:
            return None

        if to_undo[0] == "INSERT":
           self.internal_insert(to_undo[1].prev, to_undo[1].next, to_undo[1])
        else:
            self.internal_remove(to_undo[1])

        return to_undo[1]