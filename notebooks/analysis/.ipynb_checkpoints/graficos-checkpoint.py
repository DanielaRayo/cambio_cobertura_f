import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

def graficar_ndvi_vs_precipitacion(df):
    df = df.dropna(subset=['NDVI_promedio', 'Precipitacion_mm'])

    df['NDVI_norm'] = (df['NDVI_promedio'] - df['NDVI_promedio'].min()) / (df['NDVI_promedio'].max() - df['NDVI_promedio'].min())
    df['Precip_norm'] = (df['Precipitacion_mm'] - df['Precipitacion_mm'].min()) / (df['Precipitacion_mm'].max() - df['Precipitacion_mm'].min())

    fig, ax = plt.subplots(figsize=(14, 6))

    ax.plot(df['Año'], df['NDVI_norm'], 'g-o', label='NDVI (normalizado)', linewidth=2)
    ax.plot(df['Año'], df['Precip_norm'], 'b-s', label='Precipitación (normalizada)', linewidth=2)

    for i in range(len(df)):
        ax.text(df['Año'].iloc[i], df['NDVI_norm'].iloc[i] + 0.02, f"{df['NDVI_promedio'].iloc[i]:.2f}", color='green', ha='center', fontsize=8)
        ax.text(df['Año'].iloc[i], df['Precip_norm'].iloc[i] - 0.04, f"{int(df['Precipitacion_mm'].iloc[i])}", color='blue', ha='center', fontsize=8)

    ax.set_ylabel("Valores normalizados (0–1)")
    ax.set_title("NDVI vs Precipitación (valores normalizados)")
    ax.set_xticks(df['Año'])
    ax.xaxis.set_major_formatter(mticker.FormatStrFormatter('%d'))
    plt.xticks(rotation=45)
    plt.grid(True)
    ax.legend()
    plt.tight_layout()
    plt.show()

def mostrar_landtrendr_fitted(fitted_stack, years, aoi):
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    from matplotlib.colorbar import ColorbarBase
    from utils.display import mostrar_imagen_ee

    fig, axes = plt.subplots(1, len(years), figsize=(6 * len(years), 5))

    for i, year in enumerate(years):
        banda = fitted_stack.select(f'fittedResidual_{year}')

        mostrar_imagen_ee(
            imagen=banda,
            region=aoi,
            titulo=f'Fitted NDVI {year}',
            min_val=-0.2,
            max_val=0.8,
            palette=["ff0000", "ffffff", "00ff00"],
            ax=axes[i] if len(years) > 1 else axes,
            barra_color=False
        )

    plt.tight_layout()
    plt.show()
