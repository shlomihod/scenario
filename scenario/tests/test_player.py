import unittest
import pprint

import jsonschema

from scenario.player import play_scenario
from scenario.tests.consts import EXECUTABLE, DIALOUGE_PIECES
from scenario.consts import SCENARIO_JSON_SCHEMA


class PlayerTest(unittest.TestCase):

    def _generate_scenario(self, name, args, dialogue, strictness=False):
        scenario = {
            'id': name,
            'name': name,
            'description': name,
            'flow': True,
            'strictness': strictness,
            'timeout': 1,
            'verbosity': 4,
            'args': args,
            'dialogue': dialogue
        }

        return scenario

    def _run_test(self, result_bool, feedback_type, args, dialogue, **kwargs):
        name = '='.join([str(result_bool),
                         str(feedback_type),
                         '+'.join(args)])

        scenario = self._generate_scenario(name, args, dialogue, **kwargs)

        jsonschema.validate(scenario, SCENARIO_JSON_SCHEMA)

        feedback = play_scenario(scenario, EXECUTABLE)

        pprint.pprint(feedback['log'])
        self.assertEqual(feedback['result']['bool'], result_bool)
        self.assertEqual(feedback['feedback']['type'], feedback_type)


class ResultTrueTests(PlayerTest):

    def test_all_print(self):
        '''
        Working: Empty Scenario
        Empty `dialogue` with only print executable
        '''

        dialogue = []

        args = ['print']

        self._run_test(True, None, args, dialogue)

    def test_all_output(self):
        '''
        Working: All Output
        `dialogue` contains all output of executable
        '''

        dialogue = DIALOUGE_PIECES['output_all']

        args = ['print']

        self._run_test(True, None, args, dialogue)

    def test_one_output(self):
        '''
        Working: One Output
        `dialogue` contains upper case one output of executable
        '''

        dialogue = [DIALOUGE_PIECES['output4']]

        args = ['print']

        self._run_test(True, None, args, dialogue)

    def test_one_output_input_output(self):
        '''
        Working: One Output -> Input -> Output (flow=True)
        `dialogue` contains one output line of executable
        and then input and output
        '''

        dialogue = [DIALOUGE_PIECES['output4'],
                    DIALOUGE_PIECES['input_comment'],
                    DIALOUGE_PIECES['output_comment']]

        args = ['print', 'input', 'output']

        self._run_test(True, None, args, dialogue)

    def test_input_one_output_output(self):
        '''
        Working: Input -> One Output -> Output (flow=True)
        `dialogue` contains one output line of executable
        but before input and after output
        '''

        dialogue = [DIALOUGE_PIECES['input_comment'],
                    DIALOUGE_PIECES['output4'],
                    DIALOUGE_PIECES['output_comment']]

        args = ['input', 'print', 'output']

        self._run_test(True, None, args, dialogue)


class StrictnnessTests(PlayerTest):
    def test_one_output_upper_strictness_false(self):
        '''
        Working: One Output Upper (strictness=False)
        `dialogue` contains upper case one output of executable
        '''

        dialogue = [DIALOUGE_PIECES['output4_upper']]

        args = ['print']

        self._run_test(True, None, args, dialogue)

    def test_one_output_upper_strictness_true(self):
        '''
        Working: One Output Upper (strictness=True)
        `dialogue` contains upper case one output of executable
        '''

        dialogue = [DIALOUGE_PIECES['output4_upper']]

        args = ['print']

        self._run_test(False, 'ShouldOutputBeforeEOF', args, dialogue,
                       strictness=True)


class ResultFalseTests(PlayerTest):
    def test_ShouldOutput(self):
        '''
        Feedback Error: Output Incorrect
        '''

        dialogue = [DIALOUGE_PIECES['output_poet']]

        args = ['print', 'input']

        self._run_test(False, 'ShouldOutput', args, dialogue)

    def test_ShouldEOF(self):
        '''
        Feedback Error: Should EOF
        '''

        dialogue = [DIALOUGE_PIECES['output4']]

        args = ['print', 'input']

        self._run_test(False, 'ShouldEOF', args, dialogue)

    def test_ShouldOutputBeforeEOF(self):
        '''
        Feedback Error: Shpuld Output Before EOF
        '''

        dialogue = [DIALOUGE_PIECES['output4'],
                    DIALOUGE_PIECES['output_poet']]

        args = ['print']

        self._run_test(False, 'ShouldOutputBeforeEOF', args, dialogue)

    def test_SholdNoOutputBeforeInput(self):
        '''
        Feedback Error: Should No Output Before Input (flow=False)
        '''

        raise unittest.SkipTest

    def test_ShouldInputBeforeEOF(self):
        '''
        Feedback Error: Should Input Before EOF
        '''

        dialogue = [DIALOUGE_PIECES['output4'],
                    DIALOUGE_PIECES['input_comment']]

        args = ['print']

        self._run_test(False, 'ShouldInputBeforeEOF', args, dialogue)

    def test_MemoryFeedbackError(self):
        pass


class MemoryTests(PlayerTest):
    def test_MemoryFeedback(self):
        '''
        Feedback Error: MemoryFeedback
        '''

        dialogue = [DIALOUGE_PIECES['output_poet'],
                    DIALOUGE_PIECES['input_comment']]

        args = ['print', 'crash', 'input']

        self._run_test(False, 'MemoryFeedbackError', args, dialogue)
