import pandas as pd
import re

def categorizar_texto(texto):
    """
    Función para categorizar el texto según la lógica del documento de LinkedIn
    """
    texto_lower = texto.lower()
    
    # VINCULO DE NEGOCIO
    if any(palabra in texto_lower for palabra in ['talento', 'colaborador', 'empleado', 'equipo', 'liderazgo', 'desarrollo profesional', 'universidad corporativa', 'beca']):
        vinculo_negocio = "IMPULSAR AL TALENTO"
    elif any(palabra in texto_lower for palabra in ['inversión', 'expansión', 'transformación digital', 'e-commerce', 'plataforma', 'tienda', 'servicios financieros', 'crédito', 'inclusión financiera']):
        vinculo_negocio = "VISIBILIZAR OFERTA DE VALOR"
    elif any(palabra in texto_lower for palabra in ['fundación', 'comunidad', 'sostenibilidad', 'asg', 'salud', 'educación', 'arte', 'mexicano', 'impacto social', 'bienestar']):
        vinculo_negocio = "CONTRIBUIR Y REDUCIR RIESGOS"
    else:
        vinculo_negocio = "IMPULSAR AL TALENTO"  # Por defecto
    
    # PILAR
    if any(palabra in texto_lower for palabra in ['talento', 'colaborador', 'empleado', 'equipo', 'liderazgo', 'desarrollo profesional', 'universidad corporativa', 'beca']):
        pilar = "MARCA EMPLEADORA"
    elif any(palabra in texto_lower for palabra in ['inversión', 'expansión', 'transformación digital', 'e-commerce', 'plataforma', 'tienda', 'servicios financieros', 'crédito', 'inclusión financiera', 'omnicanal']):
        pilar = "OMNICANALIDAD"
    elif any(palabra in texto_lower for palabra in ['fundación', 'comunidad', 'sostenibilidad', 'asg', 'salud', 'educación', 'arte', 'mexicano', 'impacto social', 'bienestar']):
        pilar = "COMUNIDAD"
    else:
        pilar = "MARCA EMPLEADORA"  # Por defecto
    
    # TEMA
    if any(palabra in texto_lower for palabra in ['talento', 'colaborador', 'empleado', 'equipo', 'liderazgo', 'desarrollo profesional', 'universidad corporativa', 'beca']):
        tema = "DESARROLLO PROFESIONAL"
    elif any(palabra in texto_lower for palabra in ['inversión', 'expansión', 'transformación digital', 'e-commerce', 'plataforma', 'tienda', 'servicios financieros', 'crédito', 'inclusión financiera', 'omnicanal']):
        tema = "CATEGORÍAS COMERCIALES Y FINANCIERAS"
    elif any(palabra in texto_lower for palabra in ['fundación', 'salud', 'educación']):
        tema = "FUNDACIÓN COPPEL"
    elif any(palabra in texto_lower for palabra in ['sostenibilidad', 'asg', 'arte', 'mexicano', 'impacto social', 'bienestar']):
        tema = "SOSTENIBILIDAD Y ASG"
    else:
        tema = "PROPUESTA DE VALOR"  # Por defecto
    
    return vinculo_negocio, pilar, tema

def main():
    # Leer el archivo de Coppel
    print("Leyendo archivo Coppel_X_Merge_2025.csv...")
    df_coppel = pd.read_csv('Coppel_X_Merge_2025.csv')
    
    print(f"Archivo leído con {len(df_coppel)} filas")
    
    # Aplicar categorización a cada fila
    print("Aplicando categorización...")
    categorias = []
    
    for index, row in df_coppel.iterrows():
        texto = str(row['Text'])
        vinculo, pilar, tema = categorizar_texto(texto)
        categorias.append({
            'VINCULO_DE_NEGOCIO': vinculo,
            'PILAR': pilar,
            'Tema': tema
        })
    
    # Crear DataFrame con las categorías
    df_categorias = pd.DataFrame(categorias)
    
    # Concatenar las columnas originales con las nuevas categorías
    df_final = pd.concat([df_coppel, df_categorias], axis=1)
    
    # Crear directorio si no existe
    import os
    if not os.path.exists('Data_Sources'):
        os.makedirs('Data_Sources')
    
    # Guardar archivo categorizado
    nombre_archivo = 'Data_Sources/Coppel_X_Merge_2025_Categorized_01.csv'
    df_final.to_csv(nombre_archivo, index=False, encoding='utf-8')
    
    print(f"Archivo categorizado guardado como: {nombre_archivo}")
    
    # Mostrar resumen de categorización
    print("\nResumen de categorización:")
    print("VINCULO DE NEGOCIO:")
    print(df_final['VINCULO_DE_NEGOCIO'].value_counts())
    print("\nPILAR:")
    print(df_final['PILAR'].value_counts())
    print("\nTEMA:")
    print(df_final['Tema'].value_counts())
    
    # Mostrar algunas filas de ejemplo
    print("\nPrimeras 5 filas categorizadas:")
    columnas_mostrar = ['Text', 'VINCULO_DE_NEGOCIO', 'PILAR', 'Tema']
    print(df_final[columnas_mostrar].head())

if __name__ == "__main__":
    main()
