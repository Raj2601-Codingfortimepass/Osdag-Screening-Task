#Importing the libraries and functions required to enter the shear force as a piece wise function and calculate its absolute maximum value.
import numpy as np
from scipy.optimize import minimize_scalar

#It is the primary function which would calculate the required quantities and display them on the screen.
def analyze_beam(L, t1, t2, x):
#The shear force as a piece wise function.
    def sf_01(a):
        if (a + x) <= L / 2:
            return -((t1 + t2) * a + t2 * x) / L
        elif a <= L / 2 <= (a + x):
            return t2 - ((t1 + t2) * a + t2 * x) / L
        else:
            return (t1 + t2) - ((t1 + t2) * a + t2 * x) / L
#Accounting  for the negative values as absolute values.
    def neg_abs_sf(a):
        return -abs(sf_01(a))
#Calculating the Maximum Reactions at Supports A and B.
    RA_max = t1 + t2 - (t2 * x) / L
    RB_max = t1 + t2 - (t1 * x) / L
#Calculating the Shear Force SF_01 at 0.5L when the leftmost weight is directly above A.
    SF_01 = sf_01(0) 
#Calculating the Bending Moment BM_01 at A when the leftmost weight is directly above A.
    BM_01 = -t2 * x
"""
Using the piece wise function for shear force generated and the functions imported, 
finding out the maximum value of shear force as well as the corresponding location of W1 from A.
"""
    result = minimize_scalar(neg_abs_sf, bounds=(0, L - x), method='bounded')
    a_max = result.x
    SF_max = abs(sf_01(a_max))
#The maximum bending moment at support A occurs when a is maximum, i.e. (L-x).
    BM_max = -t1 * (L - x) - t2 * L
#Printing the outputs on screen after all calculations.
    print("After analyzing the beam, here are the results:")
    print(f"Maximum Reaction at A : {RA_max:.3f} kN")
    print(f"Maximum Reaction at B : {RB_max:.3f} kN")
    print(f"Shear Force at (0.5)L (SF_01) when the leftmost weight is at A: {SF_01:.3f} kN")  
    print(f"Bending Moment at A (BM_01) when the leftmost weight is at A: {BM_01:.3f} kNm")
    print(f"Maximum Shear Force at (0.5)L (SF_max): {SF_max:.3f} kN when the leftmost weight is at {a_max:.3f} m from support A.")
    print(f"Maximum Bending Moment at A (BM_max): {BM_max:.3f} kNm when the leftmost weight is at {L - x:.3f} m from support A.")
    print("\n" + "_"*30)
#Main function
if __name__ == "__main__":
#Taking inputs from the user.
    print("Enter Beam and Load Parameters:\n")
    l = float(input("Length of the beam L (in metres): "))
    W1 = float(input("Value of moving load W1 (in kN): "))
    W2 = float(input("Value of moving load W2 (in kN): "))
    X = float(input("Distance x between W1 and W2 (in metres): "))
#Ensuring that both the loads are within the span of the beam.
    while X < -l or X > l:
     X = float(input(f"Distance x between W1 and W2 (in metres, between {-l} and {l}): "))
     if X < -l or X > l:
        print(f"Please enter a value between {-l} and {l}.")
    print("\n")
    print("_"*30)
    print("\n")
"""
Negative value of x suggests that the load shown as W1 is actually present after W2 when seen from support A. 
Thus for the analysis we can simply switch W1 with W2 and take the absolute value of x entered.
"""
if (X>=0):
     analyze_beam(l, W1, W2, X)
else:
     analyze_beam(l, W2, W1, -X)
