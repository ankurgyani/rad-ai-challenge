#! /usr/bin/python
import unittest
import io
import sys
from solution import LeaderBoard

class TestLeaderBoard(unittest.TestCase):
    

    def test_print_rankings(self):
        """Test that our ranking output lines are generated and formatted correctly"""
        test_input =[
                    "France 3, Germany 3",
                    "United States 2, Argentina 1",
                    "Argentina 1, Brazil 2",
                    "Brazil 0, Germany 0",
                    "Brazil 1, Portugal 0"
                    ]
        expected_output = "1. Brazil, 7 pts\n2. United States, 3 pts\n3. Germany, 2 pts\n4. France, 1 pts\n5. Argentina, 0 pts\n5. Portugal, 0 pts\n"
        t = LeaderBoard()
        for line in test_input:
            t._record_result(line)
        captured_output = io.StringIO()
        sys.stdout = captured_output
        t.print_rankings()
        sys.stdout = sys.__stdout__
        self.assertMultiLineEqual(expected_output, captured_output.getvalue())


if __name__ == '__main__':
    unittest.main()