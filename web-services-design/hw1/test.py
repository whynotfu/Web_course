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
        ('4', 'Not Weird'),
        ('3', 'Weird'),
        ('6','Weird'),
        ('22', 'Not Weird')
    ],
    'arithmetic_operators': [
        (['1', '2'], ['3', '-1', '2']),
        (['10', '5'], ['15', '5', '50'])
    ],
    'division': [
        (['3', '5'], ['0', '0.6']),
        (['10', '2'], ['5', '5.0']),
        (['-7', '3'], ['-3', '-2.3333333333333335']),
        (['7', '-3'], ['-3', '-2.3333333333333335']),
        (['-7', '-3'], ['2', '2.3333333333333335']),
        
    ],
    'loops': [
        ('1', ['0']),
        ('2', ['0', '1']),
        ('3', ['0', '1', '4']),
        ('5', ['0', '1', '4', '9', '16']),
        ('20', [str(i * i) for i in range(20)]),
    ]
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
