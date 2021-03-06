# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\kafx\libs\draw\adv_b.py
# Compiled at: 2012-04-17 09:52:04


def fRotoZoom(steps=4, opacity=0.25, scale=1, angle=0, org_x=0, org_y=0):
    u"""Realiza un effect de rotacion y zoom progresivos sobre todo el contenido del cuadro
        @steps : cantidad de steps
        @opacity : opacity de cada paso
        @scale : incremento de scale por paso
        @angle : incremento del ángulo por paso, en radianes
        @org_x, org_y : el origen sobre el que se realizan las transformaciones
        """
    ctx = video.cf.ctx
    sfc = ctx.get_group_target()
    pat = cairo.SurfacePattern(sfc)
    ctx.set_source(pat)
    fangle = angle
    for a in xrange(int(steps)):
        fescala = 1.0 / (1.0 + a * scale)
        fangle += angle
        pat.set_matrix(extra.CreateMatrix(org_x, org_y, org_x, org_y, fangle, fescala, fescala, inverse=True))
        ctx.paint_with_alpha(opacity)


def fWave(offset, delta=0.1, amplitude=10, vertical=True, delete=True):
    u"""Realiza un effect de ondulacion sobre la imagen active.
        @offset : un offset del angle de offset (si se quiere animar esto se debe modificar)
        @delta = 0.1 : el delta que indica cuanto cambiará la onda de pixel a pixel (es como el ancho de la onda (en vertical)) (mientras mas pequeño, la onda es mas ancha) (esto es lo mismo que frecuencia)
        @amplitude = 10 : cuan fuerte es la deformacion (el alto de la onda (en vertical))
        @vertical = True : True si se quiere hacer una onda vertical, False si se la quiere horizontal
        @delete = True : True si se desea eliminar lo dibujado anteriormente, o False si se desea redibujar lo deformado encima de lo anterior
        """
    ctx = video.cf.ctx
    vi = video.vi
    sfc = extra.CopyTarget()
    if delete:
        ctx.set_operator(cairo.OPERATOR_CLEAR)
        ctx.paint()
        PaintMode()
    x1, x2, y1, y2 = (0, vi.width, 0, vi.height)
    if vertical:
        alto = y2
        ancho = 1
        min = x1
        max = x2
    else:
        alto = 1
        ancho = x2
        min = y1
        max = y2
    for i in xrange(min, max):
        dif = delta * (i + offset)
        if vertical:
            x1 = i
            mx = 0
            my = sin(pi * dif) * amplitude
        else:
            y1 = i
            mx = sin(pi * dif) * amplitude
            my = 0
        ctx.set_source_surface(sfc, mx, my)
        ctx.rectangle(x1, y1, ancho, alto)
        ctx.fill()


class cSprite:

    def __init__(self, texture, x=0, y=0, angle=0, color=None, mode=1, scale=1.0):
        u"""
                @texture : pattern que se usará como textura
                        (se puede cargar con extra.LoadTexture("archivo.png") o simplemente pasar el nombre de archivo "archivo.png")
                @mode =1: 1-> textura solida, 0-> un solo color y mascara
                @center =False: If true, then the sprite will be moved to be centered at the x/y (works better with squared textures)
                """
        texture.set_extend(cairo.EXTEND_NONE)
        self._pat = texture
        self._s = texture.get_surface()
        self._width = self._s.get_width()
        self._height = self._s.get_height()
        self.org_x = self._width / 2.0
        self.org_y = self._height / 2.0
        self.angle = angle
        self.color = color or extra.cCairoColor()
        self.mode = mode
        self.x = x
        self.y = y
        self.Scale(scale, scale)

    def Scale(self, x, y):
        u"""se puede hacer directamente accediendo a scale_x y scale_y,
                pero esta para facilitar el tema de la division,
                si usás escalas predivididas, es más rápido asignarlas directamente a scale_x y scale_y"""
        self.scale_x = 1.0 / (x or 1.0)
        self.scale_y = 1.0 / (y or 1.0)

    def Paint(self):
        u"""Pinta la imagen sobre el cuadro según las propiedades
                """
        self._pat.set_matrix(extra.CreateMatrix(self.x, self.y, self.org_x, self.org_y, self.angle, self.scale_x, self.scale_y, True))
        ctx = video.cf.ctx
        if self.mode:
            ctx.set_source(self._pat)
            ctx.paint_with_alpha(self.color.a)
        else:
            ctx.set_source_rgba(self.color.r, self.color.g, self.color.b, self.color.a)
            ctx.mask(self._pat)


class cParticleSystem:

    class cEmitter:
        x = y = angle = vel = mapertura = xg = yg = mw = mh = 0.0

    class cParticula:

        def __init__(self, i=0):
            self.index = i
            self.Reset()

        def Reset(self, active=False, x=300, y=300, life=1, color=None, xi=0, yi=0, sc1=1, sc2=1, xg=0, yg=0, rotation=0.1):
            """Llamado por el sistema de particulas para "crear" una particula nueva"""
            self.active = active
            self.life = 0
            self.scale = sc1
            self.fade = (random() / 10 + 0.1) / life
            self.color = color
            self.x = x
            self.y = y
            self.xi = xi
            self.yi = yi
            self.angle = random() * 2 * pi
            self.anglei = random() * rotation
            self.sci = (sc2 - sc1) * self.fade
            self.xg = xg
            self.yg = yg

        def BaseAnimator(self):
            """Animador default
                          puedes llamar a este animador para que haga las cosas normales, movimiento, rotacion, scale
                          tambien podes definir el tuyo y pasarlo por parametro al instanciar el sistema de particulas
                          asegurate de modificar el valor de active
                        """
            self.angle += self.anglei
            self.y += self.yi
            self.x += self.xi
            self.scale += self.sci
            self.color.a -= self.fade
            self.xi += self.xg
            self.yi += self.yg
            self.life += self.fade
            self.active = self.life < 1

    def __init__(self, png='textures/blast.png', emit_parts=5, max_parts=500, max_life=2, mode=None, color=None, scale_from=1.0, scale_to=2.0, rotation=0.1, animator=None):
        u"""
                todos los valores son opcionales

                png archivo png usado como textura/mascara
                max_parts total de particulas posibles en todo momento
                emit_parts maxima cantidad de particulas que se crearan por vez que se llama a Emitir
                color = None -> Color random, o instancia de cCairoColor
                max_life entero con el máximo de vida de cada particula
                mode = 0-> textura, 1->mascara con color solido, 2-> mascara tomando el color del punto sobre el que cae
                        Para mejor funcionamiento, no especificar color si se usará el mode 0
                scale_from valor de scale inical para cada particula
                scale_to valor de scale final para cada particula
                animator una función que se llama por cada particula, por cada cuadro, que recibe como parametro la particula en cuestion
                """
        self.parts = [ self.cParticula(i=i) for i in xrange(max_parts) ]
        self.ppc = emit_parts
        self.life = max_life or 1
        if mode == None:
            if color == None:
                mode = 0
            else:
                mode = 1
        self.mode = mode
        self.color = color
        self.sfc = cairo.ImageSurface.create_from_png(png)
        self.sc1 = 1.0 / scale_from
        self.sc2 = 1.0 / scale_to
        self.pat = cairo.SurfacePattern(self.sfc)
        self.centx = self.sfc.get_width() / 2
        self.centy = self.sfc.get_height() / 2
        self.w = self.sfc.get_width()
        self.h = self.sfc.get_height()
        self.anglei = rotation
        self.emitter = self.cEmitter()
        self.Animate = animator or self.cParticula.BaseAnimator
        return

    def Emit(self):
        u"""Cuando se llama a esta función se le indica al sistema se emiten particulas
                Cada vez que se llama, se crearán un máximo de "emitir_parts".
                Se lo puede llamar varias veces en el mismo cuadro,
                cambiando las propiedades del emitter entre las diferentes llamadas
                """
        newparts = 0
        e = self.emitter
        for p in self.parts:
            if newparts > self.ppc:
                return
            if not p.active:
                x = -(e.x + (random() * e.mw * 2 - e.mw))
                y = -(e.y + (random() * e.mh * 2 - e.mh))
                if self.color:
                    c = extra.cCairoColor(ccolor=self.color)
                else:
                    c = extra.cCairoColor()
                    if self.mode == 2:
                        im = video.cf.ctx.get_group_target()
                        stride = im.get_stride()
                        pixels = im.get_data()
                        pos = -(int(y) * stride) + int(x) * 4
                        try:
                            b, g, r, a = map(ord, pixels[pos:pos + 4])
                        except:
                            b = g = r = a = 0

                        c.r = r / 256.0
                        c.g = g / 256.0
                        c.b = b / 256.0
                    else:
                        c.r = random()
                        c.g = random()
                        c.b = random()
                        c.a = 1
                xi = -cos(e.angle + e.mapertura - e.mapertura * 2.0 * random()) * e.vel
                yi = sin(e.angle + e.mapertura - e.mapertura * 2.0 * random()) * e.vel
                p.Reset(True, x=x, y=y, life=self.life, color=c, xi=xi, yi=yi, sc1=self.sc1, sc2=self.sc2, xg=e.xg, yg=e.yg, rotation=self.anglei)
                newparts += 1

    def SetPosition(self, x, y):
        u"""Para cambiar la posicion del emitter
                @x, y : Posición en pixels"""
        self.emitter.x = x
        self.emitter.y = y

    def SetAngle(self, angle, speed, aperture=0):
        u"""Para cambiar el angle de emision
                @angle : el ángulo en radianes de la emisión
                @speed : la speed de la emisión, en pixels por cuadro
                @aperture : angulo en radianes para el ángulo de aperture máxima de emisión"""
        e = self.emitter
        e.angle = angle
        e.vel = speed
        e.mapertura = aperture / 2.0

    def SetGravity(self, angle, speed):
        u"""para cambiar la gravedad del sistema de partículas
                @angle : angulo en radianes de la gravedad
                @speed : la speed de ACELEARCION de la gravedad en pixels por cuadro
                """
        self.emitter.xg = -cos(angle) * speed
        self.emitter.yg = sin(angle) * speed

    def SetWindow(self, width, height):
        u"""para cambiar la ventana de creacion de particulas
                @width, height : indican el tamaño de la ventana donde pueden aparecer
                partículas
                """
        self.emitter.mw = width / 2.0
        self.emitter.mh = height / 2.0

    def Paint(self):
        u"""Cada vez que se llama a esta funcion se pintan todas las particulas vivas, se calcula su nueva posicion, y si estan vivas
                o no.
                Se crean particulas nuevas si se llamó a Emitir
                """
        ctx = video.cf.ctx
        for p in self.parts:
            if p.active:
                mat = cairo.Matrix()
                mat.translate(self.centx, self.centy)
                mat.rotate(p.angle)
                mat.scale(p.scale, p.scale)
                mat.translate(p.x, p.y)
                self.pat.set_matrix(mat)
                if self.mode:
                    ctx.set_source_rgba(p.color.r, p.color.g, p.color.b, p.color.a)
                    ctx.mask(self.pat)
                else:
                    ctx.set_source(self.pat)
                    ctx.paint_with_alpha(p.color.a)
                self.Animate(p)


def CreateParticles(box, texture, scale=1.0, alpha_min=0.2, vertical=True, mode=0):
    u"""This is really slow, use with care.

                :param box: A tuple with the bounding box, like (x, y, w, h)(todos los items DEBEN ser enteros (int))
                :type box: tuple
                :param texture: pattern to be used as texture
                :type texture: cairo pattern `cairo.pattern`
                :param scale: starting scale for every particle
                :type scale: `float`
                :param alpha_min: any pixel with an alpha value less than this value will be ignored (por lo tanto no generará partícula) (0.0 to 1.0)
                :type alpha_min: `float`
                :param vertical: indica si el barrido de pixels será vertical (True) u horizontal (False) esto influye en el orden en que serán creadas las partículas en el array, por lo tanto la forma en que se recorre
                :type vertical: `bool`
                :param mode: particle mode xxxx TODO EXPAND
                :type mode: int
                """
    parts = []
    im = video.cf.ctx.get_group_target()
    width = im.get_width()
    height = im.get_height()
    if hasattr(im, 'get_stride'):
        stride = im.get_stride()
    else:
        stride = video.vi.width * 4
    pixels = im.get_data()
    x1, y1, x2, y2 = box
    if vertical:
        i1, i2 = x1, x2
        j1, j2 = y1, y2
    else:
        i1, i2 = y1, y2
        j1, j2 = x1, x2
    for i in xrange(i1, i2):
        for j in xrange(j1, j2):
            if vertical:
                x = i
                y = j
            else:
                y = i
                x = j
            if x < 0 or x >= width:
                continue
            if y < 0 or y >= height:
                continue
            pos = y * stride + x * 4
            try:
                b, g, r, a = map(extra.D1, map(ord, pixels[pos:pos + 4]))
                if a < alpha_min:
                    continue
                c = extra.cCairoColor()
                c.r = r
                c.a = a
                c.g = g
                c.b = b
                parts.append(cSprite(texture=texture, x=x + 0.5, y=y + 0.5, scale=scale, color=c, mode=mode))
            except:
                import traceback
                print 'Error al crear las particulas', traceback.print_exc()

    return parts