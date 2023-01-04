from coffee_break import depth_first_search
from coffee_break.node import File
from coffee_break.task import Task


def test_single_task():
    output_file = File("output.dat")
    input_file = File("input.dat")
    task = Task([input_file], [output_file])
    actual = depth_first_search(task)
    assert actual == [task]


def test_simple_linear():
    f1 = File("f1")
    f2 = File("f2")
    f3 = File("f3")
    t1 = Task([f1], [f2])
    t2 = Task([f2], [f3])
    actual = depth_first_search(t2)
    assert actual == [t1, t2]


def test_simple_branch():
    f1 = File("f1")
    f2 = File("f2")
    f3 = File("f3")
    f4 = File("f4")
    t1 = Task([f1], [f2])
    t2 = Task([f1], [f3])
    t3 = Task([f2, f3], [f4])
    actual = depth_first_search(t3)
    assert actual == [t1, t2, t3]


def test_diamond():
    f1 = File("f1")
    f2 = File("f2")
    f3 = File("f3")
    f4 = File("f4")
    f5 = File("f5")
    f6 = File("f6")
    t1 = Task([f1], [f2, f3])
    t2 = Task([f2], [f4])
    t3 = Task([f3], [f5])
    t4 = Task([f4, f5], [f6])
    actual = depth_first_search(t4)
    assert actual == [t1, t2, t3, t4]


def test_dag():
    f1 = File("f1")
    f2 = File("f2")
    f3 = File("f3")
    f4 = File("f4")
    t1 = Task([f1, f2], [f3, f4])

    f5 = File("f5")
    t2 = Task([f4], [f5])

    f6 = File("f6")
    t3 = Task([f3, f5], [f6])

    actual = depth_first_search(t3)
    assert actual == [t1, t2, t3]
