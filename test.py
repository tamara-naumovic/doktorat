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


def integrator(t,v,p2,p3,u1,u2,u3):
    izlaz = u1+p2*u2+p3*u3
    return izlaz

def main():
    v0 = 0
    t = np.linspace(0,10,num=100)
    print(t)

    sol_m2 = solve_ivp(integrator, t_span=(0,max(t)), y0=[v0], t_eval=t, method="RK45", args=(0,0,10,0,0))
    
    v_sol_m2 = sol_m2.y[0]

    plt.plot(t, v_sol_m2)
    plt.ylabel('$v(t)$', fontsize=22)
    plt.xlabel('$t$', fontsize=22)
    plt.show()

if __name__=="__main__":
    main()