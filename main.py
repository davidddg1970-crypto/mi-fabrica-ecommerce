import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="NextGen E-commerce SaaS API",
    description="Motor de automatización y generación de landing pages para Shopify",
    version="1.0.0"
)

class LandingRequest(BaseModel):
    source_url: str
    product_title: str
    target_angle: Optional[str] = "problem_solution"
    shopify_store: str
    shopify_token: str

@app.get("/")
def health_check():
    return {"status": "online", "engine": "NextGen SaaS Core", "version": "1.0.0"}

@app.post("/api/v1/generate-landing")
def generate_landing(data: LandingRequest):
    try:
        optimized_copy = generate_ai_copy(data.product_title, data.target_angle)

        shopify_result = publish_to_shopify(
            store_url=data.shopify_store,
            token=data.shopify_token,
            title=data.product_title,
            copy=optimized_copy,
            source_url=data.source_url
        )

        if not shopify_result.get("success"):
            raise HTTPException(status_code=400, detail=shopify_result.get("error"))

        return {
            "status": "success",
            "message": "Landing page generada y publicada con éxito en Shopify.",
            "product_id": shopify_result.get("product_id"),
            "handle": shopify_result.get("handle"),
            "applied_copy": optimized_copy
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def generate_ai_copy(title: str, angle: str) -> dict:
    if angle == "fomo":
        return {
            "headline": f"¡Últimas unidades virales de {title}! No te quedes fuera de tendencia.",
            "subheadline": "Alta demanda detectada en redes sociales. Envío prioritario activado.",
            "cta_text": "ASEGURAR MI UNIDAD"
        }
    elif angle == "authority":
        return {
            "headline": f"Ingeniería avanzada: {title} diseñado para durar.",
            "subheadline": "Certificado de calidad con garantía de devolución.",
            "cta_text": "COMPRAR CON GARANTÍA"
        }
    else:
        return {
            "headline": f"¿Cansado de los problemas habituales con {title}? Aquí tienes la solución.",
            "subheadline": "Diseñado para ahorrarte tiempo y dinero desde el primer uso.",
            "cta_text": "QUIERO RESOLVER ESTO"
        }

def publish_to_shopify(store_url: str, token: str, title: str, copy: dict, source_url: str) -> dict:
    api_version = "2026-01"
    url = f"https://{store_url}/admin/api/{api_version}/products.json"
    
    headers = {
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json"
    }

    html_content = f"""
    <div class="nextgen-saas-landing">
        <div class="hero" style="text-align: center; padding: 30px;">
            <h1 style="font-size: 2.5rem; font-weight: 900; color: #111;">{copy['headline']}</h1>
            <p style="font-size: 1.2rem; color: #555; margin-top: 15px;">{copy['subheadline']}</p>
            <button style="background: #ff5722; color: #fff; padding: 15px 30px; font-size: 1.2rem; border: none; border-radius: 5px; cursor: pointer; margin-top: 20px;">{copy['cta_text']}</button>
        </div>
        <div class="cro-badge" style="background: #e6fffa; color: #234e52; padding: 12px; border-radius: 8px; text-align: center; font-weight: bold; margin: 20px 0;">
            🚀 Producto optimizado para alta conversión (CRO)
        </div>
    </div>
    """

    payload = {
        "product": {
            "title": title,
            "body_html": html_content,
            "vendor": "NextGen SaaS AI",
            "product_type": "Optimized Landing Page",
            "variants": [
                {
                    "price": "29.99",
                    "compare_at_price": "59.99",
                    "inventory_management": "shopify",
                    "inventory_quantity": 100
                }
            ]
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        prod = response.json().get("product", {})
        return {"success": True, "product_id": prod.get("id"), "handle": prod.get("handle")}
    else:
        return {"success": False, "error": response.text}
