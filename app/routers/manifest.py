import logging
import os

from fastapi import APIRouter, Request

from ..config import settings
from ..templates import TemplateResponse

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/manifest")
async def manifest(request: Request):
    if settings.hostname:
        # Settings
        base_url = f"https://{settings.hostname}"
    elif os.getenv("RENDER_EXTERNAL_URL"):
        # Render.com
        base_url = os.getenv("RENDER_EXTERNAL_URL")
    elif os.getenv("WEBSITE_HOSTNAME"):
        # Azure Functions and Azure App Service
        base_url = f"https://{os.getenv('WEBSITE_HOSTNAME')}"
    elif os.getenv("CODESPACES"):
        # GitHub Codespaces
        base_url = f"https://{os.getenv('CODESPACE_NAME')}-8000.{os.getenv('GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN')}"
    else:
        # Mostly localhost
        base_url = request.base_url

    manifest_ids = {
        "dev": settings.manifest_id_dev,
        "qa": settings.manifest_id_qa,
        "uat": settings.manifest_id_uat,
        "prod": settings.manifest_id_prod,
    }
    manifest_id = manifest_ids[settings.environment]

    return TemplateResponse(
        request=request,
        name="/manifest.xml",
        context={
            "settings": settings,
            "base_url": str(base_url).rstrip("/"),
            "manifest_id": manifest_id,
        },
        media_type="text/plain",
    )