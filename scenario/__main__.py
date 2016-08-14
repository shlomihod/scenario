import sys

from scenario import run_scenario

def main(args=None):

    if args is None:
        args = sys.argv[1:]
    
    assert len(args) == 2, 'Usage: scenario <executable> <scenario>'

    executable_path = args[0]
    scenario_path = args[1]

    result, feedback = run_scenario(executable_path, scenario_path)

    print feedback

    if result:
    	sys.exit(0)
    else:
    	sys.exit(1)

if __name__ == '__main__':
    main()