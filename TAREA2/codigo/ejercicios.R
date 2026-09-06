# TAREA2. Cálculos deterministas; ejecutar desde la carpeta TAREA2.
# Adaptación didáctica de Muestra.qmd, Antonio M. Quispe.
# Las variantes añadidas son supuestos de planificación, no datos observados.
if (!requireNamespace("pwr", quietly = TRUE) ||
    !requireNamespace("pwr2", quietly = TRUE)) {
  stop('Ejecute primero: source("codigo/instalar_paquetes.R")')
}
library(pwr)
library(pwr2)
dir.create("resultados", showWarnings = FALSE)

filas <- list()
registrar <- function(id, metodo, efecto, ajuste, potencia, objetivo = .80,
                      grupos = 1L, unidad = "personas", alternativa = "two.sided") {
  n <- ceiling(ajuste$n)
  lograda <- potencia(n)
  anterior <- if (n > 2) potencia(n - 1) else NA_real_
  stopifnot(is.finite(n), lograda >= objetivo - 1e-7)
  if (is.finite(anterior)) stopifnot(anterior < objetivo + 1e-7)
  filas[[id]] <<- data.frame(
    id, metodo, efecto, alfa = .05, potencia_objetivo = objetivo,
    alternativa, n_sin_redondear = ajuste$n, n = n,
    grupos, N_total = n * grupos, unidad,
    potencia_con_n = lograda, potencia_con_n_menos_1 = anterior)
}
t_caso <- function(id, d, tipo, alternativa = "two.sided", poder = .80) {
  ajuste <- pwr.t.test(d = d, sig.level = .05, power = poder,
                       type = tipo, alternative = alternativa)
  potencia <- function(n) pwr.t.test(n = n, d = d, sig.level = .05,
                                    type = tipo, alternative = alternativa)$power
  registrar(id, paste("t", tipo), d, ajuste, potencia, poder,
            if (tipo == "two.sample") 2L else 1L,
            if (tipo == "paired") "pares completos" else if (tipo == "two.sample") "personas por grupo" else "personas",
            alternativa)
}
p_caso <- function(id, p1, p0, dos = FALSE, alternativa = "two.sided", poder = .80) {
  h <- ES.h(p1, p0)
  fun <- if (dos) pwr.2p.test else pwr.p.test
  ajuste <- fun(h = h, sig.level = .05, power = poder, alternative = alternativa)
  potencia <- function(n) fun(h = h, n = n, sig.level = .05, alternative = alternativa)$power
  registrar(id, if (dos) "dos proporciones" else "una proporcion", h, ajuste,
            potencia, poder, if (dos) 2L else 1L,
            if (dos) "personas por grupo" else "personas", alternativa)
}
anova_caso <- function(id, f, poder = .80) {
  ajuste <- pwr.anova.test(k = 3, f = f, sig.level = .05, power = poder)
  potencia <- function(n) pwr.anova.test(k = 3, f = f, n = n, sig.level = .05)$power
  registrar(id, "ANOVA una via f", f, ajuste, potencia, poder, 3L, "personas por grupo", "F global")
}
medias_caso <- function(id, medias, sd, poder = .80) {
  f <- sqrt(mean((medias - mean(medias))^2)) / sd
  ajuste <- power.anova.test(groups = length(medias), between.var = var(medias),
                             within.var = sd^2, sig.level = .05, power = poder)
  contraste <- pwr.anova.test(k = length(medias), f = f, sig.level = .05, power = poder)
  stopifnot(abs(ajuste$n - contraste$n) < 1e-3)
  potencia <- function(n) power.anova.test(groups = length(medias),
      between.var = var(medias), within.var = sd^2, n = n, sig.level = .05)$power
  registrar(id, "ANOVA medias explicitas", f, ajuste, potencia, poder,
            length(medias), "personas por grupo", "F global")
}
factorial_caso <- function(id, fA, fB, poder = .80) {
  ajuste <- ss.2way(a = 2, b = 2, alpha = .05, beta = 1 - poder,
                    f.A = fA, f.B = fB, B = 1000)
  potencia <- function(n) pwr.2way(a = 2, b = 2, alpha = .05,
      size.A = n, size.B = n, f.A = fA, f.B = fB)$power
  registrar(id, "ANOVA factorial aditivo", min(fA, fB), ajuste, potencia, poder,
            4L, "personas por celda", "efectos principales F")
  # Comprobación independiente de los grados de libertad del modelo aditivo.
  N <- 4 * ajuste$n
  comprobacion <- pf(qf(.95, 1, N - 3), 1, N - 3,
                     ncp = N * min(fA, fB)^2, lower.tail = FALSE)
  stopifnot(abs(comprobacion - potencia(ajuste$n)) < 1e-12)
}

# Escenario 1. Hemoglobina contra una media de referencia fija (g/dL).
t_caso("E1A", (14 - 10) / 1, "one.sample")
t_caso("E1B", (14 - 10) / 1, "one.sample", "greater")
t_caso("E1C", (11 - 10) / 1, "one.sample")
# Escenario 2. Una prevalencia contra una referencia fija de 40 %.
p_caso("E2A", .20, .40)
p_caso("E2B", .20, .40, alternativa = "less")
p_caso("E2C", .30, .40)
# Escenario 3. Dos medias independientes, DE común = 1 o 2 g/dL.
t_caso("E3A", (12.5 - 12) / 1, "two.sample")
t_caso("E3B", (12.5 - 12) / 1, "two.sample", poder = .90)
t_caso("E3C", (12.5 - 12) / 2, "two.sample")
# Escenario 4. Dos prevalencias independientes, asignación 1:1.
p_caso("E4A", .43, .26, dos = TRUE)
p_caso("E4B", .43, .26, dos = TRUE, poder = .90)
p_caso("E4C", .43, .33, dos = TRUE)
# Escenario 5. Cambios pareados: la DE corresponde a las diferencias.
t_caso("E5A", 1 / 1, "paired")
t_caso("E5B", 1 / 2, "paired")
t_caso("E5C", 1 / 1, "paired", "greater")
# Escenario 6. ANOVA global, tres grupos iguales.
anova_caso("E6A", .25)
anova_caso("E6B", .25, .90)
anova_caso("E6C", sqrt(mean((c(50, 60, 70) - 60)^2)) / 30)
# Escenario 7. ANOVA a partir de medias esperadas.
medias_caso("E7A", c(550, 598, 610), 80)
medias_caso("E7B", c(550, 598, 610), 80, .90)
medias_caso("E7C", c(550, 598, 610), 100)
# Escenario 8. Factorial 2 x 2, modelo aditivo sin interacción.
factorial_caso("E8A", .25, .55)
factorial_caso("E8B", .25, .55, .90)
factorial_caso("E8C", .20, .55)

resultados <- do.call(rbind, filas)
rownames(resultados) <- NULL
write.csv(resultados, "resultados/resultados_verificados.csv", row.names = FALSE)

# Reconstrucción de los cálculos originales: n, potencia y efecto detectable.
originales <- data.frame(
 escenario = 1:8,
 n = c(pwr.t.test(d = 1, power = .8, type = "one.sample")$n,
       pwr.p.test(h = ES.h(.15, .10), power = .8)$n,
       pwr.t.test(d = .5, power = .8, type = "two.sample")$n,
       pwr.2p.test(h = ES.h(.5, .1), power = .8)$n,
       pwr.t.test(d = 1, power = .8, type = "paired")$n,
       pwr.anova.test(k = 3, f = .25, power = .8)$n,
       power.anova.test(groups = 3, between.var = var(c(550,598,610)), within.var = 6400, power = .8)$n,
       ss.2way(a=2,b=2,alpha=.05,beta=.20,f.A=.25,f.B=.55,B=40)$n),
 n_disponible = c(20,400,70,20,40,60,40,40),
 potencia = c(pwr.t.test(n=20,d=1,type="one.sample")$power,
       pwr.p.test(n=400,h=ES.h(.15,.10))$power,
       pwr.t.test(n=70,d=.5,type="two.sample")$power,
       pwr.2p.test(n=20,h=ES.h(.5,.1))$power,
       pwr.t.test(n=40,d=1,type="paired")$power,
       pwr.anova.test(k=3,n=60,f=.25)$power,
       power.anova.test(groups=3,between.var=var(c(550,598,610)),within.var=6400,n=40)$power,
       pwr.2way(a=2,b=2,alpha=.05,size.A=40,size.B=40,f.A=.25,f.B=.55)$power),
 efecto_detectable = c(pwr.t.test(n=20,power=.8,type="one.sample")$d,
       pwr.p.test(n=400,power=.8)$h,
       pwr.t.test(n=70,power=.8,type="two.sample")$d,
       pwr.2p.test(n=20,power=.8)$h,
       pwr.t.test(n=40,power=.8,type="paired")$d,
       pwr.anova.test(k=3,n=60,power=.8)$f,
       pwr.anova.test(k=3,n=40,power=.8)$f,
       NA_real_))
write.csv(originales, "resultados/puente_con_clase.csv", row.names = FALSE)

# Identidades y comprobaciones de interpretación, además de n y n-1.
stopifnot(abs(ES.h(.20,.40) - (2*asin(sqrt(.20))-2*asin(sqrt(.40)))) < 1e-12)
stopifnot(abs(pwr.2p.test(h=ES.h(.43,.26),power=.8)$n /
              pwr.p.test(h=ES.h(.43,.26),power=.8)$n - 2) < 1e-5)
stopifnot(resultados$n[resultados$id == "E1A"] == 3,
          resultados$n[resultados$id == "E2A"] == 41,
          resultados$n[resultados$id == "E4A"] == 121)

# Curva de potencia real, no un único punto como en el ejemplo original.
curva <- data.frame(n_por_grupo = 5:100)
curva$potencia <- vapply(curva$n_por_grupo, function(n)
  power.anova.test(groups=3,between.var=var(c(550,598,610)),
                   within.var=6400,n=n)$power, numeric(1))
write.csv(curva, "resultados/curva_potencia.csv", row.names = FALSE)
capture.output(sessionInfo(), file = "resultados/sessionInfo.txt")
print(resultados[,c("id","efecto","n","N_total","potencia_con_n")], row.names=FALSE)
cat("\n24 variantes verificadas bajo los métodos y supuestos declarados.\n")
