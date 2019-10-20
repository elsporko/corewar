# coding: utf-8

from corewar.redcode import Instruction

__all__ = ['DEFAULT_INITIAL_INSTRUCTION', 'Core']

DEFAULT_INITIAL_INSTRUCTION = Instruction('DAT', 'F', '$', 0, '$', 0)

class Core(object):
    """The Core itself. An array-like object with a bunch of instructions and
       warriors, and tasks.
    """

    def __init__(self, initial_instruction=DEFAULT_INITIAL_INSTRUCTION,
                 size=8000, read_limit=None, write_limit=None):
        self.size = size
        self.write_limit = write_limit if write_limit else self.size
        self.read_limit = read_limit if read_limit else self.size
        self.clear()

    def clear(self, instruction=DEFAULT_INITIAL_INSTRUCTION):
        """Writes the same instruction thorough the entire core.
        """
        self.instructions = [instruction.core_binded(self) for i in range(self.size)]

    def trim_write(self, address):
        "Return the trimmed address to write, considering the write limit."
        return self._trim(address, self.write_limit)

    def trim_read(self, address):
        "Return the trimmed address to read, considering the read limit."
        return self._trim(address, self.read_limit)

    def trim(self, value):
        "Return a trimmed value to the bounds of the core size"
        return value % len(self)

    def trim_signed(self, value):
        "Return a trimmed value to the bounds of -core size to +core size"
        return value % len(self) if abs(value) > len(self) else value

    def _trim(self, address, limit):
        "Trims an address in the core, given a limit."
        result = address % limit
        if result > limit/2:
            result += self.size - limit
        return result

    def __getitem__(self, address):
        # The zip() function in Python 2 returns an iterable list, where Python 3
        # returns an iterator. Python 2 was able to make sense of 'address % self.size'
        # when address is a slice (vs. int) but those needs to be specified for Python 3.
        if (isinstance (address, slice)):
            return [self.instructions[i % self.size] for i in range (address.start, address.stop + 1)]
        return self.instructions[address % self.size]

    def __getslice__(self, start, stop):
        if start > stop:
            return self.instructions[start:] + self.instructions[:stop]
        else:
            return self.instructions[start:stop]

    def __setitem__(self, address, instruction):
        self.instructions[address % self.size] = instruction

    def __iter__(self):
        return iter(self.instructions)

    def __len__(self):
        return self.size

    def __repr__(self):
        return "<Core size=%d>" % self.size

