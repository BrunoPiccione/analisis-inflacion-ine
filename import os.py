
import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog

# Esto oculta la ventana gris fea de fondo de tkinter
root = tk.Tk()
root.withdraw()
root.attributes('-topmost', True)

print("¡ATENCIÓN! Se acaba de abrir una ventana de Windows en tu pantalla.")
print("Busca tu archivo del INE y hazle doble clic...\n")

# Abre el explorador de archivos de Windows para que elijas el CSV con el ratón
ruta_elegida = filedialog.askopenfilename(
    title="Selecciona el archivo CSV del INE",
    filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
)

if ruta_elegida:
    print(f"Has seleccionado: {ruta_elegida}")
    try:
        # Python lee el archivo usando la ruta que tú tocaste con el ratón
        df = pd.read_csv(ruta_elegida, sep=';', encoding='latin-1', decimal=',')
        
        print("\n¡POR FIN! CARGADO CON ÉXITO. AQUÍ TIENES TUS DATOS:")
        print("====================================================")
        print(df.head(5))
        print("====================================================")
        print(f"Total de filas cargadas: {len(df)}")
        
    except Exception as e:
        print(f"\nError al leer el archivo: {e}")
else:
    print("No seleccionaste ningún archivo.")

input("\nPresiona Enter para salir...")

import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog

# Ventana visual para elegir el archivo
root = tk.Tk()
root.withdraw()
root.attributes('-topmost', True)

ruta_elegida = filedialog.askopenfilename(
    title="Selecciona el archivo CSV del INE",
    filetypes=[("Archivos CSV", "*.csv")]
)

if ruta_elegida:
    try:
        df = pd.read_csv(ruta_elegida, sep=';', encoding='latin-1', decimal=',')
        
        print("\n====================================================")
        print("          ¡INICIANDO EL ANÁLISIS DE DATOS!          ")
        print("====================================================\n")
        
        # 1. Ver qué sectores hay en el archivo
        print("1. SECTORES ECONÓMICOS DETECTADOS:")
        sectores = df['General y Grupos ECOICOP ver.2'].unique()
        for s in sectores:
            print(f"   -> {s}")
            
        # 2. Eliminar los valores vacíos (NaN)
        df_limpio = df.dropna(subset=['Total'])
        
        # 3. Buscar el récord de inflación (la mayor subida)
        print("\n2. TOP 3 DE MAYORES SUBIDAS DE PRECIOS REGISTRADAS:")
        top_subidas = df_limpio.sort_values(by='Total', ascending=False).head(3)
        print(top_subidas[['General y Grupos ECOICOP ver.2', 'Periodo', 'Total']])
        
        # 4. Buscar la mayor bajada de precios
        print("\n3. TOP 3 DE MAYORES BAJADAS DE PRECIOS REGISTRADAS:")
        top_bajadas = df_limpio.sort_values(by='Total', ascending=True).head(3)
        print(top_bajadas[['General y Grupos ECOICOP ver.2', 'Periodo', 'Total']])

    except Exception as e:
        print(f"Error analizando los datos: {e}")
else:
    print("No seleccionaste ningún archivo.") 
    
    import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog

# 1. Ventana visual para elegir el archivo
root = tk.Tk()
root.withdraw()
root.attributes('-topmost', True)

ruta_elegida = filedialog.askopenfilename(
    title="Selecciona el archivo CSV del INE",
    filetypes=[("Archivos CSV", "*.csv")]
)

if ruta_elegida:
    try:
        # 2. Cargar datos
        df = pd.read_csv(ruta_elegida, sep=';', encoding='latin-1', decimal=',')
        
        # 3. Filtrar solo Alimentos y ordenarlos por fecha (de más antiguo a más reciente)
        df_alimentos = df[df['General y Grupos ECOICOP ver.2'].str.contains('Alimentos', na=False, case=False)].copy()
        df_alimentos = df_alimentos.dropna(subset=['Total'])
        df_alimentos = df_alimentos.sort_values(by='Periodo', ascending=True)
        
        # 4. EXPORTAR A UN NUEVO ARCHIVO: Guardamos el resultado limpio
        carpeta_guardado = os.path.dirname(ruta_elegida)
        ruta_salida = os.path.join(carpeta_guardado, "reporte_alimentos_limpio.csv")
        df_alimentos.to_csv(ruta_salida, index=False, sep=';', encoding='utf-8-sig')
        
        print("\n====================================================")
        print("¡ANÁLISIS COMPLETADO EXITOSAMENTE!")
        print("====================================================")
        print(f"1. Se ha creado un archivo limpio en: {ruta_salida}")
        print("   (Ya puedes abrir ese nuevo archivo directamente en Excel).")
        
        # 5. INTENTAR CREAR EL GRÁFICO (Si tienes matplotlib instalado)
        try:
            import matplotlib.pyplot as plt
            
            plt.figure(figsize=(12, 6))
            # Tomamos los últimos 24 meses para que el gráfico no esté saturado
            df_reciente = df_alimentos.tail(24)
            
            plt.plot(df_reciente['Periodo'], df_reciente['Total'], marker='o', color='red', linewidth=2)
            plt.title('Evolución de la Inflación Mensual en Alimentos (Últimos 2 años)', fontsize=14)
            plt.xlabel('Mes (Periodo)', fontsize=12)
            plt.ylabel('Variación Mensual (%)', fontsize=12)
            plt.xticks(rotation=45)
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()
            
            # Guardamos el gráfico como imagen
            ruta_grafico = os.path.join(carpeta_guardado, "grafico_inflacion_alimentos.png")
            plt.savefig(ruta_grafico)
            print(f"2. Se ha guardado un gráfico automático en: {ruta_grafico}")
            plt.show()
            
        except ImportError:
            print("\n* Nota: Para ver el gráfico automático, necesitaríamos instalar la librería 'matplotlib'.")
            print("  Por ahora, concéntrate en el archivo Excel que se acaba de crear.")

    except Exception as e:
        print(f"Error en el análisis: {e}")
else:
    print("No seleccionaste ningún archivo.")