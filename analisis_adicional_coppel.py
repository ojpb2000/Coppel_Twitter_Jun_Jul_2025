#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análisis Adicional y Métricas Complementarias - Coppel Twitter/X
"""

import pandas as pd
import numpy as np

def load_data():
    df = pd.read_csv('/mnt/d/2025_Disco/Coppel_TW_Reporte/Data_Sources/Coppel_X_Merge_2025_Categorized_01.csv')
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    
    numeric_cols = ['Impresiones', 'Interacciones', 'Engagement_Rate', 
                   'Ampliaciones de detalles', 'Visitas del perfil', 'Clics en enlaces',
                   'Reacciones ', 'Reposteos', 'Comentarios', 'Reproducciones únicas', 'Reproducciones']
    
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

def analyze_engagement_breakdown():
    """Análisis detallado de tipos de interacciones"""
    df = load_data()
    
    print("=" * 80)
    print("ANÁLISIS DETALLADO DE TIPOS DE ENGAGEMENT")
    print("=" * 80)
    
    # Cálculo de engagement por tipo
    engagement_types = ['Reacciones ', 'Reposteos', 'Comentarios', 'Visitas del perfil', 
                       'Ampliaciones de detalles', 'Clics en enlaces']
    
    print("\nDISTRIBUCIÓN DE TIPOS DE INTERACCIÓN:")
    total_interactions = df['Interacciones'].sum()
    
    for interaction_type in engagement_types:
        if interaction_type in df.columns:
            total_type = df[interaction_type].sum()
            percentage = (total_type / total_interactions * 100) if total_interactions > 0 else 0
            print(f"   • {interaction_type}: {total_type:,} ({percentage:.1f}%)")
    
    # Top performing content por tipo de interacción
    print("\nTOP PERFORMERS POR TIPO DE INTERACCIÓN:")
    
    for interaction_type in ['Reacciones ', 'Reposteos', 'Comentarios']:
        if interaction_type in df.columns:
            top_post = df.loc[df[interaction_type].idxmax()]
            print(f"\nMás {interaction_type.strip()}:")
            print(f"   Fecha: {top_post['Date'].strftime('%d/%m/%Y')}")
            print(f"   {interaction_type}: {top_post[interaction_type]}")
            print(f"   Tema: {top_post['Tema']}")
            print(f"   Texto: {top_post['Text'][:100]}...")

def analyze_content_effectiveness():
    """Análisis de efectividad por categorías cruzadas"""
    df = load_data()
    
    print("\n" + "=" * 80)
    print("ANÁLISIS DE EFECTIVIDAD CRUZADA")
    print("=" * 80)
    
    # Análisis cruzado Tema x Pilar
    print("\nRENDIMENTO CRUZADO TEMA x PILAR:")
    cross_analysis = df.groupby(['Tema', 'PILAR']).agg({
        'Engagement_Rate': 'mean',
        'Impresiones': 'mean',
        'Date': 'count'
    }).round(2)
    
    cross_analysis.columns = ['ER_Promedio', 'Impresiones_Promedio', 'Posts']
    cross_analysis = cross_analysis.sort_values('ER_Promedio', ascending=False)
    
    print("Mejores combinaciones Tema-Pilar por Engagement Rate:")
    for i, ((tema, pilar), row) in enumerate(cross_analysis.head(5).iterrows(), 1):
        print(f"   {i}. {tema} + {pilar}")
        print(f"      ER: {row['ER_Promedio']}% | Posts: {row['Posts']} | Imp. prom: {row['Impresiones_Promedio']:,.0f}")
    
    # Análisis de eficiencia (engagement vs alcance)
    print("\nANÁLISIS DE EFICIENCIA (ER vs Impresiones):")
    df['Eficiencia'] = df['Engagement_Rate'] / (df['Impresiones'] / 1000)  # ER per 1K impressions
    
    efficiency_by_tema = df.groupby('Tema')['Eficiencia'].mean().sort_values(ascending=False)
    print("\nEficiencia por Tema (ER por cada 1K impresiones):")
    for tema, efficiency in efficiency_by_tema.items():
        print(f"   • {tema}: {efficiency:.4f}")

def analyze_timing_patterns():
    """Análisis de patrones temporales avanzados"""
    df = load_data()
    
    print("\n" + "=" * 80)
    print("ANÁLISIS DE PATRONES TEMPORALES AVANZADOS")
    print("=" * 80)
    
    # Análisis por día de la semana
    df['Dia_Semana'] = df['Date'].dt.day_name()
    
    daily_performance = df.groupby('Dia_Semana').agg({
        'Engagement_Rate': 'mean',
        'Impresiones': 'mean',
        'Date': 'count'
    }).round(2)
    
    print("\nRENDIMIENTO POR DÍA DE LA SEMANA:")
    for dia, row in daily_performance.iterrows():
        print(f"   • {dia}: ER {row['Engagement_Rate']}% | Posts: {row['Date']}")
    
    # Análisis semanal
    df['Semana'] = df['Date'].dt.isocalendar().week
    weekly_performance = df.groupby('Semana').agg({
        'Engagement_Rate': 'mean',
        'Impresiones': 'mean',
        'Date': 'count'
    }).round(2)
    
    print("\nTENDENCIA SEMANAL:")
    for semana, row in weekly_performance.iterrows():
        print(f"   Semana {semana}: ER {row['Engagement_Rate']}% | Posts: {row['Date']} | Imp. prom: {row['Impresiones']:,.0f}")

def identify_optimization_opportunities():
    """Identificación de oportunidades de optimización específicas"""
    df = load_data()
    
    print("\n" + "=" * 80)
    print("OPORTUNIDADES DE OPTIMIZACIÓN ESPECÍFICAS")
    print("=" * 80)
    
    # Contenido con potencial desaprovechado
    median_impressions = df['Impresiones'].median()
    low_engagement = df['Engagement_Rate'].quantile(0.25)
    
    underperforming = df[(df['Impresiones'] > median_impressions) & 
                        (df['Engagement_Rate'] < low_engagement)]
    
    print(f"\nCONTENIDO CON POTENCIAL DESAPROVECHADO ({len(underperforming)} publicaciones):")
    print("Alto alcance pero bajo engagement:")
    
    for idx, post in underperforming.iterrows():
        print(f"\n   • {post['Date'].strftime('%d/%m/%Y')}")
        print(f"     Impresiones: {post['Impresiones']:,} | ER: {post['Engagement_Rate']}%")
        print(f"     Tema: {post['Tema']} | Pilar: {post['PILAR']}")
        print(f"     Texto: {post['Text'][:80]}...")
    
    # Identificar gaps de contenido
    print(f"\nGAPS DE CONTENIDO IDENTIFICADOS:")
    
    tema_distribution = df['Tema'].value_counts()
    pilar_distribution = df['PILAR'].value_counts()
    
    # Temas con poca frecuencia pero buen rendimiento
    tema_performance = df.groupby('Tema').agg({
        'Engagement_Rate': 'mean',
        'Date': 'count'
    })
    
    underrepresented_high_performance = tema_performance[
        (tema_performance['Date'] <= 2) & 
        (tema_performance['Engagement_Rate'] > df['Engagement_Rate'].mean())
    ]
    
    print("\nTemas con alto rendimiento pero poca frecuencia:")
    for tema, row in underrepresented_high_performance.iterrows():
        print(f"   • {tema}: {row['Engagement_Rate']:.2f}% ER, solo {row['Date']} posts")
    
    # Recomendaciones de contenido híbrido
    print(f"\nRECOMENDACIONES DE CONTENIDO HÍBRIDO:")
    
    best_tema = df.groupby('Tema')['Engagement_Rate'].mean().idxmax()
    best_pilar = df.groupby('PILAR')['Engagement_Rate'].mean().idxmax()
    
    print(f"   • Combinar '{best_tema}' con pilar '{best_pilar}'")
    print(f"   • Crear contenido que integre elementos de temas exitosos")
    print(f"   • Experimentar con formatos de los posts más exitosos")

def generate_action_plan():
    """Generar plan de acción basado en los hallazgos"""
    df = load_data()
    
    print("\n" + "=" * 80)
    print("PLAN DE ACCIÓN ESTRATÉGICO")
    print("=" * 80)
    
    print("\n🎯 ACCIONES INMEDIATAS (0-2 semanas):")
    print("   1. Crear 2-3 publicaciones adicionales de 'DESARROLLO PROFESIONAL'")
    print("   2. Analizar y replicar elementos exitosos de las top 3 publicaciones")
    print("   3. Rediseñar estrategia de contenido para 'FUNDACIÓN COPPEL'")
    print("   4. Implementar schedule de publicaciones basado en datos de junio")
    
    print("\n📊 ACCIONES A MEDIANO PLAZO (2-4 semanas):")
    print("   1. A/B testing para contenido de bajo rendimiento")
    print("   2. Desarrollar templates para contenido híbrido exitoso")
    print("   3. Establecer KPIs específicos por tema y pilar")
    print("   4. Crear calendar de contenido balanceado entre categorías")
    
    print("\n🚀 ACCIONES A LARGO PLAZO (1-3 meses):")
    print("   1. Implementar sistema de monitoreo en tiempo real")
    print("   2. Desarrollar machine learning para predicción de rendimiento")
    print("   3. Crear benchmark interno por industria")
    print("   4. Establecer programa de optimización continua")
    
    # Métricas de seguimiento recomendadas
    print("\n📈 MÉTRICAS DE SEGUIMIENTO RECOMENDADAS:")
    print("   • Engagement Rate por tema (objetivo: > 8%)")
    print("   • Consistency Score (objetivo: CV < 80%)")
    print("   • Efficiency Ratio (ER/1K impressions)")
    print("   • Content Balance Index (distribución equilibrada por pilar)")
    print("   • Temporal Performance Index (rendimiento por día/semana)")
    
    print("\n⚠️  ALERTAS PARA ESTABLECER:")
    print("   • ER semanal < 3%: Revisar estrategia inmediatamente")
    print("   • > 3 posts consecutivos con ER < 2%: Cambio de táctica")
    print("   • Caída > 50% en interacciones mes a mes: Análisis profundo")
    print("   • Desbalance > 70% en un solo tema: Rebalancear contenido")

if __name__ == "__main__":
    analyze_engagement_breakdown()
    analyze_content_effectiveness()
    analyze_timing_patterns()
    identify_optimization_opportunities()
    generate_action_plan()