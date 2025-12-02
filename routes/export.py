from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from database import get_database
from typing import List, Dict, Any
import json

router = APIRouter()


async def serialize_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Convert MongoDB document to JSON-serializable format"""
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    if doc and "created_at" in doc:
        doc["created_at"] = doc["created_at"].isoformat() if hasattr(doc["created_at"], "isoformat") else str(doc["created_at"])
    if doc and "updated_at" in doc:
        doc["updated_at"] = doc["updated_at"].isoformat() if hasattr(doc["updated_at"], "isoformat") else str(doc["updated_at"])
    if doc and "timestamp" in doc:
        doc["timestamp"] = doc["timestamp"].isoformat() if hasattr(doc["timestamp"], "isoformat") else str(doc["timestamp"])
    return doc


@router.get("/export", response_class=HTMLResponse)
async def export_page():
    db = get_database()

    vlogs_count = await db.vlogs.count_documents({})
    sentiments_count = await db.sentiments.count_documents({})
    gps_count = await db.gps_coordinates.count_documents({})

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>EmoGo Data Export</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 40px 20px;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}
            h1 {{
                color: white;
                text-align: center;
                margin-bottom: 40px;
                font-size: 2.5em;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            }}
            .stats-container {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }}
            .stat-card {{
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                text-align: center;
                transition: transform 0.3s ease;
            }}
            .stat-card:hover {{
                transform: translateY(-5px);
            }}
            .stat-number {{
                font-size: 3em;
                font-weight: bold;
                color: #667eea;
                margin-bottom: 10px;
            }}
            .stat-label {{
                color: #666;
                font-size: 1.1em;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            .export-section {{
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }}
            h2 {{
                color: #333;
                margin-bottom: 25px;
                font-size: 1.8em;
            }}
            .button-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-bottom: 30px;
            }}
            .download-btn {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 10px;
                font-size: 1em;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                text-decoration: none;
                display: inline-block;
                text-align: center;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            }}
            .download-btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
            }}
            .download-btn.all {{
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
                grid-column: 1 / -1;
                font-size: 1.2em;
                padding: 20px 40px;
            }}
            .download-btn.all:hover {{
                box-shadow: 0 6px 20px rgba(245, 87, 108, 0.6);
            }}
            .info-text {{
                color: #666;
                margin-top: 20px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 10px;
                border-left: 4px solid #667eea;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>EmoGo Data Export Dashboard</h1>

            <div class="stats-container">
                <div class="stat-card">
                    <div class="stat-number">{vlogs_count}</div>
                    <div class="stat-label">Vlogs</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{sentiments_count}</div>
                    <div class="stat-label">Sentiments</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{gps_count}</div>
                    <div class="stat-label">GPS Coordinates</div>
                </div>
            </div>

            <div class="export-section">
                <h2>Export Data</h2>
                <div class="button-grid">
                    <a href="/export/vlogs" class="download-btn" download="vlogs.json">
                        Download Vlogs
                    </a>
                    <a href="/export/sentiments" class="download-btn" download="sentiments.json">
                        Download Sentiments
                    </a>
                    <a href="/export/gps" class="download-btn" download="gps_coordinates.json">
                        Download GPS Data
                    </a>
                    <a href="/export/all" class="download-btn all" download="emogo_all_data.json">
                        Download All Data
                    </a>
                </div>
                <div class="info-text">
                    <strong>Note:</strong> All data will be exported in JSON format.
                    Click any button above to download the respective dataset.
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@router.get("/export/vlogs")
async def export_vlogs():
    db = get_database()
    vlogs = []
    cursor = db.vlogs.find()

    async for vlog in cursor:
        vlogs.append(await serialize_doc(vlog))

    return JSONResponse(
        content=vlogs,
        headers={"Content-Disposition": "attachment; filename=vlogs.json"}
    )


@router.get("/export/sentiments")
async def export_sentiments():
    db = get_database()
    sentiments = []
    cursor = db.sentiments.find()

    async for sentiment in cursor:
        sentiments.append(await serialize_doc(sentiment))

    return JSONResponse(
        content=sentiments,
        headers={"Content-Disposition": "attachment; filename=sentiments.json"}
    )


@router.get("/export/gps")
async def export_gps():
    db = get_database()
    gps_coords = []
    cursor = db.gps_coordinates.find()

    async for gps in cursor:
        gps_coords.append(await serialize_doc(gps))

    return JSONResponse(
        content=gps_coords,
        headers={"Content-Disposition": "attachment; filename=gps_coordinates.json"}
    )


@router.get("/export/all")
async def export_all():
    db = get_database()

    vlogs = []
    cursor = db.vlogs.find()
    async for vlog in cursor:
        vlogs.append(await serialize_doc(vlog))

    sentiments = []
    cursor = db.sentiments.find()
    async for sentiment in cursor:
        sentiments.append(await serialize_doc(sentiment))

    gps_coords = []
    cursor = db.gps_coordinates.find()
    async for gps in cursor:
        gps_coords.append(await serialize_doc(gps))

    all_data = {
        "vlogs": vlogs,
        "sentiments": sentiments,
        "gps_coordinates": gps_coords,
        "export_timestamp": __import__("datetime").datetime.utcnow().isoformat()
    }

    return JSONResponse(
        content=all_data,
        headers={"Content-Disposition": "attachment; filename=emogo_all_data.json"}
    )
