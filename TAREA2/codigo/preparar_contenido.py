"""Contenido original de la adaptación; no genera LaTeX ni PDF.
Lee resultados de R y conserva una sola fuente de cifras para los documentos.
"""
from pathlib import Path
import csv, json

ROOT = Path(__file__).resolve().parents[1]
res = {r['id']: r for r in csv.DictReader((ROOT/'resultados/resultados_verificados.csv').open())}
def num(x, k=2): return f'{float(x):.{k}f}'.replace('.', ',')

casos = []
def caso(id, titulo, enunciado, fundamento, hipotesis, formula, calculo, codigo, lectura, pregunta, respuesta):
    r=res[id]
    n=int(r['n']); total=int(r['N_total']); unit=r['unidad']
    final=f"Se requieren {n} {unit}"
    if int(r['grupos'])>1: final+=f", equivalentes a {total} participantes en total"
    if unit=='pares completos': final+=f", es decir, {n} personas con dos mediciones cada una"
    final+='.'
    if id.startswith('E8'):
        raw=f"La búsqueda entera devuelve n = {n} por celda."
    else:
        raw=f"R devuelve n = {num(r['n_sin_redondear'],6)}; al redondear hacia arriba obtenemos {n}."
    verificacion=f"Con n = {n}, la potencia calculada es {num(float(r['potencia_con_n'])*100)} %. Con n = {n-1}, es {num(float(r['potencia_con_n_menos_1'])*100)} %, por debajo del objetivo de {num(float(r['potencia_objetivo'])*100,0)} %. Esta comprobación corresponde al método utilizado."
    casos.append(dict(id=id,titulo=titulo,enunciado=enunciado,fundamento=fundamento,
      hipotesis=hipotesis,formula=formula,calculo=calculo,codigo=codigo,
      resultado=raw+' '+final,lectura=lectura,pregunta=pregunta,respuesta=respuesta,
      verificacion=verificacion,datos=r))

fund1="Evaluamos una media de hemoglobina posterior frente a un valor de referencia fijado en 10 g/dL. Por eso corresponde una t de una muestra. Teoría 01 pide definir población y unidad de análisis; Teoría 02 recuerda que una comparación con referencia histórica, sin control simultáneo, no permite atribuir todo el cambio a la intervención. Aquí 10 se considera fijo: si fuera una media basal estimada en estos mismos niños, habría que plantear un cálculo pareado. [1, pp. 7 y 29; 2, pp. 9 y 11; 3, pp. 30 y 31]"
fund2="Calculamos la muestra de una evaluación de prevalencia posterior en Juliaca, comparada con una referencia fija de 40 %. El desenlace de cada niño es binario y se mide una vez para este cálculo. Teoría 01 fundamenta la medición de prevalencia; Teoría 02 ayuda a reconocer que una comparación histórica puede confundirse con cambios ajenos al programa. Si se siguiera a los mismos niños antes y después, necesitaríamos las probabilidades de cambio entre estados. [1, pp. 47 y 50; 2, pp. 9 y 11; 3, pp. 32 y 33]"
fund3="Comparamos dos grupos distintos de niños, uno de cada distrito, mediante una medición transversal. Nadie pertenece a ambos grupos y no se asigna una intervención. Según Teoría 01, esta comparación es observacional y estima prevalencias; Teoría 02 permite distinguirla de un ensayo aleatorizado. Se planifica igual cantidad de niños por distrito y observaciones independientes. [1, pp. 29 y 47; 2, p. 7; 3, pp. 36 y 37]"

for v,mu,alt,label in [('A',14,'two.sided','Comparación bilateral'),('B',14,'greater','Hipótesis de incremento'),('C',11,'two.sided','Un incremento menor')]:
    d=mu-10
    code=f'''library(pwr)
media_referencia <- 10
media_esperada <- {mu}
de_esperada <- 1
d <- (media_esperada - media_referencia) / de_esperada
calculo <- pwr.t.test(d = d, sig.level = 0.05,
  power = 0.80, type = "one.sample",
  alternative = "{alt}")
calculo$n
ceiling(calculo$n)'''
    hyp=r'$H_0: \mu=10$ frente a $H_A: \mu\ne10$.' if v!='B' else r'$H_0: \mu\le10$ frente a $H_A: \mu>10$. El cálculo usa el límite nulo de 10.'
    read={
      'A':"El resultado pequeño se explica por d = 4: la diferencia esperada equivale a cuatro desviaciones estándar. Es una respuesta matemática bajo una normalidad y variabilidad supuestas muy exigentes para una muestra de tres. No constituye, por sí sola, una recomendación suficiente para ejecutar un estudio clínico. Las observaciones deben ser independientes y la DE de planificación debe estar fundamentada.",
      'B':"La alternativa unilateral se justifica porque la pregunta se definió previamente como incremento. El n sin redondear disminuye respecto de A, pero ambos cálculos terminan en tres niños. Una menor exigencia numérica no implica que siempre cambie el entero final. La dirección no debe elegirse después de observar resultados.",
      'C':"Al esperar un aumento de solo 1 g/dL, el efecto estandarizado baja de 4 a 1. Con la misma DE, alfa y potencia, se necesitan diez niños: una diferencia menor cuesta más distinguir del ruido. El valor de 11 es una variante didáctica y no una predicción clínica."}[v]
    q={ 'A':('¿Por qué no multiplicamos n por dos?','Porque solo se toma una muestra nueva; el valor de 10 g/dL se trata como referencia fija.'),
        'B':('¿La palabra incremento obliga siempre a usar una cola?','Hay que establecer la hipótesis antes del estudio. Aquí la variante especifica formalmente una alternativa unilateral; el caso A conserva la convención bilateral de clase.'),
        'C':('¿Por qué aumenta n si la DE no cambió?','Porque disminuyó la diferencia relevante y, por tanto, d. Se necesita más información para detectarla.') }[v]
    caso('E1'+v,label,f"En niños de Puno se espera una media posterior de {mu} g/dL, frente a una referencia fija de 10 g/dL, con DE esperada de 1 g/dL. Calcule n con alfa de 0,05, potencia de 80 % y prueba {'unilateral de incremento' if v=='B' else 'bilateral'}. En esta adaptación se explicitan unidades g/dL; el enunciado previo decía mg/dL. El cociente d se conserva si media y DE usan coherentemente la misma escala.",fund1,hyp,
      r'$d=(\mu_1-\mu_0)/\sigma$',f"d = ({mu} − 10) / 1 = {d}.",code,read,*q)

for v,p1,alt,label in [('A',.20,'two.sided','Comparación bilateral con 40 %'),('B',.20,'less','Una disminución definida antes'),('C',.30,'two.sided','Detectar una reducción menor')]:
    code=f'''library(pwr)
p_referencia <- 0.40
p_esperada <- {p1:.2f}
h <- ES.h(p_esperada, p_referencia)
calculo <- pwr.p.test(h = h, sig.level = 0.05,
  power = 0.80, alternative = "{alt}")
h
calculo$n
ceiling(calculo$n)'''
    hyp=r'$H_0:p=0{,}40$ frente a $H_A:p\ne0{,}40$.' if v!='B' else r'$H_0:p\ge0{,}40$ frente a $H_A:p<0{,}40$. El cálculo usa el límite nulo de 0,40.'
    read={
      'A':"La reducción esperada es de 20 puntos porcentuales, equivalente a 50 % en términos relativos. El resultado corresponde a una muestra, pues la referencia no aporta incertidumbre muestral en este planteamiento. pwr utiliza una aproximación basada en la transformación arcoseno; una prueba binomial exacta puede requerir otra muestra.",
      'B':"Al concentrar el rechazo en la dirección de disminución, el cálculo exige 32 niños en lugar de 41. h debe conservar su signo negativo y acompañarse de alternative = \"less\". Esta elección solo es válida si la hipótesis direccional quedó establecida antes de recoger los datos.",
      'C':"La diferencia se reduce a 10 puntos porcentuales y el valor absoluto de h baja. El cálculo aumenta a 178 niños, aunque se mantiene la misma potencia. No basta con decir que se quiere disminuir la anemia: la magnitud de disminución que interesa detectar determina el esfuerzo de muestreo."}[v]
    q={ 'A':('¿Podemos llamar pareado a este cálculo porque dice luego de una intervención?','No. Para un diseño pareado deben observarse los mismos niños y conocerse las probabilidades de pares discordantes; aquí se fijó una referencia externa.'),
        'B':('¿Por qué h es negativo?','Porque calculamos proporción esperada menos referencia en la escala arcoseno, y 0,20 es menor que 0,40.'),
        'C':('¿Se trata de estimar una prevalencia con margen de error?','No. Se planifica un contraste con potencia para una alternativa concreta; no se ha fijado una precisión de intervalo.') }[v]
    caso('E2'+v,label,f"En Juliaca se espera reducir la prevalencia de anemia de una referencia fija de 40 % a {int(p1*100)} %. Calcule n con alfa de 0,05, potencia de 80 % y alternativa {'unilateral de disminución' if v=='B' else 'bilateral'}.",fund2,hyp,
      r'$h=2\arcsin\sqrt{p_1}-2\arcsin\sqrt{p_0}$',f"h = 2 asin(√{num(p1)}) − 2 asin(√0,40) = {num(res['E2'+v]['efecto'],6)}. Las proporciones se ingresan entre 0 y 1 y el arcoseno se calcula en radianes.",code,read,*q)

for v,p2,power,label in [('A',.26,.80,'Dos distritos, una muestra por distrito'),('B',.26,.90,'Exigir 90 % de potencia'),('C',.33,.80,'Prevalencias más cercanas')]:
    code=f'''library(pwr)
p_sjl <- 0.43
p_vmt <- {p2:.2f}
h <- ES.h(p_sjl, p_vmt)
calculo <- pwr.2p.test(h = h, sig.level = 0.05,
  power = {power:.2f}, alternative = "two.sided")
n_por_distrito <- ceiling(calculo$n)
calculo$n
c(por_distrito = n_por_distrito,
  total = 2 * n_por_distrito)'''
    q={ 'A':('¿Por qué no reportamos 121 como total?','Porque pwr.2p.test devuelve n por muestra. Son dos distritos y cada uno requiere 121 niños.'),
        'B':('¿90 % de potencia significa 90 % de probabilidad de que exista una diferencia?','No. Es la probabilidad de rechazar H0 si la diferencia supuesta y el modelo fueran correctos al repetir el estudio.'),
        'C':('¿La diferencia observada demostraría que vivir en un distrito causa anemia?','No. La comparación es observacional y puede estar afectada por selección, medición y confusión.') }[v]
    read={
      'A':"Las prevalencias esperadas difieren en 17 puntos porcentuales. El resultado es 121 niños en cada distrito, 242 en total. La asignación 1:1 es un supuesto explícito; si se muestrea por colegios, hogares o centros, la independencia individual puede fallar y habría que ajustar el diseño.",
      'B':"Mantener las prevalencias y elevar la potencia a 90 % exige 162 niños por distrito. Se busca reducir la probabilidad de no detectar la diferencia prevista, de 20 % a 10 %, bajo el modelo. La potencia no expresa la probabilidad de que H0 sea falsa.",
      'C':"Con 43 % frente a 33 %, la diferencia es de 10 puntos porcentuales y se requieren 369 niños por distrito. El aumento frente al caso A muestra que poblaciones más parecidas necesitan muestras mayores para distinguir sus prevalencias."}[v]
    caso('E4'+v,label,f"Compare la prevalencia esperada de anemia en San Juan de Lurigancho, 43 %, y Villa María del Triunfo, {int(p2*100)} %. Planifique dos muestras independientes de igual tamaño, alfa de 0,05, potencia de {int(power*100)} % y contraste bilateral.",fund3,
      r'$H_0:p_{SJL}=p_{VMT}$ frente a $H_A:p_{SJL}\ne p_{VMT}$.',
      r'$h=2\arcsin\sqrt{p_{SJL}}-2\arcsin\sqrt{p_{VMT}}$',
      f"h = 2 asin(√0,43) − 2 asin(√{num(p2)}) = {num(res['E4'+v]['efecto'],6)}. Se calcula n por distrito y luego N = 2n.",code,read,*q)

for v,sd,power,label in [('A',1,.80,'Dos medias con DE común'),('B',1,.90,'Más potencia para la misma diferencia'),('C',2,.80,'Mayor variabilidad entre niños')]:
    caso('E3'+v,label,f"Un ensayo paralelo compara una estrategia nutricional con su comparador. Se esperan medias de hemoglobina de 12,5 y 12 g/dL, DE común de {sd} g/dL, alfa de 0,05 y potencia de {int(power*100)} %. Calcule n por grupo para una prueba bilateral.",
      "El protocolo asigna estrategias a dos grupos de niños diferentes. Se plantea aleatorización individual, tal como el esquema de ensayo de Teoría 02; las observaciones son independientes entre grupos. Teoría 01 recuerda que el tamaño muestral y la validez de la comparación son asuntos relacionados pero distintos. Para este ejercicio se supone una DE común, coherente con pwr.t.test. [1, pp. 7 y 9; 2, pp. 12 y 14; 3, pp. 34 y 35]",
      r'$H_0:\mu_I=\mu_C$ frente a $H_A:\mu_I\ne\mu_C$.',
      r'$d=(\mu_I-\mu_C)/\sigma$',f"d = (12,5 − 12) / {sd} = {num(.5/sd)}.",
      f'''library(pwr)
d <- (12.5 - 12) / {sd}
calculo <- pwr.t.test(d = d, sig.level = 0.05,
  power = {power:.2f}, type = "two.sample",
  alternative = "two.sided")
calculo$n
c(por_grupo = ceiling(calculo$n),
  total = 2 * ceiling(calculo$n))''',
      {'A':"El resultado se expresa por grupo. El valor d = 0,5 reproduce el efecto de referencia usado en clase, pero aquí proviene de una diferencia y una DE explícitas. No se está implementando una prueba de Welch para varianzas desiguales.",
       'B':"La muestra aumenta porque se exige detectar el mismo efecto con mayor frecuencia en repeticiones hipotéticas del estudio. La mayor potencia no compensa pérdidas selectivas ni errores de medición.",
       'C':"Duplicar la DE, conservando la diferencia de medias, reduce d a la mitad. La muestra aumenta considerablemente. Este caso permite corregir la idea de que una mayor variabilidad exigiría una muestra menor."}[v],
      '¿Basta con conocer dos desviaciones estándar para calcular n?',
      'También se necesita una diferencia relevante, alfa, potencia, dirección y diseño. Si las varianzas son desiguales, este modelo común debe revisarse.')

for v,sd,alt,label in [('A',1,'two.sided','Cada niño actúa como su propia comparación'),('B',2,'two.sided','Diferencias individuales más variables'),('C',1,'greater','Incremento en datos pareados')]:
    caso('E5'+v,label,f"Se medirá hemoglobina antes y después en los mismos niños. Se espera un cambio medio de 1 g/dL y una DE de las diferencias de {sd} g/dL. Calcule el número de pares completos con alfa de 0,05, potencia de 80 % y alternativa {'unilateral de incremento' if v=='C' else 'bilateral'}.",
      "Las dos mediciones pertenecen a la misma persona; el dato analizado es su diferencia posterior menos basal. Por eso la prueba es pareada. Un antes y después sin control, discutido en Teoría 02, sigue expuesto a historia y maduración: el pareamiento estadístico no elimina esas amenazas. [1, pp. 7 y 16; 2, pp. 9 y 11; 3, pp. 38 y 39]",
      r'$H_0:\mu_D=0$ frente a $H_A:\mu_D\ne0$.' if v!='C' else r'$H_0:\mu_D\le0$ frente a $H_A:\mu_D>0$.',
      r'$d_z=\mu_D/\sigma_D$',f"d_z = 1 / {sd} = {num(1/sd)}. Si solo tuviéramos las DE basal y final, necesitaríamos además su correlación para calcular la DE de las diferencias.",
      f'''library(pwr)
de_diferencias <- {sd}
dz <- 1 / de_diferencias
calculo <- pwr.t.test(d = dz, sig.level = 0.05,
  power = 0.80, type = "paired",
  alternative = "{alt}")
calculo$n
ceiling(calculo$n)''',
      {'A':"Diez pares completos equivalen a diez niños medidos dos veces, no a veinte participantes. La función usa la misma matemática que una t de una muestra aplicada a las diferencias.",
       'B':"Una DE de diferencias mayor reduce el efecto estandarizado y eleva el número de pares. No debemos sustituir la DE de las diferencias por la DE basal o final sin justificación.",
       'C':"El cálculo unilateral exige ocho pares bajo estos supuestos. Deben contarse pares completos: una medición aislada no aporta un cambio individual para este análisis."}[v],
      '¿DE basal igual a DE final implica conocer la DE del cambio?',
      r'No. $\sigma_D=\sqrt{\sigma_{antes}^2+\sigma_{despues}^2-2\rho\sigma_{antes}\sigma_{despues}}$. Falta la correlación $\rho$.')

for v,power,label in [('A',.80,'Un efecto global de referencia'),('B',.90,'Más potencia para el contraste global'),('C',.80,'Calcular f desde las medias')]:
    efe='0.25' if v!='C' else 'sqrt(mean((c(50, 60, 70) - 60)^2)) / 30'
    caso('E6'+v,label,
      f"Un estudio compara tres estrategias educativas mediante un puntaje continuo. Planifique grupos iguales, alfa de 0,05 y potencia de {int(power*100)} %. "+('Use f = 0,25 como supuesto de planificación.' if v!='C' else 'Se esperan medias de 50, 60 y 70 puntos y una DE intragrupo de 30 puntos. Calcule f a partir de ellas.'),
      "Hay tres grupos independientes y se evalúa si todas sus medias son iguales. Teoría 02 permite plantearlo como ensayo paralelo si las estrategias se asignan al azar; Teoría 01 exige definir qué se mide y a quién. Se suponen errores normales con varianza común. El contraste F global detecta alguna diferencia, sin identificar por sí solo qué pares difieren. [1, pp. 7 y 29; 2, pp. 12 y 14; 3, pp. 40 y 41]",
      r'$H_0:\mu_1=\mu_2=\mu_3$; $H_A$: al menos una media difiere.',
      r'$f=\sqrt{\sum_{j=1}^{k}(\mu_j-\bar\mu)^2/k}\,/\sigma$',
      'f = 0,25 es un supuesto convencional que debe justificarse en un estudio real.' if v!='C' else 'Media global = 60; variación de las medias = (100 + 0 + 100) / 3. Por tanto, f = √(200/3) / 30 = 0,272166; no es exactamente 0,25.',
      f'''library(pwr)
f <- {efe}
calculo <- pwr.anova.test(k = 3, f = f,
  sig.level = 0.05, power = {power:.2f})
calculo$n
c(por_grupo = ceiling(calculo$n),
  total = 3 * ceiling(calculo$n))''',
      {'A':"f = 0,25 reproduce la elección convencional de clase. No se deriva automáticamente de las medias 50, 60 y 70 y varianza 900. El estadístico F usa una región de rechazo superior; no se introduce alternative = \"two.sided\".",
       'B':"El incremento de potencia exige 69 personas por grupo. Este es el tamaño para la hipótesis global; varias comparaciones por pares confirmatorias necesitan su propia planificación y control de multiplicidad.",
       'C':"El efecto calculado es ligeramente mayor que 0,25 y exige 45 personas por grupo. La comparación ilustra por qué conviene usar parámetros sustantivos en lugar de adoptar una categoría de efecto sin explicación."}[v],
      '¿Un ANOVA significativo prueba que las tres medias son diferentes entre sí?',
      'No. Permite rechazar que todas sean iguales. Identificar diferencias específicas requiere contrastes adicionales planificados.')

for v,sd,power,label in [('A',80,.80,'Las medias previstas definen el efecto'),('B',80,.90,'Potencia de 90 % en tres grupos'),('C',100,.80,'Una DE intragrupo mayor')]:
    caso('E7'+v,label,f"Compare tres programas de rehabilitación usando la distancia recorrida en una prueba funcional. Se esperan medias de 550, 598 y 610 metros, DE común de {sd} metros y grupos iguales. Calcule n con alfa de 0,05 y potencia de {int(power*100)} %.",
      "El desenlace es continuo y procede de tres grupos independientes. El contexto didáctico puede organizarse como ensayo paralelo; la asignación, descrita en Teoría 02, debe distinguirse del muestreo de participantes de Teoría 01. Aquí el ANOVA se parametriza directamente con las medias esperadas y la varianza intragrupo. [1, pp. 7 y 29; 2, pp. 12 y 14; 3, pp. 42 a 44]",
      r'$H_0:\mu_1=\mu_2=\mu_3$; $H_A$: al menos una media difiere.',
      r'$f^2=\frac{k-1}{k}\,\frac{s_{\mu}^2}{\sigma^2}$',
      f"R calcula var(c(550, 598, 610)) = 1008 usando divisor k − 1. La varianza dentro de los grupos es {sd}² = {sd**2}. El f equivalente es {num(res['E7'+v]['efecto'],6)}; el cociente de medias extremas no es el f del ANOVA.",
      f'''medias <- c(550, 598, 610)
calculo <- power.anova.test(groups = length(medias),
  between.var = var(medias), within.var = {sd}^2,
  sig.level = 0.05, power = {power:.2f})
calculo$n
c(por_grupo = ceiling(calculo$n),
  total = length(medias) * ceiling(calculo$n))''',
      {'A':"Se requieren 32 personas por grupo, 96 en total. Usar las tres medias conserva la estructura de la hipótesis global; (610 − 550) / 80 = 0,75 describe solo el contraste estandarizado entre extremos.",
       'B':"Al elevar la potencia se requieren 42 personas por grupo. La diferencia esperada y su variabilidad permanecen iguales; el cambio de muestra se debe a la exigencia de detección.",
       'C':"La misma separación entre medias es menos clara cuando los participantes varían más dentro de cada grupo. Por eso se requieren 49 personas por grupo. DE = 100 corresponde a varianza = 10000, no a 100."}[v],
      '¿Por qué var(medias) y la fórmula de f usan divisores distintos?',
      'var() calcula una varianza con divisor k − 1; f pondera las medias poblacionales esperadas con peso 1/k en grupos iguales. El factor (k − 1)/k conecta ambas parametrizaciones.')

for v,fA,power,label in [('A',.25,.80,'Cuatro celdas en un diseño factorial'),('B',.25,.90,'Mayor potencia por efecto principal'),('C',.20,.80,'Un efecto principal más pequeño')]:
    caso('E8'+v,label,f"Se evalúan dos intervenciones, A y B, cada una con dos niveles, mediante un puntaje continuo. Suponga un diseño factorial 2 × 2 balanceado y un modelo aditivo sin interacción. Planifique alfa de 0,05 por contraste, f_A = {num(fA)} y f_B = 0,55, con al menos {int(power*100)} % de potencia marginal para cada efecto principal.",
      "Teoría 02 incluye el diseño factorial: los participantes se distribuyen entre cuatro combinaciones de los factores. Teoría 01 ayuda a diferenciar la exposición del desenlace, que aquí es un puntaje continuo. Se usa el cálculo aditivo implementado en pwr2; no corresponde a una prueba de varias proporciones ni dimensiona una interacción. [1, pp. 7 y 11; 2, p. 14; 3, pp. 45 y 46]",
      r'$H_{0A}$: no hay efecto principal de A; $H_{0B}$: no hay efecto principal de B. Cada alternativa plantea un efecto principal distinto de cero.',
      r'$N=abn=4n,\qquad \lambda_A=Nf_A^2,\quad \lambda_B=Nf_B^2$',
      f"La función busca el tamaño por celda que satisface la potencia de ambos efectos principales por separado. El menor efecto, f_A = {num(fA)}, determina el tamaño en estas variantes. En el modelo aditivo se usan N − a − b + 1 = N − 3 grados de libertad residuales.",
      f'''library(pwr2)
calculo <- ss.2way(a = 2, b = 2, alpha = 0.05,
  beta = {1-power:.2f}, f.A = {fA:.2f}, f.B = 0.55, B = 1000)
n_celda <- calculo$n
c(por_celda = n_celda, total = 4 * n_celda)
pwr.2way(a = 2, b = 2, alpha = 0.05,
  size.A = n_celda, size.B = n_celda,
  f.A = {fA:.2f}, f.B = 0.55)''',
      {'A':"Se requieren 32 personas por celda, 128 en total. El mínimo de las dos potencias marginales no es la probabilidad de detectar ambos efectos simultáneamente. No se ha ajustado el error familiar por dos contrastes ni se ha incluido interacción.",
       'B':"Se requieren 43 personas por celda para alcanzar al menos 90 % de potencia marginal en cada efecto principal. Si el objetivo confirmatorio exigiera éxito conjunto o una interacción, sería necesaria otra planificación.",
       'C':"Al reducir f_A a 0,20 aumenta la exigencia a 50 personas por celda. B = 1000 es el límite de iteraciones de búsqueda de la función, no el número de participantes ni los niveles del factor B; siempre se comprueba la potencia devuelta."}[v],
      '¿40 participantes por celda en un diseño 2 × 2 equivalen a 80 en total?',
      'No. Hay cuatro celdas, por lo que son 160. Una potencia de 1,00 en escala de proporción equivale aproximadamente a 100 %, no a 1 %.')

contenido = {
 'autor':'Jason Chambe','titulo':'Tamaño de muestra en R: del diseño a la interpretación',
 'fecha':'6 de septiembre de 2026','casos':casos,
 'centrales':['E1A','E1B','E1C','E2A','E2B','E2C','E4A','E4B','E4C'],
 'fuentes':[
  '[1] Quispe, A. M. (s. f.). Teoría 01: Bioestadística. Material de clase proporcionado por el estudiante. Se utilizan las páginas 7, 9, 11, 16, 24, 29, 47 y 50; numeración del PDF contando la portada.',
  '[2] Quispe, A. M. (s. f.). Teoría 02: Bioestadística. Material de clase proporcionado por el estudiante. Se utilizan las páginas 7 a 14 para diseño experimental, comparación y amenazas al antes y después.',
  '[3] Quispe, A. M. (s. f.). Teoría 03: Bioestadística. Material de clase proporcionado por el estudiante. Páginas 11 a 22: supuestos y fórmulas; 26: funciones; 30 a 46: ejemplos.',
  '[4] Quispe, A. M. (s. f.). Muestra.qmd. Práctica de cálculo de tamaño de muestra proporcionada en clase. Se adaptan sus ocho escenarios y se conservan cálculos de n, potencia y efecto detectable en la práctica ampliada. Las variantes y los contextos añadidos son didácticos.',
  '[5] Champely, S. y colaboradores. pwr, versión 1.3.0. Documentación de pwr.t.test, pwr.p.test, pwr.2p.test, ES.h y pwr.anova.test. https://search.r-project.org/CRAN/refmans/pwr/html/00Index.html',
  '[6] R Core Team. R, versión 4.6.1. Documentación de power.anova.test. https://stat.ethz.ch/R-manual/R-devel/library/stats/html/power.anova.test.html',
  '[7] Lu, P., Liu, J. y Koestler, D. pwr2, versión 1.0. Documentación y código de ss.2way y pwr.2way, consultados en la instalación utilizada. Documentación accesible: https://rdrr.io/cran/pwr2/man/ss.2way.html y https://rdrr.io/cran/pwr2/man/pwr.2way.html. CRAN informa que el paquete fue archivado el 27 de mayo de 2026: https://cran.r-project.org/package=pwr2'
 ]}
(ROOT/'resultados/contenido_verificado.json').write_text(json.dumps(contenido,ensure_ascii=False,indent=2))
print(f'{len(casos)} casos redactados; 9 centrales y 15 de ampliación.')
