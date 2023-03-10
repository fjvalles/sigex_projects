# SIGEX
Script para obtener los links de los proyectos y descargar su contenido

## Dependencias
### MacOS

```
# Intalar Chrome

# Instalar Python
brew install python

# Actualizar Pip
pip3 install --upgrade pip

# Instalar Selenium
pip3 install selenium

# Instalar Webdriver manager y Chromedriver (Asegurarse de tener instalado Chrome)
pip install webdriver-manager
brew install cask chromedriver

# Authorizar el Chromedriver
xattr -d com.apple.quarantine /usr/local/bin/chromedriver
```

## Cómo ejecutar
Simplemente ejecuta el comando `python3 sigex.py` en la Terminal, preocupándose de estar posicionado en la ubicación en donde se encuentre ese archivo.