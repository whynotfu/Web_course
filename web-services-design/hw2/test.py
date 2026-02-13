import subprocess
import pytest

# Для Windows
INTERPRETER = 'python'
# Для MAC
INTERPRETER = 'python3'

def run_script(filename, input_data=None):
    proc = subprocess.run(
        [INTERPRETER, filename],
        input='\n'.join(input_data if input_data else []),
        capture_output=True,
        text=True,
        check=False
    )
    return proc.stdout.strip()

from fact import fact_rec, fact_it
from show_employee import show_employee

test_data = {
    'fact_rec': [
        (1, 1),
        (2, 2),
        (3, 6),
        (5, 120),
        (10, 3628800),
        (20, 2432902008176640000),
    ],
    'fact_rec_errors': [
        (0, ValueError),
        (-1, ValueError),
        (-100, ValueError),
        (100001, ValueError),
        (1000000, ValueError),
        (5.5, TypeError),
        ("10", TypeError),
        (None, TypeError),
        (True, TypeError),
        ([5], TypeError),
    ],
    'fact_it': [
        (1, 1),
        (2, 2),
        (3, 6),
        (5, 120),
        (10, 3628800),
        (20, 2432902008176640000),
    ],
    'fact_it_errors': [
        (0, ValueError),
        (-1, ValueError),
        (-100, ValueError),
        (100001, ValueError),
        (1000000, ValueError),
        (5.5, TypeError),
        ("10", TypeError),
        (None, TypeError),
        (True, TypeError),
        ([5], TypeError),
    ],
    'fact_consistency': [1, 2, 3, 5, 7, 10, 15, 20, 50, 100],
    'show_employee': [
        ("Иванов Иван Иванович", 30000, "Иванов Иван Иванович: 30000 ₽"),
        ("Петров Пётр Петрович", 50000, "Петров Пётр Петрович: 50000 ₽"),
        ("Сидоров Сидор Сидорович", 0, "Сидоров Сидор Сидорович: 0 ₽"),
        ("John Doe", 150000, "John Doe: 150000 ₽"),
        ("A", 1, "A: 1 ₽"),
    ],
    'show_employee_default': [
        ("Иванов Иван Иванович", "Иванов Иван Иванович: 100000 ₽"),
        ("Петров Пётр Петрович", "Петров Пётр Петрович: 100000 ₽"),
        ("Test Name", "Test Name: 100000 ₽"),
    ],
}


@pytest.mark.parametrize("n, expected", test_data['fact_rec'])
def test_fact_rec(n, expected):
    assert fact_rec(n) == expected


@pytest.mark.parametrize("n, exc", test_data['fact_rec_errors'])
def test_fact_rec_errors(n, exc):
    with pytest.raises(exc):
        fact_rec(n)


@pytest.mark.parametrize("n, expected", test_data['fact_it'])
def test_fact_it(n, expected):
    assert fact_it(n) == expected


def test_fact_it_large_100():
    assert len(str(fact_it(100))) == 158


def test_fact_it_large_1000():
    assert len(str(fact_it(1000))) == 2568


@pytest.mark.parametrize("n, exc", test_data['fact_it_errors'])
def test_fact_it_errors(n, exc):
    with pytest.raises(exc):
        fact_it(n)


@pytest.mark.parametrize("n", test_data['fact_consistency'])
def test_fact_consistency(n):
    assert fact_rec(n) == fact_it(n)


@pytest.mark.parametrize("name, salary, expected", test_data['show_employee'])
def test_show_employee(name, salary, expected):
    assert show_employee(name, salary) == expected


@pytest.mark.parametrize("name, expected", test_data['show_employee_default'])
def test_show_employee_default(name, expected):
    assert show_employee(name) == expected
