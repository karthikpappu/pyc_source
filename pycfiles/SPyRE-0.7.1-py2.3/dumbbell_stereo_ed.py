# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\demos\dumbbell_stereo_ed.py
# Compiled at: 2006-02-24 19:17:03
"""
Draws a dumbbell, (two spheres and a connecting cylinder) fixed in space, 
but with an orbiting light source.

@undocumented gl.*
@exclude gl.*
"""
import math, sys, atexit, pygame, OpenGL.GL as ogl, OpenGL.GLU as oglu
sys.path.append('..')
import spyre, stereoscopic, zoe_objects as zoeobj

class DumbBell(spyre.Object):
    """draws a dumbbell object """
    __module__ = __name__

    def __init__(self, height, radius, x=0, y=0, z=0):
        spyre.Object.__init__(self)
        self.height = height
        self.radius = radius
        self.x = x
        self.y = y
        self.z = z
        self.quad = oglu.gluNewQuadric()

    def display(self):
        ogl.glColor4f(0.5, 0.5, 0.5, 1)
        ogl.glPushMatrix()
        ogl.glTranslate(self.x, self.y, self.z - self.height / 2.0)
        ogl.glMaterialfv(ogl.GL_FRONT, ogl.GL_AMBIENT, [0.1745, 0.0, 0.1, 0.0])
        ogl.glMaterialfv(ogl.GL_FRONT, ogl.GL_DIFFUSE, [0.5, 0.5, 0.5, 0.1])
        ogl.glMaterialfv(ogl.GL_FRONT, ogl.GL_SPECULAR, [0.7, 0.6, 0.8, 0.0])
        ogl.glMaterialf(ogl.GL_FRONT, ogl.GL_SHININESS, 50)
        oglu.gluCylinder(self.quad, self.radius / 2.0, self.radius / 2.0, self.height, 60, 70)
        ogl.glTranslate(0, 0, self.height + self.radius / 2.0)
        oglu.gluSphere(self.quad, self.radius, 60, 60)
        ogl.glTranslate(0, 0, -self.height - self.radius)
        oglu.gluSphere(self.quad, self.radius, 60, 60)
        ogl.glPopMatrix()


def postMortem(engine):
    """ displays frame rate to stderr at end of run """
    print >> sys.stderr, 'frame %d rate %.2f' % (spyre.Object.runTurn, engine.runTimer.frameRate)
    for cam in engine.cameras:
        print >> sys.stderr, 'ortho.s %d, %d, %d, %d, %d, %d' % (cam.left, cam.right, cam.top, cam.bottom, cam.near, cam.far)
        print >> sys.stderr, 'eye.p %f %f %f ' % cam.eye
        print >> sys.stderr, 'up.p %f %f %f ' % cam.up
        print >> sys.stderr, 'fviewport.p %f %f %f %f ' % cam.fractViewport
        print >> sys.stderr, 'viewport.p %f %f %f %f ' % cam.viewport
        print >> sys.stderr, '---'


def main():
    """ main block """
    pygame.init()
    eng = spyre.EngineFullScreen()
    eng.studio = spyre.StudioColorMat(eng)
    light0 = spyre.Bulb([0.5, 0.6, 0.5, 1.0], [
     0.6, 0.7, 0.7, 1.0], [
     0.3, 0.3, 0.3, 1.0])
    orbiter = zoeobj.RotatingGroup(0.03, objects=[light0], ray=(1, 0, 0))
    eng.studio.addMobileLight(light0, orbiter, (0, 10, 10))
    eng.add(zoeobj.AxesObject())
    eng.add(zoeobj.GridObject())
    eng.add(DumbBell(2, 1))
    atexit.register(postMortem, eng)
    engine = stereoscopic.StereoEngineED(eng)
    engine.go()


if __name__ == '__main__':
    main()