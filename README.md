# pageRank

Trabajo de PageRank para la materia de Data Mining

## Integrantes

-  **Sebastián Romero** 
- **Juan Calderón**
- **Kristian Mendoza**

## Descripción

El trabajo consiste en implementar el algoritmo de PageRank en un grafo de la web. Para ello se utilizó la librería de NetworkX en Python.
Hay funciones para tener un grafo predefinido y otro para generar un grafo aleatorio al cual se le puede setear los parámetros de cantidad de nodos, de dead ends, y de spider traps.
El metodo del page rank implementa un random walker que se mueve por el grafo y va actualizando el rank de todos los nodos.
El page rank tiene una funcionalidad de teletransportación que permite que el random walker salga de un dead end o de un spider trap.

## Teletransportación
La matriz de adyacencia se modifica para que los nodos que no tienen salida, tengan una probabilidad de teletransportación a todos los nodos del grafo. De esta manera, el random walker puede salir de un dead end o de un spider trap.
La manera en la que se implementa la teletransportación es que se le suma a la matriz de adyacencia una matriz de teletransportación que tiene la misma cantidad de filas y columnas que la matriz de adyacencia. La matriz de teletransportación tiene todos sus valores en 1/n, donde n es la cantidad de nodos del grafo.
La matriz de adjacencia tiene una modificación, que el valor de  cada columna es la probabilidad de salida de cada nodo. 
