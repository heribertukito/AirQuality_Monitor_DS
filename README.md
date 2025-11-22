🌍 Monitor de Calidad del Aire (CDMX)

Dashboard interactivo desarrollado en Python y Streamlit para monitorear, visualizar y analizar datos históricos y en tiempo real de la calidad del aire en la Ciudad de México. Utiliza la API de Open-Meteo para obtener datos meteorológicos precisos.

🚀 Características

Pipeline ETL Modular: Extracción (API), Transformación (Pandas) y Visualización (Plotly) desacoplados.

Visualización Avanzada:

Series de tiempo interactivas con límites referenciales de la OMS.

Mapas de calor para identificar patrones horarios de contaminación.

Diagramas de caja (Boxplots) para análisis de distribución semanal.

Insights Automatizados: Algoritmos simples que generan texto descriptivo sobre las mejores y peores horas para actividades al aire libre.

Optimización: Uso de cache para minimizar llamadas a la API y mejorar la velocidad de carga.

🛠️ Tecnologías Utilizadas

Python 3.8+

Streamlit: Frontend y gestión del estado de la aplicación.

Pandas: Limpieza, manipulación de series de tiempo y manejo de datos categóricos.

Plotly: Gráficos interactivos.

Requests: Conexión HTTP robusta con manejo de errores.

📦 Instalación y Uso

Clonar el repositorio:

git clone [https://github.com/tu-usuario/monitor-calidad-aire.git](https://github.com/tu-usuario/monitor-calidad-aire.git)
cd monitor-calidad-aire


Crear un entorno virtual (Opcional pero recomendado):

python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate


Instalar dependencias:

pip install -r requirements.txt


Ejecutar la aplicación:

streamlit run dashboard.py


📂 Estructura del Proyecto

├── api_download.py    # Módulo de conexión con Open-Meteo API
├── cleaning.py        # Limpieza de datos y Feature Engineering
├── visualization.py   # Generación de gráficos con Plotly
├── dashboard.py       # Punto de entrada (Script principal de Streamlit)
├── requirements.txt   # Dependencias del proyecto
└── README.md          # Documentación


📊 Datos

Los datos son obtenidos de Open-Meteo Air Quality API. El dashboard está configurado por defecto para las coordenadas del Zócalo de la CDMX, pero es fácilmente adaptable a otras ubicaciones modificando api_download.py.

🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir qué te gustaría cambiar.

Desarrollado con ❤️ usando Streamlit.