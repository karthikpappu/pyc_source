# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/fisica/circulo.py
# Compiled at: 2016-08-25 21:09:54
import Box2D as box2d
from pilasengine.fisica.figura import Figura
from pilasengine import utils

class Circulo(Figura):
    """Representa un cuerpo de circulo.

    Generalmente estas figuras se pueden construir independientes de un
    actor, y luego asociar.

    Por ejemplo, podríamos crear un círculo:

        >>> circulo_dinamico = pilas.fisica.Circulo(10, 200, 50)

    y luego tomar un actor cualquiera, y decirle que se comporte
    cómo el circulo:

        >>> mono = pilas.actores.Mono()
        >>> mono.imitar(circulo_dinamico)
    """

    def __init__(self, fisica, pilas, x, y, radio, dinamica=True, densidad=1.0, restitucion=0.56, friccion=10.5, amortiguacion=0.1, sin_rotacion=False, sensor=False):
        Figura.__init__(self, fisica, pilas)
        if x is None:
            x = pilas.azar(10000, 110000)
        if y is None:
            y = pilas.azar(10000, 110000)
        x = utils.convertir_a_metros(x)
        y = utils.convertir_a_metros(y)
        self._radio = utils.convertir_a_metros(radio)
        self._escala = 1
        self.fisica = fisica
        if not self.fisica:
            self.fisica = pilas.escena_actual().fisica
        if not dinamica:
            densidad = 0
        try:
            fixture = box2d.b2FixtureDef(shape=box2d.b2CircleShape(radius=self._radio), density=densidad, friction=friccion, restitution=restitucion)
        except TypeError:
            fixture = box2d.b2FixtureDef(shape=box2d.b2CircleShape(radius=self._radio), density=densidad, linearDamping=amortiguacion, friction=friccion, restitution=restitucion)

        self.userData = {'id': self.id, 'figura': self}
        fixture.userData = self.userData
        self._cuerpo = self.fisica.mundo.CreateDynamicBody(position=(x, y), fixtures=fixture)
        self.sin_rotacion = sin_rotacion
        self.sensor = sensor
        self.dinamica = dinamica
        if not dinamica:
            self._cuerpo.mass = 1000000
        return

    def definir_radio(self):
        for fixture in self._cuerpo:
            fixture.shape.radius = self._radio

    def set_radius(self, radio):
        self._escala = self._escala * radio / self.radio
        self._radio = utils.convertir_a_metros(radio)
        self.definir_radio()

    def get_radius(self):
        return utils.convertir_a_pixels(self._radio)

    def set_scale(self, escala):
        self._radio = self._radio * escala / self._escala
        self._escala = escala
        self.definir_radio()

    def get_scale(self):
        return self._escala

    radio = property(get_radius, set_radius, doc='definir radio del circulo')
    escala = property(get_scale, set_scale, doc='definir escala del circulo')