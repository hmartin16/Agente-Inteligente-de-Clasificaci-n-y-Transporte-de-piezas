    # Graficar puntos de muestra con una cruz
                for i, muestra in enumerate(muestra_reducida):
                    etiqueta_muestra = self.etiquetas_muestra[i]
                    etiqueta_color = colores[etiqueta_muestra]
                    ax.scatter(
                        muestra[0], muestra[1], muestra[2], marker='x', s=100,
                        c=etiqueta_color, label=f"Muestra {i+1} ({etiqueta_muestra})"
                    )

