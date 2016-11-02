import sys
import argparse
import traceback

from scenario import run_scenario

from _consts import VERBOSITY, VERBOSITY_DEFAULT, TIMEOUT_DEFAULT

def main():

    parser = argparse.ArgumentParser(description='Checking an IO scenario on execution.')
    parser.add_argument('executable_path', type=str,
                        help='executable to be checked')

    parser.add_argument('scenario_path', type=str,
                        help='scenario file with an IO dialog')

    parser.add_argument('-v', type=int, 
                        help='set output verbosity')

    parser.add_argument('-t', type=int, default=TIMEOUT_DEFAULT, 
                        help='set execution timeout in seconds')

    args = parser.parse_args()

    try:
        result, feedback = run_scenario(args.executable_path,
                                        args.scenario_path,
                                        args.v,
                                        args.t)
    
    except Exception, e:
        if args.v >= VERBOSITY['DEBUG']:
            traceback.print_exc()
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
