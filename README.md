MAIN.PY
Este script de python permite la ejecución de otros tres scrips: "blast.py", "muscle.py" y "dominios.py"

-blast.py: permite comparar uno o varios querys de proteínas convirtiéndolo en único archivo fasta gracias a la creación de una base de datos a partir de los genbanks introducidos por el usuario.
-muscle.py: permite hacer un alineamiento múltiple de cada resultado obtenido en blastp y después un árbol filogenético con dichos alineamientos.
-dominios.py: búsqueda de dominios parseando una base de datos llamada "prosite.dat", la cual será descargada y guardada por el usuario en la ruta donde se esté ejecutando el programa.

En total se crean dos carpetas:
-"database": carpeta en la cual se guardan las bases de datos creadas con blast.py
-"results": carpeta en la cual se almacenan los resultados del blastp. Además, encontramos otras dos carpetas, "mucle" y "prosite", para almacenar los resultados de puscle.py y dominios.py respectivamente.

REQUISITOS

-Los argumentos introducidos deben ser 3 (en cuyo caso el coverage y la identity serán predefinidos) o 5 (el usuario elige los valores de identity y coverage)
-El archivo prosite.dat usado en el script dominios.py se debe encontrar en la ruta desde la cual se esté ejecutando el programa
-El usuario debe tener instalado muscle para poder realizar el alineamiento y el árbol filogenético

USO
python3 main.py [query] [subject] [cov] [identity]
1. query: ruta del archivo en formato fasta que contiene una o varias secuencias de proteínas. Si se quieren analizar varias secuencias estas deben encontrarse en el mismo archivo.
2. subject: ruta a la carpeta llamada genbank en la cual hay uno o varios genbanks
3. cov: argumento opcional. Número entre 0 y 100 que indica el porcentaje mínimo de cobertura para filtar los resultados al hacer blastp
4. identity: argumento opcional. Número entre 0 y 100 que indica el porcentaje de identidad mínimo para filtar los resultados al hacer blastp
