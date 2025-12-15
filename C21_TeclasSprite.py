""" Para obligar la transparencia en los spritesm debemos ordenarle a OpenGL que no dibuje los píxeles
    con un valor alfa de 0 (completamente transparentes). Esto se logra activando el test de alfa con:
        
    En el código del sprite con movimiento, colócarlo después del:

    glEnable(GL_TEXTURE_2D)

    Así:
    glEnable(GL_TEXTURE_2D)
                                # Necesario para transparencias en PNG
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    En caso de no indicar estas últimas lineas , el sprite se dibujará con un fondo negro. """


import glfw
from OpenGL.GL import *
from PIL import Image
import time

                                        # Para controlar el sentido del ave
va_hacia_la_derecha = False

                                        # Función para cargar textura
def cargar_textura(ruta):
    imagen = Image.open(ruta).transpose(Image.FLIP_TOP_BOTTOM)
    img_data = imagen.convert("RGBA").tobytes()
    width, height = imagen.size

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return tex_id

                                        # Función para dibujar un quad con una textura dada
def dibujar_poligono(x, y, w, h):
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(x - w, y - h)
    glTexCoord2f(1, 0); glVertex2f(x + w, y - h)
    glTexCoord2f(1, 1); glVertex2f(x + w, y + h)
    glTexCoord2f(0, 1); glVertex2f(x - w, y + h)
    glEnd()


                                        # Programa principal GLFW
def main():
    # Inicializar GLFW
    if not glfw.init():
        return

    ventana = glfw.create_window(800, 600, "Sprite con Fondo y Movimiento", None, None)
    glfw.make_context_current(ventana)

    # Cargar fondo
    fondo = cargar_textura("/home/ariel/Programacion/Python/u4/D03_RellenoPoligonosTexturas/PNGs/FondoSprite02.bmp")

    # Cargar 5 sprites (animación)

#    rutas = [
#        "/home/javier/Documentos/Programas/Python/Texturas/PNGs/PajA.png",
#        "/home/javier/Documentos/Programas/Python/Texturas/PNGs/PajB.png",
#        "/home/javier/Documentos/Programas/Python/Texturas/PNGs/PajC.png",
#        "/home/javier/Documentos/Programas/Python/Texturas/PNGs/PajD.png",
#        "/home/javier/Documentos/Programas/Python/Texturas/PNGs/PajE.png",
#        "/home/javier/Documentos/Programas/Python/Texturas/PNGs/PajF.png",
#        "/home/javier/Documentos/Programas/Python/Texturas/PNGs/PajG.png",
#        "/home/javier/Documentos/Programas/Python/Texturas/PNGs/PajH.png"
#    ]

    rutas = [
        "/home/ariel/Programacion/Python/u4/D03_RellenoPoligonosTexturas/PNGs/PajA.png",
        "/home/ariel/Programacion/Python/u4/D03_RellenoPoligonosTexturas/PNGs/PajB.png",
        "/home/ariel/Programacion/Python/u4/D03_RellenoPoligonosTexturas/PNGs/PajC.png",
        "/home/ariel/Programacion/Python/u4/D03_RellenoPoligonosTexturas/PNGs/PajD.png",
        "/home/ariel/Programacion/Python/u4/D03_RellenoPoligonosTexturas/PNGs/PajE.png",
        "/home/ariel/Programacion/Python/u4/D03_RellenoPoligonosTexturas/PNGs/PajF.png",
        "/home/ariel/Programacion/Python/u4/D03_RellenoPoligonosTexturas/PNGs/PajG.png",
        "/home/ariel/Programacion/Python/u4/D03_RellenoPoligonosTexturas/PNGs/PajH.png"
    ]
    sprites = [cargar_textura(r) for r in rutas]

    # Activar texturas
    glEnable(GL_TEXTURE_2D)


    # Activar transparencia en PNGs
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)



    # Variables del sprite
    frame = 0
    velocidad_anim = 0.12
    ultimo_tiempo = time.time()

    # Posición del sprite
    x = 0.0
    y = 0.0
    velocidad = 0.03

                                                # Loop principal
    
    while not glfw.window_should_close(ventana):

        glClear(GL_COLOR_BUFFER_BIT)

                                                # Dibujar el fondo (pantalla llena)
        glBindTexture(GL_TEXTURE_2D, fondo)
        dibujar_poligono(0, 0, 1, 1)

                                                # Actualizar animación
        if time.time() - ultimo_tiempo > velocidad_anim:
            frame = (frame + 1) % len(sprites)
            ultimo_tiempo = time.time()

                                                # Movimiento con teclas
        if glfw.get_key(ventana, glfw.KEY_UP) == glfw.PRESS:
            y += velocidad
        
        if glfw.get_key(ventana, glfw.KEY_DOWN) == glfw.PRESS:
            y -= velocidad

        if glfw.get_key(ventana, glfw.KEY_LEFT) == glfw.PRESS:
            x -= velocidad

        if glfw.get_key(ventana, glfw.KEY_RIGHT) == glfw.PRESS:
            x += velocidad

                                                # Dibujar el sprite
        glBindTexture(GL_TEXTURE_2D, sprites[frame])
        dibujar_poligono(x, y, 0.15, 0.15)

                                                # Intercambiar buffers (mas velocidad)
        glfw.swap_buffers(ventana)
        glfw.poll_events()

    glfw.terminate()


main()
