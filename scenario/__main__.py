import sys

from scenario import run_scenario

def main(args=None):

    if args is None:
        args = sys.argv[1:]
    
    assert len(args) == 2, 'Usage: python -m foo <executable> <scenario>'

    executable_path = args[0]
    scenario_path = args[1]

    run_scenario(executable_path, scenario_path)

if __name__ == '__main__':
    main()

