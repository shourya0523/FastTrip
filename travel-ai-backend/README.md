# 🛫 Flight Module - Hackathon Ready

Simple flight search with accessibility features.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Test the logic (works without setup)
python test_api.py

# Start the server
python run.py
```

## 📡 API Endpoints

### Search Flights
```http
POST /api/v1/flights/search
{
  "origin": "JFK",
  "destination": "LAX",
  "departure_date": "2024-02-15",
  "num_travelers": 2,
  "budget": "medium",
  "accessibility_requirements": true
}
```

### Get Airports
```http
GET /api/v1/flights/airports/JFK
```

## 🧪 Testing

```bash
# Test logic
python test_api.py

# Test with pytest
pytest tests/test_flights.py -v

# Start server and test API
python run.py
# Then visit: http://localhost:8000/docs
```

## 🔧 Features

- **Budget Levels**: low ($150-350), medium ($300-600), high ($500-1200)
- **Accessibility**: Single boolean flag for all accessibility features
- **Mock Data**: Works without API credentials
- **Skyscanner Integration**: Optional real flight data via RapidAPI

## 🔌 Real Flight Data (Optional)

To get real flight data:

1. Go to [RapidAPI Skyscanner](https://rapidapi.com/skyscanner-api-skyscanner-api-default/api/skyscanner-api/)
2. Sign up for free account
3. Subscribe to Skyscanner API (free tier: 1000 requests/month)
4. Copy your API key
5. Add to `.env`:
   ```env
   RAPIDAPI_KEY=your_api_key_here
   USE_MOCK_DATA=false
   ```

**Note**: Mock data works perfectly for hackathon demos!

## 📊 Response Example

```json
{
  "search_id": "uuid",
  "offers": [
    {
      "flight_id": "TEST_FLIGHT_1",
      "airline": "Delta",
      "price": 450.0,
      "accessibility_score": 8.5,
      "accessibility_features": [
        "Wheelchair assistance available",
        "Special seating options"
      ],
      "is_direct": true
    }
  ],
  "total_results": 8
}
```

## 🎯 For Hackathon

- ✅ Works immediately with mock data
- ✅ Simple boolean accessibility flag
- ✅ Budget-based pricing
- ✅ Automatic API fallback
- ✅ Ready for demo
- ✅ No API dependencies required
