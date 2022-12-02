"""A circular genome for simulating transposable elements."""

from __future__ import annotations                       # future before everything else
from typing import (
    Generic, TypeVar, Iterable,
    Callable, Protocol
)

from abc import (
    # A tag that says that we can't use this class except by specialising it
    ABC,
    # A tag that says that this method must be implemented by a child class
    abstractmethod
)


# index modulos length
# fast to index into python list
# test look at what happens when u call __str__


class Genome(ABC):
    """Representation of a circular genome."""

    def __init__(self, n: int):
        """Create a genome of size n."""    

    @abstractmethod
    def insert_te(self, pos: int, length: int) -> int:
        """
        Insert a new transposable element.

        Insert a new transposable element at position pos and len
        nucleotide forward.

        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.

        Returns a new ID for the transposable element.
        """
        ...  # not implemented yet


    @abstractmethod
    def copy_te(self, te: int, offset: int) -> int | None:
        """
        Copy a transposable element.

        Copy the transposable element te to an offset from its current
        location.

        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.

        If te is not active, return None (and do not copy it).
        """
        ...  # not implemented yet

    @abstractmethod
    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        ...  # not implemented yet

    @abstractmethod
    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        ...  # not implemented yet

    @abstractmethod
    def __len__(self) -> int:
        """Get the current length of the genome."""
        ...  # not implemented yet

    @abstractmethod
    def __str__(self) -> str:
        """
        Return a string representation of the genome.

        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immidiatetly followed
        by the first.

        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """
        ...  # not implemented yet


class ListGenome(Genome):
    """
    Representation of a genome.

    Implements the Genome interface using Python's built-in lists
    """

    def __init__(self, n: int):
        """Create a new genome with length n."""
        self.genome = ['-']*n
        self.TE_counter = 0
        self.TEs = {}

    def insert_te(self, pos: int, length: int) -> int:
        """
        Insert a new transposable element.

        Insert a new transposable element at position pos and len
        nucleotide forward.

        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.

        Returns a new ID for the transposable element.
        """
        self.TE_counter += 1

        # disable existing TE. If it is active it is continuous. 
        for te in self.TEs:      
            if self.TEs[te][2] == 'A':                                       # looking at a max of all the TEs
                start = self.TEs[te][0]
                end = self.TEs[te][0] + self.TEs[te][1]
                if start < pos and pos < end:                               # 
                    self.disable_te(te)
                    break

        # update genome with insertion
        self.genome = self.genome[:pos] + ['A']*length + self.genome[pos:]   #

        # update pos for every TE positioned after the insertion
        for te in self.TEs:
            start = self.TEs[te][0]
            if pos <= start:
                self.TEs[te][0] += length

        # add to dictionary {1 : [pos, length, status}
        self.TEs[self.TE_counter] = [pos, length, 'A']

        return self.TE_counter
    

    def copy_te(self, te: int, offset: int) -> int | None:       
        """
        Copy a transposable element.

        Copy the transposable element te to an offset from its current
        location.

        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.

        If te is not active, return None (and do not copy it).
        """
        # if active                                               
        if self.TEs[te][2] == 'A':
            pos = self.TEs[te][0]
            length = self.TEs[te][1] 
            return self.insert_te((pos + offset) % len(self.genome), length)      # use modulos to make the genome circular

        else: return None

    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        # update dictionary
        self.TEs[te][2] = 'D'
        # update genome
        pos = self.TEs[te][0]
        length = self.TEs[te][1] 
        self.genome[pos:pos+length] = 'x' * length                                # assigning to list slice in O()

    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        active_list = [te for te in self.TEs if self.TEs[te][2] == 'A']
        return active_list 

    def __len__(self) -> int:
        """Current length of the genome."""
        return len(self.genome)

    def __str__(self) -> str:
        """
        Return a string representation of the genome.

        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immediately followed
        by the first.

        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """
        return ''.join(self.genome)

# I use the doubly linked list implementation
"""Doubly-linked lists."""

T = TypeVar('T')

class Link(Generic[T]):
    """Doubly linked link."""

    val: T
    prev: Link[T]
    next: Link[T]

    def __init__(self, val: T, p: Link[T], n: Link[T]):
        """Create a new link and link up prev and next."""
        self.val = val
        self.prev = p
        self.next = n

def insert_after(link: Link[T], val: T) -> None:
    """Add a new link containing val after link."""
    new_link = Link(val, link, link.next)
    new_link.prev.next = new_link
    new_link.next.prev = new_link

class LinkedListGenome(Genome):
    """
    Representation of a genome.

    Implements the Genome interface using linked lists.
    """

    def __init__(self, n: int):
        """Create a new genome with length n."""
        
        head: Link[T]  # Dummy head link

        # Configure the head link.
        # We are violating the type invariants this one place,
        # but only here, so we ask the checker to just ignore it.
        # Once the head element is configured we promise not to do
        # it again.
        self.head = Link(None, None, None)  # type: ignore
        self.head.prev = self.head
        self.head.next = self.head

        for _ in range(n):
            insert_after(self.head, '-')

        self.TEs = {}
        self.TE_counter = 0

    def insert_te(self, pos: int, length: int) -> int:
        """
        Insert a new transposable element.

        Insert a new transposable element at position pos and len
        nucleotide forward.

        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.

        Returns a new ID for the transposable element.
        """
        self.TE_counter += 1

        # disable existing TE. If it is active it is continuous. 
        for te in self.TEs:
            if self.TEs[te][2] == 'A':    
                start = self.TEs[te][0]
                end = self.TEs[te][0] + self.TEs[te][1]
                if start < pos and pos < end:         
                    self.disable_te(te)
                    break
        
        # update genome with insertion
        count = 1

        current = self.head.next
        # iterator
        while current is not self.head:
            if count == pos:
                # insert 'A'*length at pos
                for _ in range(length):
                    insert_after(current, 'A')    # or insert before? no
                break
            current = current.next
            count += 1
        
        # update pos for every TE positioned after the insertion
        for te in self.TEs:
            start = self.TEs[te][0]
            if pos <= start:
                self.TEs[te][0] += length

        # add to dictionary {1 : [pos, length, status}
        self.TEs[self.TE_counter] = [pos, length, 'A']

        return self.TE_counter

    def copy_te(self, te: int, offset: int) -> int | None:
        """
        Copy a transposable element.

        Copy the transposable element te to an offset from its current
        location.

        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.

        If te is not active, return None (and do not copy it).
        """

        # if active                                               
        if self.TEs[te][2] == 'A':
            pos = self.TEs[te][0]
            length = self.TEs[te][1]
        
            return self.insert_te((pos + offset) % len(self), length)      # use modulos to make the genome circular

        else: return None


    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        # update dictionary
        self.TEs[te][2] = 'D'
        # update genome
        pos = self.TEs[te][0]
        length = self.TEs[te][1]

        count = 0

        current = self.head.next
        # iterator
        while current is not self.head:
            if count == pos:
                for _ in range(length):
                    # change link value to 'x'
                    current.val = 'x'
                    current = current.next
                break
            current = current.next
            count += 1

    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        active_list = [te for te in self.TEs if self.TEs[te][2] == 'A']
        return active_list

    def __len__(self) -> int:
        """Current length of the genome."""
        counter = 0
        current = self.head.next
        while current is not self.head:
            current = current.next
            counter += 1

        return counter

    def __str__(self) -> str:
        """
        Return a string representation of the genome.

        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immidiatetly followed
        by the first.

        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """
        
        """Get string with the elements going in the next direction."""
        elms: list[str] = []
        link = self.head.next
        while link is not self.head:
            elms.append(str(link.val))
            link = link.next
        return ''.join(elms)