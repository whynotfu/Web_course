import os

def file_search(filename, start_dir=None):
    if start_dir is None:
        start_dir = os.path.dirname(os.path.abspath(__file__))
    for root, dirs, files in os.walk(start_dir):
        if filename in files:
            filepath = os.path.join(root, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = []
                for i, line in enumerate(f):
                    if i >= 5:
                        break
                    lines.append(line.rstrip('\n'))
            return lines
    return None

if __name__ == '__main__':
    import sys
    name = sys.argv[1]
    result = file_search(name)
    if result is None:
        print(f"Файл {name} не найден")
    else:
        for line in result:
            print(line)
