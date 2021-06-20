FROM python:3.8.5-slim-buster

#install sqlcmd and odbc and others
RUN apt-get update && apt-get install -y --no-install-recommends \
    unixodbc-dev unixodbc gcc curl

RUN apt install -y gnupg \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && apt-get install --reinstall -y build-essential

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


COPY . .
ENTRYPOINT ["python", "KPI4_analytics.py"]