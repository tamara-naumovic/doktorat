import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy.integrate import solve_ivp

# def integrator(p2,p3,u1,u2,u3):
#     # print("usao u integrator")
#     izlaz = u1+p2*u2+p3*u3
#     nizizlaza = np.array([izlaz])
#     return nizizlaza




# def rungeKutta4(f, x0, inicVreme, duzina, intervalItegracije):
#     vremenskaOsa = np.arange(inicVreme, duzina, intervalItegracije)
#     xosa = vremenskaOsa.size

#     yosa = x0.size
#     x = np.zeros((yosa,xosa))

#     x[:,0] = x0

#     for k in range(brElemVreme-1):
#         k1 = intervalItegracije*integrator



#     pass

def dxdt(t,v):
    return 10


def integrator(t,x,p2,p3,u1,u2,u3):
    izlaz = u1+p2*u2+p3*u3
    return izlaz

def main():
    v0 = 0
    t = 0.1

    sol_m2 = solve_ivp(integrator, t_span=(0,0.2), y0=[v0], method="RK45", args=(0,0,10,0,0))
    print(sol_m2.y)

if __name__=="__main__":
    main()