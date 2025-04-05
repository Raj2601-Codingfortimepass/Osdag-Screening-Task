
import numpy as np
from scipy.optimize import minimize_scalar

def analyze_beam(L, t1, t2, x):
    def SF_01(a):
        if (a + x) <= L / 2:
            return -((t1 + t2) * a + t2 * x) / L
        elif a <= L / 2 <= (a + x):
            return t2 - ((t1 + t2) * a + t2 * x) / L
        else:
            return (t1 + t2) - ((t1 + t2) * a + t2 * x) / L

    def neg_abs_SF(a):
        return -abs(SF_01(a))

    RA_max = t1 + t2 - (t2 * x) / L
    RB_max = t1 + t2 - (t1 * x) / L
    SF_01 = SF_01(0)
    BM_01 = -t2 * x
    result = minimize_scalar(neg_abs_SF, bounds=(0, L - x), method='bounded')
    a_max = result.x
    SF_max = abs(SF_01(a_max))
    BM_max = -t1 * (L - x) - t2 * L

    print("Calculation Results:")
    print("Support Reactions:")
    print(f"  Maximum Reaction at A : {RA_max:.3f} kN")
    print(f"  Maximum Reaction at B : {RB_max:.3f} kN")
    print(f"\nShear Force at Mid-Span (SF_01 at 0.5L) when t1 is at A: {SF_01:.3f} kN")
    print(f"Bending Moment at A (BM_01) when t1 is at A: {BM_01:.3f} kNm")
    print(f"\nMaximum Shear Force (|SF_01|): {SF_max:.2f} kN at {a_max:.3f} m from support A.")
    print(f"Maximum Bending Moment at A (BM_max): {BM_max:.2f} kNm at {L - x:.3f} m from support A.")
    print("\n" + "_"*30)

# Example usage
if __name__ == "__main__":
print("Enter Beam and Load Parameters:\n")
l = float(input("Length of the beam L (in metres): "))
W1 = float(input("Value of moving load W1 (in kN): "))
W2 = float(input("Value of moving load W2 (in kN): "))
X = float(input("Distance x between W1 and W2 (in metres): "))
print("\n" + "_"*30)
analyze_beam(l, W1, W2, X)
