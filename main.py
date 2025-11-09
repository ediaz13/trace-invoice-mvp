from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

# ------------------------------
# 1. Modelos de Datos (Pydantic)
# ------------------------------

class FacturaData(BaseModel):
    """Define la estructura de los datos de la Factura y Liquidación."""
    
    # Datos de la Factura E
    monto_original_usd: float = Field(..., gt=0, description="Monto original de la factura en USD.")
    fecha_emision: date = Field(..., description="Fecha de emisión de la factura (YYYY-MM-DD).")
    
    # Datos de la Liquidación
    fecha_liquidacion: date = Field(..., description="Fecha de cobro o liquidación en el banco (YYYY-MM-DD).")
    
    # Opcional: Tipo de cambio específico que el usuario puede elegir (ej. MEP, CCL, Oficial)
    tipo_cambio_referencia: Optional[str] = Field("exportacion", description="Tipo de cambio a utilizar (ej: 'exportacion', 'mep', 'oficial').")

# ------------------------------
# 2. Funciones Lógicas (Simuladas)
# ------------------------------

def obtener_tipo_cambio(fecha: date, tipo: str) -> float:
    """
    [SIMULACIÓN] 
    En el MVP real, esta función consultaría una API externa 
    (ej: BCRA, AFIP, u otra API de mercado) para obtener el valor.
    """
    print(f"Consultando tipo de cambio '{tipo}' para la fecha: {fecha}")
    
    # Lógica de simulación simple (los valores reales cambiarían día a día)
    if tipo == "exportacion":
        # Simula un Dólar Exportación
        return 950.00
    elif tipo == "mep":
        return 1050.00
    else:
        # Simula un valor por defecto
        return 900.00

def realizar_cruce_contable(data: FacturaData, tipo_cambio: float) -> dict:
    """Calcula el valor en ARS del cruce contable."""
    
    monto_ars = data.monto_original_usd * tipo_cambio
    
    resultado = {
        "monto_original_usd": data.monto_original_usd,
        "fecha_liquidacion": str(data.fecha_liquidacion), # Convertir a str para el JSON de salida
        "tipo_cambio_aplicado": tipo_cambio,
        "monto_cruce_ars": round(monto_ars, 2),
        "referencia_cambio": data.tipo_cambio_referencia
    }
    return resultado


# ------------------------------
# 3. Inicialización de la App
# ------------------------------

app = FastAPI(
    title="Micro-SaaS Cruce Contable USD/ARS",
    description="API para automatizar la conversión contable de Facturas E.",
    version="1.0.0"
)

# ------------------------------
# 4. Endpoint Principal de la API
# ------------------------------

@app.post("/api/cruce_contable/")
def cruce_contable(factura: FacturaData):
    """
    Toma los datos de la Factura E y la fecha de liquidación, 
    consulta el tipo de cambio para esa fecha y realiza el cruce.
    """
    
    # 1. Obtener el tipo de cambio
    tipo_cambio = obtener_tipo_cambio(
        fecha=factura.fecha_liquidacion, 
        tipo=factura.tipo_cambio_referencia
    )
    
    # 2. Realizar el cálculo contable
    resultado = realizar_cruce_contable(factura, tipo_cambio)
    
    return resultado

# ------------------------------
# 5. Endpoint de Verificación (Health Check)
# ------------------------------

@app.get("/")
def health_check():
    return {"status": "ok", "message": "API Cruce Contable funcionando correctamente."}