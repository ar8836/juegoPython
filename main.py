import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time
import random
import pygame
import carga 

# --- CONFIGURACION ---
ANCHO = 800
ALTO = 800

# Estados del juego (Enteros simples)
MENU = 0
INTRO = 1
JUEGO = 2
GANAR = 3
GAME_OVER = 4

estado_actual = MENU
tiempo_inicio_juego = 0
tiempo_inicio_intro = 0
DURACION_META = 40.0 # Segundos para ganar

# --- DATOS GLOBALES (EN LUGAR DE OBJETOS) ---
# Usamos diccionarios para guardar los datos de cada cosa

datos_pato = {
    "x": 0.0, "y": 5.0,
    "w": 2.0, "h": 2.0,
    "frame": 0.0,
    "anim_actual": [], # Aquí guardaremos la lista de texturas
    "vidas": 5,
    "escudo": False
}

datos_avion = {
    "x": -20.0, "y": 10.0,
    "activo": False,
    "texturas": []
}

datos_powerup = {
    "x": 0.0, "y": -20.0,
    "activo": False,
    "giro": 0.0
}

# Listas para guardar texturas cargadas
texturas_cielo = []
texturas_pato_idle = []
texturas_pato_caida = []
texturas_globo_a = []
texturas_globo_m = []
texturas_pantano = []
texturas_power = []

# Lista de obstaculos (diccionarios simples)
lista_obstaculos = [] 

def iniciar_ventana():
    if not glfw.init(): return None
    ventana = glfw.create_window(ANCHO, ALTO, "Cuack!!endo", None, None)
    if not ventana: glfw.terminate(); return None
    glfw.make_context_current(ventana)
    glutInit()
    
    # Configuracion OpenGL
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    # Camara 2D/3D hibrida
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, ANCHO/ALTO, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    
    return ventana

def crear_texto_textura(texto, tamanio=60, color=(255, 255, 255)):
    """Convierte texto a una textura OpenGL usando Pygame"""
    try:
        font = pygame.font.SysFont("Arial", tamanio, True)
        # Renderizar texto a superficie (con fondo transparente)
        superficie = font.render(texto, True, color)
        
        # Convertir a formato que entienda OpenGL
        img_data = pygame.image.tostring(superficie, "RGBA", True)
        w, h = superficie.get_size()
        
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        
        # Filtros necesarios
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        # IMPORTANTE: Devolvemos ID, ancho y alto para saber de que tamaño dibujarlo
        return tex_id, w/50, h/50 # Dividimos entre 50 para escalar a coordenadas del juego
    except Exception as e:
        print(f"Error texto: {e}")
        return None, 0, 0

def cargar_recursos_juego():
    global texturas_cielo, texturas_pato_idle, texturas_pato_caida
    global texturas_globo_a, texturas_globo_m, texturas_pantano, texturas_power
    global datos_avion
    
    carga.inicializar_sonido()
    
    # Usamos la funcion generica de carga.py
    # Asegurate que las carpetas existan en images/
    texturas_cielo = carga.cargar_animacion("cielo", 40)
    texturas_pato_idle = carga.cargar_animacion("pato_acostado", 25)
    texturas_pato_caida = carga.cargar_animacion("pato", 40)
    datos_avion["texturas"] = carga.cargar_animacion("avion", 100)
    texturas_globo_a = carga.cargar_animacion("globo_a", 50)
    texturas_globo_m = carga.cargar_animacion("globo_m", 40)
    texturas_pantano = carga.cargar_animacion("pantano_1", 40)
    texturas_power = carga.cargar_animacion("power_azul", 5)
    
    # Estado inicial pato
    datos_pato["anim_actual"] = texturas_pato_idle

    # Crear obstaculos (pool de 6 globos)
    for _ in range(6):
        obs = {
            "x": 0, "y": -30, 
            "activo": False, 
            "tipo": 0, # 0 = A, 1 = M
            "frame": 0.0
        }
        lista_obstaculos.append(obs)

def dibujar_sprite(x, y, w, h, textura_id, z=0.0): # <--- Agregamos parametro z con valor default 0
    """Dibuja un rectangulo con textura en la posicion X, Y, Z"""
    glBindTexture(GL_TEXTURE_2D, textura_id)
    glColor3f(1,1,1)
    
    # Habilitamos mezcla para transparencia (vital para que no se vea cuadro negro)
    glEnable(GL_BLEND) 
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glBegin(GL_QUADS)
    # Notar que ahora usamos 'z' en el tercer parametro de glVertex3f
    glTexCoord2f(0, 0); glVertex3f(x - w, y - h, z)
    glTexCoord2f(1, 0); glVertex3f(x + w, y - h, z)
    glTexCoord2f(1, 1); glVertex3f(x + w, y + h, z)
    glTexCoord2f(0, 1); glVertex3f(x - w, y + h, z)
    glEnd()
    
    glDisable(GL_BLEND) # Buena practica desactivar al terminar

def dibujar_cubo_wired(x, y, tamanio, giro):
    """Dibuja el powerup 3D"""
    glDisable(GL_TEXTURE_2D) # Desactivar textura para que se vean las lineas
    glPushMatrix()
    glTranslatef(x, y, 0)
    glRotatef(giro, 1, 1, 1)
    glColor3f(0, 1, 1) # Cyan
    glutWireCube(tamanio)
    glColor3f(1, 1, 1)
    glPopMatrix()
    glEnable(GL_TEXTURE_2D)

def detectar_colision(obj1_x, obj1_y, w1, h1, obj2_x, obj2_y, w2, h2):
    """Detecta si dos rectangulos se tocan"""
    hit_x = (obj1_x - w1 < obj2_x + w2) and (obj1_x + w1 > obj2_x - w2)
    hit_y = (obj1_y - h1 < obj2_y + h2) and (obj1_y + h1 > obj2_y - h2)
    return hit_x and hit_y

def actualizar_animacion(lista_tex, frame_actual, velocidad):
    """Avanza el frame y devuelve el nuevo frame y la textura actual"""
    if not lista_tex: return 0, 0
    
    nuevo_frame = frame_actual + velocidad
    if nuevo_frame >= len(lista_tex):
        nuevo_frame = 0 # Loop
        
    idx = int(nuevo_frame)
    return nuevo_frame, lista_tex[idx]

def logica():
    global estado_actual, tiempo_inicio_juego
    
    # Variables globales de texturas de fondo
    frame_cielo = (glfw.get_time() * 10) % len(texturas_cielo) if texturas_cielo else 0
    tex_cielo_actual = texturas_cielo[int(frame_cielo)] if texturas_cielo else 0
    
    # Configurar camara
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(0, 0, 30, 0, 0, 0, 0, 1, 0)
    
    # --- FONDO SIEMPRE ACTIVO (Incluso en Game Over) ---
    if estado_actual != GANAR:
        dibujar_sprite(0, 0, 30, 30, tex_cielo_actual, -10.0) 
    
    # ================= MAQUINA DE ESTADOS =================
    
    if estado_actual == MENU:
        # Pato acostado
        datos_pato["frame"], tex = actualizar_animacion(datos_pato["anim_actual"], datos_pato["frame"], 0.15)
        dibujar_sprite(datos_pato["x"], datos_pato["y"], 2, 2, tex)
        
        # Texto de instruccion
        tex_t, w, h = crear_texto_textura("PRESIONA 'I' PARA INICIAR", 40, (255, 255, 0))
        dibujar_sprite(0, -5, w, h, tex_t, 1.0)
        glDeleteTextures(tex_t) # Limpiar memoria
        
    elif estado_actual == INTRO:
        # (Tu codigo de intro corregido que ya tenias...)
        tiempo_actual = glfw.get_time()
        diferencia = tiempo_actual - tiempo_inicio_intro
        
        dibujar_sprite(0, 5, 2, 2, datos_pato["anim_actual"][0], 0.0)
        
        if datos_avion["texturas"]:
            indice = int((diferencia * 20) % len(datos_avion["texturas"]))
            tex_av = datos_avion["texturas"][indice]
            glDisable(GL_DEPTH_TEST)
            dibujar_sprite(0, 0, 30, 30, tex_av, 0.0)
            glEnable(GL_DEPTH_TEST)

        if diferencia >= 3.0:
            datos_pato["anim_actual"] = texturas_pato_caida
            estado_actual = JUEGO
            tiempo_inicio_juego = glfw.get_time()

    elif estado_actual == JUEGO:
        tiempo_jugado = glfw.get_time() - tiempo_inicio_juego
        tiempo_restante = DURACION_META - tiempo_jugado
        
        # --- 1. DIBUJAR PATO ---
        datos_pato["frame"], tex_pato = actualizar_animacion(datos_pato["anim_actual"], datos_pato["frame"], 0.2)
        dibujar_sprite(datos_pato["x"], datos_pato["y"], 2, 2, tex_pato, 0.0)
        
        # Escudo visual
        if datos_pato["escudo"]:
            f_esc, tex_esc = actualizar_animacion(texturas_power, (glfw.get_time()*10)%5, 0.2)
            dibujar_sprite(datos_pato["x"], datos_pato["y"]+1, 1.5, 1.5, tex_esc, 0.1)

        # --- 2. OBSTACULOS ---
        if random.randint(0, 100) < 4: 
            for obs in lista_obstaculos:
                if not obs["activo"]:
                    obs["activo"] = True
                    obs["x"] = random.uniform(-12, 12)
                    obs["y"] = -25
                    obs["tipo"] = random.randint(0, 1) 
                    break
        
        for obs in lista_obstaculos:
            if obs["activo"]:
                obs["y"] += 0.15 
                lista_tex = texturas_globo_a if obs["tipo"]==0 else texturas_globo_m
                obs["frame"], tex_obs = actualizar_animacion(lista_tex, obs["frame"], 0.1)
                dibujar_sprite(obs["x"], obs["y"], 2, 2, tex_obs, 0.0)
                
                # Colision
                if detectar_colision(datos_pato["x"], datos_pato["y"], 1.5, 1.5, obs["x"], obs["y"], 1.5, 1.5):
                    if datos_pato["escudo"]:
                        obs["activo"] = False 
                        datos_pato["escudo"] = False 
                    else:
                        print("Golpe!")
                        obs["activo"] = False
                        datos_pato["vidas"] -= 1
                
                if obs["y"] > 20: obs["activo"] = False 
        
        # --- 3. POWERUP 3D ---
        if not datos_powerup["activo"] and random.randint(0, 300) < 2:
            datos_powerup["activo"] = True
            datos_powerup["x"] = random.uniform(-10, 10)
            datos_powerup["y"] = -20
            
        if datos_powerup["activo"]:
            datos_powerup["y"] += 0.15
            datos_powerup["giro"] += 2
            dibujar_cubo_wired(datos_powerup["x"], datos_powerup["y"], 2.0, datos_powerup["giro"])
            
            if detectar_colision(datos_pato["x"], datos_pato["y"], 2, 2, datos_powerup["x"], datos_powerup["y"], 1, 1):
                datos_pato["escudo"] = True
                datos_powerup["activo"] = False
            
            if datos_powerup["y"] > 20: datos_powerup["activo"] = False

        # --- 4. HUD (TEXTO EN PANTALLA) ---
        # Contador de Altitud / Tiempo
        texto_altitud = f"ALTITUD: {int(tiempo_restante * 100)} mts"
        tex_hud, w, h = crear_texto_textura(texto_altitud, 40, (0, 255, 255))
        # Dibujamos arriba a la izquierda
        dibujar_sprite(-8, 9, w, h, tex_hud, 5.0) 
        glDeleteTextures(tex_hud) # Borrar textura para no llenar la RAM

        # Vidas
        texto_vidas = f"VIDAS: {datos_pato['vidas']}"
        tex_vid, w, h = crear_texto_textura(texto_vidas, 40, (255, 0, 0))
        dibujar_sprite(8, 9, w, h, tex_vid, 5.0)
        glDeleteTextures(tex_vid)

        # --- 5. CAMBIOS DE ESTADO ---
        if tiempo_restante <= 0:
            estado_actual = GANAR
            
        if datos_pato["vidas"] <= 0:
            estado_actual = GAME_OVER

    elif estado_actual == GAME_OVER:
        # El fondo se sigue moviendo (ya esta dibujado arriba)
        # Dibujamos letrero gigante
        tex_go, w, h = crear_texto_textura("GAME OVER", 80, (255, 0, 0))
        dibujar_sprite(0, 0, w, h, tex_go, 5.0)
        glDeleteTextures(tex_go)
        
        # Opcional: Instruccion de salir
        tex_esc, w, h = crear_texto_textura("Presiona ESC para salir", 40, (255, 255, 255))
        dibujar_sprite(0, -3, w, h, tex_esc, 5.0)
        glDeleteTextures(tex_esc)

    elif estado_actual == GANAR:
        # Fondo de Pantano
        f_pan, tex_pan = actualizar_animacion(texturas_pantano, (glfw.get_time()*5)%len(texturas_pantano), 0.1)
        dibujar_sprite(0, 0, 15, 15, tex_pan, -5.0)
        
        # Letrero YOU WIN
        tex_win, w, h = crear_texto_textura("YOU WIN!", 100, (0, 255, 0))
        dibujar_sprite(0, 0, w, h, tex_win, 5.0)
        glDeleteTextures(tex_win)

def teclado(window, key, scancode, action, mods):
    global estado_actual, tiempo_inicio_intro
    
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)
            
        # Iniciar Intro
        if key == glfw.KEY_I and estado_actual == MENU:
            estado_actual = INTRO
            tiempo_inicio_intro = glfw.get_time()
            datos_avion["activo"] = True
            print("Iniciando intro...")
            
        # --- MOVIMIENTO DEL PATO CON LIMITES ---
        vel = 1.5
        LIMITE_X = 10.0  # Limite horizontal
        LIMITE_Y = 10.0  # Limite vertical

        if estado_actual == JUEGO:
            # Derecha (Solo si X es menor que el limite derecho)
            if key == glfw.KEY_RIGHT and datos_pato["x"] < LIMITE_X: 
                datos_pato["x"] += vel
            
            # Izquierda (Solo si X es mayor que el limite izquierdo)
            if key == glfw.KEY_LEFT and datos_pato["x"] > -LIMITE_X: 
                datos_pato["x"] -= vel
            
            # Arriba (Solo si Y es menor que el limite superior)
            if key == glfw.KEY_UP and datos_pato["y"] < LIMITE_Y: 
                datos_pato["y"] += vel
            
            # Abajo (Solo si Y es mayor que el limite inferior)
            if key == glfw.KEY_DOWN and datos_pato["y"] > -LIMITE_Y: 
                datos_pato["y"] -= vel

def programa_principal():
    pygame.init()
    pygame.font.init()
    ventana = iniciar_ventana()
    if not ventana: return
    
    try:
        cargar_recursos_juego()
    except Exception as e:
        print(f"Error cargando recursos: {e}")
        print("Revisa que tus carpetas (pato, cielo, etc) tengan imagenes 1.png, 2.png...")
        return

    glfw.set_key_callback(ventana, teclado)
    
    while not glfw.window_should_close(ventana):
        logica()
        glfw.swap_buffers(ventana)
        glfw.poll_events()
        # Pequeña pausa para no quemar el CPU
        time.sleep(0.01)
        
    glfw.terminate()

if __name__ == "__main__":
    programa_principal()
