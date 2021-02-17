# Importamos las librerías necesarias:
from argparse import ArgumentParser  # Paquete utilizado para definir y parsear los parámetros de entrada.

import cv2

# Definimos los parámetros de entrada (obligatorios).
argument_parser = ArgumentParser()
argument_parser.add_argument('-s', '--source', required=True, type=str, help='Ruta a la imagen fuente.')
argument_parser.add_argument('-t', '--template', required=True, type=str, help='Ruta a la imagen plantilla.')
arguments = vars(argument_parser.parse_args())

# Cargamos tanto la imagen fuente y la plantilla en memoria.
source = cv2.imread(arguments['source'])
template = cv2.imread(arguments['template'])

# Extraemos las dimensiones de la plantilla, las cuales usaremos en breve para dibujar el rectángulo de la coincidencia
# o "match"
template_height, template_width = template.shape[:2]

# La función *cv2.matchTemplate* busca coincidencias de la plantilla en la imagen fuente. Como parámetros de entrada,
# recibe:
#
# - La imagen fuente.
# - La imagen plantilla.
# - Una constante para especificar el tipo de algoritmo para cuantificar la coincidencia entre una región de la imagen
#   y la plantilla.
#
# La estructura del **result** es una matriz donde cada ubicación o celda (x, y) contiene el valor de la métrica que
# computa cuán "buena" o "mala" es la coincidencia. Tal valor es calculado por el método asociado a cv2.TM_CCOEFF.
result = cv2.matchTemplate(source, template, cv2.TM_CCOEFF)

# Pasamos la matriz de resultados al método *cv2.minMaxLoc* para obtener:
# - El mínimo valor en la matriz.
# - El máximo valor en la matriz.
# - La ubicación (x, y) del valor mínimo.
# - La ubicación (x, y) del valor máximo.
min_value, max_value, min_location, max_location = cv2.minMaxLoc(result)
(x_max, y_max) = max_location

# Dibujamos un recuadro alrededor de la mejor coincidencia en la imagen fuente.
blue = (255, 0, 0)
cv2.rectangle(source, (x_max, y_max), (x_max + template_width, y_max + template_height), blue, 2)

# Mostramos las imágenes.
cv2.imshow('Fuente', source)
cv2.imshow('Plantilla', template)
cv2.waitKey(0)
