from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from puntos import *
from homografia import *
import numpy as np
from PIL import Image
import math
from puntosFisicos import *

COL, RWS = 600,400
numModel = 0

p1 = np.array([ [-10.,10.], [-10.,-10.],[10.,-10.],[10., 10.]])
rotate_y = 0.0

p2 = ordenaPuntos(puntosFot[numModel])
H = homografia(p1,p2)
MK, MRT, vc = parametros(H, RWS, COL)
imagen = imagenes[numModel]
im = Image.open(imagen).transpose( Image.FLIP_TOP_BOTTOM )
rgb_im = im.convert('RGB')
imdata = np.asarray(im)


def calculaModelos( i ):
    global MK, MRT, vc, imdata
    p2 = ordenaPuntos(puntosFot[i])
    H = homografia(p1, p2)
    MK, MRT, vc = parametros(H, RWS, COL)
    imagen = imagenes[i]
    im = Image.open(imagen).transpose( Image.FLIP_TOP_BOTTOM )
    rgb_im = im.convert('RGB')
    imdata = np.asarray(im)

def teclado( key, x, y):
    global numModel
    if (key == 102):
        numModel = (numModel + 1) % numModelos
        calculaModelos ( numModel)
    glutPostRedisplay()


def square():
    glBegin( GL_LINE_LOOP )
    glColor3f(  0.0,  1.0,  0.0 )
    glVertex3f( -10.0, -10.0, 0 )
    glVertex3f(  10.0, -10.0, 0 )
    glVertex3f(  10.0,  10.0, 0 )
    glVertex3f( -10.0,  10.0, 0 )
    glEnd()

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def display():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho ( 0.0, COL-1, 0.0, RWS-1, 1, 51.0 )
    glMultMatrixd( MK )
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity ()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glDisable(GL_DEPTH_TEST)
    glDrawPixels( COL, RWS, GL_RGB, GL_UNSIGNED_BYTE, imdata )
    glEnable(GL_DEPTH_TEST)
    glMultMatrixd( MRT )
    square()
    if (vc[2] > 0):
        glRotatef( 180, 1.0, 0.0, 0.0 )
    glPushMatrix()
    glRotatef( -90, 1.0, 0.0, 0.0 )
    glTranslatef(2.5,0.,0.)
    glRotatef( rotate_y, 0.0, 0.3, 0.0 )
    glColor3f(  0.0,  0.0,  0.5 )
    glutSolidTeapot (3)
    glPopMatrix()
    glFlush()
    glutSwapBuffers()

def rotaTimer( value ):
    global rotate_y
    rotate_y += 1.0;
    if( rotate_y > 360.0 ) :
        rotate_y = 0.0
    glutPostRedisplay()
    glutTimerFunc( 17, rotaTimer, 0 )
    #print ()

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(COL, RWS)
wind = glutCreateWindow("HOMOGRAFIA")
glEnable(GL_DEPTH_TEST)
glClearColor(0.,0.,0.,1.)

mat_specular = (1.0, 1.0, 1.0, 1.0)
light_position = (12.3, 12.3, 12.5, 0.0)
light_position1 = (-0.3, 0.3, 0.5, 0.0)
diffuseMaterial = (1., 1., 1., 1.0)
ambientMaterial = (0.5, .5, .5, 1.0)

glClearColor(1.0, 1.0, 1.0, 1.0)
glShadeModel(GL_SMOOTH)
glEnable(GL_DEPTH_TEST)
glMaterialfv(GL_FRONT, GL_AMBIENT, ambientMaterial)
glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuseMaterial)
glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
glMaterialf(GL_FRONT, GL_SHININESS, 15.0)
glLightfv(GL_LIGHT0, GL_POSITION, light_position)
glLightfv(GL_LIGHT1, GL_POSITION, light_position1)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glEnable(GL_LIGHT1)


glColorMaterial(GL_FRONT, GL_DIFFUSE)
glEnable(GL_COLOR_MATERIAL)
glutDisplayFunc(display)
glutSpecialFunc(teclado)

glViewport (0, 0, COL,RWS)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho ( 0.0, COL-1, 0.0, RWS-1, 1, 51.0 );

glutTimerFunc( 1000, rotaTimer, 0 )
glutMainLoop()
