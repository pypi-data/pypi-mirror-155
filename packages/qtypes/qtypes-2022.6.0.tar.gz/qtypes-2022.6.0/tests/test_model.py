import qtypes


def test_append():
    item = qtypes.Null()
    item.append(qtypes.Null("a"))
    item.append(qtypes.Null("b"))
    assert len(item) == 2


def test_insert():
    item = qtypes.Null()
    item.insert(0, qtypes.Null("a"))
    item.insert(1, qtypes.Null("b"))
    item.insert(0, qtypes.Null("c"))
    item.insert(-2, qtypes.Null("d"))
    assert len(item) == 4
    assert tuple(item.keys()) == ("c", "d", "a", "b")


def test_remove():
    item = qtypes.Null()
    b = qtypes.Null("b")
    item.append(qtypes.Null("a"))
    item.append(b)
    item.append(qtypes.Null("c"))
    assert len(item) == 3
    item.remove(b)
    assert len(item) == 2


def test_del():
    item = qtypes.Null()
    item.append(qtypes.Null("a"))
    item.append(qtypes.Null("b"))
    item.append(qtypes.Null("c"))
    assert len(item) == 3
    del item[1]
    assert tuple(item.keys()) == ("a", "c")
    assert len(item) == 2


def test_getitem():
    item = qtypes.Null()
    a = qtypes.Null("a")
    b = qtypes.Null("b")
    c = qtypes.Null("c")
    item.append(a)
    item.append(b)
    item.append(c)
    assert item[1] == b
    assert item["c"] == c


def test_setitem():
    item = qtypes.Null()
    a = qtypes.Null("a")
    b = qtypes.Null("b")
    c = qtypes.Null("c")
    item.append(a)
    item.append(c)
    item[1] = b
    assert item[1] == b


def test_reverse():
    item = qtypes.Null()
    a = qtypes.Null("a")
    b = qtypes.Null("b")
    c = qtypes.Null("c")
    item.append(a)
    item.append(b)
    item.append(c)
    item.reverse()
    assert tuple(item.keys()) == ("c", "b", "a")


def test_extend():
    item = qtypes.Null()
    a = qtypes.Null("a")
    b = qtypes.Null("b")
    c = qtypes.Null("c")
    item.append(a)
    item.extend([b, c])
    assert tuple(item.keys()) == ("a", "b", "c")


def test_iadd():
    item = qtypes.Null()
    item = qtypes.Null()
    a = qtypes.Null("a")
    b = qtypes.Null("b")
    c = qtypes.Null("c")
    item.append(a)
    item += [b, c]
    assert tuple(item.keys()) == ("a", "b", "c")


def test_pop():
    item = qtypes.Null()
    a = qtypes.Null("a")
    b = qtypes.Null("b")
    c = qtypes.Null("c")
    d = qtypes.Null("d")
    item.append(a)
    item.append(b)
    item.append(c)
    item.append(d)
    assert item.pop(1) == b
    assert tuple(item.keys()) == ("a", "c", "d")
    assert item.pop() == d
    assert tuple(item.keys()) == ("a", "c")
    assert item.pop("a") == a
    assert tuple(item.keys()) == ("c",)
    assert item.popitem(c) == c


def test_clear():
    item = qtypes.Null()
    a = qtypes.Null("a")
    b = qtypes.Null("b")
    c = qtypes.Null("c")
    d = qtypes.Null("d")
    item.append(a)
    item.append(b)
    item.append(c)
    item.append(d)
    assert len(item) == 4
    item.clear()
    assert len(item) == 0


def test_contains():
    item = qtypes.Null()
    a = qtypes.Null("a")
    b = qtypes.Null("b")
    c = qtypes.Null("c")
    d = qtypes.Null("d")
    item.append(a)
    item.append(b)
    item.append(c)
    assert a in item
    assert d not in item
    assert "b" in item
    assert "d" not in item


def test_iter():
    item = qtypes.Null()
    a = qtypes.Null("a")
    b = qtypes.Null("b")
    c = qtypes.Null("c")
    item.append(a)
    item.append(b)
    item.append(c)
    lis = [a, b, c]
    for qti, lisi in zip(item, lis):
        assert qti == lisi
    assert list(item) == lis
