"""CLI interface for mykit_learn project.
"""


def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m mykit_learn` and `$ mykit_learn `.
    """

    import mykit_learn.base as base

    # Operators and Control
    inp, cut, operator = "2", "2", "and"
    print(inp + " " + operator + " " + cut)
    print(base.Control(inp, cut, operator).operate())
    print("----------\nAll Operators")
    base.Control(inp, cut).printAllOps()
