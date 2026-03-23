# Usa una imagen oficial de Python ligera
FROM python:3.12-slim

# Establece variables de entorno para que Python no genere archivos .pyc y no use buffer en la salida
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala dependencias del sistema necesarias para compilar librerías como psycopg2
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala las dependencias de Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el proyecto al contenedor
COPY . /app/

# Copia el script de inicio y dale permisos de ejecución
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Expone el puerto que usará Gunicorn
EXPOSE 8000

# Usar el script personalizado como punto de entrada
ENTRYPOINT ["/docker-entrypoint.sh"]

# Comando por defecto para iniciar la aplicación con gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]