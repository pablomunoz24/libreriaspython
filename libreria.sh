#!/bin/bash
# Instalación de librerías de Python + Spyder
# Sala 18-305B

echo "🚀 Actualizando sistema..."
sudo apt update -y
sudo apt install -y python3 python3-pip python3-venv git

echo "📦 Actualizando pip..."
python3 -m pip install --upgrade pip

echo "✅ Instalando librerías principales..."
pip3 install numpy matplotlib scipy scikit-learn pandas pathlib spyder

echo "📥 Instalando CommPy desde GitHub..."
pip3 install git+https://github.com/veeresht/CommPy.git

echo "🔍 Verificando instalación..."
python3 - <<EOF
import numpy, matplotlib, scipy, sklearn, pandas, pathlib, commpy
print("✅ Todas las librerías instaladas correctamente")
EOF

echo "🎉 Instalación finalizada en este equipo."