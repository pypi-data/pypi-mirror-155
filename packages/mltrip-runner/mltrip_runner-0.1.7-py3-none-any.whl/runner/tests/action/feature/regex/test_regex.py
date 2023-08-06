import pytest


@pytest.mark.parametrize("run", ["regex.json"], indirect=True)
def test_regex(run):
    assert run == 0
    values = [4, 52.706986632, 0.885797144782, 3.8595430149, 248.889829489,
              0.0463496945413, 3.74712588231, 247.483437342, 0.399518064935,
              4.56903994962, 50.5971768535, 0.958371135622, -4.28812108518]
    with open("output_float_all.txt") as f:
        actual = [float(x) for x in f.read().strip()[1:-1].split(',')]
        expected = values[1:]
        assert len(actual) == len(expected)
        assert all([x == y for x, y in zip(actual, expected)])
    with open("output_float_index.txt") as f:
        actual = float(f.read().strip())
        expected = values[1:][3]
        assert actual == expected
    with open("output_float_indices.txt") as f:
        actual = [float(x) for x in f.read().strip()[1:-1].split(',')]
        expected = [values[1:][3], values[1:][5]]
        assert len(actual) == len(expected)
        assert all([x == y for x, y in zip(actual, expected)])
    with open("output_all.txt") as f:
        actual = [float(x) for x in f.read().strip()[1:-1].split(',')]
        expected = values
        assert len(actual) == len(expected)
        assert all([x == y for x, y in zip(actual, expected)])


@pytest.mark.parametrize("run", ["regex_line.yml"], indirect=True)
def test_regex(run):
    assert run == 0
    expected = [9.0, -8.99999999988, 8.99999999928, 8.99999999753, 8.99999999361,
                -8.99999998612, -8.99999997328, -8.99999995298, 8.99999992282,
                8.99999988015, 8.99999982215]
    with open("output_line.txt") as f:
        lines = [x for x in f]
        actual = [float(x) for x in lines[0].strip()[1:-1].split(',')]
        assert len(actual) == len(expected)
        assert all([x == pytest.approx(y) for x, y in zip(actual, expected)])
        assert float(lines[1].strip()) == pytest.approx(max(expected))
        assert float(lines[2].strip()) == pytest.approx(min(expected))
        assert float(lines[3].strip()) == pytest.approx(sum(expected) / len(expected))
