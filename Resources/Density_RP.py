##########################################################
# Reference Paper: https://www.sciencedirect.com/science/article/abs/pii/0198014980900163
# Reference Site: http://www.csgnetwork.com/water_density_calculator.html
##########################################################
import math


def perRound(num, precision=3):
    precision = 3
    precision = int(precision)  # make certain the decimal precision is an integer
    result1 = num * math.pow(10, precision)
    result2 = round(result1)
    result3 = result2 / math.pow(10, precision)
    return result3


p = float(input("Pressure in Bars: "))
t = float(input("Temperature in ∘C: "))
s = float(input("Salinity in PSU: "))

sr = math.sqrt(abs(s))
# density pure water at atm press in kg/m3 = (10**-3)gm/cm3
r1 = (
    (((6.536332e-9 * t - 1.120083e-6) * t + 1.001685e-4) * t - 9.095290e-3) * t
    + 6.793952e-2
) * t - 0.157406
# seawater density atm press.
r2 = (((5.3875e-9 * t - 8.2467e-7) * t + 7.6438e-5) * t - 4.0899e-3) * t + 0.824493
r3 = (-1.6546e-6 * t + 1.0227e-4) * t - 5.72466e-3
r4 = 4.8314e-4
sig = (r4 * s + r3 * sr + r2) * s + r1
# compute compression terms
e = (9.1697e-10 * t + 2.0816e-8) * t - 9.9348e-7
bw = (5.2787e-8 * t - 6.12293e-6) * t + 8.50935e-5
b = bw + e * s
c = (-1.6078e-6 * t - 1.0981e-5) * t + 2.2838e-3
aw = ((-5.77905e-7 * t + 1.16092e-4) * t + 1.43713e-3) * t + 3.239908
a = (1.91075e-4 * sr + c) * s + aw
b1 = (-5.3009e-4 * t + 1.6483e-2) * t + 7.944e-2
a1 = ((-6.1670e-5 * t + 1.09987e-2) * t - 0.603459) * t + 54.6746
kw = (((-5.155288e-5 * t + 1.360477e-2) * t - 2.327105) * t + 148.4206) * t + 19652.21
k0 = (b1 * sr + a1) * s + kw
# evaluate pressure polynomial and return
k = (b * p + a) * p + k0
sig = (k * sig + 1000 * p) / (k - p)
# sig remains unchanged since is (10**-3)gm/cm**3
value = perRound(sig + 1000, precision=5)

print(f"Density of the water is: {value} kg/m³")
