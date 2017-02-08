# Scenario

Testing console applications I/O

## Install
`pip install git+https://github.com/shlomihod/scenario.git`

## Usage
`scenario <executable> <snr>`

## Known Issues
* Extra spaces in the beginning of a line with NONSTRICT mode won't be reported to user (yet the scenario will return success)
* O Actor cann't be used for checking empty lines, even with STRICT mode