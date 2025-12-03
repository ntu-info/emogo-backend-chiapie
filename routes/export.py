from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from database import get_database
from typing import List, Dict, Any
import json
import os
import glob

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

    # Get video files from videos directory
    videos_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "videos")
    video_files = []
    if os.path.exists(videos_dir):
        video_files = [os.path.basename(f) for f in glob.glob(os.path.join(videos_dir, "*"))]

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
                background: linear-gradient(135deg, #003262 0%, #3B7EA1 100%);
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
                color: #FDB515;
                margin-bottom: 10px;
            }}
            .stat-label {{
                color: #666;
                font-size: 1.1em;
                letter-spacing: 0.5px;
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
                background: linear-gradient(135deg, #003262 0%, #3B7EA1 100%);
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 10px;
                font-size: 1em;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                text-decoration: none;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                box-shadow: 0 4px 15px rgba(0, 50, 98, 0.4);
            }}
            .download-btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0, 50, 98, 0.6);
            }}
            .download-btn.all {{
                background: linear-gradient(135deg, #FDB515 0%, #FDB515 100%);
                color: #003262;
                box-shadow: 0 4px 15px rgba(253, 181, 21, 0.4);
                grid-column: 1 / -1;
                font-size: 1.2em;
                padding: 20px 40px;
                font-weight: 700;
            }}
            .download-btn.all:hover {{
                box-shadow: 0 6px 20px rgba(253, 181, 21, 0.6);
            }}
            .info-text {{
                color: #666;
                margin-top: 20px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 10px;
                border-left: 4px solid #FDB515;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>EmoGo data export dashboard</h1>

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
                    <div class="stat-label">GPS coordinates</div>
                </div>
            </div>

            <div class="export-section">
                <h2>Export data</h2>
                <div class="button-grid">
                    <a href="/export/vlogs" class="download-btn" download="vlogs.json">
                        Download vlogs
                    </a>
                    <a href="/export/sentiments" class="download-btn" download="sentiments.json">
                        Download sentiments
                    </a>
                    <a href="/export/gps" class="download-btn" download="gps_coordinates.json">
                        Download GPS data
                    </a>
                    <a href="/export/all" class="download-btn all" download="emogo_all_data.json">
                        Download all data
                    </a>
                </div>
                <div class="info-text">
                    <strong>Note:</strong> Data will be exported in JSON format. Click to download!
                </div>
            </div>

            <div class="export-section" style="margin-top: 20px;">
                <h2>Video files</h2>
                {"".join([f'<div class="button-grid"><a href="/videos/{video}" class="download-btn" download="{video}">Download {video}</a></div>' for video in video_files]) if video_files else '<p style="color: #666;">No video files available</p>'}
                <div class="info-text">
                    <strong>Backend URIs:</strong> Videos are served from backend and can be downloaded directly via URLs like <code>/videos/filename.mp4</code>
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
