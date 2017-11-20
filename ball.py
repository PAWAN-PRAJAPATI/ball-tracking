from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import cv2
from Image import *
from webcam import Webcam
from detection import Detection


class HandTracker:
    def __init__(self):
        self.webcam = Webcam()
        self.webcam.start()

        self.detection = Detection()

        self.x_axis = 0.0
        self.y_axis = 0.0
        self.z_axis = 0.0
        self.z_pos = -7.0

    def _handle_gesture(self):
        # get image from webcam
        image = self.webcam.get_current_frame()

        # detect hand gesture in image
        is_okay = self.detection.is_item_detected_in_image('haarcascade_okaygesture.xml', image.copy())
        is_vicky = self.detection.is_item_detected_in_image('haarcascade_vickygesture.xml', image.copy())

        if is_okay:
            # okay gesture moves cube towards us
            self.z_pos = self.z_pos + 1.0
        elif is_vicky:
            # vicky gesture moves cube away from us
            self.z_pos = self.z_pos - 1.0

    def _draw_cube(self):
        # draw cube
        glBegin(GL_QUADS);
        glTexCoord2f(0.0, 0.0);
        glVertex3f(-1.0, -1.0, 1.0)
        glTexCoord2f(1.0, 0.0);
        glVertex3f(1.0, -1.0, 1.0)
        glTexCoord2f(1.0, 1.0);
        glVertex3f(1.0, 1.0, 1.0)
        glTexCoord2f(0.0, 1.0);
        glVertex3f(-1.0, 1.0, 1.0)
        glTexCoord2f(1.0, 0.0);
        glVertex3f(-1.0, -1.0, -1.0)
        glTexCoord2f(1.0, 1.0);
        glVertex3f(-1.0, 1.0, -1.0)
        glTexCoord2f(0.0, 1.0);
        glVertex3f(1.0, 1.0, -1.0)
        glTexCoord2f(0.0, 0.0);
        glVertex3f(1.0, -1.0, -1.0)
        glTexCoord2f(0.0, 1.0);
        glVertex3f(-1.0, 1.0, -1.0)
        glTexCoord2f(0.0, 0.0);
        glVertex3f(-1.0, 1.0, 1.0)
        glTexCoord2f(1.0, 0.0);
        glVertex3f(1.0, 1.0, 1.0)
        glTexCoord2f(1.0, 1.0);
        glVertex3f(1.0, 1.0, -1.0)
        glTexCoord2f(1.0, 1.0);
        glVertex3f(-1.0, -1.0, -1.0)
        glTexCoord2f(0.0, 1.0);
        glVertex3f(1.0, -1.0, -1.0)
        glTexCoord2f(0.0, 0.0);
        glVertex3f(1.0, -1.0, 1.0)
        glTexCoord2f(1.0, 0.0);
        glVertex3f(-1.0, -1.0, 1.0)
        glTexCoord2f(1.0, 0.0);
        glVertex3f(1.0, -1.0, -1.0)
        glTexCoord2f(1.0, 1.0);
        glVertex3f(1.0, 1.0, -1.0)
        glTexCoord2f(0.0, 1.0);
        glVertex3f(1.0, 1.0, 1.0)
        glTexCoord2f(0.0, 0.0);
        glVertex3f(1.0, -1.0, 1.0)
        glTexCoord2f(0.0, 0.0);
        glVertex3f(-1.0, -1.0, -1.0)
        glTexCoord2f(1.0, 0.0);
        glVertex3f(-1.0, -1.0, 1.0)
        glTexCoord2f(1.0, 1.0);
        glVertex3f(-1.0, 1.0, 1.0)
        glTexCoord2f(0.0, 1.0);
        glVertex3f(-1.0, 1.0, -1.0)
        glEnd();

    def _init_gl(self, Width, Height):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

        # initialize lighting
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 0.8, 0.0, 1.0))
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)

        # initialize blending
        glColor4f(0.2, 0.2, 0.2, 0.5)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)
        glEnable(GL_BLEND)

        # initialize texture
        image = open("devil.jpg")
        ix = image.size[0]
        iy = image.size[1]
        image = image.tostring("raw", "RGBX", 0, -1)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        glEnable(GL_TEXTURE_2D)

    def _draw_scene(self):
        # handle any hand gesture
        self._handle_gesture()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        glLoadIdentity();

        # position and rotate cube
        glTranslatef(0.0, 0.0, self.z_pos);
        glRotatef(self.x_axis, 1.0, 0.0, 0.0)
        glRotatef(self.y_axis, 0.0, 1.0, 0.0)
        glRotatef(self.z_axis, 0.0, 0.0, 1.0)

        # position lighting
        glLightfv(GL_LIGHT0, GL_POSITION, (0.0, 0.0, 2.0, 1.0))

        # draw cube
        self._draw_cube()

        # update rotation values
        self.x_axis = self.x_axis - 10
        self.z_axis = self.z_axis - 10

        glutSwapBuffers()

    def main(self):
        # setup and run OpenGL
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(640, 480)
        glutInitWindowPosition(800, 400)
        glutCreateWindow("OpenGL Hand Tracker")
        glutDisplayFunc(self._draw_scene)
        glutIdleFunc(self._draw_scene)
        self._init_gl(640, 480)
        glutMainLoop()


# run instance of Hand Tracker
handTracker = HandTracker()
handTracker.main()