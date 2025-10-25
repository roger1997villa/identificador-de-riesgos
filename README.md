# 🏥 Sistema de Análisis de Riesgo EPS/IPS

## 📋 Tabla de Contenidos
- [Descripción General](#descripción-general)
- [Características Principales](#características-principales)
- [Arquitectura del Sistema](#arquitectura-del-sistema)
- [Módulos y Funcionalidades](#módulos-y-funcionalidades)
- [Instalación y Configuración](#instalación-y-configuración)
- [Guía de Uso](#guía-de-uso)
- [Estructura de Datos](#estructura-de-datos)
- [Clasificación Financiera](#clasificación-financiera)
- [Análisis de Riesgo](#análisis-de-riesgo)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Manejo de Errores](#manejo-de-errores)
- [Contribución](#contribución)
- [Licencia](#licencia)

## 🎯 Descripción General

El **Sistema de Análisis de Riesgo EPS/IPS** es una aplicación web desarrollada en Streamlit diseñada para evaluar el riesgo financiero de Entidades Promotoras de Salud (EPS) e Instituciones Prestadoras de Servicios de Salud (IPS) en Colombia. El sistema integra validación de entidades en el REPS (Registro Especial de Prestadores de Servicios de Salud), clasificación automática de cuentas financieras y predicción de riesgo mediante análisis de indicadores financieros clave.

### 🎯 Objetivos Principales

- **Validar** la existencia y estado de EPS/IPS en el REPS
- **Clasificar automáticamente** cuentas contables en categorías financieras
- **Calcular indicadores** financieros clave (liquidez, endeudamiento, rentabilidad)
- **Predecir niveles de riesgo** mediante algoritmos de scoring
- **Visualizar resultados** mediante dashboards interactivos

## ✨ Características Principales

### 🔍 Validación REPS
- Consulta simulada del Registro Especial de Prestadores
- Identificación automática de tipo de entidad (EPS/IPS)
- Validación de NITs y estados de operación
- Base de datos de ejemplo con entidades comunes del sector salud

### 💰 Clasificación Financiera Inteligente
- Mapeo automático de códigos contables a categorías financieras
- Clasificación por patrones y palabras clave
- Sistema de confianza para clasificaciones estimadas
- Soporte para múltiples formatos de datos (CSV, Excel)

### ⚠️ Análisis de Riesgo Predictivo
- Cálculo de 7 indicadores financieros clave
- Algoritmo de scoring con umbrales configurables
- Identificación de factores de riesgo críticos
- Visualización comparativa entre entidades

### 📊 Dashboard Interactivo
- Interfaz moderna con gradientes y diseño responsive
- Filtros dinámicos por tipo de entidad, categoría y NIT
- Gráficos interactivos con Plotly (barras, tortas, radar, gauges)
- Exportación de resultados en formatos CSV

## 🏗️ Arquitectura del Sistema

### Diagrama de Componentes
Sistema de Análisis de Riesgo EPS/IPS
│
├── 🎨 Interfaz de Usuario (Streamlit)
│ ├── Sidebar de Navegación
│ ├── Módulo de Validación REPS
│ ├── Módulo de Clasificación Financiera
│ └── Módulo de Análisis de Riesgo
│
├── 🔧 Núcleo de Procesamiento
│ ├── REPSValidator (Validación de entidades)
│ ├── FinancialClassifier (Clasificación contable)
│ ├── DataProcessor (Procesamiento de datos)
│ └── RiskPredictor (Predicción de riesgo)
│
├── 📊 Motor de Visualización
│ ├── Gráficos de Métricas
│ ├── Dashboard Interactivo
│ ├── Reportes Comparativos
│ └── Alertas de Riesgo
│
└── 💾 Gestión de Estado
├── Session State Management
├── Cache de Resultados
└── Persistencia de Filtros

# 🧠 Sistema de Análisis de Riesgo EPS/IPS

### 🚀 Versión Interactiva del Dashboard  
[👉 Haz clic aquí para abrir la aplicación en Streamlit](https://identificador-de-riesgos-wb5d4rxq478vspwwdkfvzy.streamlit.app/)

---

