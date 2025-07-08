import unittest
from math import isclose
from Settings import DesignValue, DesignFactor
from EC0 import Eq6_1


class TestEq6_1(unittest.TestCase):

    def check_combination(self, Q, Qunits, psi, expected_result,
                          expected_units):
        Q_k = DesignValue("Q_{k}", Q, Qunits)
        psi_0 = DesignFactor("psi_{0}", psi)
        Q_comb = Eq6_1(psi_0, Q_k)

        self.assertEqual(Q_comb.abbreviation, "Q_{comb}",
                         "Incorrect abbreviation")
        self.assertTrue(
            isclose(Q_comb.number, expected_result, abs_tol=1e-8),
            f"Incorrect number: got {Q_comb.number}, expected {expected_result}"
        )
        self.assertEqual(Q_comb.units, expected_units, "Incorrect units")

    def test_examples(self):
        test_cases = [(120231, "MN", 0.75, 90173.25, "MN"),
                      (5343, "kN", 0.7, 3740.1, "kN"),
                      (6745, "N", 0.8, 5396.0, "N"),
                      (9876, "kN/m2", 0.9, 8888.4, "kN/m2"),
                      (567, "kNm", 1.1, 623.7, "kNm"),
                      (32.1, "Nmm", 1.2, 38.52, "Nmm"),
                      (65342.12, "cN", 1.45, 94746.074, "cN")]
        for Q, Qunits, psi, result, resultUnits in test_cases:
            with self.subTest(Q=Q, Qunits=Qunits, psi=psi):
                self.check_combination(Q, Qunits, psi, result, resultUnits)


if __name__ == "__main__":
    unittest.main()
