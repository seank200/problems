import os
import subprocess
import time
import argparse
from dataclasses import dataclass
from datetime import datetime
from types import NoneType
from typing import Callable, List, Set, Union


# ###### CONSTANTS ######
VERSION = "1.0"
SRC_EXT = ['.py', '.c', '.cpp', '.o', '.js', '.ts']

# ##### UTILITIES #####
@dataclass
class SolutionResult:
    testcase_name: str = ''
    exec_time: float = 0.0
    checked: bool = False
    correct: bool = False
    proc_error: Union[subprocess.CalledProcessError, NoneType] = None
    infile_error: Union[OSError, NoneType] = None
    outfile_error: Union[OSError, NoneType] = None
    ansfile_error: Union[OSError, NoneType] = None
    timeout_exec: Union[subprocess.TimeoutExpired, NoneType] = None
    input_filepath: str = ''
    output_filepath: str = ''
    answer_filepath: str = ''

    @property
    def success(self):
        if self.proc_error or \
            self.infile_error or \
                self.outfile_error or \
                    self.ansfile_error or \
                        self.timeout_exec:
            return False
        
        if self.checked:
            return self.correct
        
        return True
    
    def __str__(self):
        s = ''

        # Result

        if self.success:
            s += 'CORRECT' if self.checked and self.correct else 'NO ERRORS'
            s += f' ({self.exec_time:.4f} s)'
        elif self.checked and not self.correct:
            s += 'WRONG'
            s += f' ({self.exec_time:.4f} s)'

        errors = []
        if self.proc_error:
            errors.append('RUNTIME ERROR')
        elif self.infile_error:
            errors.append('INPUT FILE ERROR')
        elif self.outfile_error:
            errors.append('OUTPUT FILE ERROR')
        elif self.ansfile_error:
            errors.append('ANSWER FILE ERROR')
        elif self.timeout_exec:
            errors.append('TIMED OUT')
        
        if errors:
            s += ", ".join(errors)

        return s


def print_seperator(sep: str = "=", width: int = 0):
    print(sep * (width if width else os.get_terminal_size().columns))


def recursive_listdir(filenames: Set[str], path: str):
    for p in os.listdir(path):
        if os.path.isdir(p):
            recursive_listdir(filenames, os.path.join(path, p))
        else:
            filenames.add(os.path.join(path, p))


# ##### FUNCTIONS #####

def parse_args()->argparse.Namespace:
    parser = argparse.ArgumentParser()

    # Special arguments
    parser.add_argument("--version", action="version", version=VERSION)
    
    # Positional arguments
    parser.add_argument("problem")

    # Optional arguments
    parser.add_argument("-i", "--input-path",  nargs="*", metavar="PATH")
    parser.add_argument("-a", "--answer-path", nargs="*", metavar="PATH")
    parser.add_argument("-s", "--solution-path", nargs=1, metavar="PATH")

    parser.add_argument("--stdin",
        action='store_const',
        const=True,
        default=False,
        help="Add a testcase without an answer that will accept input from stdin."
    )
    # parser.add_argument("--infile",
    #     action=argparse.BooleanOptionalAction,
    #     default=True,
    #     help="Ignore all input files"
    # )
    # parser.add_argument("--outfile",
    #     action=argparse.BooleanOptionalAction,
    #     default=False,
    #     help="Always keep/delete all output files. By default, only failed outputs will be kept."
    # )
    parser.add_argument("-t", "--timeout", type=int, default=0)
    parser.add_argument("-T", "--solution-type",
        choices=['s', 'python-script', 'm', 'python-module', 'e', 'executable'],
        default="python-script"
    )

    return parser.parse_args()


def get_input_filenames(problem: str, input_path: List[str] = [])->Set[str]:
    input_filenames: Set[str] = set()

    if os.path.isfile(f"{problem}.in"):
        input_filenames.add(f"{problem}.in")
    elif os.path.isdir(f"{problem}.in"):
        recursive_listdir(input_filenames, f"{problem}.in")

    if input_path:
        for path in input_path:
            if os.path.isfile(path):
                input_filenames.add(path)
            elif os.path.isdir(path):
                recursive_listdir(input_filenames, path)
    
    return input_filenames


def get_answer_filenames(problem: str, answer_path: Union[List[str], NoneType])->Set[str]:
    answer_filenames: Set[str] = set()

    if os.path.isfile(f"{problem}.ans"):
        answer_filenames.add(f"{problem}.ans")
    elif os.path.isdir(f"{problem}.ans"):
        recursive_listdir(answer_filenames, f"{problem}.ans")
    
    if answer_path:
        for path in answer_path:
            if os.path.isfile(path):
                answer_filenames.add(path)
            elif os.path.isdir(path):
                recursive_listdir(answer_filenames, path)

    return answer_filenames


def get_solution_filename(
    problem: str, 
    solution_path: Union[List[str], NoneType],
    solution_type: str
)->str:
    solution_filename: str = solution_path if solution_path else problem
    solution_ext = os.path.splitext(solution_filename)[1]

    if solution_type in ['s', 'python-script'] and solution_ext != '.py':
        solution_filename += '.py'
    elif solution_type in ['m', 'python-module'] and solution_ext:
        solution_filename = os.path.splitext(solution_filename)[0]
    elif solution_type not in ['e', 'executable']:
        raise RuntimeError
    
    return solution_filename


def check_answer(output_filepath: str, answer_filepath: str)->bool:
    diff_filepath = os.path.splitext(output_filepath)[0] + '.diff'
    run_kwargs = dict()
    diff_file = None

    try:
        diff_file = open(diff_filepath, "w")
        run_kwargs['stdout'] = diff_file
        run_kwargs['stderr'] = subprocess.STDOUT
    except OSError:
        print("ERROR - Failed to create {diff_filepath}")
    
    correct = True

    try:
        subprocess.run(
            ['diff', output_filepath, answer_filepath],
            check=True,
            text=True,
            encoding='utf-8',
            **run_kwargs
        )
    except subprocess.CalledProcessError:
        correct = False
    finally:
        if diff_file and not diff_file.closed:
            diff_file.close()

    return correct


def print_file(filepath: str):
    subprocess.run(['cat', filepath], encoding='utf-8', check=False)


def run_solution(
    args: argparse.Namespace,
    solution_filename: str, 
    input_filepath: str = '',
    answer_filepath: str = '',
    output_dirpath: str = '',
    testcase_count: int = -1,
    timeout: int = 0,
)->SolutionResult:
    # Init
    run_args = []
    run_kwargs = {}
    infile = None
    outfile = None
    result = SolutionResult()

    # Set timeout for solution run
    if timeout:
        run_kwargs['timeout'] = timeout

    # Resolve solution file path
    if args.solution_type in ['s', 'python-script']:
        run_args.append('python3')
    run_args.append('.' + os.path.sep + solution_filename)

    # Resolve output filepath
    output_filepath = ''
    if testcase_count >= 0:     # Multiple testcases
        if input_filepath:      # input_filepath + ".out"
            output_filepath += os.path.splitext(input_filepath)[0]
        elif answer_filepath:   # answer_filepath + ".out"
            output_filepath += os.path.splitext(answer_filepath)[0]
    else:                       # Single testcase
        output_filepath = os.path.splitext(solution_filename)[0]

    # Generate all outputs inside a single directory
    if output_dirpath:
        output_filepath = os.path.join(output_dirpath, output_filepath)
    
    # Output files have .out extensions
    if output_filepath:
        output_filepath += '.out'

    # Resolve the name of the current testcase
    testcase_name = 'testcase_'
    if testcase_count >= 0:
        testcase_name += f"{testcase_count}_"
    if input_filepath:
        testcase_name += f"{os.path.basename(input_filepath)}_"
    if not input_filepath and answer_filepath:
        testcase_name += f"{os.path.basename(answer_filepath)}"
    if testcase_name[-1] == "_":
        testcase_name = testcase_name[:-1]
    
    result.testcase_name = testcase_name
    result.input_filepath = input_filepath
    result.output_filepath = output_filepath
    result.answer_filepath = answer_filepath

    try:
        # Open input file
        if input_filepath:
            try:
                infile = open(input_filepath, "r")
                run_kwargs['stdin'] = infile
            except OSError as e:
                result.infile_error = e
        
        # Open output file
        if output_filepath:
            try:
                outfile = open(output_filepath, "w")
                run_kwargs['stdout'] = outfile
                run_kwargs['stderr'] = subprocess.STDOUT
            except OSError as e:
                result.outfile_error = e
        
        # If input source is stdin, prompt user to enter input in stdin
        if 'stdin' not in run_kwargs:
            print_seperator()
            print(f"Waiting input for {testcase_name}: ")

        # Run solution
        try:
            start = time.time()
            subprocess.run(
                run_args,
                check=True,
                encoding='utf-8',
                **run_kwargs
            )
            end = time.time()

            if 'stdin' not in run_kwargs:
                print_seperator()
                print()

            result.exec_time = end - start
        except subprocess.CalledProcessError as e:
            result.proc_error = e
            if 'stdin' not in run_kwargs:
                print(f"ERROR - runtime error at {testcase_name}")
        except subprocess.TimeoutExpired as e:
            result.timeout_exec = e
    finally:
        # Close files
        if infile and not infile.closed:
            infile.close()
        if outfile and not outfile.closed:
            outfile.close()
    
    # Check answer
    if answer_filepath:
        result.checked = True
        result.correct = check_answer(output_filepath, answer_filepath)
    
    return result


def run_solution_module(
    solution_function: Callable,
    input_filename: str = '',
    timeout: int = 0
)->SolutionResult:
    raise NotImplementedError


# ##### MAIN #####
def main():
    args = parse_args()
    solution_filename: str     = get_solution_filename(args.problem, args.solution_path, args.solution_type)
    input_filenames:  Set[str] = get_input_filenames(args.problem, args.input_path)
    answer_filenames: Set[str] = get_answer_filenames(args.problem, args.answer_path)

    num_testcases = len(input_filenames) 
    print(f"Found {num_testcases} test case{'s' if num_testcases > 1 else ''}.")

    results: List[SolutionResult] = []
    for i, input_filepath in enumerate(input_filenames):
        print(f"Running ({i + 1}/{num_testcases})...")

        # Look for answer file
        answer_filename = os.path.splitext(input_filepath)[0] + '.ans'
        if answer_filename in answer_filenames:
            answer_filenames.remove(answer_filename)
        else:
            # Answer file not found. Skip check
            answer_filename = ''

        result = run_solution(
            args=args,
            solution_filename=solution_filename,
            input_filepath=input_filepath,
            answer_filepath=answer_filename,
            testcase_count=i + 1,
            timeout=args.timeout
        )
        results.append(result)
    
    # Accept input from stdin and print output
    if args.stdin:
        testcase_count = len(input_filenames) + 1 if len(input_filenames) else -1
        result = run_solution(
            args=args,
            solution_filename=solution_filename,
            testcase_count=testcase_count
        )
        results.append(result)

        print()
        print_seperator()
        print(f"OUTPUT FOR {result.testcase_name}")
        print_file(result.output_filepath)
        print_seperator()
        print()
    
    
    print("\n[RESULTS]")
    passed = 0
    failed = 0
    total = len(results)
    for result in results:
        print(result)
        if result.success:
            passed += 1
        else:
            failed += 1
    
    print(f"\nTotal: {total} / Passed: {passed} / Failed: {failed}")

    if total and passed and total == passed:
        print(":)")
    
    
    

if __name__ == "__main__":
    main()