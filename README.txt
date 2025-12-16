Cuack!!endo - Proyecto de Graficación

Cuack!!endo es un videojuego de estilo *Arcade* en 2.5D desarrollado en Python. El proyecto demuestra la implementación de primitivas gráficas, manejo de texturas y transformaciones geométricas utilizando la librería OpenGL.

El jugador controla a un pato en caída libre que debe esquivar globos y recolectar *power-ups* para sobrevivir hasta llegar al suelo.

📋 Características Técnicas

Este proyecto fue creado para la materia de Graficación y destaca por:

* Motor Gráfico Híbrido: Uso de **OpenGL (PyOpenGL)** para renderizado en tiempo real.
* Entorno 2.5D: Combinación de *sprites* 2D (personajes) con elementos 3D (Power-ups renderizados como `glutWireCube`).
* Manejo de Texturas: Carga dinámica de animaciones y fondos usando texturas mapeadas en polígonos (`GL_QUADS`).
* Texto como Textura: Implementación de un sistema para convertir fuentes de `pygame` en texturas de OpenGL para el HUD (Vidas y Altitud).
* Máquina de Estados: Control de flujo del juego (Menú, Intro Cinemática, Gameplay, Game Over, Victoria).
* Doble Buffer: Implementación de `glfw.swap_buffers` para animaciones fluidas sin parpadeos.

Requisitos e Instalación

Para ejecutar este juego en tu computadora, necesitas tener instalado **Python 3.x** y las siguientes librerías.

1.  Clonar el repositorio:
    git clone [https://github.com/ar8836/juegoPython.git](https://github.com/ar8836/juegoPython.git)
    cd juegoPython

2.  Instalar dependencias:
    Puedes instalar todas las librerías necesarias con el siguiente comando:
    pip install PyOpenGL PyOpenGL_accelerate glfw pygame

🎮 Controles

| Tecla            |              Acción              |
| Flechas ⬆⬇⬅➡   | Mover al pato en los ejes X e Y  |
| Tecla 'I'        | Iniciar el juego (Desde el Menú) |
| ESC              | Salir del juego                  |

🕹️ Mecánicas de Juego

* Objetivo: Sobrevivir durante 40 segundos (simulando la altitud de caída) sin perder todas las vidas.
* Vidas: Comienzas con 5 vidas. Cada choque con un globo resta 1 vida.
* Power-Up (Escudo): Ocasionalmente aparecerá un **cubo 3D giratorio** (Color Cyan). Al recogerlo, obtienes un escudo temporal que te permite destruir un obstáculo sin recibir daño.

📂 Estructura del Proyecto

* `main.py`: Script principal que contiene el ciclo de juego, lógica de renderizado y manejo de eventos.
* `carga.py`: Módulo auxiliar para la importación y gestión de recursos (imágenes/texturas).
* `/images`: Carpeta que contiene los sprites y frames de animación (Pato, Globos, Cielo, etc.).

🛠️ Tecnologías Utilizadas

* [Python](https://www.python.org/) - Lenguaje principal.
* [PyOpenGL](http://pyopengl.sourceforge.net/) - Wrapper de OpenGL para gráficos.
* [GLFW](https://www.glfw.org/) - Manejo de ventanas e inputs.
* [GLUT](https://freeglut.sourceforge.net/) - Utilidades para geometrías 3D (WireCube).
* [Pygame](https://www.pygame.org/) - Utilizado auxiliarmente para renderizado de texto y manejo de audio.
**Materia:** Graficación
