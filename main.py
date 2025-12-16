# Aqui se experimentara con colisiones 3D de Figuras Precargadas y immagenes cargadas en poligonos.

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *       # <-- Aqui estamos importando la biblioteca GLUT FreeGLUT para las figuras precargadas.
from carga import cargar_textura, dibujar_poligono, va_hacia_la_derecha
    
giro1 = 0.5
width_ = 100; height_ = 100; deep_ = 100

mc = None
escudos_por_3 = None
repite = 0

valores_cuadro = {
    "pos_x": 0.0,      # Posición inicial en X
    "pos_y": 10.0,       # Posición inicial en Y
    "tamanio": 10.0
}

def iniciar_ventana():
    if not glfw.init():
        raise Exception("No se pudo iniciar GLFW")
    ventana = glfw.create_window(1000, 1000, "Formas Básicas con transformaciones", None, None)
    if not ventana:
        glfw.terminate()
        raise Exception("No se pudo crear la ventana")
    glfw.make_context_current(ventana)

    glutInit(sys.argv)  # Linea para recurrir a recursos del Systema y usar funciones para mostrar texto precargado en pantalla.

    # Activar buffer de profundidad, necesario para trabajar en 3D y calcular la profundidad de los
    # objetos en la escena.
    glEnable(GL_DEPTH_TEST)
    glutInit()                      # Inicializar GLUT para usar figuras precargadas
    return ventana

# Para cambiar la perspectiva
def cambiar_perspectiva(ancho, alto, fov):

    # global deep_

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(100, ancho/alto, 0.1, 200.0)

    glMatrixMode(GL_MODELVIEW)      # Configurar cámara
    glLoadIdentity()
    gluLookAt(
        0, 0, 100,                # Cámara POSICIONADA para ver toda la escena, un angulo mayor a 45 da efecto a ojo de pez.
        0, 0, 0,                    # Mira al CENTRO de la escena
        0, 1, 0                     # Vector "arriba"
        # 0, 0, 1                   # Vector "enfrente"
    )

def key_callback(window, key, scancode, action, mods):

    global valores_cuadro, mc   # Recordar que 'mc' es el Main Character (personaje principal).
    x = valores_cuadro["pos_x"]    
    y = valores_cuadro["pos_y"]    
    tamanio = valores_cuadro["tamanio"]    

    if action == glfw.PRESS or action == glfw.REPEAT:
    
        # Moviendo el cuadro hacia arriba y abajo
        if key == glfw.KEY_UP or key == glfw.KEY_W:
            if( tamanio + y < height_):
                valores_cuadro["pos_y"] += 1

        elif key == glfw.KEY_DOWN or key == glfw.KEY_S:
            if( y > -height_):
                valores_cuadro["pos_y"] -= 1
    
        # MOVIMIENTO HORIZONTAL
        elif key == glfw.KEY_LEFT or key == glfw.KEY_A:
            if( x > -width_):
                valores_cuadro["pos_x"] -= 1
        
        elif key == glfw.KEY_RIGHT or key == glfw.KEY_D:
            if( x < width_):
                valores_cuadro["pos_x"] += 1

        # CONTROL DE LA VENTANA
        elif key == glfw.KEY_ESCAPE:
            # Cierra la ventana cuando se presiona ESC
            glfw.set_window_should_close(window, True)
    
    mc.actualizar(x, y)
    print(f"Posición X: {valores_cuadro['pos_x']}, Posición Y: {valores_cuadro['pos_y']}")

class Poligono():   # Todavia no es capaz de cargar un png sobre el poligono... TODO.

    # CONSTRUCTOR
    def __init__(this, x, y, lado):
        this.x = x
        this.y = y
        this.lado = lado

        # Cargamos los sprites del MC usando la función del módulo 'carga'.
        sprites_data = carga.cargar_mc()
        this.sprites = sprites_data[0]
        this.frame = sprites_data[4]
        this.velocidad_anim = sprites_data[5]
        this.ultimo_tiempo = sprites_data[6]
        
        this.actualizar(x, y) # Inicializa la hitbox

    # METODOS

    def actualizar(this, x, y):
        this.x = x
        this.y = y
        # Actualizamos la 'hitbox'
        this.vx1 = this.x
        this.vy1 = this.y
        this.vx2 = this.x + this.lado
        this.vy2 = this.y + this.lado 

    def actualizar_animacion(this):
        """ Actualiza el frame de animación basado en el tiempo. """
        tiempo_actual = time.time()
        if tiempo_actual - this.ultimo_tiempo > this.velocidad_anim:
            this.frame = (this.frame + 1) % len(this.sprites)
            this.ultimo_tiempo = tiempo_actual

    def dibujar(this):
        this.actualizar_animacion() # Actualiza el frame ANTES de dibujar
        
        # Como usaremos poligono probablente mas adelante sea necesario ajusatr el eje 'Z'.
        glPushMatrix()
        
        glBindTexture(GL_TEXTURE_2D, this.sprites[this.frame])
        
        # Dibujar el quad con textura.
        centro_x = this.x + (this.lado / 2)
        centro_y = this.y + (this.lado / 2)
        mitad = this.lado / 2 
        
        dibujar_poligono(centro_x, centro_y, mitad, mitad) 
        
        glPopMatrix()
        
#        glBegin(GL_POLYGON)
#        glVertex2f(this.x, this.y)
#        glVertex2f(this.x + this.lado, this.y)
#        glVertex2f(this.x + this.lado, this.y + this.lado)
#        glVertex2f(this.x, this.y + this.lado)
#        glEnd()

    def colisionando_power1(this):  # Esta funcion llamara a sonidos u animaciones para una mejor exeriencia de juego.
        print("COLISION DETECTADA!")

# Esta clase planeo usarla para crear figuras precargadas en 3D para usarlas como PowerUp para el personaje principal. Este power up sera un cubo alambrado (wire)
# que en cuanto entre en contacto con el objeto "Poligono", podre saber si ha colisionado y posteriormente activar "banderas" o estados de objetos para cargar
# animaciones, efectos en el personaje y sonidos.
class Power(): 
    # CONSTRUCTOR
    def __init__(this, x, y, tamanio):
        this.x = x
        this.y = y
        this.tamanio = tamanio
        this.actualizar(x, y, tamanio)

    # METODOS
    def actualizar(this, x, y, tamanio):
        this.x = x
        this.y = y
        this.tamanio = tamanio / 2 
        this.vx1 = x - tamanio
        this.vy1 = y - tamanio
        this.vx2 = x + tamanio
        this.vy2 = y + tamanio

    def up1(this, x, y, tamanio):   # Dibuja un cubo wired.
        this.actualizar(x, y, tamanio)

        glPushMatrix()
        glTranslatef(x, y, 0,)
        glRotatef(giro1, 1.0, 1.0, 1.0)     # Gira en todos los ejes
        glutWireCube(tamanio)
        glPopMatrix()

def colision_2d_3d():
    global mc, escudos_por_3
    escudos = escudos_por_3

    if (mc.vx2 >= escudos.vx1 and mc.vx1 <= escudos.vx2): # Comprueba una colision en el eje 'X'.
        if ( escudos.vy2 >= mc.vy1 and escudos.vy1 <= mc.vy1): # Comprueba una colision en el eje 'Y'.
            mc.colisionando_power1()   # Esta sera una funcion que llamara a efectos de sonido y auna animacion que se le aplcara al poligono del MC.
            print("El MC atrapo un PowerUp que le da 3 escudos.")

def programa_principal():

    global giro1, mc, escudos_por_3

    # Inicializar GLFW y crear la ventana
    try:
        ventana = iniciar_ventana()
    except Exception as e:
        print(f"Error fatal al iniciar la ventana: {e}")
        return

    # configurar_coordenadas_ventana(-15.0, 15.0, -15.0, 15.0, -15.0, 15.0)
    # Configurar perspectiva
    ancho, alto = glfw.get_window_size(ventana)
    # cambiar_perspectiva(ancho, alto, 45)
    cambiar_perspectiva(ancho, alto, 45)

    intervalos_escudos = 15.0    # Intervalos de timepo deseados para el respawn de escudos
    spawn = 0.0                 # Momento del ultimo respawm (cambia de cero a algun segundo despues de haber iniviado la ventana GLFW)

    mc = Poligono(valores_cuadro["pos_x"], valores_cuadro["pos_y"], 10)
    escudos_por_3 = Power(0, -15, 10)
        
    velocidad = 0.0
        
    glfw.set_key_callback(ventana, key_callback)

    while not glfw.window_should_close(ventana):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
   
        tiempo_actual = glfw.get_time()     # Asi conseguimos el tiempo desde que se inicio la ventana GLFW
        if tiempo_actual - intervalos_escudos >= spawn:
            print("Aparecio un PowerUp de escudos x3!")
            spawn = tiempo_actual
 
        mc.dibujar(valores_cuadro["pos_x"], valores_cuadro["pos_y"], valores_cuadro["tamanio"])
        escudos_por_3.up1(0.0, velocidad, 10)
        colision_2d_3d()

        giro1 += 0.1
        if giro1 > 360: giro1 = 0.0

        velocidad += 0.1
        if (velocidad > 30): velocidad= 0.0

        glfw.swap_buffers(ventana)
        glfw.poll_events()
    glfw.terminate()

if __name__ == "__main__":
    programa_principal()


























