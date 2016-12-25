import sys
import os
import glob
import argparse
import traceback

from scenario import run_scenario

from _consts import VERBOSITY, VERBOSITY_DEFAULT, TIMEOUT_DEFAULT

def main():

    parser = argparse.ArgumentParser(description='Checking an IO scenario on execution.')
    parser.add_argument('executable_path', type=str,
                        help='executable to be checked')

    parser.add_argument('scenario_path', type=str,
                        help='scenario file (or directory with -d flag)')

    parser.add_argument('-v', type=int, default=VERBOSITY_DEFAULT,
                        help='set output verbosity')

    parser.add_argument('-a', type=str,
                        help='set extra arguments for executable')

    parser.add_argument('-d', '--directory', help='run on all scenario files (.snr) in the directory',
                        action="store_true")
    
    parser.add_argument('-t', type=int, default=TIMEOUT_DEFAULT, 
                        help='set execution timeout in seconds')

    args = parser.parse_args()

    try:
        if not args.directory:
            result, feedback = run_scenario(args.executable_path,
                                            args.scenario_path,
                                            args.v,
                                            args.t,
                                            args.a)
        else:
            results = []
            feedbacks = []
            
            scenario_file_directory_path = os.path.join(args.scenario_path, '*.snr')
            scenario_file_paths = glob.glob(scenario_file_directory_path)

            for scenario_file_path in scenario_file_paths:
                scenario_file_result, scenario_file_feedback = run_scenario(args.executable_path,
                                                scenario_file_path,
                                                args.v,
                                                args.t,
                                                args.a)
                
                results.append(scenario_file_result)
                feedbacks.append(scenario_file_feedback)

            result = all(results)
            feedback = '\n'.join(feedbacks)

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
