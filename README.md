# EmoGo Backend

## Sprint Goal
Making an EmoGo backend on a public server using FastAPI + MongoDB.

## Data Export Page URI

🔗: https://emogo-backend.onrender.com/export

Stored data include:
- Vlogs (videos)
- Sentiment Scores
- GPS Coordinates

## Tech Stack

- **Backend Framework:** FastAPI
- **Database:** MongoDB Atlas
- **Deployment:** Render

## API Endpoints

### Data Collection (for EmoGo Frontend)
- `POST /api/vlogs` - Submit vlog data
- `POST /api/sentiments` - Submit sentiment scores
- `POST /api/gps` - Submit GPS coordinates

### Data Retrieval
- `GET /api/vlogs` - Get all vlogs
- `GET /api/sentiments` - Get all sentiment scores
- `GET /api/gps` - Get all GPS coordinates

### Data Export (for TAs)
- `GET /export` - Data export dashboard (HTML page)
- `GET /export/vlogs` - Download vlogs as JSON
- `GET /export/sentiments` - Download sentiments as JSON
- `GET /export/gps` - Download GPS data as JSON
- `GET /export/all` - Download all data as JSON

## Interactive API Documentation

- **Swagger UI:** https://emogo-backend.onrender.com/docs

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

## Author

Janet Chen