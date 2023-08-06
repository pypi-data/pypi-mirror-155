"""
mykit_learn base module.
"""

NAME = "mykit_learn"


class Control:
    import operator as o

    operators = {
        ">": o.gt,
        "<": o.lt,
        ">=": o.ge,
        "<=": o.le,
        "==": o.eq,
        "+": o.add,
        "-": o.sub,
        "//": o.floordiv,
        "/": o.truediv,
        "%": o.mod,
        "*": o.mul,
        "@": o.matmul,
        "**": o.pow,
        "not": o.not_,
        "is": o.is_,
        "and": o.and_,
        "or": o.or_,
        "xor": o.xor,
        "concat": o.concat,
        "contains": o.contains,
    }

    def __init__(self, inp, cut, op="", prints=True):
        self.inp = inp
        self.cut = cut
        self.op = op
        self.prints = prints

    def operate(self):
        try:
            return self.operators[self.op](self.inp, self.cut)
        except Exception:
            return "N/A"

    def printAllOps(self):
        last_op = ""

        for op in self.operators:
            self.op = op
            last_op = self.operate()
            if self.prints is True:
                print(
                    str(self.inp)
                    + " "
                    + op
                    + " "
                    + str(self.cut)
                    + " : "
                    + str(last_op)
                )

        return last_op
