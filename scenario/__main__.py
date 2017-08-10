# -*- coding: utf-8 -*-

import sys
import os
import glob
import argparse
import traceback
import json

from scenario.runner import run_scenario
from scenario.parser import ParserError

from scenario.consts import VERBOSITY,\
    TIMEOUT_DEFAULT,              \
    OUTPUT_FORMATS, OUTPUT_FORMATS_DEFAULT

from scenario.utils import build_feedback_text


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

    parser.add_argument('-d', '--directory', help='run on all scenario files (.json) in the directory',
                        action="store_true")

    parser.add_argument('-s', '--forward-signal', help='forward signal from executable to scenario',
                        action="store_true")

    parser.add_argument('-t', type=float, default=TIMEOUT_DEFAULT,
                        help='set execution timeout in seconds')

    parser.add_argument('-f', '--format', dest='format', default=OUTPUT_FORMATS_DEFAULT,
                        action='store', choices=OUTPUT_FORMATS, help='output format to stdout')

    args = parser.parse_args()

    try:
        if not args.directory:
            feedback = run_scenario(args.executable_path,
                                    args.scenario_path,
                                    args.v,
                                    args.t,
                                    args.a)

            result = feedback['result']['bool']
            signal_ = feedback['signal_code']

            feedback_text = build_feedback_text(feedback)

        else:
            feedback = []
            feedback_texts = []

            scenario_file_directory_path = os.path.join(args.scenario_path, '*.snr')
            scenario_file_paths = glob.glob(scenario_file_directory_path)

            for scenario_file_path in scenario_file_paths:
                scenario_file_feedback = run_scenario(args.executable_path,
                                                      scenario_file_path,
                                                      args.v,
                                                      args.t,
                                                      args.a)

                feedback.append(scenario_file_feedback)
                feedback_texts.append(scenario_file_feedback['log']['text'] +
                                      '\n' + '====' + '\n' + str(feedback['result']['bool']))

            result = all([feedback['result']['bool'] for feedback in feedbacks])

            signals = [feedback['signal_code'] for feedback in feedbacks]
            signal_ = next((item for item in signals if item is not None), None)

            feedback_text = build_feedback_text(feedback)

    except ParserError as e:
        print(e.msg)
        sys.exit(2)

    except Exception as e:
        if args.v and args.v >= VERBOSITY['DEBUG']:
            traceback.print_exc()
        else:
            print('ERROR: {!s}'.format(e))
        sys.exit(-1)

    if args.format == 'json':
        print(json.dumps(feedback, indent=2, sort_keys=True))
    elif args.format == 'text':
        print(feedback_text)

    if args.forward_signal and signal_ is not None:
        os.kill(os.getpid(), signal_)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
