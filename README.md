# MCOC2020-P3-E7

Si bien se logró simular de buena manera los efectos de la temperatura en los ejes centrales del bloque de hormigón, no se pudo simular la temperatura en los sensoreas, ya que por la complejidad del código este no generaba las imagenes de manera rápida. Además, debido a problemas de conexión con el cluster, no se pudo correr el código en su totalidad para obtener los gráficos correctos.

Para que los costos computacionales no fueran tan altos, ya que el problema se resolvería en los 3 ejes al mismo tiempo, se consideró separar en 3 planos (xy, yz, xz) para aprovechar el código de la entrega 5. Como se puede notar en las siguientes imágenes, a medida que pasa el tiempo, el hormigón va generando calor, pero también la parte superior se va viendo afectada por la temperatura ambiente. Esta última, al ir variando no tiene mayor incidencia en el fondo del bloque. 
Se comprueba que ambos planos expuestos tienden a descender más rápido su temperatura, mientras el otro (ubicado en el corte central) solo aumenta.

### Caso xy (ubicado en el corte central)
![](caso_xy.gif) 

### Caso xz
![](caso_xz.gif)

### Caso yz
![](caso_yz.gif)
