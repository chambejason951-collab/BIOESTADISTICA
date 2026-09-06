"""Crea las fuentes del carrusel horizontal; se compilan con el LaTeX local."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
D=json.loads((R/'resultados/contenido_verificado.json').read_text())
C={c['id']:c for c in D['casos']}

def esc(s):
    return ''.join({'\\':r'\textbackslash{}','%':r'\%','&':r'\&','_':r'\_',
      '#':r'\#','$':r'\$','{':r'\{','}':r'\}','−':'-','×':r'\(\times\)'}.get(c,c) for c in str(s))
def text(x,y,w,s,size=16,color='Navy',bold=False,raw=False,leading=None):
    return (rf'\node[anchor=north west,inner sep=0pt,text width={w}mm,align=left,text={color},'
      rf'font=\fontsize{{{size}}}{{{leading or round(size*1.22,1)}}}\selectfont'+(r'\bfseries' if bold else '')+
      rf'] at ({x},-{y}) {{'+(s if raw else esc(s))+"};\n")
def rect(x,y,w,h,color,radius=3):
    return rf'\fill[{color},rounded corners={radius}mm] ({x},-{y}) rectangle ({x+w},-{y+h});'+'\n'
def line(x,y,w,color='Line'):
    return rf'\draw[{color},line width=.4pt] ({x},-{y}) -- ({x+w},-{y});'+'\n'

spec={
 'E1A':dict(title='Hemoglobina: una media frente a referencia',short='Puno · Variante A · Bilateral',question='Después de la intervención esperamos una media de 14 g/dL. ¿Cuántos niños necesitamos para compararla con 10 g/dL?',math=r'$10\ \mathrm{g/dL}\ \longrightarrow\ 14\ \mathrm{g/dL}$',inputs=['Referencia fija: 10 g/dL','DE esperada: 1 g/dL','Alfa: 0,05 · Potencia: 80 %','Alternativa: bilateral'],hyp=r'$H_0:\mu=10\qquad H_A:\mu\ne10$',reason='Hay una muestra nueva. La referencia de 10 se considera fija, sin incertidumbre muestral.',take='El tamaño pequeño se explica por d = 4. Depende de normalidad y de una DE bien sustentada.',calc=r'$d=(14-10)/1=4$',caption='niños en una muestra',source='Teoría 01, pp. 7 y 29 · Teoría 02, pp. 9 y 11 · Teoría 03, pp. 30 y 31'),
 'E1B':dict(title='La dirección se decide antes de medir',short='Puno · Variante B · Incremento',question='Con los mismos valores de hemoglobina, ahora planteamos formalmente una hipótesis unilateral de incremento.',math=r'$10\ \mathrm{g/dL}\ \longrightarrow\ 14\ \mathrm{g/dL}$',inputs=['Referencia fija: 10 g/dL','DE esperada: 1 g/dL','Alfa: 0,05 · Potencia: 80 %','Alternativa: mayor que 10'],hyp=r'$H_0:\mu\le10\qquad H_A:\mu>10$',reason='Seguimos comparando una muestra con una referencia. Cambia la dirección del contraste.',take='El n sin redondear disminuye, pero ambas variantes terminan en 3. Una cola no siempre cambia el entero.',calc=r'$d=4\qquad \mathrm{alternative}=\texttt{greater}$',caption='niños en una muestra',source='Teoría 01, p. 7 · Teoría 02, pp. 9 y 11 · Teoría 03, pp. 18 y 19'),
 'E1C':dict(title='Una diferencia menor necesita más muestra',short='Puno · Variante C · Menor incremento',question='Ahora esperamos 11 g/dL en lugar de 14. Mantenemos la referencia, la DE, el alfa y la potencia del caso bilateral.',math=r'$10\ \mathrm{g/dL}\ \longrightarrow\ 11\ \mathrm{g/dL}$',inputs=['Referencia fija: 10 g/dL','DE esperada: 1 g/dL','Alfa: 0,05 · Potencia: 80 %','Alternativa: bilateral'],hyp=r'$H_0:\mu=10\qquad H_A:\mu\ne10$',reason='La comparación sigue siendo de una muestra. Cambia la diferencia que queremos detectar.',take='El efecto baja de d = 4 a d = 1. Con los demás supuestos iguales, la muestra aumenta de 3 a 10.',calc=r'$d=(11-10)/1=1$',caption='niños en una muestra',source='Teoría 01, p. 7 · Teoría 02, pp. 9 y 11 · Teoría 03, pp. 15 y 19'),
 'E2A':dict(title='Anemia: una proporción frente a referencia',short='Juliaca · Variante A · Bilateral',question='Esperamos una prevalencia posterior de 20 %. Para este cálculo tratamos el 40 % previo como referencia fija.',math=r'$40\,\%\ \longrightarrow\ 20\,\%$',inputs=['Desenlace: anemia sí/no','Referencia fija: 40 %','Alfa: 0,05 · Potencia: 80 %','Alternativa: bilateral'],hyp=r'$H_0:p=0{,}40\qquad H_A:p\ne0{,}40$',reason='Se mide prevalencia en una muestra nueva. Una comparación histórica no demuestra por sí sola causalidad.',take='40 % a 20 % son 20 puntos porcentuales de reducción. El n corresponde a una sola muestra.',calc=r'$h=2\arcsin\sqrt{0{,}20}-2\arcsin\sqrt{0{,}40}$',caption='niños en una muestra',source='Teoría 01, pp. 47 y 50 · Teoría 02, pp. 9 y 11 · Teoría 03, pp. 32 y 33'),
 'E2B':dict(title='Una hipótesis de disminución',short='Juliaca · Variante B · Unilateral',question='Se mantienen 40 % y 20 %, pero se plantea antes del estudio que el contraste evaluará una disminución.',math=r'$40\,\%\ \longrightarrow\ 20\,\%$',inputs=['Desenlace: anemia sí/no','Referencia fija: 40 %','Alfa: 0,05 · Potencia: 80 %','Alternativa: menor que 40 %'],hyp=r'$H_0:p\ge0{,}40\qquad H_A:p<0{,}40$',reason='La comparación sigue siendo de una proporción. La hipótesis direccional debe estar justificada de antemano.',take='Conserva h negativo y usa less. Cambiar a una cola después de ver los datos no es una justificación válida.',calc=r'$h=-0{,}442143\qquad\mathrm{alternative}=\texttt{less}$',caption='niños en una muestra',source='Teoría 01, p. 47 · Teoría 02, pp. 9 y 11 · Teoría 03, pp. 18 y 19'),
 'E2C':dict(title='Detectar una reducción más discreta',short='Juliaca · Variante C · Menor diferencia',question='Ahora se espera pasar de 40 % a 30 %. Conservamos el contraste bilateral, alfa de 0,05 y potencia de 80 %.',math=r'$40\,\%\ \longrightarrow\ 30\,\%$',inputs=['Desenlace: anemia sí/no','Referencia fija: 40 %','Alfa: 0,05 · Potencia: 80 %','Alternativa: bilateral'],hyp=r'$H_0:p=0{,}40\qquad H_A:p\ne0{,}40$',reason='Mantenemos una muestra contra referencia. Solo cambia la prevalencia que esperamos detectar.',take='Al reducir la diferencia de 20 a 10 puntos porcentuales, la muestra aumenta de 41 a 178 niños.',calc=r'$h=2\arcsin\sqrt{0{,}30}-2\arcsin\sqrt{0{,}40}$',caption='niños en una muestra',source='Teoría 01, pp. 47 y 50 · Teoría 02, p. 11 · Teoría 03, pp. 15 y 19'),
 'E4A':dict(title='Dos distritos, dos muestras independientes',short='SJL y VMT · Variante A · Potencia de 80 %',question='Comparemos 43 % de prevalencia en San Juan de Lurigancho y 26 % en Villa María del Triunfo.',math=r'$43\,\%\quad\mathrm{vs.}\quad26\,\%$',inputs=['Niños distintos por distrito','Asignación de muestra: 1:1','Alfa: 0,05 · Potencia: 80 %','Alternativa: bilateral'],hyp=r'$H_0:p_{SJL}=p_{VMT}\quad H_A:p_{SJL}\ne p_{VMT}$',reason='Es una comparación transversal observacional. Aquí ambas prevalencias se estimarán mediante muestras.',take='pwr.2p.test devuelve n por distrito: 121 + 121 = 242 niños. No confundas n con el total.',calc=r'$h=2\arcsin\sqrt{0{,}43}-2\arcsin\sqrt{0{,}26}$',caption='niños por distrito',source='Teoría 01, pp. 29 y 47 · Teoría 02, p. 7 · Teoría 03, pp. 36 y 37'),
 'E4B':dict(title='Más potencia exige más participantes',short='SJL y VMT · Variante B · Potencia de 90 %',question='Mantenemos las prevalencias de 43 % y 26 %, pero exigimos una potencia de 90 % para la diferencia prevista.',math=r'$43\,\%\quad\mathrm{vs.}\quad26\,\%$',inputs=['Muestras independientes','Asignación de muestra: 1:1','Alfa: 0,05 · Potencia: 90 %','Alternativa: bilateral'],hyp=r'$H_0:p_{SJL}=p_{VMT}\quad H_A:p_{SJL}\ne p_{VMT}$',reason='El diseño y el efecto permanecen iguales. Queremos reducir beta de 20 % a 10 % bajo esa alternativa.',take='La muestra aumenta de 121 a 162 por distrito. Potencia no significa probabilidad de que exista un efecto.',calc=r'$h=0{,}360193\qquad 1-\beta=0{,}90$',caption='niños por distrito',source='Teoría 01, p. 47 · Teoría 02, p. 7 · Teoría 03, pp. 11 y 14'),
 'E4C':dict(title='Prevalencias más cercanas cuestan distinguir',short='SJL y VMT · Variante C · Menor diferencia',question='Comparamos ahora 43 % y 33 %, con potencia de 80 %, alfa de 0,05 y dos muestras de igual tamaño.',math=r'$43\,\%\quad\mathrm{vs.}\quad33\,\%$',inputs=['Muestras independientes','Asignación de muestra: 1:1','Alfa: 0,05 · Potencia: 80 %','Alternativa: bilateral'],hyp=r'$H_0:p_{SJL}=p_{VMT}\quad H_A:p_{SJL}\ne p_{VMT}$',reason='La diferencia se reduce de 17 a 10 puntos porcentuales. La comparación sigue siendo observacional.',take='El resultado es 369 por distrito, 738 en total. El tamaño de muestra no elimina la confusión entre poblaciones.',calc=r'$h=2\arcsin\sqrt{0{,}43}-2\arcsin\sqrt{0{,}33}$',caption='niños por distrito',source='Teoría 01, pp. 24 y 47 · Teoría 02, p. 7 · Teoría 03, pp. 15 y 19')
}

preamble=r'''\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[paperwidth=320mm,paperheight=180mm,margin=0mm]{geometry}
\usepackage{tikz,amsmath,amssymb,tgheros,hyperref}
\renewcommand{\familydefault}{\sfdefault}
\pagestyle{empty}
\setlength{\parindent}{0pt}
\definecolor{Navy}{HTML}{102A43}
\definecolor{Blue}{HTML}{2563EB}
\definecolor{Gray}{HTML}{52606D}
\definecolor{Pale}{HTML}{F3F6FA}
\definecolor{Ice}{HTML}{DBEAFE}
\definecolor{Line}{HTML}{D7E2EB}
\hypersetup{pdfauthor={Jason Chambe},pdftitle={Tamaño de muestra en R: nueve variantes},colorlinks=true,urlcolor=Blue}
\begin{document}
'''
pages=[]; meta=[]
def start(page,label,dark=False):
    bg='Navy' if dark else 'Pale'; fg='white' if dark else 'Navy'
    s=r'\noindent\begin{tikzpicture}[remember picture,overlay,x=1mm,y=1mm]\begin{scope}[shift={(current page.north west)}]'+'\n'
    s+=rect(0,0,320,180,bg,0)
    s+=text(14,10,265,label,10,'Ice' if dark else 'Blue',True)
    s+=text(286,10,24,f'{page:02} / 20',10,fg,True)
    s+=line(14,169,292,'Gray' if dark else 'Line')
    s+=text(14,172,250,'Jason Chambe  ·  Bioestadística  ·  TAREA 2',9,'Ice' if dark else 'Gray')
    s+=text(274,172,34,'DESLIZA →'.replace('→','>'),9,'Ice' if dark else 'Gray',True)
    return s
def end(s): return s+r'\end{scope}\end{tikzpicture}\mbox{}\newpage'+'\n'

s=start(1,'TUTORIAL REPRODUCIBLE EN R',True)
s+=text(14,37,198,'Tamaño de\nmuestra en R'.replace('\n',r'\\'),43,'white',True,True,47)
s+=text(15,88,174,'Entender qué comparamos antes de elegir una función.',23,'Ice',False)
s+=rect(213,40,93,104,'Blue')
s+=text(222,48,74,'3',55,'white',True)
s+=text(223,73,71,'ejercicios centrales',16,'white',True)
s+=text(222,94,74,'9',55,'white',True)
s+=text(223,119,73,'variantes explicadas',16,'white',True)
s+=text(15,125,184,'Hemoglobina · Anemia · Dos distritos',14,'white',True)
s+=text(15,140,181,'Código, supuestos y resultados.\nPráctica completa: 8 escenarios y 24 variantes.'.replace('\n',r'\\'),12,'Ice',raw=True)
pages.append(end(s));meta.append({'pagina':1,'tipo':'portada','titulo':'Tamaño de muestra en R'})

for idx,id in enumerate(D['centrales']):
    c=C[id]; v=spec[id]; r=c['datos']; n=int(r['n']); N=int(r['N_total'])
    page=2+idx*2
    s=start(page,'PLANTEAR  /  '+v['short'].upper())
    s+=text(14,25,290,v['title'],27,'Navy',True)
    s+=rect(14,55,177,92,'white');s+=rect(197,55,109,92,'white')
    s+=text(21,62,160,'LA COMPARACIÓN',10,'Blue',True)
    s+=text(21,73,160,v['question'],18,'Navy',False,leading=23)
    s+=text(21,108,160,v['math'],25,'Blue',True,True)
    s+=text(21,129,160,v['hyp'],12.4,'Navy',False,True)
    s+=text(204,62,95,'SUPUESTOS DEL CÁLCULO',10,'Blue',True)
    for k,t in enumerate(v['inputs']):
      s+=text(204,76+k*14.5,95,t,14,'Navy',k==2)
    s+=rect(14,151,292,14,'Ice')
    s+=text(19,155,282,v['reason'],12,'Navy',False,leading=14)
    # Source line in the top subtitle area.
    s+=text(14,45,292,v['source'],8.5,'Gray')
    pages.append(end(s));meta.append({'pagina':page,'caso':id,'tipo':'planteamiento','titulo':v['title']})
    s=start(page+1,'CALCULAR E INTERPRETAR  /  '+v['short'].upper())
    s+=text(14,25,292,'Del código al tamaño que reportamos',28,'Navy',True)
    s+=text(14,44,292,v['calc'],15,'Blue',False,True)
    s+=rect(14,58,180,89,'Navy');s+=rect(200,58,106,89,'white')
    s+=text(21,64,163,'R · PAQUETE pwr',10,'Ice',True)
    # Código completo, tipografía real y líneas conservadas.
    code=r'\ttfamily '+r'\\'.join(esc(line).replace(' ',r'\ ') for line in c['codigo'].splitlines())
    s+=text(21,76,166,code,13.5,'white',False,True,16.9)
    s+=text(208,64,90,'RESULTADO',10,'Blue',True)
    s+=text(207,72,91,str(n),51,'Blue',True)
    s+=text(208,95,90,v['caption'],14,'Navy',True)
    unrounded=f"{float(r['n_sin_redondear']):.6f}".replace('.',',')
    s+=text(208,108,90,f'n calculado: {unrounded}',11.5,'Gray')
    if N!=n: s+=text(208,120,90,f'{N} niños en total',16,'Navy',True)
    else: s+=text(208,120,90,'Redondeo hacia arriba',12,'Navy',True)
    p=f"{100*float(r['potencia_con_n']):.2f}".replace('.',',')
    s+=text(208,134,90,f'Potencia con n: {p} %',11,'Gray')
    s+=rect(14,151,292,14,'Ice')
    s+=text(19,154.5,282,v['take'],12,'Navy',False,leading=14)
    pages.append(end(s));meta.append({'pagina':page+1,'caso':id,'tipo':'calculo','n':n,'N_total':N,'titulo':'Del código al tamaño que reportamos'})

s=start(20,'GUARDA EL TUTORIAL Y PRUEBA LAS VARIANTES',True)
s+=text(14,26,292,'La muestra depende de la pregunta',30,'white',True)
for x,head,body in [(14,'MENOR DIFERENCIA','Más muestra para distinguirla.'),(113,'MAYOR POTENCIA','Más muestra para detectar el efecto.'),(212,'OTRO DISEÑO','Otra comparación y otro cálculo.')]:
 s+=rect(x,55,94,47,'Blue')
 s+=text(x+6,63,82,head,12,'white',True)
 s+=text(x+6,76,82,body,17,'white')
s+=text(14,110,290,'Descarga el QMD, el PDF y los scripts de R.',21,'white',True)
s+=text(14,126,290,'github.com/chambejason951-collab/BIOESTADISTICA',15,'Ice',True)
s+=text(14,138,290,'Carpeta TAREA2 · 24 variantes auditadas · Resultados reproducibles',12,'Ice')
s+=text(14,151,292,'Basado en Teoría 01, 02 y 03 y Muestra.qmd de Antonio M. Quispe. Documentación de R y pwr. Referencias completas en el tutorial.',10,'Ice')
pages.append(end(s));meta.append({'pagina':20,'tipo':'cierre','titulo':'La muestra depende de la pregunta'})

tex=preamble+''.join(pages).removesuffix('\\newpage\n')+r'\end{document}'+'\n'
(R/'linkedin/carrusel_tamano_muestra.tex').write_text(tex)
(R/'linkedin/guion_carrusel.json').write_text(json.dumps({'dimensiones':'1920 x 1080 px','proporcion':'16:9','paginas':meta,'variantes':spec},ensure_ascii=False,indent=2))
print('Carrusel de 20 páginas horizontales listo para compilar.')
