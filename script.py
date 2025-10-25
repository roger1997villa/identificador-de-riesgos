import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings
import time
import re


warnings.filterwarnings('ignore')


# Configuración de la página
st.set_page_config(
   page_title="Sistema de Riesgo EPS/IPS",
   page_icon="🏥",
   layout="wide",
   initial_sidebar_state="expanded"
)


# Estilos CSS personalizados con fondo gris y botones azules llamativos
st.markdown("""
<style>
   /* Fondo principal */
   .stApp {
       background-color: #3E3C38;
   }


   /* Header con gradiente azul */
   .gradient-header {
       background: linear-gradient(135deg, #5770EF 0%, #2a5298 100%);
       color: white;
       padding: 2rem;
       border-radius: 15px;
       text-align: center;
       margin-bottom: 2rem;
       box-shadow: 0 4px 15px rgba(0,0,0,0.2);
   }


   .gradient-header h1 {
       color: white;
       font-size: 2.8rem;
       font-weight: 700;
       margin: 0;
       text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
   }


   .gradient-header p {
       color: #e0e0e0;
       font-size: 1.2rem;
       margin: 0.5rem 0 0 0;
   }


   /* Botones azules llamativos */
   .stButton>button {
       background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
       color: white;
       border: none;
       padding: 0.75rem 1.5rem;
       border-radius: 8px;
       font-weight: 600;
       font-size: 1rem;
       transition: all 0.3s ease;
       box-shadow: 0 2px 8px rgba(0,123,255,0.3);
   }


   .stButton>button:hover {
       background: linear-gradient(135deg, #0056b3 0%, #004494 100%);
       transform: translateY(-2px);
       box-shadow: 0 4px 12px rgba(0,123,255,0.4);
   }


   /* Botones primarios aún más llamativos */
   div[data-testid="stButton"] button[kind="primary"] {
       background: linear-gradient(135deg, #ff6b35 0%, #ff8e53 100%);
       box-shadow: 0 3px 10px rgba(255,107,53,0.4);
   }


   div[data-testid="stButton"] button[kind="primary"]:hover {
       background: linear-gradient(135deg, #e55a2b 0%, #ff7a40 100%);
       transform: translateY(-2px);
       box-shadow: 0 5px 15px rgba(255,107,53,0.5);
   }


   .risk-high {
       background-color: #f8d7da;
       border: 1px solid #f5c6cb;
       border-radius: 5px;
       padding: 15px;
       margin: 10px 0;
   }
   .risk-medium {
       background-color: #fff3cd;
       border: 1px solid #ffeaa7;
       border-radius: 5px;
       padding: 15px;
       margin: 10px 0;
   }
   .risk-low {
       background-color: #d4edda;
       border: 1px solid #c3e6cb;
       border-radius: 5px;
       padding: 15px;
       margin: 10px 0;
   }
   .metric-card {
       background-color: #f8f9fa;
       border-radius: 10px;
       padding: 15px;
       text-align: center;
       border-left: 4px solid #1f77b4;
   }
   .comparison-container {
       background-color: #f8f9fa;
       border-radius: 10px;
       padding: 20px;
       margin: 10px 0;
       border: 2px solid #dee2e6;
   }
   .good-indicator {
       color: #28a745;
       font-weight: bold;
   }
   .warning-indicator {
       color: #ffc107;
       font-weight: bold;
   }
   .danger-indicator {
       color: #dc3545;
       font-weight: bold;
   }
   .filter-section {
       background-color: #f8f9fa;
       padding: 15px;
       border-radius: 10px;
       margin-bottom: 20px;
       border-left: 4px solid #007bff;
   }


   /* Sidebar styling */
   .css-1d391kg {
       background-color: #f8f9fa;
   }


   /* Cards y contenedores */
   .main-container {
       background-color: white;
       border-radius: 15px;
       padding: 25px;
       margin-bottom: 20px;
       box-shadow: 0 4px 12px rgba(0,0,0,0.1);
   }
</style>
""", unsafe_allow_html=True)




# Resto del código permanece igual...
class REPSValidator:
   """Clase para validar entidades en el REPS"""


   def __init__(self):
       self.entidades_ejemplo = self._inicializar_entidades_ejemplo()


   def _inicializar_entidades_ejemplo(self):
       """Inicializa el diccionario de entidades de ejemplo"""
       return {
           '800123456': {'nombre': 'EPS SANITAS', 'tipo': 'EPS', 'estado': 'ACTIVO'},
           '900987654': {'nombre': 'CLINICA DEL COUNTRY', 'tipo': 'IPS', 'estado': 'ACTIVO'},
           '830456789': {'nombre': 'IPS SALUD TOTAL', 'tipo': 'IPS', 'estado': 'ACTIVO'},
           '860123987': {'nombre': 'LABORATORIO CLINICO ABC', 'tipo': 'IPS', 'estado': 'ACTIVO'},
           '870456123': {'nombre': 'EPS COOMEVA', 'tipo': 'EPS', 'estado': 'ACTIVO'},
           '880789456': {'nombre': 'HOSPITAL CENTRAL', 'tipo': 'IPS', 'estado': 'ACTIVO'},
           '890123456': {'nombre': 'EPS SURA', 'tipo': 'EPS', 'estado': 'ACTIVO'},
       }


   def validar_entidad(self, nit, razon_social=""):
       """Valida una entidad en el REPS"""
       try:
           return self._simular_validacion_reps(nit, razon_social)
       except Exception as e:
           return self._crear_respuesta_error(nit, str(e))


   def _simular_validacion_reps(self, nit, razon_social=""):
       """Simula la validación en el REPS"""
       nit_limpio = self._limpiar_nit(nit)


       if nit_limpio in self.entidades_ejemplo:
           info = self.entidades_ejemplo[nit_limpio]
           return {
               'nit': nit_limpio,
               'nombre_reps': info['nombre'],
               'tipo': info['tipo'],
               'estado_reps': info['estado'],
               'valido': True,
               'fecha_consulta': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
               'razon_social_db': razon_social
           }
       else:
           tipo_estimado = self._estimar_tipo_por_nit(nit_limpio)
           return {
               'nit': nit_limpio,
               'nombre_reps': 'NO ENCONTRADO EN REPS',
               'tipo': tipo_estimado,
               'estado_reps': 'NO VERIFICADO',
               'valido': False,
               'fecha_consulta': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
               'razon_social_db': razon_social
           }


   def _estimar_tipo_por_nit(self, nit):
       """Estima el tipo de entidad basado en patrones del NIT"""
       if nit.startswith('8'):
           return 'EPS'
       elif nit.startswith('9'):
           return 'IPS'
       elif len(nit) == 9 and nit.isdigit():
           if nit[0] in ['8', '9']:
               return 'EPS' if nit[0] == '8' else 'IPS'
       return 'NO DETERMINADO'


   def _limpiar_nit(self, nit):
       """Limpia y formatea el NIT"""
       if pd.isna(nit):
           return ""
       nit_str = str(nit).strip()
       if '.' in nit_str:
           try:
               nit_float = float(nit_str)
               nit_str = str(int(nit_float))
           except ValueError:
               pass
       nit_limpio = re.sub(r'[^\d]', '', nit_str)
       return nit_limpio


   def _crear_respuesta_error(self, nit, error):
       """Crea una respuesta de error"""
       return {
           'nit': self._limpiar_nit(nit),
           'nombre_reps': f'ERROR: {error}',
           'tipo': 'ERROR',
           'estado_reps': 'ERROR',
           'valido': False,
           'fecha_consulta': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
           'razon_social_db': ''
       }




class FinancialClassifier:
   """Clase para clasificar cuentas financieras"""


   def __init__(self):
       self.categorias_map = self._inicializar_categorias()


   def _inicializar_categorias(self):
       """Inicializa el mapeo de códigos a categorías financieras"""
       return {
           '1': ('Activo corriente', '1 - Efectivo y equivalentes'),
           '11': ('Activo corriente', '11 - Inversiones'),
           '1105': ('Disponible', '1105 - Caja'),
           '1110': ('Disponible', '1110 - Bancos'),
           '12': ('Activo corriente', '12 - Deudores comerciales'),
           '13': ('Inventarios', '13 - Inventarios'),
           '2': ('Pasivo corriente', 'Pasivo corriente'),
           '21': ('Pasivo corriente', '21 - Obligaciones financieras'),
           '22': ('Pasivo corriente', '22 - Cuentas por pagar'),
           '3': ('Pasivo No corriente', 'Pasivo No corriente'),
           '5': ('Patrimonio', 'Patrimonio'),
           '51': ('Patrimonio', '51 - Capital social'),
           '55': ('Utilidad neta', '55 - Resultado del ejercicio'),
           '4': ('Ventas', 'Ventas'),
           '41': ('Ventas', '41 - Ingresos actividades ordinarias'),
           '4105': ('Ventas', '4105 - Ingresos por actividades de salud'),
           '6': ('Costos', 'Costos de ventas'),
           '7': ('Gastos', 'Gastos operacionales'),
       }


   def clasificar_cuenta(self, codigo_concepto, denominacion):
       """Clasifica una cuenta en categorías financieras"""
       if pd.isna(codigo_concepto):
           return 'No clasificada', 'No clasificada', 0.0


       codigo_str = str(codigo_concepto).strip()


       # Buscar coincidencia exacta
       if codigo_str in self.categorias_map:
           categoria, subcategoria = self.categorias_map[codigo_str]
           return categoria, subcategoria, 1.0


       # Buscar por prefijo
       for codigo, (categoria, subcategoria) in self.categorias_map.items():
           if codigo_str.startswith(codigo):
               return categoria, subcategoria, 0.8


       # Clasificación por palabras clave
       denominacion_lower = str(denominacion).lower()
       if any(palabra in denominacion_lower for palabra in ['activo', 'inversión']):
           return 'Activo corriente', 'Clasificado por denominación', 0.6
       elif any(palabra in denominacion_lower for palabra in ['pasivo', 'deuda']):
           return 'Pasivo corriente', 'Clasificado por denominación', 0.6
       elif any(palabra in denominacion_lower for palabra in ['patrimonio', 'capital']):
           return 'Patrimonio', 'Clasificado por denominación', 0.6
       elif any(palabra in denominacion_lower for palabra in ['ingreso', 'venta']):
           return 'Ventas', 'Clasificado por denominación', 0.6
       elif any(palabra in denominacion_lower for palabra in ['costo', 'gasto']):
           return 'Costos', 'Clasificado por denominación', 0.6


       return 'No clasificada', 'No clasificada', 0.0




class RiskPredictor:
   """Clase para predecir riesgo financiero"""


   def __init__(self):
       self.umbrales = self._definir_umbrales()


   def _definir_umbrales(self):
       return {
           'liquidez_alto_riesgo': 1.0,
           'liquidez_medio_riesgo': 1.5,
           'endeudamiento_alto_riesgo': 0.7,
           'endeudamiento_medio_riesgo': 0.5,
           'margen_alto_riesgo': 0.0,
           'margen_medio_riesgo': 0.05,
       }


   def predecir_riesgo(self, indicadores):
       """Predice el riesgo basado en indicadores financieros"""
       puntaje = 0
       factores = []
       umbral = self.umbrales


       # Evaluar liquidez
       liquidez = indicadores.get('razon_corriente', 0)
       if liquidez < umbral['liquidez_alto_riesgo']:
           puntaje += 3
           factores.append(('Liquidez crítica', 0.9))
       elif liquidez < umbral['liquidez_medio_riesgo']:
           puntaje += 1
           factores.append(('Liquidez moderada', 0.6))


       # Evaluar endeudamiento
       endeudamiento = indicadores.get('razon_endeudamiento', 0)
       if endeudamiento > umbral['endeudamiento_alto_riesgo']:
           puntaje += 3
           factores.append(('Endeudamiento alto', 0.9))
       elif endeudamiento > umbral['endeudamiento_medio_riesgo']:
           puntaje += 1
           factores.append(('Endeudamiento moderado', 0.6))


       # Evaluar rentabilidad
       margen = indicadores.get('margen_neto', 0)
       if margen < umbral['margen_alto_riesgo']:
           puntaje += 2
           factores.append(('Pérdidas operacionales', 0.8))
       elif margen < umbral['margen_medio_riesgo']:
           puntaje += 1
           factores.append(('Baja rentabilidad', 0.5))


       # Determinar nivel de riesgo
       if puntaje >= 6:
           return "ALTO", min(0.95, 0.6 + (puntaje * 0.05)), factores
       elif puntaje >= 3:
           return "MEDIO", min(0.8, 0.3 + (puntaje * 0.1)), factores
       else:
           return "BAJO", max(0.1, 0.1 + (puntaje * 0.05)), factores




class DataProcessor:
   """Clase para procesar datos financieros"""


   def __init__(self):
       self.classifier = FinancialClassifier()


   def procesar_dataframe(self, df, info_entidades=None):
       """Procesa un DataFrame completo y clasifica todas las cuentas"""
       resultados = []


       # Usar nombres de columnas normalizados
       CODIGO_CONCEPTO = 'codigoconcepto'
       DENOMINACION = 'denominacion'
       NIT = 'nit'


       for _, row in df.iterrows():
           codigo_concepto_val = row.get(CODIGO_CONCEPTO)
           denominacion_val = row.get(DENOMINACION)


           # Asegurar que los valores existen antes de clasificar
           if pd.isna(codigo_concepto_val) and pd.isna(denominacion_val):
               categoria, subcategoria, confianza = 'No clasificada', 'No clasificada', 0.0
           else:
               categoria, subcategoria, confianza = self.classifier.clasificar_cuenta(
                   codigo_concepto_val,
                   denominacion_val
               )


           nit = str(row[NIT]).strip() if NIT in row and not pd.isna(row[NIT]) else ''
           tipo_entidad = self._determinar_tipo_entidad(nit, info_entidades, row)


           resultados.append({
               'categoria_principal': categoria,
               'subcategoria': subcategoria,
               'confianza_clasificacion': confianza,
               'tipo_entidad': tipo_entidad
           })


       df_resultado = df.copy()
       df_clasificaciones = pd.DataFrame(resultados)


       # Resetear índices para concatenación segura
       df_resultado = df_resultado.reset_index(drop=True)
       df_clasificaciones = df_clasificaciones.reset_index(drop=True)


       return pd.concat([df_resultado, df_clasificaciones], axis=1)


   def _determinar_tipo_entidad(self, nit, info_entidades, row):
       """Determina el tipo de entidad (EPS/IPS)"""
       RAZON_SOCIAL = 'razonsocial'


       if info_entidades and nit in info_entidades:
           return info_entidades[nit].get('tipo', 'NO VALIDADO')


       razon_social = str(row.get(RAZON_SOCIAL, '')).upper()
       if 'EPS' in razon_social:
           return 'EPS'
       elif any(palabra in razon_social for palabra in ['IPS', 'CLINICA', 'HOSPITAL']):
           return 'IPS'


       if nit.startswith('8') and len(nit) == 9:
           return 'EPS'
       elif nit.startswith('9') and len(nit) == 9:
           return 'IPS'


       return 'NO DETERMINADO'


   def calcular_indicadores_por_nit(self, df_clasificado, info_entidades=None):
       """Calcula indicadores financieros por NIT"""
       df_clasificado['nit'] = df_clasificado['nit'].astype(str)


       # Usar nombre de columna normalizado
       VALOR = 'valor'
       RAZON_SOCIAL = 'razonsocial'


       df_clasificado['valor_numerico'] = pd.to_numeric(df_clasificado[VALOR], errors='coerce')


       indicadores_por_nit = {}


       for nit in df_clasificado['nit'].unique():
           df_nit = df_clasificado[df_clasificado['nit'] == nit].copy()
           indicadores = self._calcular_indicadores_completos(df_nit)
           if indicadores:
               razon_social = self._obtener_razon_social_desde_datos(df_nit)
               indicadores['razon_social'] = razon_social
               indicadores['tipo_entidad'] = df_nit['tipo_entidad'].iloc[
                   0] if 'tipo_entidad' in df_nit.columns else 'NO DETERMINADO'
               indicadores_por_nit[nit] = indicadores


       return indicadores_por_nit


   def _obtener_razon_social_desde_datos(self, df_nit):
       """Obtiene la razón social desde la base de datos original"""
       RAZON_SOCIAL = 'razonsocial'


       if RAZON_SOCIAL in df_nit.columns and not df_nit[RAZON_SOCIAL].isna().all():
           return df_nit[RAZON_SOCIAL].iloc[0]
       return 'Sin razón social'


   def _calcular_indicadores_completos(self, df_nit):
       """Calcula todos los indicadores financieros para un NIT específico"""
       categorias_totales = {}


       for _, row in df_nit.iterrows():
           categoria = row['categoria_principal']
           valor = row['valor_numerico']


           if not pd.isna(valor) and valor != 0:
               categorias_totales[categoria] = categorias_totales.get(categoria, 0) + valor


       if not categorias_totales:
           return None


       return self._calcular_ratios_financieros(categorias_totales)


   def _calcular_ratios_financieros(self, categorias_totales):
       """Calcula ratios financieros"""
       indicadores = {}


       # Valores básicos
       activo_corriente = categorias_totales.get('Activo corriente', 0)
       pasivo_corriente = categorias_totales.get('Pasivo corriente', 0)
       pasivo_no_corriente = categorias_totales.get('Pasivo No corriente', 0)
       pasivo_total = pasivo_corriente + pasivo_no_corriente


       # Calcular activo total sumando todas las categorías de Activo
       activo_total = sum(v for k, v in categorias_totales.items() if 'Activo' in k)


       patrimonio = categorias_totales.get('Patrimonio', 0)
       utilidad_neta = categorias_totales.get('Utilidad neta', 0)
       ventas = categorias_totales.get('Ventas', 0)


       # Ratios de liquidez
       indicadores['razon_corriente'] = self._safe_divide(activo_corriente, pasivo_corriente)
       indicadores['prueba_acida'] = self._safe_divide(activo_corriente - categorias_totales.get('Inventarios', 0),
                                                       pasivo_corriente)


       # Ratios de endeudamiento
       indicadores['razon_endeudamiento'] = self._safe_divide(pasivo_total, activo_total)
       indicadores['leverage_financiero'] = self._safe_divide(pasivo_total, patrimonio)


       # Ratios de rentabilidad
       indicadores['roa'] = self._safe_divide(utilidad_neta, activo_total)
       indicadores['roe'] = self._safe_divide(utilidad_neta, patrimonio)
       indicadores['margen_neto'] = self._safe_divide(utilidad_neta, ventas)


       # Valores absolutos
       indicadores.update({
           'activo_corriente': activo_corriente,
           'pasivo_corriente': pasivo_corriente,
           'activo_total': activo_total,
           'pasivo_total': pasivo_total,
           'patrimonio': patrimonio,
           'utilidad_neta': utilidad_neta,
           'ventas': ventas
       })


       return indicadores


   def _safe_divide(self, numerador, denominador):
       """División segura evitando división por cero"""
       return numerador / denominador if denominador != 0 else 0




class FinancialAnalyzerApp:
   """Clase principal de la aplicación Streamlit"""


   def __init__(self):
       self.reps_validator = REPSValidator()
       self.data_processor = DataProcessor()
       self.risk_predictor = RiskPredictor()


   def run(self):
       """Ejecuta la aplicación principal"""
       # Header con gradiente azul
       st.markdown("""
       <div class="gradient-header">
           <h1>🔍 Sistema de Análisis de Riesgo EPS/IPS</h1>
           <p>Análisis integral de riesgo financiero para entidades de salud</p>
       </div>
       """, unsafe_allow_html=True)


       modulo = self._show_sidebar()


       if modulo == "Validación REPS":
           self._show_validation_module()
       elif modulo == "Clasificación Financiera":
           self._show_financial_classification()
       else:
           self._show_risk_analysis()


   def _load_dataframe(self, uploaded_file):
       """Carga el DataFrame desde el archivo subido y normaliza las columnas."""
       try:
           # Intentar leer CSV con diferentes codificaciones si falla UTF-8
           if uploaded_file.name.endswith('.csv'):
               try:
                   df = pd.read_csv(uploaded_file, dtype={'nit': str}, encoding='utf-8')
               except UnicodeDecodeError:
                   uploaded_file.seek(0)  # Resetear puntero del archivo
                   df = pd.read_csv(uploaded_file, dtype={'nit': str}, encoding='latin1')


           else:
               df = pd.read_excel(uploaded_file, dtype={'nit': str})


           # 1. Normalización de Nombres de Columnas
           def normalize_column_name(col):
               col_str = str(col).strip()
               col_str = col_str.lower()
               # Eliminar tildes (ejemplo básico)
               col_str = col_str.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú',
                                                                                                                 'u')
               # Eliminar caracteres no alfanuméricos (excepto guiones bajos)
               col_str = re.sub(r'[^a-z0-9_]', '', col_str)
               return col_str


           column_mapping = {
               col: normalize_column_name(col)
               for col in df.columns
           }
           df = df.rename(columns=column_mapping)


           # 2. Ajustar el tipo de dato de NIT
           if 'nit' in df.columns:
               df['nit'] = df['nit'].astype(str).str.strip()


           return df


       except Exception as e:
           st.error(f"Error al cargar el archivo: {str(e)}")
           raise e


   def _show_sidebar(self):
       """Muestra la barra lateral"""
       st.sidebar.title("🏥 Sistema de Riesgo EPS/IPS")
       st.sidebar.markdown("---")


       st.sidebar.markdown("### 📊 Módulos")
       modulo = st.sidebar.radio(
           "Selecciona el módulo:",
           ["Validación REPS", "Clasificación Financiera", "Análisis de Riesgo"]
       )


       st.sidebar.markdown("---")
       st.sidebar.markdown("**Desarrollado para análisis de riesgo en entidades de salud**")


       return modulo


   def _show_validation_module(self):
       """Muestra el módulo de validación REPS"""
       st.markdown('<div class="main-container">', unsafe_allow_html=True)
       st.header("🔍 Validación de Entidades en REPS")


       uploaded_file = st.file_uploader(
           "Cargar archivo con NITs para validar",
           type=['csv', 'xlsx'],
           help="El archivo debe contener columnas: nit y RazonSocial"
       )


       if uploaded_file is not None:
           try:
               df = self._load_dataframe(uploaded_file)
               self._process_validation_file(df, uploaded_file.name)
           except Exception as e:
               st.error(f"❌ Error al procesar el archivo: {str(e)}")
               st.session_state.df_validacion = None
               st.session_state.info_entidades = None


       # Mostrar resultados si existen, incluso después de un rerun
       if 'df_validacion' in st.session_state and st.session_state.df_validacion is not None:
           self._show_validation_results(st.session_state.df_validacion)
       st.markdown('</div>', unsafe_allow_html=True)


   def _process_validation_file(self, df, filename):
       """Procesa el archivo de validación"""
       st.success(f"✅ Archivo cargado: {filename}")
       st.info(f"📊 Dimensiones: {df.shape[0]} filas × {df.shape[1]} columnas")


       # Usar nombre de columna normalizado
       RAZON_SOCIAL = 'razonsocial'


       if 'nit' not in df.columns:
           st.error("❌ El archivo debe contener la columna 'nit'")
           return


       with st.expander("📋 NITs Únicos a Validar"):
           nits_unicos = df['nit'].dropna().unique()
           st.write(f"**Total de NITs únicos:** {len(nits_unicos)}")


           df_nits_unicos = pd.DataFrame({
               'NIT': nits_unicos,
               'Razón Social': [df[df['nit'] == nit][RAZON_SOCIAL].iloc[0] if RAZON_SOCIAL in df.columns and len(
                   df[df['nit'] == nit]) > 0 else 'No disponible' for nit in nits_unicos]
           })
           st.dataframe(df_nits_unicos)


       if st.button("🔍 Validar en REPS", type="primary"):
           with st.spinner("Validando entidades en REPS..."):
               self._validate_entities(df)


   def _validate_entities(self, df):
       """Valida las entidades en el REPS"""
       nits_unicos = df['nit'].dropna().unique()
       RAZON_SOCIAL = 'razonsocial'


       progress_bar = st.progress(0)
       status_text = st.empty()


       resultados = []
       for i, nit in enumerate(nits_unicos):
           progress = (i + 1) / len(nits_unicos)
           progress_bar.progress(progress)
           status_text.text(f"Validando NIT {i + 1}/{len(nits_unicos)}: {nit}")


           razon_social = ''
           if RAZON_SOCIAL in df.columns:
               matching_rows = df[df['nit'] == nit]
               if len(matching_rows) > 0:
                   razon_social = matching_rows[RAZON_SOCIAL].iloc[0]


           resultado = self.reps_validator.validar_entidad(nit, razon_social)
           resultados.append(resultado)
           time.sleep(0.01)


       progress_bar.empty()
       status_text.empty()


       df_resultados = pd.DataFrame(resultados)


       columnas_finales = ['nit', 'razon_social_db', 'tipo', 'valido', 'fecha_consulta']
       df_resultados = df_resultados[columnas_finales]


       df_resultados = df_resultados.rename(columns={
           'razon_social_db': 'Razón Social',
           'tipo': 'Tipo Entidad',
           'valido': 'Válido REPS'
       })


       st.session_state.df_validacion = df_resultados
       st.session_state.info_entidades = {
           row['nit']: {
               'nombre': row['Razón Social'],
               'tipo': row['Tipo Entidad'],
               'valido': row['Válido REPS']
           }
           for _, row in df_resultados.iterrows()
       }


       st.success(f"✅ Validación completada para {len(nits_unicos)} NITs")
       # st.rerun() para mostrar los resultados en el siguiente ciclo
       st.rerun()


   def _show_validation_results(self, df_validacion):
       """Muestra los resultados de la validación"""
       st.subheader("📊 Resultados de Validación REPS")


       # Métricas
       col1, col2, col3, col4 = st.columns(4)


       total_entidades = len(df_validacion)
       eps_count = len(df_validacion[df_validacion['Tipo Entidad'] == 'EPS'])
       ips_count = len(df_validacion[df_validacion['Tipo Entidad'] == 'IPS'])
       validas_count = len(df_validacion[df_validacion['Válido REPS'] == True])


       with col1:
           st.metric("Total Entidades", total_entidades)
       with col2:
           st.metric("EPS Identificadas", eps_count)
       with col3:
           st.metric("IPS Identificadas", ips_count)
       with col4:
           st.metric("Entidades Válidas", validas_count)


       st.dataframe(df_validacion, use_container_width=True)


       fig = px.pie(
           df_validacion,
           names='Tipo Entidad',
           title='Distribución de Tipos de Entidades'
       )
       st.plotly_chart(fig, use_container_width=True)


       csv = df_validacion.to_csv(index=False)
       st.download_button(
           "📥 Descargar resultados validación",
           data=csv,
           file_name="validacion_reps.csv"
       )


   def _show_financial_classification(self):
       """Muestra el módulo de clasificación financiera"""
       st.markdown('<div class="main-container">', unsafe_allow_html=True)
       st.header("💰 Clasificación Financiera")


       info_entidades = st.session_state.get('info_entidades', None)
       if info_entidades:
           st.success("✅ Información de validación REPS disponible")
       else:
           st.info("ℹ️ Carga el archivo de NITs en el módulo anterior para una mejor clasificación.")


       uploaded_file = st.file_uploader(
           "Cargar archivo con datos financieros",
           type=['csv', 'xlsx'],
           help="El archivo debe contener: nit, RazonSocial, codigoConcepto, valor, Denominacion"
       )


       if uploaded_file is not None:
           try:
               df = self._load_dataframe(uploaded_file)
               self._process_financial_file(df, uploaded_file.name)
           except Exception as e:
               # El error ya se muestra en _load_dataframe
               pass


       # FIX FINAL CLAVE: Llamar a la visualización si existe data clasificada
       if 'df_clasificado' in st.session_state and st.session_state.df_clasificado is not None:
           self._show_classification_results()
       st.markdown('</div>', unsafe_allow_html=True)


   def _process_financial_file(self, df, filename):
       """Procesa el archivo financiero"""
       st.success(f"✅ Archivo cargado: {filename}")


       # Usar nombres de columnas normalizados y verificar su existencia
       columnas_requeridas = ['nit', 'codigoconcepto', 'valor', 'denominacion']
       columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]


       if columnas_faltantes:
           st.error(f"❌ Faltan columnas requeridas o los nombres son incorrectos: {columnas_faltantes}")
           st.info(f"💡 Columnas encontradas: {df.columns.tolist()}")
           return


       with st.expander("📋 Vista previa de datos"):
           st.dataframe(df.head(10))


       # Solo mostrar el botón si no hay data clasificada O la data cargada es diferente
       if st.button("🎯 Clasificar Datos Financieros", type="primary"):
           with st.spinner("Clasificando datos financieros..."):
               self._process_financial_data(df)
               # FIX: Se establece una bandera y se recarga la página
               st.session_state.data_just_classified = True
               st.rerun()


   def _process_financial_data(self, df):
       """Procesa los datos financieros"""
       info_entidades = st.session_state.get('info_entidades', None)
       df_clasificado = self.data_processor.procesar_dataframe(df, info_entidades)
       indicadores_por_nit = self.data_processor.calcular_indicadores_por_nit(df_clasificado, info_entidades)


       st.session_state.df_clasificado = df_clasificado
       st.session_state.indicadores_por_nit = indicadores_por_nit


       st.success("✅ Clasificación completada! Preparando resultados...")


   def _show_classification_results(self):
       """Muestra los resultados de la clasificación"""
       if 'df_clasificado' not in st.session_state or st.session_state.df_clasificado is None:
           st.warning("⚠️ Primero debes procesar los datos financieros")
           return


       df_clasificado = st.session_state.df_clasificado


       # FIX: Reinicio de filtros si se acaba de clasificar data
       if st.session_state.get('data_just_classified', False):
           st.session_state.filtros_clasificacion = {
               'tipo': 'TODOS',
               'categoria': 'TODAS',
               'nit': 'TODOS'
           }
           st.session_state.data_just_classified = False


       # 1. INICIALIZAR FILTROS EN SESSION STATE
       if 'filtros_clasificacion' not in st.session_state:
           st.session_state.filtros_clasificacion = {
               'tipo': 'TODOS',
               'categoria': 'TODAS',
               'nit': 'TODOS'
           }


       # SECCIÓN DE FILTROS - FUERA DE LAS TABS
       st.markdown('<div class="filter-section">', unsafe_allow_html=True)
       st.subheader("🔍 Filtros de Datos")


       col1, col2, col3 = st.columns(3)


       # Obtener valores actuales de la sesión
       current_tipo = st.session_state.filtros_clasificacion.get('tipo', 'TODOS')
       current_categoria = st.session_state.filtros_clasificacion.get('categoria', 'TODAS')
       current_nit = st.session_state.filtros_clasificacion.get('nit', 'TODOS')


       # --- FILTRO 1: TIPO DE ENTIDAD ---
       with col1:
           tipos_entidad = ['TODOS'] + sorted(df_clasificado['tipo_entidad'].unique().tolist())
           initial_index_tipo = tipos_entidad.index(current_tipo) if current_tipo in tipos_entidad else 0


           st.session_state.filtros_clasificacion['tipo'] = st.selectbox(
               "Tipo entidad:",
               tipos_entidad,
               index=initial_index_tipo,
               key="filtro_tipo_clasificacion"
           )


       # --- FILTRO 2: CATEGORÍA PRINCIPAL ---
       with col2:
           categorias = ['TODAS'] + sorted(df_clasificado['categoria_principal'].unique().tolist())
           initial_index_categoria = categorias.index(current_categoria) if current_categoria in categorias else 0


           st.session_state.filtros_clasificacion['categoria'] = st.selectbox(
               "Categoría:",
               categorias,
               index=initial_index_categoria,
               key="filtro_categoria_clasificacion"
           )


       # --- FILTRO 3: NIT ---
       with col3:
           nits = ['TODOS'] + sorted(df_clasificado['nit'].unique().tolist())
           initial_index_nit = nits.index(current_nit) if current_nit in nits else 0


           st.session_state.filtros_clasificacion['nit'] = st.selectbox(
               "NIT:",
               nits,
               index=initial_index_nit,
               key="filtro_nit_clasificacion"
           )


       # 2. APLICAR FILTROS (Usando directamente los valores de la sesión actualizados)
       df_filtrado = df_clasificado.copy()


       tipo_filtro = st.session_state.filtros_clasificacion['tipo']
       categoria_filtro = st.session_state.filtros_clasificacion['categoria']
       nit_filtro = st.session_state.filtros_clasificacion['nit']


       if tipo_filtro != 'TODOS':
           df_filtrado = df_filtrado[df_filtrado['tipo_entidad'] == tipo_filtro]


       if categoria_filtro != 'TODAS':
           df_filtrado = df_filtrado[df_filtrado['categoria_principal'] == categoria_filtro]


       if nit_filtro != 'TODOS':
           df_filtrado = df_filtrado[df_filtrado['nit'] == nit_filtro]


       # Mostrar información del filtro
       st.info(f"**📊 Registros mostrados:** {len(df_filtrado):,} de {len(df_clasificado):,} totales")


       # Botón para limpiar filtros
       if st.button("🔄 Limpiar Filtros", key="limpiar_filtros_clasificacion"):
           st.session_state.filtros_clasificacion = {
               'tipo': 'TODOS',
               'categoria': 'TODAS',
               'nit': 'TODOS'
           }
           st.rerun()


       st.markdown('</div>', unsafe_allow_html=True)


       # GUARDAR DATOS FILTRADOS EN SESSION STATE
       st.session_state.df_filtrado_clasificacion = df_filtrado


       # TABS QUE USAN LOS DATOS FILTRADOS
       tab1, tab2, tab3 = st.tabs(["📋 Datos Clasificados", "📊 Resumen por Categoría", "📈 Análisis Gráfico"])
       with tab1:
           self._show_classified_data(df_filtrado)
       with tab2:
           self._show_category_summary(df_filtrado)
       with tab3:
           if 'indicadores_por_nit' in st.session_state:
               self._show_graphical_analysis(df_filtrado)
           else:
               st.warning("⚠️ No hay indicadores para el análisis gráfico. Ejecute la clasificación de datos primero.")


   def _show_classified_data(self, df_filtrado):
       """Muestra los datos clasificados filtrados"""
       st.subheader("Datos Clasificados Filtrados")
       RAZON_SOCIAL = 'razonsocial'
       CODIGO_CONCEPTO = 'codigoconcepto'
       DENOMINACION = 'denominacion'


       if len(df_filtrado) > 0:
           st.success(f"✅ Mostrando {len(df_filtrado)} registros filtrados")
           # Mostrar columnas relevantes
           columnas_a_mostrar = ['nit', RAZON_SOCIAL, CODIGO_CONCEPTO, DENOMINACION, 'valor', 'categoria_principal',
                                 'subcategoria', 'tipo_entidad']
           columnas_disponibles = [col for col in columnas_a_mostrar if col in df_filtrado.columns]


           # Renombrar para visualización (solo si las columnas existen)
           df_display = df_filtrado[columnas_disponibles].rename(columns={
               RAZON_SOCIAL: 'Razón Social',
               CODIGO_CONCEPTO: 'Código Concepto',
               DENOMINACION: 'Denominación'
           })


           # Mostrar DataFrame
           st.dataframe(df_display, use_container_width=True)


           # Botón de descarga
           csv = df_filtrado[columnas_disponibles].to_csv(index=False)
           st.download_button(
               "📥 Descargar datos clasificados filtrados",
               data=csv,
               file_name="datos_clasificados_filtrados.csv",
               type="primary"
           )
       else:
           st.warning("🚫 No hay datos que coincidan con los filtros aplicados")
           st.info("💡 Prueba con diferentes combinaciones de filtros")


   def _show_category_summary(self, df_filtrado):
       """Muestra resumen por categoría de datos filtrados"""
       st.subheader("Resumen por Categoría (Datos Filtrados)")
       if len(df_filtrado) == 0:
           st.warning("No hay datos para mostrar con los filtros actuales")
           return


       # Asegurar que tenemos la columna valor_numerico
       if 'valor_numerico' not in df_filtrado.columns:
           df_filtrado['valor_numerico'] = pd.to_numeric(df_filtrado['valor'], errors='coerce')


       # Resumen por categoría y tipo de entidad
       resumen = df_filtrado.groupby(['categoria_principal', 'tipo_entidad']).agg({
           'valor_numerico': 'sum',
           'nit': 'nunique'
       }).reset_index()
       resumen = resumen.rename(columns={
           'valor_numerico': 'Valor Total',
           'nit': 'Número de Entidades'
       })


       st.success(f"📊 Resumen de {len(resumen)} categorías filtradas")
       st.dataframe(resumen, use_container_width=True)


       # Gráficos
       if len(resumen) > 0:
           col1, col2 = st.columns(2)
           with col1:
               # Gráfico de barras
               fig = px.bar(
                   resumen,
                   x='categoria_principal',
                   y='Valor Total',
                   color='tipo_entidad',
                   title="Valor por Categoría y Tipo de Entidad",
                   barmode='group',
                   labels={'categoria_principal': 'Categoría', 'Valor Total': 'Valor Total'}
               )
               st.plotly_chart(fig, use_container_width=True)
           with col2:
               # Gráfico de torta por categoría
               fig_pie = px.pie(
                   resumen,
                   values='Valor Total',
                   names='categoria_principal',
                   title='Distribución de Valor por Categoría'
               )
               st.plotly_chart(fig_pie, use_container_width=True)


           # Gráfico adicional - número de entidades por categoría
           fig_entidades = px.bar(
               resumen,
               x='categoria_principal',
               y='Número de Entidades',
               color='tipo_entidad',
               title="Número de Entidades por Categoría",
               barmode='group'
           )
           st.plotly_chart(fig_entidades, use_container_width=True)


   def _show_graphical_analysis(self, df_filtrado):
       """Muestra análisis gráfico de datos filtrados"""
       st.subheader("📈 Análisis Gráfico de Indicadores (Datos Filtrados)")
       if len(df_filtrado) == 0:
           st.warning("No hay datos para análisis gráfico con los filtros actuales")
           return


       if 'indicadores_por_nit' not in st.session_state:
           st.warning("No hay indicadores financieros calculados")
           return


       indicadores_por_nit = st.session_state.indicadores_por_nit


       nits_filtrados = df_filtrado['nit'].unique()
       indicadores_filtrados = {nit: indicadores_por_nit[nit] for nit in nits_filtrados if nit in indicadores_por_nit}


       if not indicadores_filtrados:
           st.warning("No hay indicadores disponibles para los datos filtrados")
           return


       st.success(f"✅ {len(indicadores_filtrados)} entidades con indicadores disponibles")


       entidades_opciones = []
       for nit, indicadores in indicadores_filtrados.items():
           razon_social = indicadores.get('razon_social', 'Sin razón social')
           tipo_entidad = indicadores.get('tipo_entidad', 'NO VALIDADO')
           display_text = f"{nit} - {razon_social} ({tipo_entidad})"
           entidades_opciones.append((nit, display_text, razon_social, tipo_entidad))


       if not entidades_opciones:
           st.info("No hay entidades disponibles para análisis")
           return


       col1, col2 = st.columns([2, 1])
       with col1:
           entidad_principal = st.selectbox(
               "Seleccionar entidad para análisis detallado:",
               options=[opt[1] for opt in entidades_opciones],
               key="selector_entidad_analisis_filtrado"
           )
       with col2:
           opciones_comparacion = [opt[1] for opt in entidades_opciones if opt[1] != entidad_principal]
           entidades_comparacion = st.multiselect(
               "Seleccionar para comparar:",
               options=opciones_comparacion,
               default=opciones_comparacion[:min(2, len(opciones_comparacion))] if opciones_comparacion else [],
               key="selector_comparacion_filtrado"
           )


       nit_principal = None
       for nit, display_text, razon_social, tipo_entidad in entidades_opciones:
           if display_text == entidad_principal:
               nit_principal = nit
               break


       if nit_principal:
           self._show_individual_analysis(indicadores_filtrados, nit_principal)


           if entidades_comparacion:
               self._show_comparative_analysis(indicadores_filtrados, nit_principal, entidades_comparacion,
                                               entidades_opciones)


   def _show_individual_analysis(self, indicadores_por_nit, nit_principal):
       """Muestra análisis individual de una entidad"""
       st.markdown("---")
       st.subheader(f"📊 Análisis Individual: {indicadores_por_nit[nit_principal]['razon_social']}")
       indicadores = indicadores_por_nit[nit_principal]


       # Métricas principales
       col1, col2, col3, col4 = st.columns(4)
       with col1:
           rc = indicadores.get('razon_corriente', 0)
           st.metric("Razón Corriente", f"{rc:.2f}")
       with col2:
           endeudamiento = indicadores.get('razon_endeudamiento', 0)
           st.metric("Endeudamiento", f"{endeudamiento:.2%}")
       with col3:
           roa = indicadores.get('roa', 0)
           st.metric("ROA", f"{roa:.2%}")
       with col4:
           roe = indicadores.get('roe', 0)
           st.metric("ROE", f"{roe:.2%}")


       # Gráficos
       tab1, tab2, tab3 = st.tabs(["📈 Liquidez", "💰 Endeudamiento", "📊 Rentabilidad"])
       with tab1:
           self._create_liquidity_charts(indicadores)
       with tab2:
           self._create_leverage_charts(indicadores)
       with tab3:
           self._create_profitability_charts(indicadores)


   def _create_liquidity_charts(self, indicadores):
       """Crea gráficos de liquidez"""
       col1, col2 = st.columns(2)
       with col1:
           fig_gauge = go.Figure(go.Indicator(
               mode="gauge+number",
               value=indicadores.get('razon_corriente', 0),
               title={'text': "Razón Corriente"},
               domain={'x': [0, 1], 'y': [0, 1]},
               gauge={
                   'axis': {'range': [0, 3]},
                   'bar': {'color': "darkblue"},
                   'steps': [
                       {'range': [0, 1], 'color': "red"},
                       {'range': [1, 1.5], 'color': "yellow"},
                       {'range': [1.5, 3], 'color': "green"}]
               }
           ))
           st.plotly_chart(fig_gauge, use_container_width=True)
       with col2:
           liquidez_metrics = {
               'Razón Corriente': indicadores.get('razon_corriente', 0),
               'Prueba Ácida': indicadores.get('prueba_acida', 0)
           }
           fig_bar = px.bar(
               x=list(liquidez_metrics.keys()),
               y=list(liquidez_metrics.values()),
               title="Indicadores de Liquidez",
               labels={'x': 'Indicador', 'y': 'Valor'}
           )
           st.plotly_chart(fig_bar, use_container_width=True)


   def _create_leverage_charts(self, indicadores):
       """Crea gráficos de endeudamiento"""
       col1, col2 = st.columns(2)
       with col1:
           patrimonio = indicadores.get('patrimonio', 0)
           pasivo_total = indicadores.get('pasivo_total', 0)
           total = patrimonio + pasivo_total
           if total > 0:
               fig_pie = px.pie(
                   values=[patrimonio, pasivo_total],
                   names=['Patrimonio', 'Pasivo Total'],
                   title='Estructura de Capital'
               )
               st.plotly_chart(fig_pie, use_container_width=True)
       with col2:
           leverage_metrics = {
               'Endeudamiento': indicadores.get('razon_endeudamiento', 0),
               'Leverage': indicadores.get('leverage_financiero', 0)
           }
           fig_bar = px.bar(
               x=list(leverage_metrics.keys()),
               y=list(leverage_metrics.values()),
               title="Indicadores de Endeudamiento"
           )
           st.plotly_chart(fig_bar, use_container_width=True)


   def _create_profitability_charts(self, indicadores):
       """Crea gráficos de rentabilidad"""
       col1, col2 = st.columns(2)
       with col1:
           profit_metrics = {
               'ROA': indicadores.get('roa', 0),
               'ROE': indicadores.get('roe', 0),
               'Margen Neto': indicadores.get('margen_neto', 0)
           }
           fig_bar = px.bar(
               x=list(profit_metrics.keys()),
               y=list(profit_metrics.values()),
               title="Indicadores de Rentabilidad"
           )
           fig_bar.update_layout(yaxis_tickformat='.2%')
           st.plotly_chart(fig_bar, use_container_width=True)
       with col2:
           categories = ['ROA', 'ROE', 'Margen Neto']
           values = [
               max(0, indicadores.get('roa', 0)),
               max(0, indicadores.get('roe', 0)),
               max(0, indicadores.get('margen_neto', 0))
           ]
           fig_radar = go.Figure()
           fig_radar.add_trace(go.Scatterpolar(
               r=values,
               theta=categories,
               fill='toself',
               name='Rentabilidad'
           ))
           fig_radar.update_layout(
               polar=dict(
                   radialaxis=dict(
                       visible=True,
                       range=[0, max(values) * 1.2 if max(values) > 0 else 0.1]
                   )),
               showlegend=False,
               title="Análisis de Rentabilidad"
           )
           st.plotly_chart(fig_radar, use_container_width=True)


   def _show_comparative_analysis(self, indicadores_por_nit, nit_principal, entidades_comparacion, entidades_opciones):
       """Muestra análisis comparativo"""
       st.markdown("---")
       st.subheader("🔄 Análisis Comparativo")


       nits_comparacion = [nit_principal]
       for display_text in entidades_comparacion:
           for nit, display, razon_social, tipo_entidad in entidades_opciones:
               if display == display_text:
                   nits_comparacion.append(nit)
                   break


       datos_comparativos = []
       for nit in nits_comparacion:
           if nit in indicadores_por_nit:
               info = indicadores_por_nit[nit]
               datos_comparativos.append({
                   'Entidad': info['razon_social'],
                   'Razón Corriente': info.get('razon_corriente', 0),
                   'Endeudamiento': info.get('razon_endeudamiento', 0),
                   'Margen Neto': info.get('margen_neto', 0)
               })


       df_comparacion = pd.DataFrame(datos_comparativos)


       def format_ratios(val, is_percent=False):
           if pd.isna(val) or val == 0:
               return 'N/A'
           return f"{val:.2%}" if is_percent else f"{val:.2f}"


       df_comparacion['Endeudamiento'] = df_comparacion['Endeudamiento'].apply(
           lambda x: format_ratios(x, is_percent=True))
       df_comparacion['Margen Neto'] = df_comparacion['Margen Neto'].apply(lambda x: format_ratios(x, is_percent=True))
       df_comparacion['Razón Corriente'] = df_comparacion['Razón Corriente'].apply(
           lambda x: format_ratios(x, is_percent=False))


       st.dataframe(df_comparacion, use_container_width=True)


       # Gráfico Radar de comparación (usando valores sin formatear)
       fig_radar_comp = go.Figure()


       metrics = ['Razón Corriente', 'Endeudamiento', 'Margen Neto']
       df_raw = pd.DataFrame([d for d in datos_comparativos if d['Razón Corriente'] != 0])
       if df_raw.empty:
           return


       df_raw = df_raw.set_index('Entidad')


       # Invertir endeudamiento para que mayor sea mejor en el radar
       df_raw['Endeudamiento'] = 1 - df_raw['Endeudamiento']


       def scale(series):
           min_val = series.min()
           max_val = series.max()
           if max_val == min_val:
               return pd.Series([0.5] * len(series), index=series.index)
           # Normalización min-max
           return (series - min_val) / (max_val - min_val)


       df_scaled = pd.DataFrame()
       df_scaled['Razón Corriente'] = scale(df_raw['Razón Corriente'])
       df_scaled['Endeudamiento (Invertido)'] = scale(df_raw['Endeudamiento'])
       df_scaled['Margen Neto'] = scale(df_raw['Margen Neto'])


       for entidad in df_scaled.index:
           fig_radar_comp.add_trace(go.Scatterpolar(
               r=df_scaled.loc[entidad].values.tolist(),
               theta=df_scaled.columns.tolist(),
               fill='toself',
               name=entidad
           ))


       fig_radar_comp.update_layout(
           polar=dict(
               radialaxis=dict(
                   visible=True,
                   range=[0, 1]
               )),
           showlegend=True,
           title="Comparación Normalizada de Indicadores Clave"
       )
       st.plotly_chart(fig_radar_comp, use_container_width=True)


   def _show_risk_analysis(self):
       """Muestra el módulo de análisis de riesgo"""
       st.markdown('<div class="main-container">', unsafe_allow_html=True)
       st.header("⚠️ Análisis y Predicción de Riesgo")


       indicadores_por_nit = st.session_state.get('indicadores_por_nit', None)


       if not indicadores_por_nit:
           st.warning(
               "⚠️ Primero debes clasificar los datos financieros en el módulo anterior para calcular los indicadores.")
           return


       st.success(f"✅ Calculando riesgo para {len(indicadores_por_nit)} entidades.")


       df_indicadores = pd.DataFrame.from_dict(indicadores_por_nit, orient='index')
       df_indicadores.index.name = 'nit'
       df_indicadores = df_indicadores.reset_index()


       riesgos = []
       for index, row in df_indicadores.iterrows():
           indicadores_input = row.drop(['nit', 'razon_social', 'tipo_entidad']).apply(pd.to_numeric,
                                                                                       errors='coerce').to_dict()


           # Asegurar que los indicadores son números y no nulos para el predictor
           if all(pd.notna(v) for v in indicadores_input.values()):
               nivel_riesgo, score, factores = self.risk_predictor.predecir_riesgo(indicadores_input)
           else:
               nivel_riesgo, score, factores = "NO CALC.", 0.0, [("Datos insuficientes", 1.0)]


           factores_str = ", ".join([f"{f[0]} ({f[1] * 100:.0f}%)" for f in factores])
           riesgos.append({
               'Nivel Riesgo': nivel_riesgo,
               'Probabilidad': score,
               'Factores Clave': factores_str
           })


       df_riesgos = pd.DataFrame(riesgos)
       df_final = pd.concat([df_indicadores, df_riesgos], axis=1)


       st.subheader("Tabla de Indicadores y Riesgo por Entidad")


       # Formatear columnas de ratios
       columnas_ratio = ['razon_corriente', 'prueba_acida', 'razon_endeudamiento', 'leverage_financiero', 'roa', 'roe',
                         'margen_neto', 'Probabilidad']
       for col in columnas_ratio:
           if col in df_final.columns:
               if col == 'Probabilidad':
                   df_final[col] = df_final[col].apply(lambda x: f"{x:.1%}" if not pd.isna(x) and x != 0.0 else 'N/A')
               else:
                   df_final[col] = pd.to_numeric(df_final[col], errors='coerce').apply(
                       lambda x: f"{x:,.2f}" if not pd.isna(x) else 'N/A')


       # Formatear valores monetarios
       columnas_monetarias = ['activo_total', 'pasivo_total', 'utilidad_neta', 'ventas', 'activo_corriente',
                              'pasivo_corriente', 'patrimonio']
       for col in columnas_monetarias:
           if col in df_final.columns:
               df_final[col] = pd.to_numeric(df_final[col], errors='coerce').apply(
                   lambda x: f"${x:,.0f}" if not pd.isna(x) else 'N/A')


       def highlight_risk(s):
           if 'Nivel Riesgo' in s and s['Nivel Riesgo'] == 'ALTO':
               return ['background-color: #f8d7da'] * len(s)
           elif 'Nivel Riesgo' in s and s['Nivel Riesgo'] == 'MEDIO':
               return ['background-color: #fff3cd'] * len(s)
           elif 'Nivel Riesgo' in s and s['Nivel Riesgo'] == 'BAJO':
               return ['background-color: #d4edda'] * len(s)
           return [''] * len(s)


       columnas_a_mostrar = [
           'nit', 'razon_social', 'tipo_entidad', 'Nivel Riesgo', 'Probabilidad',
           'razon_corriente', 'razon_endeudamiento', 'margen_neto',
           'utilidad_neta', 'Factores Clave'
       ]


       columnas_existentes = [col for col in columnas_a_mostrar if col in df_final.columns]


       st.dataframe(
           df_final[columnas_existentes].style.apply(highlight_risk, axis=1),
           use_container_width=True
       )


       st.subheader("Visualización del Riesgo")


       conteo_riesgo = df_final['Nivel Riesgo'].value_counts().reset_index()
       conteo_riesgo.columns = ['Nivel Riesgo', 'Conteo']


       fig = px.bar(
           conteo_riesgo,
           x='Nivel Riesgo',
           y='Conteo',
           title='Distribución de Entidades por Nivel de Riesgo',
           color='Nivel Riesgo',
           category_orders={'Nivel Riesgo': ['ALTO', 'MEDIO', 'BAJO', 'NO CALC.']},
           color_discrete_map={'ALTO': '#dc3545', 'MEDIO': '#ffc107', 'BAJO': '#28a745', 'NO CALC.': '#6c757d'}
       )
       st.plotly_chart(fig, use_container_width=True)


       st.download_button(
           "📥 Descargar Análisis de Riesgo",
           data=df_final.to_csv(index=False),
           file_name="analisis_riesgo_eps_ips.csv",
           type="primary"
       )
       st.markdown('</div>', unsafe_allow_html=True)




if __name__ == '__main__':
   # Inicializar session state si es la primera ejecución
   if 'df_validacion' not in st.session_state:
       st.session_state.df_validacion = None
   if 'info_entidades' not in st.session_state:
       st.session_state.info_entidades = None
   if 'df_clasificado' not in st.session_state:
       st.session_state.df_clasificado = None
   if 'indicadores_por_nit' not in st.session_state:
       st.session_state.indicadores_por_nit = None
   # FIX: Inicializar la bandera de clasificación
   if 'data_just_classified' not in st.session_state:
       st.session_state.data_just_classified = False


   app = FinancialAnalyzerApp()
   app.run()
