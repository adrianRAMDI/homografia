import numpy as np
import math

def normalizar(p):
    S = np.zeros((len(p), 2))
    proms = np.average(p, axis=0)
    sigma = np.std(p, axis=0)
    for i in range(len(p)):
        #normalizar x
        S[i][0] = (p[i][0]-proms[0])/sigma[0]
        #normalizar y
        S[i][1] = (p[i][1]-proms[1])/sigma[1]
    return S, proms, sigma



def homografia(p1, p2):
    pn1, med1, sig1 = normalizar(p1)
    pn2, med2, sig2 = normalizar(p2)
    n = len(p1)
    A = np.zeros((2*n,8))
    b = np.zeros(2*n)
    #se construye la matriz A
    for i in range (len(p1)):
        k = 2*i
        A[k,0] = pn1[i][0]
        A[k,1] = pn1[i][1]
        A[k,2] = 1.0
        A[k,6] = -pn1[i][0] * pn2[i][0]
        A[k,7] = -pn1[i][1] * pn2[i][0]
        b[k] = pn2[i][0]
        k = k +1
        A[k,3] = pn1[i][0]
        A[k,4] = pn1[i][1]
        A[k,5] = 1.0
        A[k,6] = -pn1[i][0] * pn2[i][1]
        A[k,7] = -pn1[i][1] * pn2[i][1]
        b[k] = pn2[i][1]
    hp = np.linalg.inv(A) @ b.transpose()
    Hp = np.array([[hp[0],hp[1],hp[2]],[hp[3],hp[4],hp[5]],[hp[6],hp[7],1.]])
    #se calcula la matríz homografia
    T1 = np.zeros((3,3))
    T1[0][0] = 1/sig1[0]
    T1[0][2] = -med1[0]/sig1[0]
    T1[1][1] = 1./sig1[1]
    T1[1][2] = -med1[1]/sig1[1]
    T1[2][2] = 1.
    T2i = np.zeros((3,3))
    T2i[0][0] = sig2[0]
    T2i[0][2] = med2[0]
    T2i[1][1] = sig2[1]
    T2i[1][2] = med2[1]
    T2i[2][2] = 1.
    H = T2i @ Hp @ T1
    return H

def parametros (H, height, width):
    u0 = -width/2.0
    v0 = -height/2.0
    w33 = -H[0][1]*( H[0][0] + H[2][0]*u0 )
    w33 = w33-H[1][1]*(H[1][0]+ H[2][0]*v0)
    w33 = w33-H[2][1]*H[0][0]*u0
    w33 = w33-H[2][1]*H[1][0]*v0
    w33 = w33/(H[2][1]*H[2][0]);

    f2 = w33 - u0*u0 - v0*v0;
    f = 0;
    if(f2 <  0):
        print("Error en el cálculo")
    else:
        f = np.sqrt( f2 )
    Kinv = np.array([[1./f,0.,u0/f],[0., 1./f, v0/f],[0., 0., -1.]])

    A = Kinv @ H
    l1 = np.linalg.norm(A[:,0])
    l2 = np.linalg.norm(A[:,1])
    l = (l1+l2)/2.0;

    A2 = (1.0/l) * A
    vt = np.array([A2[0][2],A2[1][2],A2[2][2]])
    Rp = np.copy(A2)
    cross = np.cross(Rp[:,0],Rp[:,1])
    for i in range( len(cross) ):
        Rp[i][2] = cross[i]

    U, vd, VT = np.linalg.svd(Rp)
    R = U @ VT
    vc = (-R.transpose())@ vt

    MK  = np.zeros(16)
    MRT = np.zeros(16)

    MK[0]  = f
    MK[5]  = f
    MK[8]  = u0
    MK[9]  = v0
    MK[10] = 51.0
    MK[11] = -1
    MK[14] = 20.0

    MRT[0 ] = R[0][0]
    MRT[1 ] = R[1][0]
    MRT[2 ] = R[2][0]
    MRT[3 ] = 0.0

    MRT[4 ] = R[0][1]
    MRT[5 ] = R[1][1]
    MRT[6 ] = R[2][1]
    MRT[7 ] = 0.0

    MRT[8 ] = R[0][2]
    MRT[9 ] = R[1][2]
    MRT[10] = R[2][2]
    MRT[11] = 0.0

    MRT[12] = vt[0]
    MRT[13] = vt[1]
    MRT[14] = vt[2]
    MRT[15] = 1.0

    return MK, MRT, vc
