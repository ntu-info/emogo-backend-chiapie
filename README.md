# EmoGo Backend

**Data Export Page:** https://emogo-backend-chiapie.onrender.com/export
**API Documentation:** https://emogo-backend-chiapie.onrender.com/docs
**Sample Video URI:** https://emogo-backend-chiapie.onrender.com/videos/christmas.mp4

## Sprint Goal
Making an EmoGo backend on a public server using FastAPI + MongoDB.

## Stored Data
- Vlogs (videos)
- Sentiment Scores
- GPS Coordinates

## Tech Stack
- **Backend Framework:** FastAPI
- **Database:** MongoDB Atlas
- **Deployment:** Render

## API Endpoints

### Data Collection
- `POST /api/vlogs` - Submit vlog data
- `POST /api/sentiments` - Submit sentiment scores
- `POST /api/gps` - Submit GPS coordinates

### Data Retrieval
- `GET /api/vlogs` - Get all vlogs
- `GET /api/sentiments` - Get all sentiment scores
- `GET /api/gps` - Get all GPS coordinates

### Data Export
- `GET /export` - Data export dashboard (HTML page)
- `GET /export/vlogs` - Download vlogs as JSON
- `GET /export/sentiments` - Download sentiments as JSON
- `GET /export/gps` - Download GPS data as JSON
- `GET /export/all` - Download all data as JSON

## Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create `.env` file:**
   ```
   MONGODB_URI=your_mongodb_connection_string
   DB_NAME=emogo_db
   ```

3. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```

4. **Access locally:**
   - API: http://localhost:8000
   - Export page: http://localhost:8000/export
   - API docs: http://localhost:8000/docs