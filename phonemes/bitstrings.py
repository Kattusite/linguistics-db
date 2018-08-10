# A file dedicated to performing operations on bitstrings as if they were
# actually strings of bits (i.e. integers)
# This is not the best way of doing things, but it can be revised later by
# swapping in a more efficient bitstring representation (ie actually using bitwise ops)\\

def AND(a, b):
    validate(a, b)
    arr = []
    for i in range(len(a)):
        if a[i] == "1" and b[i] == "1":
            arr.append("1")
        else:
            arr.append("0")
    return "".join(arr)

def OR(a, b):
    validate(a, b)
    arr = []
    for i in range(len(a)):
        if a[i] == "1" or b[i] == "1":
            arr.append("1")
        else:
            arr.append("0")
    return "".join(arr)

def XOR(a, b):
    validate(a, b)
    arr = []
    for i in range(len(a)):
        if int(a[i]) + int(b[i]) == 1:
            arr.append("1")
        else:
            arr.append("0")
    return "".join(arr)

def NOT(a):
    validate(a, a)
    arr = []
    for i in range(len(a)):
        if a[i] == "1":
            arr.append("0")
        else:
            arr.append("1")
    return "".join(arr)

def validate(a, b):
    if len(a) != len(b):
        raise ValueError("Lengths of operand bitsrings do not match!")
    if type(a) != type("") or type(b) != type(""):
        raise TypeError("Type of operand is not a bitstring")
