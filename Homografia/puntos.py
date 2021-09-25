import numpy as np

def distancia(p1, p2):
    return (p2[0] - p1[0])*(p2[0] - p1[0]) + (p2[1] - p1[1])*(p2[1] - p1[1])

def det_norm(p1,p2,p3):
    return (p1[0]-p3[0])*(p2[1]-p3[1])-(p2[0]-p3[0])*(p1[1]-p3[1])

def ordenaPuntos(p):
    pn = p.copy()
    org = np.array([0.0,0.0])
    for i in range(4):
        if (distancia(org, pn[0]) > distancia(org, pn[i]) ):
            pn[[0,i], :] = pn[[i,0], :]
    if (det_norm(pn[0], pn[1], pn[2] ) < 0.0):
        pn[[1,2], :] = pn[[2,1], :]
    if (det_norm(pn[0], pn[2], pn[3] ) < 0.0):
        pn[[2,3], :] = pn[[3,2], :]
    if (det_norm(pn[0], pn[1], pn[2] ) < 0.0):
        pn[[1,2], :] = pn[[2,1], :]
    return pn
