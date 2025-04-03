import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString
from matplotlib.patches import FancyArrowPatch, Patch
from matplotlib.colors import to_rgba


def tecnica_1():
    # Crear un DataFrame con datos aproximados del gasto público por áreas en España (2010-2024)
    years = list(range(2010, 2025))
    data = {
        "Protección Social": [
            160, 165, 170, 180, 190, 200, 210, 225, 240, 255, 270, 285, 300, 320, 340
        ],
        "Sanidad": [
            60, 62, 64, 66, 68, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115
        ],
        "Educación": [
            40, 41, 42, 43, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64
        ],
        "Defensa": [
            12, 12, 13, 13, 14, 14, 15, 15, 16, 17, 17, 18, 18, 19, 20
        ],
        "Vivienda": [
            4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 8, 8, 9, 9
        ]
    }

    df = pd.DataFrame(data, index=years)

    # Crear el gráfico de barras apiladas
    df.plot(kind='bar', stacked=True, figsize=(14, 7))

    plt.title("Evolución del Gasto Público por Áreas en España (2010–2024)")
    plt.xlabel("Año")
    plt.ylabel("Miles de millones de euros")
    plt.legend(title="Áreas de gasto")
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()


def tecnica_2():
    # Load shapefile
    world = gpd.read_file(
        r"c:\Users\prabh\Desktop\FOLDERS\UOC\Cuatri_2\Visualizacion de datos\PEC2\Graficas_PEC2\ne_110m_admin_0_countries\ne_110m_admin_0_countries.shp"
    )

    # Normalize country names
    world['NAME'] = world['NAME'].str.strip().str.title()
    world['NAME_lower'] = world['NAME'].str.lower()

    # European countries to plot as base
    european_countries = [
        'France', 'Germany', 'Italy', 'Spain', 'Portugal', 'Poland', 'Sweden', 'Norway',
        'Finland', 'Denmark', 'Netherlands', 'Belgium', 'Austria', 'Greece', 'Switzerland',
        'Czechia', 'Slovakia', 'Hungary', 'Romania', 'Bulgaria', 'Ireland', 'United Kingdom',
        'Croatia', 'Slovenia', 'Lithuania', 'Latvia', 'Estonia', 'Serbia', 'Bosnia and Herzegovina',
        'Albania', 'North Macedonia', 'Montenegro', 'Ukraine', 'Moldova'
    ]
    europe = world[world['NAME'].isin(european_countries)]

    # Simulated migration flows
    flows = [
        {"origin": "Syria", "dest": "Germany", "migrants": 800000},
        {"origin": "Afghanistan", "dest": "Germany", "migrants": 200000},
        {"origin": "Iraq", "dest": "Sweden", "migrants": 150000},
        {"origin": "Eritrea", "dest": "Italy", "migrants": 120000},
        {"origin": "Nigeria", "dest": "Italy", "migrants": 180000},
        {"origin": "Sudan", "dest": "France", "migrants": 110000},
        {"origin": "Ukraine", "dest": "Poland", "migrants": 1000000},
        {"origin": "Ukraine", "dest": "Germany", "migrants": 900000},
        {"origin": "Turkey", "dest": "Greece", "migrants": 400000},
        {"origin": "Morocco", "dest": "Spain", "migrants": 300000}
    ]

    # Region-color mapping
    region_colors = {
        'Africa': 'green',
        'Asia': 'blue',
        'Eastern Europe': 'red'
    }
    africa = {"nigeria", "eritrea", "sudan", "morocco"}
    asia = {"syria", "iraq", "afghanistan"}
    eastern_europe = {"ukraine", "turkey"}

    # Color selector function
    def get_region_color(country):
        name = country.strip().lower()
        if name in africa:
            return region_colors['Africa']
        elif name in asia:
            return region_colors['Asia']
        elif name in eastern_europe:
            return region_colors['Eastern Europe']
        else:
            return "gray"

    fig, ax = plt.subplots(figsize=(12, 10))

    # Highlight origin countries in soft color
    origin_countries = {flow['origin'] for flow in flows}
    for country in origin_countries:
        norm_country = country.strip().lower()
        color = get_region_color(country)
        shape = world[world['NAME_lower'] == norm_country]
        if not shape.empty:
            shape.plot(ax=ax, color=to_rgba(color, alpha=0.3), edgecolor='none')
        else:
            print(f"[!] Could NOT find '{country}' in shapefile")

    # Base map of Europe
    europe.plot(ax=ax, color='lightgrey', edgecolor='white')

    # Draw curved arrows for each flow
    for flow in flows:
        origin = world[world['NAME_lower'] == flow["origin"].strip().lower()].geometry.centroid
        dest = europe[europe['NAME'] == flow["dest"]].geometry.centroid
        if not origin.empty and not dest.empty:
            x0, y0 = origin.iloc[0].x, origin.iloc[0].y
            x1, y1 = dest.iloc[0].x, dest.iloc[0].y
            color = get_region_color(flow["origin"])
            arrow = FancyArrowPatch(
                (x0, y0), (x1, y1),
                arrowstyle='-|>',
                connectionstyle="arc3,rad=0.2",
                color=to_rgba(color, alpha=0.6),
                linewidth=max(1.5, flow["migrants"] / 80000),
                mutation_scale=15
            )
            ax.add_patch(arrow)

    # Legend
    legend_elements = [
        Patch(facecolor='green', edgecolor='green', label='África'),
        Patch(facecolor='blue', edgecolor='blue', label='Asia'),
        Patch(facecolor='red', edgecolor='red', label='Europa del Este')
    ]
    ax.legend(handles=legend_elements, loc='lower left', fontsize=10, frameon=False)

    # Title and cleanup
    ax.set_title("Flujos Migratorios en Europa (2022)", fontsize=15)
    ax.set_xlim(-25, 45)
    ax.set_ylim(25, 75)
    ax.axis('off')
    plt.tight_layout()
    plt.show()


def tecnica_3():
    # Datos simulados de posiciones por jornada para los 20 equipos de la Premier League
    data = {
        'Jornada': list(range(1, 39)),
        'Manchester City':     [3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 3, 1, 2, 4, 5, 4, 3, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 1, 2, 2, 2, 1, 1],
        'Arsenal':             [4, 3, 5, 5, 3, 3, 2, 2, 3, 2, 3, 4, 4, 3, 2, 2, 1, 2, 2, 4, 4, 3, 3, 3, 3, 3, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        'Liverpool':           [12, 5, 4, 3, 4, 4, 4, 4, 3, 4, 3, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        'Aston Villa':         [20, 9, 6, 7, 6, 6, 6, 5, 5, 5, 5, 5, 5, 4, 4, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4],
        'Tottenham Hotspur':   [9, 6, 3, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        'Manchester United':   [8, 8, 8, 8, 8, 8, 6, 6, 6, 6, 6, 6, 7, 7, 7, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 6, 6, 6, 8, 8, 8, 8, 8, 8],
        'Newcastle United':    [1, 8, 13, 14, 13, 14, 14, 8, 8, 8, 8, 8, 6, 6, 6, 6, 6, 6, 6, 7, 9, 9, 9, 10, 10, 10, 10, 10, 8, 8, 8, 8, 7, 7, 7, 7, 7, 7],
        'Chelsea':             [11, 10, 12, 14, 14, 13, 11, 11, 11, 11, 11, 10, 10, 10, 10, 10, 11, 11, 11, 10, 10, 10, 10, 10, 11, 11, 11, 11, 10, 9, 9, 9, 9, 9, 9, 9, 6, 6],
        'Brighton & Hove Albion': [2, 1, 6, 4, 5, 5, 4, 6, 7, 7, 7, 7, 7, 7, 7, 7, 8, 9, 9, 9, 9, 8, 8, 9, 9, 9, 8, 8, 9, 9, 10, 10, 10, 10, 11, 11, 10, 10],
        'Brentford':           [6, 13, 7, 10, 10, 9, 9, 9, 9, 9, 10, 10, 10, 11, 12, 13, 14, 14, 14, 14, 14, 14, 14, 15, 15, 15, 15, 15, 14, 14, 14, 14, 14, 14, 14, 14, 15, 15],
        'Fulham':              [6, 13, 10, 13, 13, 12, 13, 13, 13, 13, 13, 13, 13, 13, 15, 15, 15, 15, 15, 15, 13, 13, 13, 13, 13, 13, 13, 13, 12, 12, 13, 13, 13, 13, 13, 13, 13, 13],
        'Crystal Palace':      [5, 11, 11, 10, 11, 11, 10, 12, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 14, 14, 15, 15, 15, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14],
        'West Ham United':     [13, 2, 4, 6, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9, 9, 9, 9, 9, 8, 8, 8, 8, 8, 8, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 9, 9],
        'Wolverhampton Wanderers': [17, 19, 15, 15, 15, 15, 15, 15, 14, 14, 14, 14, 14, 14, 10, 10, 10, 10, 11, 11, 11, 11, 9, 9, 9, 9, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11],
        'Everton':             [15, 20, 20, 18, 18, 18, 18, 18, 18, 16, 16, 16, 16, 16, 18, 18, 18, 18, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16],
        'Bournemouth':         [10, 14, 16, 16, 17, 17, 17, 19, 19, 17, 15, 14, 14, 14, 12, 12, 12, 12, 12, 12, 12, 12, 13, 13, 13, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
        'Nottingham Forest':   [14, 10, 8, 11, 12, 10, 12, 17, 17, 18, 18, 18, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17],
        'Luton Town':          [17, 17, 19, 20, 19, 19, 19, 18, 18, 19, 19, 19, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18],
        'Burnley':             [18, 18, 18, 19, 20, 20, 20, 20, 20, 20, 20, 20, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19],
        'Sheffield United':    [16, 16, 17, 17, 16, 16, 16, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20],
    }

    df = pd.DataFrame(data)
    jornadas = df['Jornada']

    # Crear gráfico
    plt.figure(figsize=(16, 12))

    for team in df.columns[1:]:
        plt.plot(jornadas, df[team], linewidth=2)

    # Invertir eje Y (posición 1 arriba)
    plt.gca().invert_yaxis()

    # Añadir nombres de equipos al final de las líneas, fuera del grid
    for team in df.columns[1:]:
        y = df[team].iloc[-1]
        plt.text(jornadas.max() + 0.5, y, team, va='center', ha='left', fontsize=9)

    # Ajustar límites para dejar espacio a la derecha
    plt.xlim(jornadas.min(), jornadas.max() - 4)

    # Ejes y estilo
    plt.yticks(range(1, 21), [str(i) for i in range(1, 21)])
    plt.xticks(jornadas)
    plt.xlabel('Jornada')
    plt.ylabel('Posición')
    plt.title('Evolución de la Clasificación - Premier League 2023-2024')
    plt.grid(True, axis='y', linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.show()



#tecnica_1()
tecnica_2()
#tecnica_3()