
# Simple Math Calculator

This is a simple math calculator. It has the basic operations such as addition, subtraction,
multiplication, division. It also has capabilites to find the nth root. This calculator has
a memory so it stores all the computed values until the memory is reset.


## Installation

Install tcCalculator with pip

```bash
  pip install tcCalculator

```
    
## Features

- Addition operation
- Subtraction operation
- Multiplication operation
- Division operation
- nth Root operation


## Usage/Examples

```python
    from tcCalculator import calculate
    
    #initialize instance
    calculate = calculate()
    
    #calling methods
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
 
```

