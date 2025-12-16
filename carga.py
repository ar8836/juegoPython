# Este sera una libreria de carga de imagenes y sonidos

import glfw
import pygame
import os

# --- Configuración de Archivos y Directorios ---
# Sonidos funcionales pero solo son temporales, despues los cambiare por otros
RUTA_AMBIENTE1 = "/home/ariel/Programacion/Python/juegoPython/sounds/ambiente1.mp3"
RUTA_DISPARO1 = "/home/ariel/Programacion/Python/juegoPython/sounds/disparo1.mp3"
RUTA_RECARGA1 = "/home/ariel/Programacion/Python/juegoPython/sounds/recarga1.mp3"

# Variable global para almacenar el objeto de sonido de Pygame
sonido_disparo = None
sonido_recarga = None
va_hacia_la_derecha = False

def inicializar_pygame_sonido():
    """
    Inicializa el módulo de mezclador de Pygame y carga el efecto de sonido.
    """
    global sonido_disparo, sonido_recarga
    try:
        # Inicializar solo el módulo de mezclador (mixer) de Pygame
        pygame.mixer.init(44100, -16, 2, 2048)
        print(f"Buscando sonido en: {RUTA_DISPARO1}")

        if not os.path.exists(RUTA_DISPARO1):
            print(f"ERROR: Archivo de sonido no encontrado en la ruta: {RUTA_DISPARO1}")
            print(f"Asegúrate de que 'disparo1.mp3' esté en la carpeta 'sounds'.")
            return
        sonido_disparo = pygame.mixer.Sound(RUTA_DISPARO1)

        if not os.path.exists(RUTA_RECARGA1):
            print(f"ERROR: Archivo de sonido no encontrado en la ruta: {RUTA_RECARGA1}")
            print(f"Asegúrate de que 'recarga1.mp3' esté en la carpeta 'sounds'.")
            return
        sonido_recarga = pygame.mixer.Sound(RUTA_RECARGA1)

        # --- 2. CARGA Y REPRODUCCIÓN DE MÚSICA DE AMBIENTE1 (gestionado por mixer.music) ---
        print(f"Buscando música de ambiente en: {RUTA_AMBIENTE1}")
        if not os.path.exists(RUTA_AMBIENTE1):
            print(f"ERROR: Música de ambiente no encontrada en: {RUTA_AMBIENTE1}")
        else:
            # Cargar la música
            pygame.mixer.music.load(RUTA_AMBIENTE1)
            # Reproducir la música en bucle infinito (-1)
            pygame.mixer.music.play(-1)
            print("Música de ambiente iniciada en bucle.")

        print("Módulo de sonido de Pygame inicializado y sonido cargado.")

    except pygame.error as e:
        print(f"Error al inicializar Pygame Mixer o cargar el sonido: {e}")
        print("Verifica el archivo de sonido y la instalación de Pygame/SDL.")

def key_callback(window, key, scancode, action, mods):
    """
    Función de callback de teclado que reproduce el sonido al presionar ESPACIO.
    """
    global sonido_disparo, sonido_recarga

    # Solo procesamos eventos cuando la tecla es PRESIONADA o REPETIDA
    if action == glfw.PRESS or action == glfw.REPEAT:

        if key == glfw.KEY_SPACE:
            print("Tecla ESPACIO presionada. Reproduciendo sonido de disparo...")

            if sonido_disparo:
                # Reproducir el sonido
                sonido_disparo.play()
            else:
                print("Advertencia: El sonido no pudo ser cargado o inicializado.")

        if key == glfw.KEY_R:
            print("Tecla R presionada. Reproduciendo sonido de recarga del airma...")
            sonido_recarga.play()
        else:
            print("Advertencia: El sonido no pudo ser cargado o inicializado.")

        # Movimiento con teclas
        if key == glfw.PRESS:
            y += velocidad

        if key == glfw.PRESS:
            y -= velocidad

        if key == glfw.PRESS:
            x -= velocidad

        if key == glfw.PRESS:
            x += velocidad

        if key == glfw.KEY_ESCAPE:
            print("Escape presionado - Cerrando ventana")
            glfw.set_window_should_close(window, True)

        # Dibujar el sprite
        glBindTexture(GL_TEXTURE_2D, sprites[frame])
        dibujar_poligono(x, y, 0.15, 0.15)

# ======================= CARGAR FONDOS ==========================
def cargar_fondo():
    # Cargar fondo

    ruta_fondo = []
    for i in range(1, 41):
        ruta = "~/Programacion/Python/juegoPython/images/cielo/" + {i} + ".png"
        ruta_fondo[i] = ruta
        fondo = cargar_textura(ruta_fondo[i])
    # Hay 40 imagenes en .../images/cielo que se llaman 1.png, 2.png, 3.png y asi hasta 40.png
	sprites = [cargar_textura(r) for r in ruta_fondo]
	
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

def cargar_mc():    # Carga los sprites de animacion del "Main Character" mientras cae en picada, estaa nimacion se repite hasta un game over.
    # Cargar Personaje Principale

    ruta_mc = []
    for i in range(1, 41):
        ruta = "~/Programacion/Python/juegoPython/images/pato/" + {i} + ".png"
        ruta_mc[i] = ruta
        fondo = cargar_textura(ruta_mc[i])
    # Hay 40 imagenes en .../images/pato que se llaman 1.png, 2.png, 3.png y asi hasta 40.png
    sprites = [cargar_textura(r) for r in ruta_mc]
    
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

def cargar_mc_principio():      # Carga los sprites de animacion del "Main Character" en la que pasa de estar descanzando en una nube a empezar a caer.
                                # Esta animacion solo ocurre al principio del juego y no se vuelve a repetir.
    for i in range(1, 26):
        ruta[i] = "~/Programacion/Python/juegoPython/images/pato_acostado/" + {i} + ".png"
        fondo = cargar_textura(ruta_mc[i])
    # Hay 25 imagenes en .../images/pato_acostado que se llaman 1.png, 2.png, 3.png y asi hasta 25.png
    sprites = [cargar_textura(r) for r in ruta_mc]
    
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

def cargar_pantano_1():      # Carga los sprites de animacion del "pantano". Esta animacion solo aparecera al final del juego si es que el usuario logro ganar.
    ruta = []
    while os.path_exists("~/Programacion/Python/juegoPython/images/pantano_1/" + {i} + ".png"):
        ruta[i] = "~/Programacion/Python/juegoPython/images/pantano_1/" + {i} + ".png"
        fondo = cargar_textura(ruta[i])
    sprites = [cargar_textura(r) for r in ruta]
    
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

def cargar_pantano_2():     # Carga los sprites de animacion del "pantano". Esta animacion solo aparecera al final del juego si es que el usuario logro ganar.
                            # Esta es la segunda parte de la animacion "cargar_pantano_1". 
    ruta = []
    while os.path_exists("~/Programacion/Python/juegoPython/images/pantano_2/" + {i} + ".png"):
        ruta[i] = "~/Programacion/Python/juegoPython/images/pantano_2/" + {i} + ".png"
        fondo = cargar_textura(ruta[i])
    sprites = [cargar_textura(r) for r in ruta]
    
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

def cargar_avion():      # Carga los sprites de animacion de una vioneta que simula atropellar al pato. Quedandose desplumado y empezando a caer (inicio del juego).
                                # Esta animacion solo ocurre al principio del juego y no se vuelve a repetir.
    ruta_mc = []
    for i in range(1, 170):
        ruta = "~/Programacion/Python/juegoPython/images/avion/" + {i} + ".png"
        ruta_avion[i] = ruta
        fondo = cargar_textura(ruta_avion[i])
    # Hay 169 imagenes en .../images/avion que se llaman 1.png, 2.png, 3.png y asi hasta 169.png
    sprites = [cargar_textura(r) for r in ruta_avion]
    
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

def cargar_globo_a():      # Carga los sprites de animacion del un globo aerostatico, este objeto le hara danio al pato.
    # Hay 98 imagenes en .../images/globo_a que se llaman 1.png, 2.png, 3.png y asi hasta 98.png
    i = 1
    while os.path.exists("~/Programacion/Python/juegoPython/images/globo_a/" + {i} + ".png"):
        ruta[i] = "~/Programacion/Python/juegoPython/images/globo_a/" + {i} + ".png" 
        fondo = cargar_textura(ruta[i])
        i += 1

    sprites = [cargar_textura(r) for r in ruta]
    
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

def cargar_globo_m():      # Carga los sprites de animacion del un globo metorologico, este objeto le hara danio al pato.
    # Hay 40 imagenes en .../images/globo_m que se llaman 1.png, 2.png, 3.png y asi hasta 40.png
    i = 1
    while os.path.exists("~/Programacion/Python/juegoPython/images/globo_m/" + {i} + ".png"):
        ruta[i] = "~/Programacion/Python/juegoPython/images/globo_m/" + {i} + ".png" 
        fondo = cargar_textura(ruta[i])
        i += 1

    sprites = [cargar_textura(r) for r in ruta]
    
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

def cargar_power1():      # Carga los sprites de animacion de una llama azul.
    # Hay 5 imagenes en .../images/power_azul que se llaman 1.png, 2.png, 3.png y asi hasta 5.png
    i = 1
    while os.path.exists("~/Programacion/Python/juegoPython/images/power_azul/" + {i} + ".png"):
        ruta[i] = "~/Programacion/Python/juegoPython/images/power_azul/" + {i} + ".png" 
        fondo = cargar_textura(ruta[i])
        i += 1

    sprites = [cargar_textura(r) for r in ruta]
    
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

def cargar_power2():      # Carga los sprites de animacion de una llama purpura/morada.
    # Hay 5 imagenes en .../images/power_morado que se llaman 1.png, 2.png, 3.png y asi hasta 5.png
    i = 1
    while os.path.exists("~/Programacion/Python/juegoPython/images/power_morado/" + {i} + ".png"):
        ruta[i] = "~/Programacion/Python/juegoPython/images/power_morado/" + {i} + ".png" 
        fondo = cargar_textura(ruta[i])
        i += 1

    sprites = [cargar_textura(r) for r in ruta]
    
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

def cargar_power3():      # Carga los sprites de animacion de una llama rojo.
    # Hay 5 imagenes en .../images/power_rojo que se llaman 1.png, 2.png, 3.png y asi hasta 5.png
    i = 1
    while os.path.exists("~/Programacion/Python/juegoPython/images/power_rojo/" + {i} + ".png"):
        ruta[i] = "~/Programacion/Python/juegoPython/images/power_rojo/" + {i} + ".png" 
        fondo = cargar_textura(ruta[i])
        i += 1

    sprites = [cargar_textura(r) for r in ruta]
    
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

def dibujar_escena():
    """
    Función de dibujo de la escena de OpenGL. Utiliza glBegin/glEnd.
    """
    # Establecer el color de fondo (negro)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(-0.2, 0.2)
    glVertex2f( 0.2, 0.2)
    glVertex2f( 0.2, -0.2)
    glVertex2f(-0.2, -0.2)
    glEnd()

def dibujar_poligono(x, y, w, h):
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(x - w, y - h)
    glTexCoord2f(1, 0); glVertex2f(x + w, y - h)
    glTexCoord2f(1, 1); glVertex2f(x + w, y + h)
    glTexCoord2f(0, 1); glVertex2f(x - w, y + h)
    glEnd()

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

# Esto lo debe de llevar ?????
def programa_principal():

    # Inicializar Pygame Mixer y cargar el sonido
    inicializar_pygame_sonido()

    # Inicializar GLFW y crear la ventana
    try:
        ventana = iniciar_ventana()
    except Exception as e:
        print(f"Error fatal al iniciar la ventana: {e}")
        pygame.mixer.quit()
        return

    # Registrar la función de callback de teclado
    glfw.set_key_callback(ventana, key_callback)

    # Bucle principal de renderizado
    while not glfw.window_should_close(ventana):

        # Dibujar la escena
        # dibujar_escena()

        # Intercambiar búferes para mostrar el resultado
        glfw.swap_buffers(ventana)

        # Procesar eventos (teclado, ratón, etc.)
        glfw.poll_events()

    # Terminar GLFW y Pygame Mixer
    pygame.mixer.quit()
    glfw.terminate()




















