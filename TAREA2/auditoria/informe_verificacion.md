# Informe de verificación de TAREA2

Autor: Jason Chambe. Edición: 6 de septiembre de 2026.

## Contenido y procedencia

Se adaptaron los ocho escenarios de `Muestra.qmd`, de Antonio M. Quispe, a 24 variantes prácticas. El tutorial desarrolla nueve variantes centrales y las quince restantes en anexo. La práctica mantiene además las preguntas originales de muestra, potencia y efecto detectable y sustituye el gráfico de un punto por una curva de potencia.

Teoría 01 y 02 fundamentan el diseño de cada variante de forma breve. Teoría 03 y el QMD aportan el enfoque de clase. Se verificaron los métodos con documentación de R, pwr y pwr2. Las páginas de procedencia están identificadas en el tutorial y sus archivos originales se registran mediante SHA-256 en `referencias/procedencia.json`.

## Cálculos

Las 24 variantes alcanzan la potencia planificada con el tamaño entero reportado. En todas, restar una persona por grupo, par o celda deja la potencia por debajo del objetivo. Se redondea antes de obtener el total. Se comprobaron signos y escalas de los efectos, la equivalencia entre las dos parametrizaciones del ANOVA de una vía y los grados de libertad del ANOVA factorial aditivo.

El alcance es numérico y condicionado a los modelos: las aproximaciones de arcoseno no se presentan como pruebas binomiales exactas; el factorial no se presenta como cálculo de interacción o potencia conjunta. No se infiere causalidad de la potencia ni se consideran pérdidas o conglomerados sin parámetros para hacerlo.

## Reproducción

R 4.6.1, pwr 1.3-0 y pwr2 1.0. Quarto 1.9.38. MacTeX/TeX Live 2026. Los dos QMD ejecutaron todos sus bloques de cálculo y sus comprobaciones de tamaños enteros. Se guardaron versiones HTML con sus recursos incorporados.

Se intentó inicialmente usar Strive PDF Generator. Su generación omitió contenido y las compilaciones posteriores presentaron fallos. El usuario autorizó expresamente continuar con el LaTeX local de su Mac. Los PDF finales se compilaron localmente y no proceden de la versión incompleta de Strive.

## Revisión visual y de archivos

El tutorial tiene 33 páginas y conserva las 24 variantes. El carrusel tiene 20 páginas con proporción 16:9. Sus 20 PNG tienen 1920 × 1080 píxeles y se renderizaron directamente desde el PDF. Se revisaron todas las páginas en vistas de conjunto y se ampliaron páginas representativas de código, tablas y fuentes. Los registros finales de LaTeX no muestran cajas desbordadas.

El PDF de la publicación reúne el texto propuesto con las 20 láminas. Es un material listo para compartir; no constituye evidencia de que se haya publicado en LinkedIn.

## Precisiones documentadas

Se distingue tamaño del efecto de efecto de diseño. Se corrige la relación entre variabilidad y muestra. Se explicita DE común en dos medias y DE de diferencias en el caso pareado. Se distingue f convencional de f derivado de medias. Se conserva la diferencia entre los parámetros del QMD y los de las diapositivas cuando no coinciden. Se aclara n por grupo, por pares o por celda y la conversión de proporciones a porcentajes.

Se utilizaron unidades de hemoglobina g/dL de forma explícita en la adaptación, señalando la escritura mg/dL del enunciado anterior. Las referencias fijas y los demás supuestos añadidos se declaran antes de interpretar los resultados.

## Publicación

Destino: `chambejason951-collab/BIOESTADISTICA`, carpeta `TAREA2`. La entrega incluye material elaborado para esta tarea y las referencias; no incluye los PDF originales del profesor, borradores de compilación ni archivos temporales. El estado y el commit de publicación se registran por separado para no confundir preparación local con publicación verificada.
