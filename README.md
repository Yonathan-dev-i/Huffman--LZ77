# Demostración Interactiva de Compresión Sin Pérdida

Una **aplicación web interactiva** construida con Streamlit para explorar y comparar dos de los algoritmos de compresión sin pérdida más importantes: **Huffman Coding** y **LZ77**.

##  Características

 **Interfaz Visual Moderna**
- Diseño oscuro con tema ciberpunk (gradientes, animaciones suave)
- Gráficos interactivos con Plotly
- Cálculo de métricas de compresión en tiempo real

 **Dos Algoritmos Clásicos**
- **Huffman Coding** (1952): Códigos óptimos basados en frecuencia
- **LZ77** (1977): Compresión basada en diccionario deslizante

 **Análisis Detallado**
- Visualización de ratio de compresión
- Tablas de códigos Huffman generados
- Distribución de tokens LZ77
- Estadísticas de tiempo de ejecución

 **Validación de Compresión**
- Verificación de integridad (compresión sin pérdida)
- Descargar archivos recuperados
- Confirmación visual de éxito/error

---

##  Instalación Rápida

### Requisitos Previos
- **Python 3.8+**
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/Yonathan-dev-i/Huffman--LZ77.git
cd Huffman--LZ77
```

2. **Crear un entorno virtual (recomendado)**
```bash
# En macOS/Linux
python -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación**
```bash
streamlit run app.py
```

5. **Abrir en el navegador**
La aplicación se abrirá automáticamente en `http://localhost:8501`

---

##  Cómo Usar

### Uso Básico

1. **Cargar un archivo** en el panel lateral izquierdo
   - Soporta: `.txt`, `.csv`, `.json`, `.py`, `.html`, `.xml`, `.log`, `.bin` y más

2. **Seleccionar algoritmo**
   - Elige entre **Huffman Coding** o **LZ77**

3. **Comprimir el archivo**
   - Haz clic en el botón " Comprimir"
   - Observa las métricas de compresión en tiempo real

4. **Descomprimir**
   - Haz clic en " Descomprimir"
   - Verifica que el archivo recuperado sea idéntico al original

5. **Analizar resultados**
   - Visualiza gráficos de compresión
   - Explora códigos generados o tokens
   - Descarga el archivo recuperado

### Parámetros LZ77 (Avanzado)

Si seleccionas **LZ77**, puedes ajustar:
- **Tamaño de ventana**: 32-512 bytes (por defecto 255)
- **Tamaño lookahead**: 4-32 caracteres (por defecto 15)

Estos parámetros afectan la eficiencia y tiempo de compresión.

---

##  Estructura del Proyecto

```
Huffman--LZ77/
├── app.py              # Aplicación Streamlit (interfaz web)
├── huffman.py          # Implementación del algoritmo Huffman
├── lz77.py             # Implementación del algoritmo LZ77
├── requirements.txt    # Dependencias de Python
├── README.md           # Este archivo
└── .gitignore          # Archivos ignorados por Git
```

---

##  Descripción Técnica de Módulos

### `app.py` - Aplicación Principal
- Interfaz web con Streamlit
- Gestión de UI/UX con CSS personalizado
- Orquestación de compresión/descompresión
- Visualización de resultados con Plotly

### `huffman.py` - Codificación Huffman
```python
compress(text: str) -> (bytes, metadata, stats)
decompress(compressed_bytes: bytes, metadata: dict) -> (str, stats)
```

**Características:**
- Construcción de árbol de prefijos óptimo
- Códigos binarios de longitud variable
- Serialización del árbol en JSON
- Complejidad: O(n log n)

### `lz77.py` - Compresión LZ77
```python
compress(text: str, window_size: int, lookahead_size: int) -> (tokens, serialized, stats)
decompress_from_bytes(serialized: bytes) -> (str, stats)
```

**Características:**
- Ventana deslizante configurable
- Búsqueda de coincidencias (offset, length, next_char)
- Serialización JSON de tokens
- Complejidad: O(n·w) donde w = window_size

---

##  Dependencias

| Paquete | Versión | Propósito |
|---------|---------|----------|
| streamlit | ≥1.32.0 | Framework web interactivo |
| plotly | ≥5.18.0 | Gráficos interactivos |
| pandas | ≥2.0.0 | Tablas de datos |

---

##  Métricas de Compresión Mostradas

- **Tamaño original**: Bytes del archivo original
- **Tamaño comprimido**: Bytes después de compresión
- **Reducción (%)**: Porcentaje de espacio ahorrado
- **Ratio**: Proporción original/comprimido
- **Tiempo**: Duración de la operación en ms

---

##  Contexto Educativo

Este proyecto fue desarrollado como **material académico** para la enseñanza de:
-  Teoría de la Información
-  Algoritmos de Compresión
-  Estructuras de Datos (Árboles binarios, Heaps)
-  Análisis de Complejidad

**Ideal para:**
- Estudiantes de Ingeniería Informática
- Cursos de Algoritmos
- Presentaciones interactivas
- Investigación educativa

---

##  Limitaciones Conocidas

- Archivos muy grandes (>50MB) pueden ser lentos
- LZ77 con ventanas grandes consume más memoria
- Algunos archivos binarios pueden no comprimirse bien
- La compresión LZ77 usa JSON para serialización (menos eficiente)

---

##  Ejemplos de Uso

### Ejemplo 1: Comprimir un archivo de texto
```bash
streamlit run app.py
# Carga un archivo .txt con mucho texto repetido
# Selecciona Huffman Coding
# Observa la compresión efectiva
```

### Ejemplo 2: Comparar algoritmos
1. Comprime el mismo archivo con Huffman
2. Descarga los resultados
3. Repite con LZ77
4. Compara las métricas

### Ejemplo 3: Ajustar parámetros LZ77
```bash
streamlit run app.py
# Selecciona LZ77
# Prueba con diferentes window_size y lookahead_size
# Observa cómo varían las estadísticas
```

---

##  Licencia

Este proyecto es de código abierto con fines educativos.

---

##  Autoría

**Yonathan-dev-i** - Desarrollo inicial y diseño

---

##  Soporte & Contribuciones

¿Encontraste un bug? ¿Tienes sugerencias?
- Abre un **issue** en GitHub
- Envía un **pull request** con mejoras
- Contacta al autor

---

##  Referencias

- **Huffman Coding**: D. A. Huffman, "A method for the construction of minimum-redundancy codes" (1952)
- **LZ77**: A. Lempel, J. Ziv, "A universal algorithm for sequential data compression" (1977)
- **Streamlit Docs**: https://docs.streamlit.io
- **Plotly Docs**: https://plotly.com/python/

---

**¡Gracias por usar CompresorLab! 🎉**
