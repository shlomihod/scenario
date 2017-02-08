from unittest import TestCase
import pexpect
from scenario import play_scenario

from utils import ANNABEL_LEE, EXECUTABLE

TEST_VERBOSITY = 4

class TestPlayer(TestCase):
    def __generate_scenario_test(self, test_name, strictness=True):
        scenario = {}
        scenario['name'] = test_name
        scenario['pre_dialog'] = []
        scenario['verobisty'] = TEST_VERBOSITY
        scenario['strictness'] = True
        scenario['flow'] = False

        scenario['args'] = test_name.replace('_strict', '') \
                                    .replace('_nonstrict', '')

        if test_name == 'print':
            scenario['dialog'] = [('O', quote) \
                                  for quote in ANNABEL_LEE.splitlines()]
            exp_result = True

        elif test_name == 'print_input':
            scenario['dialog'] = [('O', quote) \
                                  for quote in ANNABEL_LEE.splitlines()]   \
                                  + [('I', 'some text')]
            exp_result = True

        elif test_name == 'print_print-input':
            scenario['dialog'] = [('O', quote) \
                                  for quote in ANNABEL_LEE.splitlines()]   \
                                  + [('I', 'some text')]                   \
                                  + [('O', 'some text')]
            exp_result = True

        elif test_name == 'print-input':
            scenario['dialog'] =  [('I', 'some text')]                    \
                                  + [('O', 'some text')]
            exp_result = True

        elif test_name.startswith('print-cases-spaces_print-input')          or \
             test_name.startswith('extra-spaces-beginning-line-print_input') or \
             test_name.startswith('extra-spaces-end-line-print_input')       or \
             test_name.startswith('extra-spaces-end-print_input'):

            if 'nonstrict' in test_name:
                scenario['strictness'] = False
                exp_result = True

            elif 'strict' in test_name:
                scenario['strictness'] = True
                if 'end' in test_name:
                    exp_result = True
                else:
                    exp_result = False


            scenario['dialog'] = [('O', quote) \
                                  for quote in ANNABEL_LEE.splitlines()]   \
                                  + [('I', 'some text')]                   \
                                  + [('O', 'some text')]      

        elif test_name.startswith('snr-exta-spaces-end-line_print-input'):
            scenario['args'] = 'print_print-input'

            if 'nonstrict' in test_name:
                scenario['strictness'] = False
                exp_result = True

            elif 'strict' in test_name:
                scenario['strictness'] = True
                exp_result = False

            scenario['dialog'] = [['O', quote] \
                                  for quote in ANNABEL_LEE.splitlines()]   \
                                  + [('I', 'some text')]                   \
                                  + [('O', 'some text')] 
            scenario['dialog'][3][1] = scenario['dialog'][3][1] + ' '
            scenario['dialog'][5][1] = scenario['dialog'][5][1] + '  '
            scenario['dialog'][7][1] = '    '.join(scenario['dialog'][7][1].split())
        return scenario, exp_result, ''

    def __tester(self, test_name):
        scenario, exp_result, exp_feedback = self.__generate_scenario_test(test_name)
        result, feedback = play_scenario(scenario, EXECUTABLE, verbosity=4)
        print feedback

        self.assertTrue(exp_result == result)
        #self.assertTrue(exp_feedback == feedback)

    def test_print(self):
        self.__tester('print')
    
    def test_print_input(self):
        self.__tester('print_input')

    def test_print__print_input(self):
        self.__tester('print_print-input')

    def test_print__input(self):
        self.__tester('print-input')

    def test_print_caeses_spaces__print_input__strict(self):
        self.__tester('print-cases-spaces_print-input_strict')

    def test_print_caeses_spaces__print_input__nonstrict(self):
        self.__tester('print-cases-spaces_print-input_nonstrict')

    def test_extra_spaces_beginning_line_print__input__strict(self):
        self.__tester('extra-spaces-beginning-line-print_input_strict')

    def test_extra_spaces_beginning_line_print__input__nonstrict(self):
        self.__tester('extra-spaces-beginning-line-print_input_nonstrict')

    def test_extra_spaces_end_line_print__input__strict(self):
        self.__tester('extra-spaces-end-line-print_input_strict')

    def test_extra_spaces_end_line_print__input__nonstrict(self):
        self.__tester('extra-spaces-end-line-print_input_nonstrict')

    def test_extra_spaces_end_print__input__strict(self):
        self.__tester('extra-spaces-end-print_input_strict')

    def test_extra_spaces_end_print__input__nonstrict(self):
        self.__tester('extra-spaces-end-print_input_nonstrict')

    def test_snr_exta_spaces_end_line__input__strict(self):
        self.__tester('snr-exta-spaces-end-line_print-input_strict')

    def test_snr_exta_spaces_end_line__input__nonstrict(self):
        self.__tester('snr-exta-spaces-end-line_print-input_nonstrict')

