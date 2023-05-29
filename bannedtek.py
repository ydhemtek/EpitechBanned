import os
import re
import sys
from termcolor import colored
from pyfiglet import Figlet

def load_ignored_functions(filename):
    ignored_functions = []

    if not os.path.exists(filename):
        return ignored_functions

    with open(filename, 'r') as f:
        lines = f.readlines()

    for line in lines:
        ignored_function = line.strip()
        if ignored_function:
            ignored_functions.append(ignored_function)

    return ignored_functions

def search_c_functions(directory, ignored_functions):
    total_files = 0
    c_func_count = 0

    c_functions = ['abort', 'abs', 'acos', 'asctime', 'asin', 'atan', 'atan2', 'atof', 'atoi',
                   'atol', 'bsearch', 'calloc', 'ceil', 'clearerr', 'clock', 'cos', 'cosh',
                   'ctime', 'difftime', 'div', 'exit', 'exp', 'fabs', 'fclose', 'feof', 'ferror',
                   'fflush', 'fgetc', 'fgetpos', 'fgets', 'floor', 'fmod', 'fopen', 'fprintf',
                   'fputc', 'fputs', 'fread', 'free', 'freopen', 'frexp', 'fscanf', 'fseek',
                   'fsetpos', 'ftell', 'fwrite', 'getc', 'getchar', 'gets', 'gmtime', 'isalnum',
                   'isalpha', 'iscntrl', 'isdigit', 'isgraph', 'islower', 'isprint', 'ispunct',
                   'isspace', 'isupper', 'isxdigit', 'labs', 'ldexp', 'ldiv', 'localtime', 'log',
                   'log10', 'longjmp', 'malloc', 'mblen', 'mbstowcs', 'mbtowc', 'memchr', 'memcmp',
                   'memcpy', 'memmove', 'memset', 'mktime', 'modf', 'putc', 'putchar', 'puts',
                   'qsort', 'raise', 'rand', 'realloc', 'remove', 'rename', 'rewind', 'scanf',
                   'setbuf', 'setjmp', 'setlocale', 'setvbuf', 'signal', 'sin', 'sinh', 'sprintf',
                   'sqrt', 'srand', 'sscanf', 'strcat', 'strchr', 'strcmp', 'strcoll', 'strcpy',
                   'strcspn', 'strerror', 'strftime', 'strlen', 'strncat', 'strncmp', 'strncpy',
                   'strpbrk', 'strrchr', 'strspn', 'strstr', 'strtod', 'strtok', 'strtol', 'strtoul',
                   'strxfrm', 'system', 'tan', 'tanh', 'time', 'tmpfile', 'tmpnam', 'tolower',
                   'toupper', 'ungetc', 'ungetwc', 'va_arg', 'va_end', 'va_start', 'vfprintf',
                   'vprintf', 'vsprintf', 'vsnprintf', 'wcstombs', 'wctomb']

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.c') or file.endswith('.h'):
                total_files += 1
                file_path = os.path.join(root, file)

                with open(file_path, 'r') as f:
                    lines = f.readlines()

                for line_num, line in enumerate(lines, start=1):
                    for func in c_functions:
                        pattern = rf'\b{func}\b'
                        if re.search(pattern, line):
                            if func not in ignored_functions:
                                if re.search(rf'(?<!my_){func}(?!\w)', line):
                                    c_func_count += 1
                                    colored_line = re.sub(pattern, lambda m: colored(m.group(), "yellow"), line)
                                    print(f"[{file_path}:{line_num}] {colored_line.strip()}")

    if total_files == 0:
        print("No .c or .h file found in specified folder.")
        return

    percentage = (c_func_count / total_files) * 100
    percentage_text = f"Percentage of C library functions present : {percentage:.2f}%."
    print(colored(percentage_text, "red"))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please specify the path of the folder to scan.")
        print("Example usage: python3 script.py /path/to/the/folder")
        sys.exit(1)

    directory_path = sys.argv[1]

    f = Figlet(font='big')
    ascii_text = f.renderText("VERIF BANNED FUNCTION")
    print(colored(ascii_text, "blue"))

    if not os.path.exists(directory_path):
        print("The specified path does not exist.")
        sys.exit(1)

    ignored_functions_file = "ignored_functions.txt"
    ignored_functions = load_ignored_functions(ignored_functions_file)

    search_c_functions(directory_path, ignored_functions)
