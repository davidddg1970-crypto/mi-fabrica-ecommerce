from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI(
    title="NextGen E-commerce SaaS API",
    description="Motor de automatización y generación de landing pages para Shopify",
    version="1.0.0"
)

class LandingRequest(BaseModel):
    source_url: str
    product_title: str
    target_angle: str = "problem_solution"
    shopify_store: str
    shopify_token: str

@app.get("/")
def health_check():
    return {"status": "online", "engine": "NextGen SaaS Core", "version": "1.0.0"}

@app.post("/api/v1/generate-landing")
def generate_landing(data: LandingRequest):
    try:
        optimized_copy = {
            "headline": f"¡Descubre {data.product_title}! La solución definitiva.",
            "subheadline": "Diseñado para ofrecerte el mejor rendimiento y calidad desde el primer día.",
            "cta_text": "COMPRAR AHORA"
        }

        api_version = "2026-01"
        url = f"https://{data.shopify_store}/admin/api/{api_version}/products.json"
        
        headers = {
            "X-Shopify-Access-Token": data.shopify_token,
            "Content-Type": "application/json"
        }

        html_content = f"""
        <div class="nextgen-saas-landing" style="text-align: center; padding: 40px; font-family: sans-serif;">
            <h1 style="font-size: 2.5rem; color: #111;">{optimized_copy['headline']}</h1>
            <p style="font-size: 1.2rem; color: #555; margin: 20px 0;">{optimized_copy['subheadline']}</p>
            <a href="#" style="background: #ff5722; color: #fff; padding: 15px 30px; text-decoration: none; font-size: 1.2rem; border-radius: 5px; display: inline-block; font-weight: bold;">{optimized_copy['cta_text']}</a>
        </div>
        """

        payload = {
            "product": {
                "title": data.product_title,
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
        if response.status_code != 201:
            raise HTTPException(status_code=400, detail=response.text)

        prod = response.json().get("product", {})
        return {
            "status": "success",
            "message": "Landing page generada y publicada con éxito en Shopify.",
            "product_id": prod.get("id"),
            "handle": prod.get("handle")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
