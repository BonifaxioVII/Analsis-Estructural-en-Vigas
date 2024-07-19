Analisis estructural sobre una viga. 

Este es un proyecto en Python en desarrollo que inicié hace 3 años en mi tercer semestre estudiante ingeniería mecánica. Es capaz de calcular y simular el comportamiento de una barra de cualquier tipo bajo distintas cargas y momentos. 
El proyecto consta de tres scripts. 
- El primero 'CDist20.py' corre la interfaz de usuario del proyecto y agrupa el contenido de los codigos restantes.
- El archivo 'Funciones.py' personaliza la interfaz de acuerdo a la elección de procedimiento del cliente en 'CDist20.py' y da lugar a la ejecución del procedimiento en 'Metodos.py'
- 'Metodos.py' desarrolla cada uno de los procedimientos. La creación y presentación de diagramas e imagenes y la simulación de cargas y momentos en la barra.
Cabe resaltar que no se hace uso de una interfaz normal, si no que se emplea la consola de Python para mostrar resultados e interactuar con el usuario.

A pesar del funcionamiento aparentemente normal y correcto del programa, se presentan los siguientes defectos:
1. Se desconocen los errores que podría presentar y la precisión de la simulación.
2. A pesar de que se usaron métodos de diferencias finitas para la resolución del problema, no se tiene claro como fueron solucionadas.
3. La interacción con el usuario es bruzca y posiblemente abierta a errores.
4. El programa no está optimizado.
5. El programa es bastante restrictivo.
  - No se tiene en cuenta la forma de la sección transversal
  - No se tiene en cuenta las dimensiones de la sección transversal.
  - No se permiten cargas que no sean verticales.
  - No todo tipo de carga ni momento son permitidos.
  - No aporta información sobre la deflexión de la viga.
  - No realiza un analisis de fallas.

Cabe resaltar que este proyecto lo desarrollé en mis primeros años programando producto de la necesidad de un programa gratis que solucione todo (o casi todo) ejercicio de analisis estructural en vigas.
Por tal motivo, es un proyecto que no es robuzto y deberá mejorar en varios aspectos.

Se deberá realizar lo sigueinte:
1. Documentar el método usado para desarrollar el análisis estructural en busca de errores y cosas para mejorar.
2. Desarrollar una interfaz para el usuario.
3. Añadir información de interes al analisis estructural.
4. Permitir  
