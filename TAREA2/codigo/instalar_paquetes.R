# Ejecutar una sola vez desde TAREA2, con conexión a internet.
paquetes <- c("pwr", "knitr", "rmarkdown")
faltan <- paquetes[!vapply(paquetes, requireNamespace, logical(1), quietly = TRUE)]
if (length(faltan)) install.packages(faltan, repos = "https://cloud.r-project.org")
# pwr2 1.0 fue archivado por CRAN. Se conserva para reproducir la clase.
if (!requireNamespace("pwr2", quietly = TRUE)) {
  install.packages("https://cran.r-project.org/src/contrib/Archive/pwr2/pwr2_1.0.tar.gz",
                   repos = NULL, type = "source")
}
