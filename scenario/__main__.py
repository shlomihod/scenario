import sys
import argparse

from scenario import run_scenario

verbose = False

def main(args=None):

    if args is None:
        args = sys.argv[1:]
    
    assert len(args) == 2, 'Usage: scenario <executable> <scenario>'

    executable_path = args[0]
    scenario_path = args[1]

    try:
        result, feedback = run_scenario(executable_path, scenario_path, verbose)
    
    except Exception, e:
        if verbose:
            raise e
        else:
            print 'ERROR: {!s}'.format(e)
            sys.exit(2)

    print feedback

    if result:
    	sys.exit(0)
    else:
    	sys.exit(1)

if __name__ == '__main__':
    main()