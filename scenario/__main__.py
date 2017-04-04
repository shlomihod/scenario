import sys
import os
import glob
import argparse
import traceback
import collections

from scenario.runner import run_scenario

from scenario.consts import VERBOSITY, VERBOSITY_DEFAULT, TIMEOUT_DEFAULT

def main():

    parser = argparse.ArgumentParser(description='Checking an IO scenario on execution.')
    parser.add_argument('executable_path', type=str,
                        help='executable to be checked')

    parser.add_argument('scenario_path', type=str,
                        help='scenario file (or directory with -d flag)')

    parser.add_argument('-v', type=int,
                        help='set output verbosity')

    parser.add_argument('-a', type=str,
                        help='set extra arguments for executable')

    parser.add_argument('-d', '--directory', help='run on all scenario files (.snr) in the directory',
                        action="store_true")
    
    parser.add_argument('-s', '--forward-signal', help='forward signal from executable to scenario',
                        action="store_true")

    parser.add_argument('-t', type=float, default=TIMEOUT_DEFAULT, 
                        help='set execution timeout in seconds')

    args = parser.parse_args()
    
    try:
        if not args.directory:
            feedback, feedback_text = run_scenario(args.executable_path,
                                            args.scenario_path,
                                            args.v,
                                            args.t,
                                            args.a)

            result = feedback['result']
            signal_ = feedback['signal_code']

        else:
            feedbacks = []
            feedback_texts = []
            
            scenario_file_directory_path = os.path.join(args.scenario_path, '*.snr')
            scenario_file_paths = glob.glob(scenario_file_directory_path)

            for scenario_file_path in scenario_file_paths:
                scenario_file_feedback, scenario_file_feedback_text = run_scenario(args.executable_path,
                                                scenario_file_path,
                                                args.v,
                                                args.t,
                                                args.a)
                
                feedbacks.append(scenario_file_feedback)
                feedback_texts.append(scenario_file_feedback_text)

            result = all([feedback['result'] for feedback in feedbacks])

            signals = [feedback['signal_code'] for feedback in feedbacks]
            signal_ = next((item for item in signals if item is not None), None)

            feedback_text = '\n\n'.join(feedback_texts)

    except Exception as e:
        if args.v and args.v >= VERBOSITY['DEBUG']:
            traceback.print_exc()
        else:
            print('ERROR: {!s}'.format(e))
        sys.exit(2)

    print(feedback_text)

    if args.forward_signal and signal_ is not None:
        os.kill(os.getpid(), signal_)

    if result:
    	sys.exit(0)
    else:
    	sys.exit(1)
    
if __name__ == '__main__':
    main()

