#!/bin/bash

# Aumenta el límite de inotify para el monitoreo de archivos
echo fs.inotify.max_user_watches=524288 | tee -a /etc/sysctl.conf && sysctl -p

# Ejecuta el comando de inicio de Streamlit
exec streamlit run app.py
