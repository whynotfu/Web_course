import subprocess
import pytest

# Для Windows
INTERPRETER = 'python'
# Для MAC
# INTERPRETER = 'python3' 

def run_script(filename, input_data=None):
    proc = subprocess.run(
        [INTERPRETER, filename],
        input='\n'.join(input_data if input_data else []),
        capture_output=True,
        text=True,
        check=False
    )
    return proc.stdout.strip()

test_data = {
    'python_if_else': [
        ('1', 'Weird'),       
        ('2', 'Not Weird'),    
        ('4', 'Not Weird'),
        ('5', 'Weird'),        
        ('6','Weird'),
        ('20','Weird'),        
        ('21','Weird'),        
        ('22', 'Not Weird'),  
        ('100','Not Weird'),
        ('101', 'Weird'),    
    ],
    'arithmetic_operators': [
        (['1', '2'], ['3', '-1', '2']),
        (['10', '5'], ['15', '5', '50']),
        (['10000000000', '1'], ['10000000001', '9999999999', '10000000000']),
        (['0', '5'], ['5', '-5', '0']),
        (['-3', '4'], ['1', '-7', '-12']),
    ],
    'division': [
        (['3', '5'], ['0', '0.6']),
        (['10', '2'], ['5', '5.0']),
        (['-7', '3'], ['-3', '-2.3333333333333335']),
        (['7', '-3'], ['-3', '-2.3333333333333335']),
        (['-7', '-3'], ['2', '2.3333333333333335']),
        (['0', '5'], ['0', '0.0']),
        (['5', '0'], ['division by zero']),
    ],
    'loops': [
        ('1', ['0']),
        ('2', ['0', '1']),
        ('3', ['0', '1', '4']),
        ('5', ['0', '1', '4', '9', '16']),
        ('20', [str(i * i) for i in range(20)]),
        ('20', [str(i * i) for i in range(20)]),
    ],
     'print_function': [
        ('1', '1'),
        ('2', '12'),
        ('5', '12345'),
        ('10', '12345678910'),
        ('20', ''.join(str(i) for i in range(1, 21))),
    ],
    'second_score': [
        (['5', '2 3 6 6 5'], '5'),        
        (['4', '1 2 3 4'], '3'),          
        (['6', '10 10 9 8 8 7'], '9'),    
        (['3', '5 5 4'], '4'),            
        (['5', '-1 -2 -3 -4 -5'], '-2'),  
    ],
    'nested_list': [
        (['5',
         'Harry', '37.21',
         'Berry', '37.21',
         'Tina', '37.2',
         'Akriti', '41',
         'Harsh', '39'],
        ['Berry', 'Harry']),
        (['3',
         'a', '10',
         'b', '20',
         'c', '30'],
        ['b']),
        (['4',
        'z', '50',
        'y', '40',
        'x', '40',
        'w', '60'],
        ['z']),
        (['3',
         'a', '-1',
         'b', '-2',
         'c', '-3'],
        ['b']),
    ],
    'lists': [
    (   ['4',
         'append 1',
         'append 2',
         'insert 1 3',
         'print'],
        ['[1, 3, 2]']
    ),

    (   ['12',
         'insert 0 5',
         'insert 1 10',
         'insert 0 6',
         'print',
         'remove 6',
         'append 9',
         'append 1',
         'sort',
         'print',
         'pop',
         'reverse',
         'print'],
        [
            '[6, 5, 10]',
            '[1, 5, 9, 10]',
            '[9, 5, 1]'
        ]
    ),
    (
        ['5',
         'append 1',
         'append 2',
         'print',
         'reverse',
         'print'],
        [
            '[1, 2]',
            '[2, 1]'
        ]
    ),
    ],
    'swap_case': [
        ('Www.MosPolytech.ru', 'wWW.mOSpOLYTECH.RU'),
        ('Pythonist 2', 'pYTHONIST 2'),
        ('abcDEF', 'ABCdef'),
        ('12345', '12345'),   # без букв
        ('aBc DeF', 'AbC dEf'),
    ],
    'split_and_join': [
        ('this is a string', 'this-is-a-string'),
        ('hello world', 'hello-world'),
        ('a b c', 'a-b-c'),
        ('  a   b  c ', 'a-b-c'),
        ('hello', 'hello'),
    ],


}

def test_hello_world():
    assert run_script('hello.py') == 'Hello, world!'

@pytest.mark.parametrize("input_data, expected", test_data['python_if_else'])
def test_python_if_else(input_data, expected):
    assert run_script('python_if_else.py', [input_data]) == expected

@pytest.mark.parametrize("input_data, expected", test_data['arithmetic_operators'])
def test_arithmetic_operators(input_data, expected):
    assert run_script('arithmetic_operators.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['division'])
def test_division(input_data, expected):
    assert run_script('division.py', input_data).split('\n') == expected    

@pytest.mark.parametrize("input_data, expected", test_data['loops'])
def test_loops(input_data, expected):
    assert run_script('loops.py', [input_data]).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['print_function'])
def test_print_function(input_data, expected):
    assert run_script('print_function.py', [input_data]) == expected

@pytest.mark.parametrize("input_data, expected", test_data['second_score'])
def test_second_score(input_data, expected):
    assert run_script('second_score.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['nested_list'])
def test_nested_list(input_data, expected):
    assert run_script('nested_list.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['lists'])
def test_lists(input_data, expected):
    assert run_script('lists.py', input_data).split('\n') == expected
    
@pytest.mark.parametrize("input_data, expected", test_data['swap_case'])
def test_swap_case(input_data, expected):
    assert run_script('swap_case.py', [input_data]) == expected

@pytest.mark.parametrize("input_data, expected", test_data['split_and_join'])
def test_split_and_join(input_data, expected):
    assert run_script('split_and_join.py', [input_data]) == expected


