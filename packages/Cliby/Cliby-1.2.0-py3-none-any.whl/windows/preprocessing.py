from dataclasses import dataclass
import re

@dataclass
class cfuncition:
    raw: str
    return_type: str
    name: str
    args: dict

def findfunctions(src: str) -> list[cfuncition]:
    """
    Finds all functions in C source code
    :param src: C source code
    :return: list of functions
    """
    functions = []
    # Open source code
    with open(src, 'r') as f:
        for line in f.readlines():
            # If a letter is followed by a ( then another letter, then it is a function
            if re.search(r'[a-zA-Z][^ ]\([a-zA-Z]', line) and not ("if" in line or "else" in line or "while" in line) and not line.endswith(';'):
                declaration = line.split('{')[0]
                # Get return type
                return_type = declaration.split(' ')[0]
                # Get function name
                name = declaration.split(' ')[1].split('(')[0]
                # Get arguments
                args_dict = {}
                args = declaration.split('(')[1].split(')')[0].split(',')
                for arg in args:
                    arg = arg.strip()
                    args_dict[arg.split(' ')[-1]] = arg.split(' ')[0]
                # Iterate every argument and get type and name
                functions.append(cfuncition(declaration, return_type, name, args_dict))
    return functions

def prepend_includes(src: str, includes: list[str]) -> int:
    """
    Prepends includes to C source code
    :param src: C source code
    :param includes: list of includes
    :return: C source code with includes prepended
    """
    functions = findfunctions(src)
    # Open source code
    with open(src, 'r') as f:
        lines = f.readlines()
    # Write source code
    with open(src.split('.')[-2] + "_.c", 'w') as f:
        for line in lines:
            if re.search(r'[a-zA-Z][^ ]\([a-zA-Z]', line) and not ("if" in line or "else" in line or "while" in line) and not line.endswith(';'):
                line = "DllExport " + line
                f.write(line)
            else:
                f.write(line)
    # Prepend includes
    with open(src.split('.')[-2] + "_.c", 'r') as f:
        lines = f.readlines()

    for include in includes:
        lines.insert(0, '#include "{}"\n'.format(include))
    # Write source code
    with open(src.split('.')[-2] + "_.c", 'w') as f:
        for line in lines:
            f.write(line)

    return 0

def generate_header(src: str) -> int:
    """
    Generates header file from C source code functions
    :param src: C source code
    :param header: output header file
    :return: 0 if successful
    """
    header = src.split('.')[-2] + '_.h'
    # Find functions
    functions = findfunctions(src)
    # Find libs
    # Open header file
    with open(header, 'w') as f:
        # Write header
        f.write("#define DllExport   __declspec( dllexport )" + '\n')
    prepend_includes(src, [header.split('/')[-1].split('\\')[-1]])
    return 0

if __name__ == "__main__":
    generate_header('./tests/add.c', './tests/add.h')