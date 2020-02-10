import numpy as np
import pygame

class Vec3D(object):
    """A vertex in 3D space"""

    def __init__(self, pos=np.array([0.0, 0.0, 0.0])):
        self.pos = np.array(pos)

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    @property
    def z(self):
        return self.pos[2]

    def translate(self, vector=[0.0, 0.0, 0.0]):
        return Vec3D([self.x + vector[0],
                      self.y + vector[1],
                      self.z + vector[2]])

    def transform(self, m):
        """transform vertex using given matrix"""
        '''
        # explicit version
        new_x = self.x * m[0][0] + self.y * m[1][0] + self.z * m[2][0] + m[3][0]
        new_y = self.x * m[0][1] + self.y * m[1][1] + self.z * m[2][1] + m[3][1]
        new_z = self.x * m[0][2] + self.y * m[1][2] + self.z * m[2][2] + m[3][2]
        w = self.x * m[0][3] + self.y * m[1][3] + self.z * m[2][3] + m[3][3]

        if w != 0.0:
            new_x /= w
            new_y /= w
            new_z /= w

        return Vec3D([new_x, new_y, new_z])
        '''
        new_vec = np.dot(list(self.pos)+[1], m)
        if new_vec[3] != 0.0:
            new_vec /= new_vec[3]
        return Vec3D(new_vec[:3])
        

    def scale(self, width, height):
        """scale vertex to given screen height and width"""
        return Vec3D([(self.x + 1.0) * (0.5 * width),
                      (self.y + 1.0) * (0.5 * height),
                      self.z])

class Triangle(object):
    """A triangle in 3D space defined as a triplet of vertices"""

    def __init__(self, vec1, vec2, vec3):
        self.vecs = [vec1, vec2, vec3]

    @property
    def vec1(self):
        return self.vecs[0]

    @property
    def vec2(self):
        return self.vecs[1]

    @property
    def vec3(self):
        return self.vecs[2]

    def translate(self, vector=[0.0, 0.0, 0.0]):
        """translate triangle by given values"""
        return Triangle(self.vec1.translate(vector),
                        self.vec2.translate(vector),
                        self.vec3.translate(vector))

    def transform(self, matrix):
        """transform triangle using given matrix"""
        return Triangle(self.vec1.transform(matrix),
                        self.vec2.transform(matrix),
                        self.vec3.transform(matrix))

    def scale(self, width, height):
        """scale triangle to given screen height and width"""
        return Triangle(self.vec1.scale(width, height),
                        self.vec2.scale(width, height),
                        self.vec3.scale(width, height))

    def draw(self, screen, colour):
        """draw triangle on pygame screen object"""
        pygame.draw.line(screen, colour, [self.vec1.x, self.vec1.y], [self.vec2.x, self.vec2.y])
        pygame.draw.line(screen, colour, [self.vec2.x, self.vec2.y], [self.vec3.x, self.vec3.y])
        pygame.draw.line(screen, colour, [self.vec3.x, self.vec3.y], [self.vec1.x, self.vec1.y])

class Mesh(object):
    """A mesh in 3D space defined as a collection of triangles"""

    def __init__(self, tris=[]):
        self.tris = []
        for tri in tris:
            self.tris.append(Triangle(Vec3D(tri[0:3]),
                                      Vec3D(tri[3:6]),
                                      Vec3D(tri[6:9])))
