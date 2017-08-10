# Scenario

Testing console applications I/O

## Install
`pip install git+https://github.com/shlomihod/scenario.git`

## Usage
`usage: scenario [-h] [-v V] [-a A] [-d] [-s] [-t T] [-f {json,text}]
                executable_path scenario_path

Checking an IO scenario on execution.

positional arguments:
  executable_path       executable to be checked
  scenario_path         scenario file (or directory with -d flag)

optional arguments:
  -h, --help            show this help message and exit
  -v V                  set output verbosity
  -a A                  set extra arguments for executable
  -d, --directory       run on all scenario files (.snr) in the directory
  -s, --forward-signal  forward signal from executable to scenario
  -t T                  set execution timeout in seconds
  -f {json,text}, --format {json,text}
                        output format to stdout`

## Exit Code
| Value | Meaning                   |
|-------|---------------------------|
|  0    | Success Scenario          |
|  1    | Failed Scenario           |
|  2    | Error in Scenario JSON    |
| -1    | Error in Scenario Program |

## Known Issues (TODO update)
* Extra spaces in the beginning of a line with NONSTRICT mode won't be reported to user (yet the scenario will return success)
* Extra space in the end of a line with STRICT mode are ignored
* O Actor cann't be used for checking empty lines, even with STRICT mode
* Empty SNR file for only printing running doesn't work sometimes, only part of the printing is shown. Probably flush buffer issues.
