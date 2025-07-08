import unittest
from math import isclose
from Settings import DesignValue, DesignFactor
from EC0 import Eq8_10


class TestEq8_10(unittest.TestCase):

    def check_design_value(self, Q, Qunits, gamma, expected_result,
                           expected_units):
        Q_comb = DesignValue("Q_{comb}", Q, Qunits)
        gamma_Q = DesignFactor("gamma_{Q}", gamma)
        Q_d = Eq8_10(gamma_Q, Q_comb)

        self.assertEqual(Q_d.abbreviation, "Q_{d}", "Incorrect abbreviation")
        self.assertTrue(
            isclose(Q_d.number, expected_result, abs_tol=1e-8),
            f"Incorrect number: got {Q_d.number}, expected {expected_result}")
        self.assertEqual(Q_d.units, expected_units, "Incorrect units")

    def test_examples(self):
        test_cases = [(100, "kN", 1.5, 150.0, "kN"),
                      (200, "MN", 1.35, 270.0, "MN"),
                      (50, "N", 1.2, 60.0, "N"),
                      (75.5, "kNm", 1.1, 83.05, "kNm"),
                      (32.1, "Nmm", 1.0, 32.1, "Nmm"),
                      (65342.12, "cN", 1.25, 81677.65, "cN")]
        for Q, Qunits, gamma, result, resultUnits in test_cases:
            with self.subTest(Q=Q, Qunits=Qunits, gamma=gamma):
                self.check_design_value(Q, Qunits, gamma, result, resultUnits)


if __name__ == "__main__":
    unittest.main()
