#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análisis Completo de Datos de Twitter/X de Coppel
Junio-Julio 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime
import re

def load_and_clean_data():
    """Cargar y limpiar los datos del CSV"""
    df = pd.read_csv('/mnt/d/2025_Disco/Coppel_TW_Reporte/Data_Sources/Coppel_X_Merge_2025_Categorized_01.csv')
    
    # Convertir fecha a datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    
    # Crear columnas de mes y semana
    df['Mes'] = df['Date'].dt.month_name()
    df['Semana'] = df['Date'].dt.isocalendar().week
    
    # Limpiar valores numéricos y convertir a float
    numeric_cols = ['Impresiones', 'Interacciones', 'Engagement_Rate', 
                   'Ampliaciones de detalles', 'Visitas del perfil', 'Clics en enlaces',
                   'Reacciones ', 'Reposteos', 'Comentarios', 'Reproducciones únicas', 'Reproducciones']
    
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

def analyze_content_themes(df):
    """1. Categorización de contenido por Tema"""
    print("="*80)
    print("1. ANÁLISIS DE TEMAS DE CONTENIDO")
    print("="*80)
    
    tema_stats = df.groupby('Tema').agg({
        'Date': 'count',
        'Impresiones': ['mean', 'sum'],
        'Interacciones': ['mean', 'sum'],
        'Engagement_Rate': 'mean'
    }).round(2)
    
    tema_stats.columns = ['Frecuencia', 'Impresiones_Promedio', 'Impresiones_Total', 
                         'Interacciones_Promedio', 'Interacciones_Total', 'Engagement_Rate_Promedio']
    
    tema_stats = tema_stats.sort_values('Engagement_Rate_Promedio', ascending=False)
    
    print("\nDistribución y Rendimiento por Tema:")
    print(tema_stats)
    
    print(f"\nTemas únicos identificados: {df['Tema'].nunique()}")
    print("\nTemas ordenados por Engagement Rate:")
    for i, (tema, rate) in enumerate(tema_stats['Engagement_Rate_Promedio'].items(), 1):
        freq = tema_stats.loc[tema, 'Frecuencia']
        print(f"{i}. {tema}: {rate}% (Frecuencia: {freq})")
    
    return tema_stats

def analyze_pillars(df):
    """2. Análisis de Pilares"""
    print("\n" + "="*80)
    print("2. ANÁLISIS DE PILARES ESTRATÉGICOS")
    print("="*80)
    
    pilar_stats = df.groupby('PILAR').agg({
        'Date': 'count',
        'Impresiones': ['mean', 'sum'],
        'Interacciones': ['mean', 'sum'],
        'Engagement_Rate': 'mean'
    }).round(2)
    
    pilar_stats.columns = ['Frecuencia', 'Impresiones_Promedio', 'Impresiones_Total', 
                          'Interacciones_Promedio', 'Interacciones_Total', 'Engagement_Rate_Promedio']
    
    pilar_stats = pilar_stats.sort_values('Engagement_Rate_Promedio', ascending=False)
    
    print("\nDistribución y Rendimiento por Pilar:")
    print(pilar_stats)
    
    print(f"\nPilares únicos identificados: {df['PILAR'].nunique()}")
    print("\nPilares ordenados por Engagement Rate:")
    for i, (pilar, rate) in enumerate(pilar_stats['Engagement_Rate_Promedio'].items(), 1):
        freq = pilar_stats.loc[pilar, 'Frecuencia']
        print(f"{i}. {pilar}: {rate}% (Frecuencia: {freq})")
    
    return pilar_stats

def analyze_business_links(df):
    """3. Análisis de Vínculos de Negocio"""
    print("\n" + "="*80)
    print("3. ANÁLISIS DE VÍNCULOS DE NEGOCIO")
    print("="*80)
    
    vinculo_stats = df.groupby('VINCULO_DE_NEGOCIO').agg({
        'Date': 'count',
        'Impresiones': ['mean', 'sum'],
        'Interacciones': ['mean', 'sum'],
        'Engagement_Rate': 'mean'
    }).round(2)
    
    vinculo_stats.columns = ['Frecuencia', 'Impresiones_Promedio', 'Impresiones_Total', 
                            'Interacciones_Promedio', 'Interacciones_Total', 'Engagement_Rate_Promedio']
    
    vinculo_stats = vinculo_stats.sort_values('Engagement_Rate_Promedio', ascending=False)
    
    print("\nDistribución y Rendimiento por Vínculo de Negocio:")
    print(vinculo_stats)
    
    print(f"\nVínculos de negocio únicos: {df['VINCULO_DE_NEGOCIO'].nunique()}")
    print("\nVínculos ordenados por Engagement Rate:")
    for i, (vinculo, rate) in enumerate(vinculo_stats['Engagement_Rate_Promedio'].items(), 1):
        freq = vinculo_stats.loc[vinculo, 'Frecuencia']
        print(f"{i}. {vinculo}: {rate}% (Frecuencia: {freq})")
    
    return vinculo_stats

def analyze_performance_metrics(df):
    """4. Análisis de Rendimiento por Categoría"""
    print("\n" + "="*80)
    print("4. MÉTRICAS DE RENDIMIENTO DETALLADAS")
    print("="*80)
    
    # Estadísticas generales
    print("\nESTADÍSTICAS GENERALES:")
    print(f"Total de publicaciones: {len(df)}")
    print(f"Período: {df['Date'].min().strftime('%d/%m/%Y')} - {df['Date'].max().strftime('%d/%m/%Y')}")
    print(f"Impresiones totales: {df['Impresiones'].sum():,.0f}")
    print(f"Interacciones totales: {df['Interacciones'].sum():,.0f}")
    print(f"Engagement Rate promedio general: {df['Engagement_Rate'].mean():.2f}%")
    
    # Top performers por métricas
    print("\nTOP 3 PUBLICACIONES POR ENGAGEMENT RATE:")
    top_engagement = df.nlargest(3, 'Engagement_Rate')[['Date', 'Text', 'Engagement_Rate', 'Impresiones', 'Interacciones']]
    for idx, row in top_engagement.iterrows():
        print(f"\n{row['Date'].strftime('%d/%m/%Y')} - ER: {row['Engagement_Rate']}%")
        print(f"Impresiones: {row['Impresiones']:,.0f} | Interacciones: {row['Interacciones']:,.0f}")
        print(f"Texto: {row['Text'][:100]}...")
    
    print("\nTOP 3 PUBLICACIONES POR IMPRESIONES:")
    top_impressions = df.nlargest(3, 'Impresiones')[['Date', 'Text', 'Engagement_Rate', 'Impresiones', 'Interacciones']]
    for idx, row in top_impressions.iterrows():
        print(f"\n{row['Date'].strftime('%d/%m/%Y')} - Impresiones: {row['Impresiones']:,.0f}")
        print(f"ER: {row['Engagement_Rate']}% | Interacciones: {row['Interacciones']:,.0f}")
        print(f"Texto: {row['Text'][:100]}...")
    
    print("\nTOP 3 PUBLICACIONES POR INTERACCIONES:")
    top_interactions = df.nlargest(3, 'Interacciones')[['Date', 'Text', 'Engagement_Rate', 'Impresiones', 'Interacciones']]
    for idx, row in top_interactions.iterrows():
        print(f"\n{row['Date'].strftime('%d/%m/%Y')} - Interacciones: {row['Interacciones']:,.0f}")
        print(f"ER: {row['Engagement_Rate']}% | Impresiones: {row['Impresiones']:,.0f}")
        print(f"Texto: {row['Text'][:100]}...")

def analyze_best_performers(df, tema_stats, pilar_stats, vinculo_stats):
    """5. Mejores Performers"""
    print("\n" + "="*80)
    print("5. MEJORES PERFORMERS")
    print("="*80)
    
    print("MEJOR TEMA:")
    best_tema = tema_stats.index[0]
    print(f"- {best_tema}")
    print(f"  Engagement Rate: {tema_stats.loc[best_tema, 'Engagement_Rate_Promedio']}%")
    print(f"  Frecuencia: {tema_stats.loc[best_tema, 'Frecuencia']} publicaciones")
    print(f"  Impresiones promedio: {tema_stats.loc[best_tema, 'Impresiones_Promedio']:,.0f}")
    
    print("\nMEJOR PILAR:")
    best_pilar = pilar_stats.index[0]
    print(f"- {best_pilar}")
    print(f"  Engagement Rate: {pilar_stats.loc[best_pilar, 'Engagement_Rate_Promedio']}%")
    print(f"  Frecuencia: {pilar_stats.loc[best_pilar, 'Frecuencia']} publicaciones")
    print(f"  Impresiones promedio: {pilar_stats.loc[best_pilar, 'Impresiones_Promedio']:,.0f}")
    
    print("\nMEJOR VÍNCULO DE NEGOCIO:")
    best_vinculo = vinculo_stats.index[0]
    print(f"- {best_vinculo}")
    print(f"  Engagement Rate: {vinculo_stats.loc[best_vinculo, 'Engagement_Rate_Promedio']}%")
    print(f"  Frecuencia: {vinculo_stats.loc[best_vinculo, 'Frecuencia']} publicaciones")
    print(f"  Impresiones promedio: {vinculo_stats.loc[best_vinculo, 'Impresiones_Promedio']:,.0f}")

def analyze_temporal_patterns(df):
    """6. Patrones Temporales - Junio vs Julio"""
    print("\n" + "="*80)
    print("6. ANÁLISIS TEMPORAL: JUNIO VS JULIO")
    print("="*80)
    
    monthly_stats = df.groupby('Mes').agg({
        'Date': 'count',
        'Impresiones': ['mean', 'sum'],
        'Interacciones': ['mean', 'sum'],
        'Engagement_Rate': 'mean'
    }).round(2)
    
    monthly_stats.columns = ['Publicaciones', 'Impresiones_Promedio', 'Impresiones_Total', 
                            'Interacciones_Promedio', 'Interacciones_Total', 'Engagement_Rate_Promedio']
    
    print("\nComparación Mensual:")
    print(monthly_stats)
    
    # Análisis de cambios
    if 'June' in monthly_stats.index and 'July' in monthly_stats.index:
        june_er = monthly_stats.loc['June', 'Engagement_Rate_Promedio']
        july_er = monthly_stats.loc['July', 'Engagement_Rate_Promedio']
        er_change = ((july_er - june_er) / june_er) * 100
        
        june_imp = monthly_stats.loc['June', 'Impresiones_Promedio']
        july_imp = monthly_stats.loc['July', 'Impresiones_Promedio']
        imp_change = ((july_imp - june_imp) / june_imp) * 100
        
        print(f"\nCAMBIOS DE JUNIO A JULIO:")
        print(f"Engagement Rate: {er_change:+.1f}%")
        print(f"Impresiones promedio: {imp_change:+.1f}%")
    
    # Análisis por tema en cada mes
    print("\nRendimiento por Tema por Mes:")
    tema_mes = df.groupby(['Mes', 'Tema'])['Engagement_Rate'].mean().round(2)
    for mes in tema_mes.index.get_level_values(0).unique():
        print(f"\n{mes.upper()}:")
        mes_data = tema_mes[mes].sort_values(ascending=False)
        for tema, rate in mes_data.items():
            print(f"  {tema}: {rate}%")

def analyze_correlations(df):
    """7. Análisis de Correlaciones"""
    print("\n" + "="*80)
    print("7. ANÁLISIS DE CORRELACIONES")
    print("="*80)
    
    # Matriz de correlaciones para métricas numéricas
    numeric_cols = ['Impresiones', 'Interacciones', 'Engagement_Rate', 
                   'Ampliaciones de detalles', 'Visitas del perfil', 'Reacciones ', 'Reposteos', 'Comentarios']
    
    correlation_matrix = df[numeric_cols].corr().round(3)
    
    print("\nMatriz de Correlaciones (métricas principales):")
    print("Impresiones vs Interacciones:", correlation_matrix.loc['Impresiones', 'Interacciones'])
    print("Impresiones vs Engagement_Rate:", correlation_matrix.loc['Impresiones', 'Engagement_Rate'])
    print("Interacciones vs Engagement_Rate:", correlation_matrix.loc['Interacciones', 'Engagement_Rate'])
    
    # Análisis de patrones de contenido
    print("\nPatrones de Contenido:")
    
    # Longitud del texto vs engagement
    df['Longitud_Texto'] = df['Text'].str.len()
    text_engagement_corr = df['Longitud_Texto'].corr(df['Engagement_Rate'])
    print(f"Correlación longitud de texto vs Engagement Rate: {text_engagement_corr:.3f}")
    
    # Uso de hashtags
    df['Num_Hashtags'] = df['Text'].str.count('#')
    hashtag_engagement_corr = df['Num_Hashtags'].corr(df['Engagement_Rate'])
    print(f"Correlación número de hashtags vs Engagement Rate: {hashtag_engagement_corr:.3f}")
    
    # Menciones
    df['Num_Menciones'] = df['Text'].str.count('@')
    mention_engagement_corr = df['Num_Menciones'].corr(df['Engagement_Rate'])
    print(f"Correlación número de menciones vs Engagement Rate: {mention_engagement_corr:.3f}")

def generate_insights_and_recommendations(df, tema_stats, pilar_stats, vinculo_stats):
    """8. Insights y Recomendaciones Estratégicas"""
    print("\n" + "="*80)
    print("8. INSIGHTS CLAVE Y RECOMENDACIONES ESTRATÉGICAS")
    print("="*80)
    
    print("\nINSIGHTS CLAVE:")
    
    # 1. Rendimiento por categorías
    best_tema = tema_stats.index[0]
    worst_tema = tema_stats.index[-1]
    print(f"\n1. RENDIMIENTO POR TEMAS:")
    print(f"   ✓ Mejor tema: '{best_tema}' ({tema_stats.loc[best_tema, 'Engagement_Rate_Promedio']}% ER)")
    print(f"   ✗ Tema con menor rendimiento: '{worst_tema}' ({tema_stats.loc[worst_tema, 'Engagement_Rate_Promedio']}% ER)")
    
    # 2. Distribución de contenido
    total_posts = len(df)
    tema_distribution = (tema_stats['Frecuencia'] / total_posts * 100).round(1)
    print(f"\n2. DISTRIBUCIÓN DE CONTENIDO:")
    for tema, pct in tema_distribution.items():
        print(f"   {tema}: {pct}% del contenido total")
    
    # 3. Variabilidad en engagement
    cv_engagement = (df['Engagement_Rate'].std() / df['Engagement_Rate'].mean()) * 100
    print(f"\n3. CONSISTENCIA:")
    print(f"   Coeficiente de variación del Engagement Rate: {cv_engagement:.1f}%")
    if cv_engagement > 100:
        print("   ⚠️  Alta variabilidad en el rendimiento del contenido")
    
    # 4. Alcance vs Engagement
    high_reach_low_engagement = df[(df['Impresiones'] > df['Impresiones'].median()) & 
                                   (df['Engagement_Rate'] < df['Engagement_Rate'].median())]
    print(f"\n4. OPORTUNIDADES:")
    print(f"   Publicaciones con alto alcance pero bajo engagement: {len(high_reach_low_engagement)}")
    
    print("\nRECOMENDACIONES ESTRATÉGICAS:")
    
    print(f"\n1. OPTIMIZACIÓN DE CONTENIDO:")
    print(f"   • Incrementar contenido de '{best_tema}' (mejor rendimiento)")
    print(f"   • Revisar estrategia para '{worst_tema}' (menor engagement)")
    print(f"   • Mantener equilibrio en distribución de pilares")
    
    print(f"\n2. ESTRATEGIA DE ENGAGEMENT:")
    best_engagement_posts = df[df['Engagement_Rate'] > df['Engagement_Rate'].quantile(0.75)]
    common_themes = best_engagement_posts['Tema'].value_counts()
    if len(common_themes) > 0:
        print(f"   • Temas más efectivos para engagement: {', '.join(common_themes.index[:3])}")
    
    print(f"\n3. OPTIMIZACIÓN TEMPORAL:")
    monthly_performance = df.groupby('Mes')['Engagement_Rate'].mean()
    if len(monthly_performance) > 1:
        best_month = monthly_performance.idxmax()
        print(f"   • Mejor mes para engagement: {best_month}")
        print(f"   • Aplicar learnings de {best_month} en futuros períodos")
    
    print(f"\n4. EQUILIBRIO ESTRATÉGICO:")
    pilar_balance = pilar_stats['Frecuencia'] / pilar_stats['Frecuencia'].sum() * 100
    print("   • Distribución actual por pilares:")
    for pilar, pct in pilar_balance.items():
        print(f"     - {pilar}: {pct:.1f}%")
    
    print(f"\n5. ACCIONES INMEDIATAS:")
    print("   • Incrementar frecuencia de contenido de alta performance")
    print("   • Desarrollar contenido híbrido combinando temas exitosos")
    print("   • Establecer benchmarks de engagement por categoría")
    print("   • Implementar A/B testing para optimizar contenido de bajo rendimiento")

def main():
    """Función principal que ejecuta todo el análisis"""
    print("ANÁLISIS COMPLETO DE TWITTER/X - COPPEL")
    print("Período: Junio-Julio 2025")
    print("=" * 80)
    
    # Cargar datos
    df = load_and_clean_data()
    
    # Ejecutar todos los análisis
    tema_stats = analyze_content_themes(df)
    pilar_stats = analyze_pillars(df)
    vinculo_stats = analyze_business_links(df)
    
    analyze_performance_metrics(df)
    analyze_best_performers(df, tema_stats, pilar_stats, vinculo_stats)
    analyze_temporal_patterns(df)
    analyze_correlations(df)
    generate_insights_and_recommendations(df, tema_stats, pilar_stats, vinculo_stats)
    
    print("\n" + "="*80)
    print("ANÁLISIS COMPLETO FINALIZADO")
    print("="*80)

if __name__ == "__main__":
    main()