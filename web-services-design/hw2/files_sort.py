import os

def files_sort(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    files.sort(key=lambda f: (os.path.splitext(f)[1], f))
    return files

if __name__ == '__main__':
    import sys
    path = sys.argv[1]
    for f in files_sort(path):
        print(f)
