# PLANIFICADOR DE TREKKING Y ALTA MONTAÑA

Aplicación profesional desarrollada en Python que permite planificar expediciones de trekking y montaña mediante el consumo de APIs externas en tiempo real. El sistema analiza condiciones climáticas, calcula rutas de senderismo y genera alertas de seguridad para apoyar la toma de decisiones antes de iniciar una expedición.

El principal usuario de esta herramienta es un guía profesional de trekking y montañismo que necesita evaluar rápidamente las condiciones ambientales y la viabilidad de una ruta antes de iniciar una expedición con un grupo de personas.

La aplicación también puede ser utilizada por:

- excursionistas
- senderistas
- montañistas
- deportistas de alta montaña



Problema
En actividades de montaña y trekking, las condiciones climáticas pueden cambiar drásticamente en pocos minutos, representando riesgos importantes para los excursionistas, como:

- tormentas repentinas
- vientos extremos
- temperaturas bajo cero
- precipitaciones intensas
- rutas inseguras o inaccesibles

Actualmente muchos usuarios deben consultar múltiples plataformas para obtener información crítica como coordenadas geográficas, clima, rutas y tiempos estimados de caminata. Esto provoca pérdida de tiempo, mala planificación y aumenta el riesgo de accidentes en terreno.
Además, excursionistas menos experimentados pueden no interpretar correctamente la información meteorológica antes de iniciar una ruta.

Solución
El sistema centraliza toda la información importante de una expedición en una sola aplicación de consola.

La herramienta:
- obtiene coordenadas geográficas mediante OpenStreetMap
- consulta datos meteorológicos en tiempo real usando Open-Meteo
- calcula rutas de trekking utilizando Geoapify
- analiza automáticamente las condiciones climáticas
- genera alertas de seguridad según viento, precipitaciones y sensación térmica
- entrega un reporte claro y fácil de interpretar para el usuario

Gracias a esto, el excursionista puede evaluar de manera rápida y segura si las condiciones son adecuadas para realizar el ascenso o trekking planificado.


 APIs Utilizadas
- OpenStreetMap Nominatim API
- Open-Meteo API
- Geoapify Routing API (Necesita API key)

Características Principales
- Consulta de coordenadas geográficas
- Obtención de clima en tiempo real
- Evaluación automática de riesgos
- Análisis de viento y precipitaciones
- Cálculo de rutas de trekking
- Alertas de seguridad para montaña
- Manejo robusto de errores
- Uso seguro de variables de entorno
- Integración preparada para Docker y Jenkins

---

# Configuración de Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
API_KEY_PROYECTO=tu_api_key
