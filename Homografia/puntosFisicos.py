import numpy as np

numModelos = 3

puntosFot = np.zeros((numModelos,4,2))
imagenes = []

imagenes.append("./img/plato.jpg")
puntosFot[0] = np.array([[486.0,400-223.0],[109.0,400-179.0],[339.0, 400-130.0],[217.0,400-294.0]])

imagenes.append("./img/mesa.jpg")
puntosFot[1] = np.array([[26.0,400-117.0],[238.0,400-240.0],[583.0, 400-141.0],[353.0, 400-49.0]])

imagenes.append("./img/charola.jpg")
puntosFot[2] = np.array([[34.0,400-222.0],[481.0, 400-268.0],[190.0,400-125.0],[560.0, 400-156.0]])
