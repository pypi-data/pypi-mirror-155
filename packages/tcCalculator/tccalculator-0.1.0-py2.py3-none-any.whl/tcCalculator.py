"""Simple math calculator package"""

__version__ = "0.1.0"


class calculate:

    """
     Has the basic math operations implemented including nth root:
     * addition
     * subtraction
     * multiplication
     * division
     * nth root

     By default, the memory is 0

    Usage example:

    >>> calculate = calculate()
    >>> calculate.add(2)
    2
    >>> calculate.add(4)
    6
    >>> calculate.add(2)
    8
    >>> calculate.root(3)
    2.0
    >>> calculate.subtract(0.5)
    1.5
    >>> calculate.reset()
    >>> calculate.memory()
    0

    """

    def __init__(self, value: float = 0) -> None:
        self.value = value

    def add(self, x: float) -> float:
        """Addition operation: adds x to the current memory value (inital = 0)."""
        self.value += x
        return self.value

    def subtract(self, x: float) -> float:
        """Subtraction operation: subtract x from the current memory value (inital = 0)."""
        self.value -= x
        return self.value

    def multiply(self, x: float) -> float:
        """Multiplication operation: multiplies x with the current memory value (inital = 0)."""
        self.value *= x
        return self.value

    def divide(self, x: float) -> float:
        """Division operation: divide x by the current memory value (inital = 0)."""
        self.value /= x
        return self.value

    def root(self, x: float) -> float:
        """Root operation: x root of the current memory value (inital = 0). """
        try:
            self.value = self.value ** (1/x)
            return self.value
        except:
            print("Root can't be 0 or negative number. Try again")

    def memory(self) -> float:
        """Returns the memory value"""
        return self.value

    def reset(self) -> None:
        """Resets the memory value"""
        self.value = 0


if __name__ == "__main__":

    import doctest
    print(doctest.testmod())
