#Example of how to run a unit test
from os import name
from EC0.UnitTests.UT_Eq6_1 import TestEq6_1
from EC0.UnitTests.UT_Eq8_10 import TestEq8_10
import unittest

suite1 = unittest.TestLoader().loadTestsFromTestCase(TestEq6_1)
suite2 = unittest.TestLoader().loadTestsFromTestCase(TestEq8_10)

all_tests = unittest.TestSuite([suite1, suite2])

print("Running Unit Tests:")
runner = unittest.TextTestRunner(verbosity=2)
runner.run(all_tests)

#Disable logging for the main script
import logging
for handler in logging.root.handlers[:]:
  logging.root.removeHandler(handler)

logging.disable(logging.CRITICAL)

print(
    "_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________\n\n"
)

#Example of how to use the equations
print("Equations Ouputs:")
from Settings import DesignValue, DesignFactor
import EC0

Q_k_wind = DesignValue("Q_{k}", 532, "kN", name="wind")
Q_k_live = DesignValue("Q_{k}", 132, "kN", name="live")
Q_k_heat = DesignValue("Q_{k}", 32, "kN", name="heat")

psi_0 = DesignFactor("psi_{0}", 0.7)
psi_1 = DesignFactor("psi_{1}", 0.6)
psi_2 = DesignFactor("psi_{2}", 0.9)
gamma_Q = DesignFactor("gamma_{Q}", 1.50)

Q_comb_wind = EC0.Eq6_1(psi_0, Q_k_wind)
Q_d_wind = EC0.Eq8_10(gamma_Q, Q_comb_wind)

Q_comb_live = EC0.Eq6_2(psi_1, Q_k_live)
Q_d_live = EC0.Eq8_10(gamma_Q, Q_comb_live)

Q_comb_heat = EC0.Eq6_3(psi_2, Q_k_heat)
Q_d_heat = EC0.Eq8_10(gamma_Q, Q_comb_heat)

print("\nLoading Calculations:")
print(Q_comb_wind)
print("Process is repeated for other loads")
print(f"  {psi_0:value}\n")
print(f"  {Q_k_live:value}")
print(f"  {Q_comb_live:value}\n")
print(f"  {Q_k_heat:value}")
print(f"  {Q_comb_heat:value}\n")

print(Q_d_wind)
print("Process is repeated for other loads")
print(f"  {gamma_Q:value}\n")
print(f"  {Q_comb_live:value}")
print(f"  {Q_d_live:value}\n")
print(f"  {Q_comb_heat:value}")
print(f"  {Q_d_heat:value}\n")


Ed = DesignValue("E_{d}", 3532, "kN")
Rd = DesignValue("R_{d}", 5.241, "MN")
Utilisation_1 = EC0.Eq8_1(Ed, Rd)

Ed = DesignValue("E_{d}", 0.242, "m")
Cd_ULS = DesignValue("C_{d,ULS}", 24, "cm")
Utilisation_2 = EC0.Eq8_2(Ed, Cd_ULS)

print(f"\nOUT:")
print(f"{Utilisation_1}")
print(f"{Utilisation_2:short}")


total = max(Utilisation_1.number, Utilisation_2.number) * 100
print(f"Overall Utilisation: {total:.2f} [%]")
print("")