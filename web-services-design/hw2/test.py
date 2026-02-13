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
from sum_and_sub import sum_and_sub
from process_list import process_list, process_list_gen
from my_sum import my_sum
from files_sort import files_sort
from file_search import file_search
from email_validation import fun as email_fun, filter_mail
from fibonacci import fibonacci, cube
from average_scores import compute_average_scores
from plane_angle import Point, plane_angle
from people_sort import name_format
from complex_numbers import Complex
from circle_square_mk import circle_square_mk
from log_decorator import function_logger
from phone_number import format_phone, sort_phone
import math
import os

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
    'sum_and_sub': [
        (1, 2, (3, -1)),
        (10, 5, (15, 5)),
        (0, 0, (0, 0)),
        (-3, -7, (-10, 4)),
        (-5, 5, (0, -10)),
        (2.5, 1.5, (4.0, 1.0)),
        (0.1, 0.2, (pytest.approx(0.3), pytest.approx(-0.1))),
        (1000000, 999999, (1999999, 1)),
    ],
    'process_list': [
        ([1, 2, 3, 4], [1, 4, 27, 16]),
        ([2, 4, 6], [4, 16, 36]),
        ([1, 3, 5], [1, 27, 125]),
        ([0], [0]),
        ([1], [1]),
        ([-1, -2, -3], [-1, 4, -27]),
        ([10, 11], [100, 1331]),
        ([0, 1, 2, 3], [0, 1, 4, 27]),
    ],
    'my_sum': [
        ((1, 2, 3), 6),
        ((10,), 10),
        ((), 0),
        ((1, -1), 0),
        ((-5, -3, -2), -10),
        ((0, 0, 0), 0),
        ((1.5, 2.5, 3.0), 7.0),
        ((1000000, 2000000, 3000000), 6000000),
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

@pytest.mark.parametrize("a, b, expected", test_data['sum_and_sub'])
def test_sum_and_sub(a, b, expected):
    assert sum_and_sub(a, b) == expected

@pytest.mark.parametrize("arr, expected", test_data['process_list'])
def test_process_list(arr, expected):
    assert process_list(arr) == expected

@pytest.mark.parametrize("arr, expected", test_data['process_list'])
def test_process_list_gen(arr, expected):
    assert list(process_list_gen(arr)) == expected


@pytest.mark.parametrize("arr, expected", test_data['process_list'])
def test_process_list_consistency(arr, expected):
    assert process_list(arr) == list(process_list_gen(arr))


@pytest.mark.parametrize("args, expected", test_data['my_sum'])
def test_my_sum(args, expected):
    assert my_sum(*args) == expected


def test_files_sort_grouped_by_ext(tmp_path):
    for name in ['a.py', 'b.py', 'a.txt', 'b.txt', 'c.py', 'c.txt']:
        (tmp_path / name).write_text('')
    assert files_sort(str(tmp_path)) == ['a.py', 'b.py', 'c.py', 'a.txt', 'b.txt', 'c.txt']


def test_files_sort_ignores_dirs(tmp_path):
    (tmp_path / 'a.py').write_text('')
    (tmp_path / 'subdir').mkdir()
    assert files_sort(str(tmp_path)) == ['a.py']


def test_files_sort_single_file(tmp_path):
    (tmp_path / 'only.txt').write_text('')
    assert files_sort(str(tmp_path)) == ['only.txt']


def test_files_sort_empty_dir(tmp_path):
    assert files_sort(str(tmp_path)) == []


def test_files_sort_no_extension(tmp_path):
    for name in ['Makefile', 'README', 'a.txt']:
        (tmp_path / name).write_text('')
    assert files_sort(str(tmp_path)) == ['Makefile', 'README', 'a.txt']


def test_files_sort_same_ext(tmp_path):
    for name in ['c.py', 'a.py', 'b.py']:
        (tmp_path / name).write_text('')
    assert files_sort(str(tmp_path)) == ['a.py', 'b.py', 'c.py']


def test_files_sort_multiple_exts(tmp_path):
    for name in ['z.csv', 'a.csv', 'b.json', 'a.json']:
        (tmp_path / name).write_text('')
    assert files_sort(str(tmp_path)) == ['a.csv', 'z.csv', 'a.json', 'b.json']


def test_files_sort_mixed_dirs_and_files(tmp_path):
    (tmp_path / 'dir1').mkdir()
    (tmp_path / 'dir2').mkdir()
    for name in ['b.txt', 'a.py']:
        (tmp_path / name).write_text('')
    assert files_sort(str(tmp_path)) == ['a.py', 'b.txt']


def test_file_search_found(tmp_path):
    (tmp_path / 'hello.txt').write_text('line1\nline2\nline3\n')
    result = file_search('hello.txt', str(tmp_path))
    assert result == ['line1', 'line2', 'line3']


def test_file_search_first_5_lines(tmp_path):
    content = '\n'.join(f'line{i}' for i in range(1, 11))
    (tmp_path / 'big.txt').write_text(content)
    result = file_search('big.txt', str(tmp_path))
    assert result == ['line1', 'line2', 'line3', 'line4', 'line5']


def test_file_search_not_found(tmp_path):
    assert file_search('nonexistent.txt', str(tmp_path)) is None


def test_file_search_in_subdir(tmp_path):
    sub = tmp_path / 'sub'
    sub.mkdir()
    (sub / 'deep.txt').write_text('found\n')
    result = file_search('deep.txt', str(tmp_path))
    assert result == ['found']


def test_file_search_empty_file(tmp_path):
    (tmp_path / 'empty.txt').write_text('')
    result = file_search('empty.txt', str(tmp_path))
    assert result == []


def test_file_search_less_than_5_lines(tmp_path):
    (tmp_path / 'short.txt').write_text('a\nb\n')
    result = file_search('short.txt', str(tmp_path))
    assert result == ['a', 'b']


def test_file_search_nested_deep(tmp_path):
    deep = tmp_path / 'a' / 'b' / 'c'
    deep.mkdir(parents=True)
    (deep / 'target.txt').write_text('deep content\n')
    result = file_search('target.txt', str(tmp_path))
    assert result == ['deep content']


def test_file_search_exactly_5_lines(tmp_path):
    content = '\n'.join(f'L{i}' for i in range(1, 6))
    (tmp_path / 'five.txt').write_text(content)
    result = file_search('five.txt', str(tmp_path))
    assert result == ['L1', 'L2', 'L3', 'L4', 'L5']


test_data['email_valid'] = [
    ('lara@mospolytech.ru', True),
    ('brian-23@mospolytech.ru', True),
    ('britts_54@mospolytech.ru', True),
    ('user@site.com', True),
    ('a@b.c', True),
    ('user123@test.org', True),
    ('my-name_99@web1.io', True),
]

test_data['email_invalid'] = [
    ('lara@mospolytech.technology', False),
    ('@mospolytech.ru', False),
    ('user@.ru', False),
    ('user@site.', False),
    ('user@site', False),
    ('user site@mail.ru', False),
    ('user@site!.ru', False),
    ('user@si te.ru', False),
    ('user@@site.ru', False),
    ('user@site.r4', False),
    ('', False),
]


@pytest.mark.parametrize("email, expected", test_data['email_valid'])
def test_email_valid(email, expected):
    assert email_fun(email) == expected


@pytest.mark.parametrize("email, expected", test_data['email_invalid'])
def test_email_invalid(email, expected):
    assert email_fun(email) == expected


def test_filter_mail_example():
    emails = ['lara@mospolytech.ru', 'brian-23@mospolytech.ru', 'britts_54@mospolytech.ru']
    result = filter_mail(emails)
    result.sort()
    assert result == ['brian-23@mospolytech.ru', 'britts_54@mospolytech.ru', 'lara@mospolytech.ru']


def test_filter_mail_mixed():
    emails = ['good@mail.ru', 'bad@@mail.ru', 'ok@site.com', 'nope@x.toolong']
    result = filter_mail(emails)
    result.sort()
    assert result == ['good@mail.ru', 'ok@site.com']


test_data['fibonacci'] = [
    (1, [0]),
    (2, [0, 1]),
    (3, [0, 1, 1]),
    (5, [0, 1, 1, 2, 3]),
    (7, [0, 1, 1, 2, 3, 5, 8]),
    (10, [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]),
    (15, [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]),
]

test_data['fibonacci_cubed'] = [
    (5, [0, 1, 1, 8, 27]),
    (3, [0, 1, 1]),
    (1, [0]),
]


@pytest.mark.parametrize("n, expected", test_data['fibonacci'])
def test_fibonacci(n, expected):
    assert fibonacci(n) == expected


@pytest.mark.parametrize("n, expected", test_data['fibonacci_cubed'])
def test_fibonacci_cubed(n, expected):
    assert list(map(cube, fibonacci(n))) == expected


def test_cube():
    assert cube(3) == 27
    assert cube(0) == 0
    assert cube(-2) == -8


test_data['average_scores'] = [
    (
        [(89, 90, 78, 93, 80), (90, 91, 85, 88, 86), (91, 92, 83, 89, 90.5)],
        (90.0, 91.0, 82.0, 90.0, 85.5),
    ),
    (
        [(100,), (50,)],
        (75.0,),
    ),
    (
        [(80, 60), (40, 20)],
        (60.0, 40.0),
    ),
    (
        [(0, 0, 0),],
        (0.0, 0.0, 0.0),
    ),
    (
        [(100, 100), (100, 100), (100, 100)],
        (100.0, 100.0),
    ),
    (
        [(10, 20, 30)],
        (10.0, 20.0, 30.0),
    ),
]


@pytest.mark.parametrize("scores, expected", test_data['average_scores'])
def test_average_scores(scores, expected):
    assert compute_average_scores(scores) == expected


def test_plane_angle_perpendicular():
    a = Point(0, 0, 0)
    b = Point(1, 0, 0)
    c = Point(1, 1, 0)
    d = Point(1, 1, 1)
    assert round(plane_angle(a, b, c, d), 2) == 90.0


def test_plane_angle_same_plane():
    a = Point(0, 0, 0)
    b = Point(1, 0, 0)
    c = Point(1, 1, 0)
    d = Point(2, 1, 0)
    assert round(plane_angle(a, b, c, d), 2) == 180.0


def test_plane_angle_opposite():
    a = Point(0, 0, 0)
    b = Point(1, 0, 0)
    c = Point(1, 1, 0)
    d = Point(0, 1, 0)
    assert round(plane_angle(a, b, c, d), 2) == 0.0


def test_plane_angle_45():
    a = Point(0, 0, 0)
    b = Point(1, 0, 0)
    c = Point(1, 1, 0)
    d = Point(1, 1, 1)
    angle = plane_angle(a, b, c, d)
    assert round(angle, 2) == 90.0


def test_plane_angle_arbitrary():
    a = Point(1, 2, 3)
    b = Point(4, 6, 5)
    c = Point(7, 8, 2)
    d = Point(10, 11, 15)
    angle = plane_angle(a, b, c, d)
    assert 0 <= angle <= 180


def test_point_sub():
    p1 = Point(3, 5, 7)
    p2 = Point(1, 2, 3)
    r = p1 - p2
    assert (r.x, r.y, r.z) == (2, 3, 4)


def test_point_dot():
    p1 = Point(1, 2, 3)
    p2 = Point(4, 5, 6)
    assert p1.dot(p2) == 32


def test_point_cross():
    p1 = Point(1, 0, 0)
    p2 = Point(0, 1, 0)
    r = p1.cross(p2)
    assert (r.x, r.y, r.z) == (0, 0, 1)


test_data['people_sort'] = [
    (
        [['Mike', 'Thomson', '20', 'M'], ['Robert', 'Bustle', '32', 'M'], ['Andria', 'Bustle', '30', 'F']],
        ['Mr. Mike Thomson', 'Ms. Andria Bustle', 'Mr. Robert Bustle'],
    ),
    (
        [['Anna', 'Smith', '25', 'F']],
        ['Ms. Anna Smith'],
    ),
    (
        [['John', 'Doe', '30', 'M'], ['Jane', 'Doe', '30', 'F']],
        ['Mr. John Doe', 'Ms. Jane Doe'],
    ),
    (
        [['C', 'Z', '50', 'M'], ['B', 'Y', '20', 'F'], ['A', 'X', '35', 'M']],
        ['Ms. B Y', 'Mr. A X', 'Mr. C Z'],
    ),
    (
        [['Tom', 'A', '5', 'M'], ['Sue', 'B', '3', 'F'], ['Bob', 'C', '1', 'M']],
        ['Mr. Bob C', 'Ms. Sue B', 'Mr. Tom A'],
    ),
    (
        [['X', 'Y', '10', 'F'], ['A', 'B', '10', 'M'], ['Z', 'W', '10', 'F']],
        ['Ms. X Y', 'Mr. A B', 'Ms. Z W'],
    ),
]


@pytest.mark.parametrize("people, expected", test_data['people_sort'])
def test_people_sort(people, expected):
    assert name_format(people) == expected


def test_complex_add():
    c = Complex(2, 1) + Complex(5, 6)
    assert str(c) == '7.00+7.00i'


def test_complex_sub():
    c = Complex(2, 1) - Complex(5, 6)
    assert str(c) == '-3.00-5.00i'


def test_complex_mul():
    c = Complex(2, 1) * Complex(5, 6)
    assert str(c) == '4.00+17.00i'


def test_complex_div():
    c = Complex(2, 1) / Complex(5, 6)
    assert str(c) == '0.26-0.11i'


def test_complex_mod():
    assert str(Complex(2, 1).mod()) == '2.24+0.00i'
    assert str(Complex(5, 6).mod()) == '7.81+0.00i'


def test_complex_str_zero_imag():
    assert str(Complex(3, 0)) == '3.00+0.00i'


def test_complex_str_zero_real():
    assert str(Complex(0, 5)) == '0.00+5.00i'
    assert str(Complex(0, -3)) == '0.00-3.00i'


def test_complex_str_negative_imag():
    assert str(Complex(4, -2)) == '4.00-2.00i'


def test_complex_add_zeros():
    c = Complex(0, 0) + Complex(0, 0)
    assert str(c) == '0.00+0.00i'


def test_complex_mul_by_zero():
    c = Complex(3, 4) * Complex(0, 0)
    assert str(c) == '0.00+0.00i'


def test_mk_r1():
    exact = math.pi
    approx = circle_square_mk(1, 100000)
    assert abs(approx - exact) / exact < 0.05


def test_mk_r5():
    exact = math.pi * 25
    approx = circle_square_mk(5, 100000)
    assert abs(approx - exact) / exact < 0.05


def test_mk_r10():
    exact = math.pi * 100
    approx = circle_square_mk(10, 100000)
    assert abs(approx - exact) / exact < 0.05


def test_mk_precision_grows():
    r = 5
    exact = math.pi * r ** 2
    err_small = abs(circle_square_mk(r, 1000) - exact) / exact
    err_large = abs(circle_square_mk(r, 500000) - exact) / exact
    assert err_large < err_small or err_large < 0.02


def test_mk_positive():
    assert circle_square_mk(3, 10000) > 0


def test_mk_small_n():
    result = circle_square_mk(1, 1)
    assert result >= 0


def test_logger_basic(tmp_path):
    logfile = str(tmp_path / 'test.log')

    @function_logger(logfile)
    def greeting(name):
        return f'Hello, {name}!'

    result = greeting('John')
    assert result == 'Hello, John!'
    with open(logfile, encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
    assert lines[0] == 'greeting'
    assert "('John',)" in lines[2]
    assert lines[3] == 'Hello, John!'
    assert len(lines) == 6


def test_logger_no_return(tmp_path):
    logfile = str(tmp_path / 'test.log')

    @function_logger(logfile)
    def do_nothing():
        pass

    do_nothing()
    with open(logfile, encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
    assert lines[0] == 'do_nothing'
    assert '-' in lines


def test_logger_kwargs(tmp_path):
    logfile = str(tmp_path / 'test.log')

    @function_logger(logfile)
    def add(a, b=0):
        return a + b

    add(1, b=2)
    with open(logfile, encoding='utf-8') as f:
        content = f.read()
    assert '(1,)' in content
    assert "'b': 2" in content
    assert '3' in content


def test_logger_appends(tmp_path):
    logfile = str(tmp_path / 'test.log')

    @function_logger(logfile)
    def inc(x):
        return x + 1

    inc(1)
    inc(2)
    with open(logfile, encoding='utf-8') as f:
        content = f.read()
    assert content.count('inc') == 2


def test_logger_preserves_name(tmp_path):
    logfile = str(tmp_path / 'test.log')

    @function_logger(logfile)
    def my_func():
        return 42

    assert my_func.__name__ == 'my_func'


def test_logger_datetime_format(tmp_path):
    logfile = str(tmp_path / 'test.log')
    import re

    @function_logger(logfile)
    def noop():
        return 1

    noop()
    with open(logfile, encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
    assert re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', lines[1])
    assert re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', lines[3])


test_data['format_phone'] = [
    ('07895462130', '+7 (789) 546-21-30'),
    ('89875641230', '+7 (987) 564-12-30'),
    ('9195969878', '+7 (919) 596-98-78'),
    ('+79195969878', '+7 (919) 596-98-78'),
    ('89001234567', '+7 (900) 123-45-67'),
    ('9001234567', '+7 (900) 123-45-67'),
    ('+79001234567', '+7 (900) 123-45-67'),
    ('09001234567', '+7 (900) 123-45-67'),
]

test_data['sort_phone'] = [
    (
        ['07895462130', '89875641230', '9195969878'],
        ['+7 (789) 546-21-30', '+7 (919) 596-98-78', '+7 (987) 564-12-30'],
    ),
    (
        ['9001112233', '9001112200'],
        ['+7 (900) 111-22-00', '+7 (900) 111-22-33'],
    ),
    (
        ['+79991234567'],
        ['+7 (999) 123-45-67'],
    ),
    (
        ['89991112233', '09991112233', '9991112233', '+79991112233'],
        ['+7 (999) 111-22-33', '+7 (999) 111-22-33', '+7 (999) 111-22-33', '+7 (999) 111-22-33'],
    ),
]


@pytest.mark.parametrize("number, expected", test_data['format_phone'])
def test_format_phone(number, expected):
    assert format_phone(number) == expected


@pytest.mark.parametrize("phones, expected", test_data['sort_phone'])
def test_sort_phone(phones, expected):
    assert sort_phone(phones) == expected


def test_sort_phone_example():
    phones = ['07895462130', '89875641230', '9195969878']
    result = sort_phone(phones)
    assert result == ['+7 (789) 546-21-30', '+7 (919) 596-98-78', '+7 (987) 564-12-30']


def test_sort_phone_single():
    assert sort_phone(['9001234567']) == ['+7 (900) 123-45-67']


def test_sort_phone_already_sorted():
    phones = ['9001112233', '9002223344', '9003334455']
    result = sort_phone(phones)
    assert result == ['+7 (900) 111-22-33', '+7 (900) 222-33-44', '+7 (900) 333-44-55']


def test_format_phone_strips_plus():
    assert format_phone('+79998887766') == '+7 (999) 888-77-66'
