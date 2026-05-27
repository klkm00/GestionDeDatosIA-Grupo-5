# Proyecto DataOps - Predicción Incumplimiento Préstamos


## Validación y limpieza del dataset de préstamos

**Fecha de ejecución:** 2026-05-24 06:50:27

### Archivos utilizados
- Dataset de entrada: `data/raw/loan_preprocesado.csv`
- Dataset validado generado: `data/processed/loan_validado.csv`
- Reporte de validación: `reports/reporte_errores_validacion.csv`

### Resumen del procesamiento
- Filas originales: 45000
- Filas finales: 44990
- Filas eliminadas: 10
- Problemas registrados en logs: 10

### Transformaciones aplicadas
- Estandarización de nombres de columnas.
- Limpieza y normalización de columnas de texto.
- Conversión de columnas numéricas cuando corresponde.
- Eliminación de filas vacías, duplicadas y con nulos.
- Validación de rangos: edad (18-100), credit_score (300-850), tasa interés (0-100).
- Creación de columnas derivadas: ratio_monto_ingreso, categoria_credito.
- Generación de reporte de validación con logs detallados.
