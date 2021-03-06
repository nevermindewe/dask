import networkx as nx
from dask.dot import to_networkx, dot_graph
import os


def add(x, y):
    return x + y


def inc(x):
    return x + 1

dsk = {'x': 1, 'y': (inc, 'x'),
       'a': 2, 'b': (inc, 'a'),
       'z': (add, 'y', 'b'),
       'c': (sum, ['y', 'b'])}


def test_to_networkx():
    g = to_networkx(dsk)
    assert isinstance(g, nx.DiGraph)
    assert all(n in g.node for n in ['x', 'a', 'z', 'b', 'y'])


def test_dot_graph():
    fn = 'test_dot_graph'
    fns = [fn + ext for ext in ['.png', '.pdf', '.dot']]
    try:
        dot_graph(dsk, filename=fn)
        assert all(os.path.exists(f) for f in fns)
    finally:
        for f in fns:
            if os.path.exists(f):
                os.remove(f)
