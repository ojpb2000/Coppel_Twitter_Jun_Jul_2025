#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Resumen Ejecutivo - Análisis Twitter/X Coppel
Junio-Julio 2025
"""

import pandas as pd
import numpy as np

def load_data():
    """Cargar datos del CSV"""
    df = pd.read_csv('/mnt/d/2025_Disco/Coppel_TW_Reporte/Data_Sources/Coppel_X_Merge_2025_Categorized_01.csv')
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    df['Mes'] = df['Date'].dt.month_name()
    
    numeric_cols = ['Impresiones', 'Interacciones', 'Engagement_Rate']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

def executive_summary():
    """Generar resumen ejecutivo con métricas clave"""
    df = load_data()
    
    print("=" * 80)
    print("RESUMEN EJECUTIVO - TWITTER/X COPPEL")
    print("PERÍODO: JUNIO-JULIO 2025")
    print("=" * 80)
    
    # Métricas generales
    total_posts = len(df)
    total_impressions = df['Impresiones'].sum()
    total_interactions = df['Interacciones'].sum()
    avg_engagement = df['Engagement_Rate'].mean()
    
    print(f"\n📊 MÉTRICAS GENERALES:")
    print(f"   • Total de publicaciones: {total_posts}")
    print(f"   • Impresiones totales: {total_impressions:,}")
    print(f"   • Interacciones totales: {total_interactions:,}")
    print(f"   • Engagement Rate promedio: {avg_engagement:.2f}%")
    
    # Performance por categoría
    tema_performance = df.groupby('Tema').agg({
        'Engagement_Rate': 'mean',
        'Impresiones': 'mean',
        'Date': 'count'
    }).round(2)
    tema_performance.columns = ['ER_Promedio', 'Impresiones_Promedio', 'Frecuencia']
    tema_performance = tema_performance.sort_values('ER_Promedio', ascending=False)
    
    print(f"\n🎯 RENDIMIENTO POR TEMA:")
    for tema, row in tema_performance.iterrows():
        print(f"   • {tema}: {row['ER_Promedio']}% ER | {row['Impresiones_Promedio']:,.0f} imp. | {row['Frecuencia']} posts")
    
    # Análisis temporal
    monthly_comparison = df.groupby('Mes').agg({
        'Engagement_Rate': 'mean',
        'Impresiones': 'mean',
        'Date': 'count'
    }).round(2)
    
    print(f"\n📅 COMPARACIÓN TEMPORAL:")
    for mes, row in monthly_comparison.iterrows():
        print(f"   • {mes}: {row['Engagement_Rate']}% ER | {row['Impresiones']:,.0f} imp. | {row['Date']} posts")
    
    # Mejores publicaciones
    print(f"\n🏆 TOP 3 PUBLICACIONES (por Engagement Rate):")
    top_posts = df.nlargest(3, 'Engagement_Rate')
    for i, (idx, post) in enumerate(top_posts.iterrows(), 1):
        print(f"   {i}. {post['Date'].strftime('%d/%m/%Y')}: {post['Engagement_Rate']}% ER")
        print(f"      {post['Text'][:80]}...")
        print(f"      Tema: {post['Tema']} | Pilar: {post['PILAR']}")
        print()
    
    # Oportunidades y alertas
    print(f"\n⚠️  ALERTAS ESTRATÉGICAS:")
    
    # Caída en engagement de junio a julio
    june_er = monthly_comparison.loc['June', 'Engagement_Rate'] if 'June' in monthly_comparison.index else 0
    july_er = monthly_comparison.loc['July', 'Engagement_Rate'] if 'July' in monthly_comparison.index else 0
    if june_er > 0 and july_er > 0:
        er_decline = ((july_er - june_er) / june_er) * 100
        print(f"   • Caída significativa en ER de junio a julio: {er_decline:.1f}%")
    
    # Variabilidad alta en rendimiento
    cv_engagement = (df['Engagement_Rate'].std() / df['Engagement_Rate'].mean()) * 100
    if cv_engagement > 100:
        print(f"   • Alta inconsistencia en rendimiento: CV = {cv_engagement:.1f}%")
    
    # Contenido con alto alcance pero bajo engagement
    median_impressions = df['Impresiones'].median()
    median_engagement = df['Engagement_Rate'].median()
    underperforming_content = df[(df['Impresiones'] > median_impressions) & 
                                (df['Engagement_Rate'] < median_engagement)]
    if len(underperforming_content) > 0:
        print(f"   • {len(underperforming_content)} publicaciones con alto alcance pero bajo engagement")
    
    print(f"\n💡 RECOMENDACIONES PRIORITARIAS:")
    print(f"   1. Incrementar contenido de 'DESARROLLO PROFESIONAL' (14.25% ER)")
    print(f"   2. Investigar causas de la caída de engagement en julio")
    print(f"   3. Optimizar contenido de 'FUNDACIÓN COPPEL' (0% ER actual)")
    print(f"   4. Establecer estrategia para consistencia en rendimiento")
    print(f"   5. Aprovechar el potencial de alcance para mejorar engagement")
    
    print(f"\n📈 OPORTUNIDADES DE CRECIMIENTO:")
    best_performing_tema = tema_performance.index[0]
    worst_performing_tema = tema_performance.index[-1]
    
    print(f"   • Escalar exitoso modelo de '{best_performing_tema}'")
    print(f"   • Rediseñar estrategia para '{worst_performing_tema}'")
    print(f"   • Balancear distribución entre pilares estratégicos")
    print(f"   • Implementar calendario de contenido basado en datos de junio")

def generate_kpi_dashboard():
    """Generar dashboard de KPIs clave"""
    df = load_data()
    
    print("\n" + "=" * 80)
    print("DASHBOARD DE KPIs - COPPEL SOCIAL MEDIA")
    print("=" * 80)
    
    # KPIs principales
    print(f"\n🎯 KPIs PRINCIPALES:")
    print(f"   Engagement Rate Objetivo vs Real:")
    target_er = 5.0  # Asumiendo un objetivo del 5%
    actual_er = df['Engagement_Rate'].mean()
    er_performance = "✅" if actual_er >= target_er else "❌"
    print(f"   {er_performance} ER: {actual_er:.2f}% (Objetivo: {target_er}%)")
    
    print(f"\n   Alcance Total:")
    total_reach = df['Impresiones'].sum()
    print(f"   📊 {total_reach:,} impresiones totales")
    
    print(f"\n   Interacción Total:")
    total_engagement = df['Interacciones'].sum()
    print(f"   👥 {total_engagement:,} interacciones totales")
    
    # Performance por categoría estratégica
    print(f"\n📊 PERFORMANCE POR PILAR ESTRATÉGICO:")
    pilar_performance = df.groupby('PILAR').agg({
        'Engagement_Rate': 'mean',
        'Impresiones': 'sum',
        'Interacciones': 'sum'
    }).round(2)
    
    for pilar, row in pilar_performance.iterrows():
        status = "🟢" if row['Engagement_Rate'] > 5 else "🟡" if row['Engagement_Rate'] > 2 else "🔴"
        print(f"   {status} {pilar}:")
        print(f"      ER: {row['Engagement_Rate']}% | Alcance: {row['Impresiones']:,} | Interacciones: {row['Interacciones']:,}")
    
    # Tendencias temporales
    print(f"\n📈 TENDENCIAS TEMPORALES:")
    weekly_trends = df.groupby(df['Date'].dt.isocalendar().week)['Engagement_Rate'].mean().round(2)
    print(f"   Semanas con mejor rendimiento:")
    top_weeks = weekly_trends.nlargest(3)
    for week, er in top_weeks.items():
        print(f"   • Semana {week}: {er}% ER")
    
    print(f"\n⚡ ACCIONES INMEDIATAS:")
    print(f"   1. Analizar factores de éxito en contenido de 'DESARROLLO PROFESIONAL'")
    print(f"   2. Replicar mecánicas exitosas de junio en agosto")
    print(f"   3. A/B testing para optimizar contenido de 'FUNDACIÓN COPPEL'")
    print(f"   4. Revisar timing de publicaciones en julio")
    print(f"   5. Desarrollar contenido híbrido entre temas exitosos")

if __name__ == "__main__":
    executive_summary()
    generate_kpi_dashboard()