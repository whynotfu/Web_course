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
    ],
    'python_if_else_errors': [
        (['0'], 'ERROR'),
        (['101'], 'ERROR'),
        (['abc'], 'ERROR'),
    ],
    'arithmetic_operators': [
        (['1', '2'], ['3', '-1', '2']),
        (['10', '5'], ['15', '5', '50']),
        (['10000000000', '1'], ['10000000001', '9999999999', '10000000000']),
        (['0', '5'], ['5', '-5', '0']),
        (['-3', '4'], ['1', '-7', '-12']),
    ],
    'arithmetic_operators_errors': [
        (['5', '0'], 'ERROR'),
        (['10000000001', '1'], 'ERROR'),
        (['abc', '5'], 'ERROR'),        
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
    'loops_errors': [
        (['0'], 'ERROR'),     
        (['21'], 'ERROR'),   
        (['abc'], 'ERROR'),  
    ],

     'print_function': [
        ('1', '1'),
        ('2', '12'),
        ('5', '12345'),
        ('10', '12345678910'),
        ('20', ''.join(str(i) for i in range(1, 21))),
    ],
    'print_function_errors': [
        (['0'], 'ERROR'),
        (['21'], 'ERROR'),
        (['abc'], 'ERROR'),
    ],
    'second_score': [
        (['5', '2 3 6 6 5'], '5'),        
        (['4', '1 2 3 4'], '3'),          
        (['6', '10 10 9 8 8 7'], '9'),    
        (['3', '5 5 4'], '4'),            
        (['5', '-1 -2 -3 -4 -5'], '-2'),  
    ],
    'second_score_errors': [
        (['1', '5'], 'ERROR'),     
        (['3', '1 2'], 'ERROR'),   
        (['3', '5 5 5'], 'ERROR'), 
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
    'nested_list_errors': [
        (
        ['1',
         'a','10'],
        'ERROR'
        ),
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
        ('12345', '12345'),  
        ('aBc DeF', 'AbC dEf'),
    ],
    'swap_case_errors': [
        ([''], 'ERROR'),                 
        (['a' * 1001], 'ERROR'),       
    ],
    'split_and_join': [
        ('this is a string', 'this-is-a-string'),
        ('hello world', 'hello-world'),
        ('a b c', 'a-b-c'),
        ('  a   b  c ', 'a-b-c'),
        ('hello', 'hello'),
    ],
    'split_and_join_errors': [
        ([''], 'ERROR'),
        (['a' * 1001], 'ERROR'),
    ],
    'anagram': [
        (['abc', 'cba'], 'YES'),
        (['listen', 'silent'], 'YES'),
        (['hello', 'world'], 'NO'),
        (['aabbcc', 'abcabc'], 'YES'),
        (['abc', 'ab'], 'NO'),
        (['123', '321'], 'YES'),
    ],
    'metro': [
    (
        ['3',
         '1 5',
         '2 6',
         '7 10',
         '3'],
        '2'
    ),
    (
        ['2',
         '5 10',
         '10 15',
         '10'],
        '2'
    ),
    (
        ['2',
         '1 2',
         '3 4',
         '5'],
        '0'
    ),
    (
        ['3',
         '1 10',
         '2 9',
         '3 8',
         '5'],
        '3'
    ),
    ],
    'minion_game': [
        (['BANANA'], 'Stuart 12'),
        (['ABCD'], 'Stuart 6'),
        (['AEIOU'], 'Kevin 15'),
        (['BBBB'], 'Stuart 10'),
        (['AAAA'], 'Kevin 10'),
    ],
    'minion_game_errors': [
        ([''], 'ERROR'),         
        (['banana'], 'ERROR'),   
        (['ABC123'], 'ERROR'),   
    ],

    'is_leap': [
        (['2000'], 'True'),   
        (['1900'], 'False'),  
        (['2024'], 'True'),   
        (['2023'], 'False'),  
        (['2400'], 'True'),   
    ],
    'is_leap_errors': [
        (['1899'], 'ERROR'),    
        (['100001'], 'ERROR'),  
        (['abc'], 'ERROR'),     
    ],

    'happiness': [
    (
        ['3 2',
         '1 5 3',
         '3 1',
         '5 7'],
        '1'
    ),
    (
        ['3 3',
         '1 2 3',
         '1 2 3',
         '4 5 6'],
        '3'
    ),
    (
        ['3 3',
         '1 2 3',
         '4 5 6',
         '1 2 3'],
        '-3'
    ),
    (
        ['5 2',
         '1 2 3 2 1',
         '1 3',
         '2 4'],
        '1'
    ),
    ],
    'happiness_errors': [
        (
        ['0 2',
         '1 2',
         '1 2',
         '3 4'],
        'ERROR'
        ),
        (
        ['3 2',
         '1 2',
         '1 2',
         '3 4'],
        'ERROR'
        ),
        (
        ['2 1',
         '1 10000000000',
         '1',
         '2'],
        'ERROR'
        ),
        (
        ['2 2',
         '1 2',
         '1',
         '3 4'],
        'ERROR'
        ),
    ],
    'pirate_ship': [
    (
        ['50 3',
         'gold 10 60',
         'silver 20 100',
         'bronze 30 120'],
        [
            'gold 10.00 60.00',
            'silver 20.00 100.00',
            'bronze 20.00 80.00'
        ]
    ),
    (
        ['10 1',
         'diamond 20 200'],
        [
            'diamond 10.00 100.00'
        ]
    ),
    ],
    'matrix_mult': [
    (
        ['2',
         '1 2',
         '3 4',
         '5 6',
         '7 8'],
        [
            '19 22',
            '43 50'
        ]
    ),
    (
        ['2',
         '1 0',
         '0 1',
         '9 8',
         '7 6'],
        [
            '9 8',
            '7 6'
        ]
    ),
    (
        ['2',
         '-1 2',
         '3 -4',
         '5 6',
         '7 8'],
        [
            '9 10',
            '-13 -14'
        ]
    ),
    ],
    'matrix_mult': [
        (
        ['2',
         '1 2',
         '3 4',
         '5 6',
         '7 8'],
        ['19 22', '43 50']
        ),
    ],

    'matrix_mult_errors': [
        (['1'], 'ERROR'),   
        (['11'], 'ERROR'),  
        (
            ['2',
             '1 2 3',
             '3 4',
             '5 6',
             '7 8'],
            'ERROR'
        ),
        (
            ['2',
             '1 x',
             '3 4',
             '5 6',
             '7 8'],
            'ERROR'
        ),
    ]    
}

def test_hello_world():
    assert run_script('hello.py') == 'Hello, world!'

def test_max_word():
    output = run_script('max_word.py')
    assert output == "сосредоточенности"

def test_price_sum():
    output = run_script('price_sum.py')
    assert output == "6842.84 5891.06 6810.90"


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

@pytest.mark.parametrize("input_data, expected", test_data['anagram'])
def test_anagram(input_data, expected):
    assert run_script('anagram.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['metro'])
def test_metro(input_data, expected):
    assert run_script('metro.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['minion_game'])
def test_minion_game(input_data, expected):
    assert run_script('minion_game.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['is_leap'])
def test_is_leap(input_data, expected):
    assert run_script('is_leap.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['happiness'])
def test_happiness(input_data, expected):
    assert run_script('happiness.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['pirate_ship'])
def test_pirate_ship(input_data, expected):
    assert run_script('pirate_ship.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['matrix_mult_errors'])
def test_matrix_mult_errors(input_data, expected):
    assert run_script('matrix_mult.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['happiness_errors'])
def test_happiness_errors(input_data, expected):
    assert run_script('happiness.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['is_leap_errors'])
def test_is_leap_errors(input_data, expected):
    assert run_script('is_leap.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['minion_game_errors'])
def test_minion_game_errors(input_data, expected):
    assert run_script('minion_game.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['split_and_join_errors'])
def test_split_and_join_errors(input_data, expected):
    assert run_script('split_and_join.py', input_data) == expected 

@pytest.mark.parametrize("input_data, expected", test_data['nested_list_errors'])
def test_nested_list_errors(input_data, expected):
    assert run_script('nested_list.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['print_function_errors'])
def test_print_function_errors(input_data, expected):
    assert run_script('print_function.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['second_score_errors'])
def test_second_score_errors(input_data, expected):
    assert run_script('second_score.py', input_data) == expected


@pytest.mark.parametrize("input_data, expected", test_data['loops_errors'])
def test_loops_errors(input_data, expected):
    assert run_script('loops.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['arithmetic_operators_errors'])
def test_arithmetic_operators_errors(input_data, expected):
    assert run_script('arithmetic_operators.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['python_if_else_errors'])
def test_python_if_else_errors(input_data, expected):
    assert run_script('python_if_else.py', input_data) == expected