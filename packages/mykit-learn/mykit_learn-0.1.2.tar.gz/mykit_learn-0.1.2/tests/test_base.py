import mykit_learn.base as base


def test_base():
    assert base.NAME == "mykit_learn"

    # Control and Operators
    inp, cut, operator = "a", "b", "<"
    assert base.Control(inp, cut, operator).operate() == True
    assert base.Control(inp, cut, prints=False).printAllOps() == False
    assert base.Control(inp, cut).printAllOps() == False

    inp, cut, operator = "2", "2", "and"
    assert base.Control(inp, cut, operator).operate() == 'N/A'
    assert base.Control(inp, cut, prints=False).printAllOps() == True
    assert base.Control(inp, cut).printAllOps() == True