# EmoGo Backend Development Plan

## Project Overview
Build a FastAPI backend with MongoDB to support the EmoGo frontend application. The backend will collect and serve three types of data: vlogs, sentiments, and GPS coordinates.

## Goals
1. Create a FastAPI application with MongoDB integration
2. Deploy the backend on Render (public server)
3. Deploy MongoDB on MongoDB Atlas
4. Implement data collection endpoints for the EmoGo frontend
5. Create a data-exporting/downloading page for TAs & Tren to view/download all collected data
6. Add the data page URI to README.md

## Technology Stack
- **Backend Framework**: FastAPI
- **Database**: MongoDB Atlas (cloud-hosted)
- **Async MongoDB Driver**: motor[srv]
- **Deployment Platform**: Render
- **Python Version**: 3.9+

## Data Models

### 1. Vlogs
```python
{
    "_id": ObjectId,
    "user_id": str,
    "title": str,
    "content": str,
    "video_url": str (optional),
    "audio_url": str (optional),
    "created_at": datetime,
    "updated_at": datetime
}
```

### 2. Sentiments
```python
{
    "_id": ObjectId,
    "user_id": str,
    "vlog_id": str (optional, reference to vlog),
    "sentiment_score": float,  # e.g., -1.0 to 1.0
    "sentiment_label": str,    # e.g., "positive", "negative", "neutral"
    "emotion": str,            # e.g., "happy", "sad", "angry", "calm"
    "confidence": float,       # 0.0 to 1.0
    "created_at": datetime
}
```

### 3. GPS Coordinates
```python
{
    "_id": ObjectId,
    "user_id": str,
    "latitude": float,
    "longitude": float,
    "accuracy": float (optional),
    "altitude": float (optional),
    "timestamp": datetime,
    "created_at": datetime
}
```

## API Endpoints

### Health Check
- `GET /` - Root endpoint with welcome message
- `GET /health` - Health check endpoint

### Data Collection Endpoints (for EmoGo Frontend)
- `POST /api/vlogs` - Create a new vlog entry
- `POST /api/sentiments` - Create a new sentiment entry
- `POST /api/gps` - Create a new GPS coordinate entry

### Data Retrieval Endpoints
- `GET /api/vlogs` - Get all vlogs (with pagination)
- `GET /api/vlogs/{vlog_id}` - Get specific vlog
- `GET /api/sentiments` - Get all sentiments (with pagination)
- `GET /api/sentiments/{sentiment_id}` - Get specific sentiment
- `GET /api/gps` - Get all GPS coordinates (with pagination)
- `GET /api/gps/{gps_id}` - Get specific GPS coordinate

### Data Export Endpoints (Required for TAs & Tren)
- `GET /export` - HTML page displaying all data with download options
- `GET /export/vlogs` - Export all vlogs as JSON
- `GET /export/sentiments` - Export all sentiments as JSON
- `GET /export/gps` - Export all GPS coordinates as JSON
- `GET /export/all` - Export all data as a single JSON file

## Implementation Steps

### Phase 1: MongoDB Setup
1. Create MongoDB Atlas account
2. Create a new cluster (free tier)
3. Configure network access with IP `0.0.0.0/0` (allow all IPs)
4. Create database user with username and password
5. Get connection string: `mongodb+srv://<username>:<password>@<cluster>.mongodb.net/`
6. Create database named `emogo_db`
7. Create three collections: `vlogs`, `sentiments`, `gps_coordinates`
8. Use MongoDB Compass to:
   - Connect to the cluster
   - Create sample data for testing
   - Verify data structure

### Phase 2: Local Development
1. Update `requirements.txt` to include:
   - `fastapi[all]`
   - `motor[srv]`
   - `python-dotenv`
   - `pydantic`
   - `uvicorn`
2. Create `.env` file for environment variables (MongoDB URI, DB name)
3. Add `.env` to `.gitignore`
4. Create project structure:
   ```
   /
   ├── main.py
   ├── models/
   │   ├── vlog.py
   │   ├── sentiment.py
   │   └── gps.py
   ├── routes/
   │   ├── vlogs.py
   │   ├── sentiments.py
   │   ├── gps.py
   │   └── export.py
   ├── database.py
   ├── config.py
   ├── requirements.txt
   ├── .env (not in git)
   └── README.md
   ```
5. Implement database connection in `database.py`:
   - Use `motor.motor_asyncio.AsyncIOMotorClient`
   - Implement startup and shutdown events
6. Create Pydantic models for data validation
7. Implement CRUD operations for each collection
8. Implement export page with HTML template
9. Test locally with `uvicorn main:app --reload`

### Phase 3: Data Export Page
1. Create `/export` endpoint with HTML interface
2. Display data in tables (vlogs, sentiments, GPS)
3. Add download buttons for each data type (JSON format)
4. Add "Download All" button for combined export
5. Style the page for readability
6. Test downloading functionality

### Phase 4: Render Deployment
1. Ensure `render.yaml` is configured correctly:
   ```yaml
   services:
     - type: web
       name: emogo-backend
       runtime: python
       plan: free
       buildCommand: pip install -r requirements.txt
       startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
2. Push code to GitHub repository
3. Connect Render to GitHub repository
4. Configure environment variables in Render dashboard:
   - `MONGODB_URI`
   - `DB_NAME`
5. Deploy the service
6. Verify deployment at the Render-provided URL
7. Test all endpoints on production

### Phase 5: Documentation & Testing
1. Update README.md with:
   - Project description
   - Setup instructions
   - **Data Export Page URI**: `https://your-app.onrender.com/export`
   - API documentation link
   - Deployment information
2. Test all endpoints:
   - POST endpoints for data collection
   - GET endpoints for data retrieval
   - Export endpoints for downloading data
3. Verify data persistence in MongoDB Atlas
4. Test pagination and error handling
5. Ensure the export page is accessible to TAs & Tren

## Environment Variables
Create `.env` file locally (do not commit):
```
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/
DB_NAME=emogo_db
```

In Render dashboard, add these as environment variables.

## Testing Checklist
- [ ] MongoDB connection successful
- [ ] Can create vlogs via POST /api/vlogs
- [ ] Can create sentiments via POST /api/sentiments
- [ ] Can create GPS coordinates via POST /api/gps
- [ ] Can retrieve all vlogs via GET /api/vlogs
- [ ] Can retrieve all sentiments via GET /api/sentiments
- [ ] Can retrieve all GPS coordinates via GET /api/gps
- [ ] Export page loads at /export
- [ ] Can download vlogs as JSON
- [ ] Can download sentiments as JSON
- [ ] Can download GPS coordinates as JSON
- [ ] Can download all data as JSON
- [ ] App deployed successfully on Render
- [ ] README.md updated with export page URI
- [ ] Sample data visible in MongoDB Compass

## Key Dependencies
```txt
fastapi[all]
motor[srv]
python-dotenv
pydantic
uvicorn
```

## Important Notes
1. Use async functions with FastAPI and Motor for better performance
2. MongoDB Atlas IP whitelist: Use `0.0.0.0/0` to allow all IPs
3. Keep MongoDB credentials secure (use environment variables)
4. The export page URI must be prominently listed in README.md
5. Ensure CORS is enabled if frontend needs to access the API from different domains
6. Use proper error handling and validation
7. Test with sample data before deploying

## Success Criteria
1. ✅ Backend deployed on Render and accessible via public URL
2. ✅ MongoDB Atlas configured and connected
3. ✅ All three data types (vlogs, sentiments, GPS) can be:
   - Created via POST endpoints
   - Retrieved via GET endpoints
   - Downloaded via export page
4. ✅ Export page URI listed in README.md
5. ✅ TAs & Tren can access and download all data
6. ✅ Code pushed to GitHub repository

## Resources
- FastAPI Documentation: https://fastapi.tiangolo.com
- Render FastAPI Deployment: https://render.com/docs/deploy-fastapi
- MongoDB Atlas Setup: https://askstw.medium.com/re-mongodb-atlas-b331acd3d7c
- Motor Documentation: https://motor.readthedocs.io
- MongoDB Compass: https://www.mongodb.com/products/compass
