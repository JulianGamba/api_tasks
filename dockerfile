FROM python:3.12

FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

# Instalar virtualenv, crear un entorno virtual llamado 'contenedor' e instalar dependencias en una sola instrucción RUN
RUN pip install virtualenv && \
    virtualenv contenedor && \
    . contenedor/bin/activate && \
    pip install -r requirements.txt

COPY . /app/

# CMD para ejecutar el comando en el entorno virtual
CMD ["bash", "-c", ". contenedor/bin/activate && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
