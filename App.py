import requests
import os
from dotenv import load_dotenv

load_dotenv()

# ==========================================
#        FASE 1: BÚSQUEDA Y CLIMA
# ==========================================

def obtener_coordenadas(lugar, pais):
    headers = {'User-Agent': 'TrekkingApp/4.0'}
    url = f"https://nominatim.openstreetmap.org/search?q={lugar}+{pais}&format=json"

    try:
        respuesta = requests.get(url, headers=headers, timeout=5)
        respuesta.raise_for_status()

        datos_json = respuesta.json()

        if len(datos_json) > 0:
            datos = datos_json[0]

            return (
                float(datos['lat']),
                float(datos['lon']),
                datos['display_name'].split(",")[0]
            )

        else:
            print("❌ No se encontraron coordenadas para ese lugar.")

    except requests.exceptions.Timeout:
        print("⏰ Tiempo de espera agotado buscando coordenadas.")

    except requests.exceptions.ConnectionError:
        print("🌐 Error de conexión a internet.")

    except requests.exceptions.HTTPError:
        print("❌ Error HTTP al consultar OpenStreetMap.")

    except requests.exceptions.RequestException as error:
        print(f"⚠️ Error general en la API de coordenadas: {error}")

    except ValueError:
        print("⚠️ Error procesando las coordenadas recibidas.")

    return None, None, None


def obtener_clima_montana(lat, lon):

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,apparent_temperature,"
        f"precipitation,wind_speed_10m,wind_gusts_10m"
        f"&daily=sunrise,sunset,uv_index_max"
        f"&timezone=auto"
    )

    try:
        respuesta = requests.get(url, timeout=5)
        respuesta.raise_for_status()

        datos = respuesta.json()

        altitud = datos.get("elevation", 0)

        actual = datos.get("current", {})

        diario = datos.get("daily", {})

        amanecer = diario.get("sunrise", ["--:--"])[0]
        atardecer = diario.get("sunset", ["--:--"])[0]

        if "T" in amanecer:
            amanecer = amanecer.split("T")[-1]

        if "T" in atardecer:
            atardecer = atardecer.split("T")[-1]

        return (
            altitud,
            actual.get("temperature_2m"),
            actual.get("apparent_temperature"),
            actual.get("precipitation"),
            actual.get("wind_speed_10m"),
            actual.get("wind_gusts_10m"),
            amanecer,
            atardecer,
            diario.get("uv_index_max", [0])[0]
        )

    except requests.exceptions.Timeout:
        print("⏰ La API meteorológica tardó demasiado en responder.")

    except requests.exceptions.ConnectionError:
        print("🌐 No se pudo conectar con la API meteorológica.")

    except requests.exceptions.HTTPError:
        print("❌ Error HTTP al consultar el clima.")

    except requests.exceptions.RequestException as error:
        print(f"⚠️ Error general en la API meteorológica: {error}")

    except ValueError:
        print("⚠️ Error procesando los datos meteorológicos.")

    return (None,) * 9


# ==========================================
#        EVALUACIÓN DE SEGURIDAD
# ==========================================

def evaluar_condiciones(sensacion, viento, rafagas, precip):

    alertas = []

    estado = "🟢 ÓPTIMAS (Buen clima para ascender)"

    # VALIDACIONES PARA EVITAR ERRORES CON None

    if (
        rafagas is not None and viento is not None
    ):

        if rafagas > 60 or viento > 40:
            alertas.append(
                "🌬️ Vientos huracanados. Riesgo altísimo en filos y cumbres."
            )

            estado = "🔴 PELIGRO (No se recomienda el ascenso)"

        elif rafagas > 40 or viento > 25:
            alertas.append(
                "💨 Viento moderado a fuerte. Asegura tu equipo."
            )

            if "🔴" not in estado:
                estado = "🟡 PRECAUCIÓN"

    if sensacion is not None:

        if sensacion < -15:
            alertas.append(
                "❄️ Frío extremo. Riesgo de hipotermia o congelamiento."
            )

            estado = "🔴 PELIGRO (No se recomienda el ascenso)"

        elif sensacion < 0:
            alertas.append(
                "🥶 Temperaturas bajo cero. Usa sistema de capas."
            )

            if "🔴" not in estado:
                estado = "🟡 PRECAUCIÓN"

    if precip is not None:

        if precip > 2:
            alertas.append(
                "🌧️/🌨️ Precipitaciones fuertes. Riesgo de avalanchas o hipotermia."
            )

            estado = "🔴 PELIGRO (No se recomienda el ascenso)"

        elif precip > 0:
            alertas.append(
                "💧 Precipitaciones leves. Roca resbaladiza."
            )

            if "🔴" not in estado:
                estado = "🟡 PRECAUCIÓN"

    if not alertas:
        alertas.append("✅ Condiciones estables en este momento.")

    return estado, alertas


# ==========================================
#        FASE 2: RUTA DE TREKKING
# ==========================================

def calcular_ruta_trekking(lat_inicio, lon_inicio, lat_fin, lon_fin):

    print("\n⏳ Calculando senderos y ruta a pie...\n")

    # API KEY DESDE VARIABLE DE ENTORNO

    API_KEY = os.getenv("API_KEY_PROYECTO")

    if not API_KEY:
        print("❌ No se encontró la API KEY.")
        return

    url = (
        f"https://api.geoapify.com/v1/routing?"
        f"waypoints={lat_inicio},{lon_inicio}|{lat_fin},{lon_fin}"
        f"&mode=hike"
        f"&apiKey={API_KEY}"
    )

    try:
        respuesta = requests.get(url, timeout=10)

        respuesta.raise_for_status()

        datos = respuesta.json()

        if "features" in datos and len(datos["features"]) > 0:

            propiedades = datos["features"][0]["properties"]

            distancia_km = propiedades.get("distance", 0) / 1000

            tiempo_segundos = propiedades.get("time", 0)

            horas = int(tiempo_segundos // 3600)

            minutos = int((tiempo_segundos % 3600) // 60)

            print("=" * 55)
            print(" 🥾 RUTA DE ASCENSO (TREKKING)")
            print("=" * 55)

            print(
                f"  • Distancia total a pie: {distancia_km:.2f} km (Solo ida)"
            )

            if horas > 0:
                print(
                    f"  • Tiempo estimado de caminata: "
                    f"{horas} horas y {minutos} minutos."
                )

            else:
                print(
                    f"  • Tiempo estimado de caminata: "
                    f"{minutos} minutos."
                )

            print(
                "  *(El tiempo se basa en un ritmo promedio)"
            )

        else:
            print(
                "❌ Geoapify no encontró un sendero peatonal."
            )

    except requests.exceptions.Timeout:
        print("⏰ Tiempo agotado calculando la ruta.")

    except requests.exceptions.ConnectionError:
        print("🌐 Error de conexión al consultar la ruta.")

    except requests.exceptions.HTTPError:
        print("❌ Error HTTP en Geoapify.")

    except requests.exceptions.RequestException as error:
        print(f"⚠️ Error general calculando la ruta: {error}")

    except ValueError:
        print("⚠️ Error procesando la ruta.")


# ==========================================
#        INTERFAZ PRINCIPAL
# ==========================================

def main():

    print("\n" + "=" * 55)
    print(" ⛰️  PLANIFICADOR DE TREKKING Y MONTAÑA ⛰️ ")
    print("=" * 55 + "\n")

    print("--- PUNTO DE PARTIDA ---")

    origen = input(
        "📍 Desde dónde empiezas a caminar: "
    ).strip()

    pais_origen = input(
        "🏳️ País de origen: "
    ).strip()

    print("\n--- DESTINO ---")

    destino = input(
        "⛰️ Montaña o cumbre a la que vas: "
    ).strip()

    pais_destino = input(
        "🏳️ País destino: "
    ).strip()

    print("\n⏳ Buscando coordenadas...\n")

    lat_origen, lon_origen, nombre_origen = obtener_coordenadas(
        origen,
        pais_origen
    )

    lat_destino, lon_destino, nombre_destino = obtener_coordenadas(
        destino,
        pais_destino
    )

    if (
        lat_origen is not None and
        lat_destino is not None
    ):

        (
            altitud,
            temp,
            sensacion,
            precip,
            viento,
            rafagas,
            amanecer,
            atardecer,
            uv_max

        ) = obtener_clima_montana(lat_destino, lon_destino)

        if temp is not None:

            estado, alertas = evaluar_condiciones(
                sensacion,
                viento,
                rafagas,
                precip
            )

            print("=" * 55)

            print(
                f" 🏕️ REPORTE DE CUMBRE: "
                f"{nombre_destino.upper()}"
            )

            print("=" * 55)

            print("\n🏔️ GEOGRAFÍA")

            print(
                f"  • Altitud base estimada: "
                f"{altitud} m.s.n.m."
            )

            print("\n🌡️ CLIMA EN TIEMPO REAL")

            print(
                f"  • Temperatura: {temp}°C "
                f"(Sensación térmica: {sensacion}°C)"
            )

            print(
                f"  • Viento: {viento} km/h "
                f"| Ráfagas: {rafagas} km/h"
            )

            print(
                f"  • Precipitaciones: {precip} mm"
            )

            print("\n☀️ LUZ")

            print(
                f"  • Ventana de luz: "
                f"{amanecer} a {atardecer}"
            )

            print(f"  • Índice UV: {uv_max}")

            print("\n🚦 SEMÁFORO DE SEGURIDAD")

            print(f"  ESTADO: {estado}")

            for alerta in alertas:
                print(f"  - {alerta}")

            calcular_ruta_trekking(
                lat_origen,
                lon_origen,
                lat_destino,
                lon_destino
            )

        else:
            print(
                "❌ La estación meteorológica no responde."
            )

    else:
        print(
            "❌ No pudimos ubicar los puntos en el mapa."
        )

    print("\n" + "=" * 55)

    print(
        " Respeta la montaña. "
        "Tu seguridad es lo primero. 🌲"
    )

    print("=" * 55 + "\n")


if __name__ == "__main__":
    main()
