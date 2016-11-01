import sys
import argparse

from scenario import run_scenario

from _consts import VERBOSITY

def main():

    parser = argparse.ArgumentParser(description='Checking an IO scenario on execution.')
    parser.add_argument('executable_path', type=str,
                        help='executable to be checked')

    parser.add_argument('scenario_path', type=str,
                        help='scenario file with an IO dialog')

    parser.add_argument('-v', type=int, default=1, 
                        help='set output verbosity')

    args = parser.parse_args()

    #try:
    result, feedback = run_scenario(args.executable_path,
                                        args.scenario_path,
                                        args.v)
    
  #  except Exception, e:
   #     if args.v >= 4:
    #        raise e
    #    else:
     #       print 'ERROR: {!s}'.format(e)
      #      sys.exit(2)

    print feedback
    
    if result:
    	sys.exit(0)
    else:
    	sys.exit(1)
    
if __name__ == '__main__':
    main()
