# FastTrip - AI-Powered Accessible Travel Planning Platform
An intelligent travel planning platform designed specifically for accessibility-conscious travelers 55+ using Google Gemini AI

## 🌟 Overview
FastTrip is an AI-powered travel planning platform that prioritizes accessibility and ease of use for travelers aged 55 and above. Built during a 48-hour hackathon, it leverages Google Gemini AI to provide personalized, accessibility-focused travel recommendations and itineraries.
### [Demo](https://drive.google.com/file/d/1aEV7GtAFdfEdpCkorSwyDbsyh4MK7tXq/view?usp=sharing)
## ✨ Key Features
### 🤖 AI-Powered Conversation
- Natural language trip planning with Google Gemini 2.5 Flash
- Intelligent parameter extraction from conversational input
- Context-aware follow-up questions
- Session-based state management
### ♿ Accessibility-First Design
- Comprehensive accessibility scoring (0-10 scale)
- Wheelchair accessibility considerations
- Mobility-friendly venue recommendations
- Large fonts (≥18px) and high contrast (≥4.5:1)
- Screen reader compatibility
- Keyboard navigation support
### 🗺️ Smart Itinerary Generation
- AI-curated place recommendations
- Google Places integration with accessibility data
- Intelligent scheduling based on user preferences
- Interactive maps with accessibility markers
- PDF export functionality
### ✈️ Flight Search & Booking
- Amadeus API integration for flight search
- Accessibility-focused flight scoring
- Direct flight preferences
- Budget-conscious recommendations
## 🏗️ Architecture
### Backend
- Framework : FastAPI (Python 3.9+)
- AI Engine : Google Gemini 2.5 Flash
- APIs : Google Places, Serapi
- Session Management : In-memory (demo-focused)
### Frontend
- Framework : Next.js 15 with React 19
- Styling : Tailwind CSS 4
- UI Components : Material-UI (MUI) 7
- Maps : Google Maps API
- Testing : Jest + Cypress
## 🚀 Quick Start
### Prerequisites
- Python 3.9+
- Node.js 18+
- Google Gemini API Key
- Google Places API Key
- Amadeus API Credentials
### Backend Setup
1. Navigate to backend directory
```
cd travel-ai-backend
```
2. Install dependencies
```
pip install -r requirements.txt
```
3. Set up environment variables
```
cp .env.example .env
```
Edit .env with your API keys:

```
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_PLACES_API_KEY=your_google_places_key
AMADEUS_API_KEY=your_amadeus_key
AMADEUS_API_SECRET=your_amadeus_secret
```
4. Run the development server
```
uvicorn app.main:app --reload
```
Backend will be available at http://localhost:8000

### Frontend Setup
1. Navigate to frontend directory
```
cd fast-trip-front-end
```
2. Install dependencies
```
npm install
```
3. Set up environment variables
```
cp .env.local.example .env.local
```
Edit .env.local with your API keys:

```
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_google_ma
ps_key
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```
4. Run the development server
```
npm run dev
```
Frontend will be available at http://localhost:3000

## 📦 Dependencies
### Backend Requirements
```
fastapi>=0.104.1
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
aiohttp>=3.9.1
pytest>=7.4.3
pytest-asyncio>=0.21.1
python-dotenv>=1.0.0
google-generativeai>=0.3.0
googlemaps>=4.10.0
```
### Frontend Dependencies
```
{
  "dependencies": {
    "@emotion/react": "^11.14.0",
    "@emotion/styled": "^11.14.0",
    "@mui/material": "^7.0.2",
    "@mui/icons-material": "^7.0.2",
    "@react-google-maps/api": "^2.20.7",
    "html2canvas": "^1.4.1",
    "jspdf": "^3.0.1",
    "next": "15.3.1",
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  },
  "devDependencies": {
    "@types/react": "^19",
    "@types/node": "^20",
    "cypress": "^14.3.2",
    "jest": "^29.7.0",
    "tailwindcss": "^4",
    "typescript": "^5"
  }
}
```
## 🧪 Testing
### Backend Tests
```
cd travel-ai-backend
pytest
```
### Frontend Tests
```
cd fast-trip-front-end
npm test
```
### E2E Tests
```
cd fast-trip-front-end
npm run cypress:open
```
## 🎯 API Endpoints
### Chat API
```
POST /api/v1/chat/message
Content-Type: application/json

{
  "message": "I want to plan a trip to New 
  York",
  "session_id": "unique-session-id"
}
```
### Flight Search
```
POST /api/v1/flights/search
Content-Type: application/json

{
  "origin": "LAX",
  "destination": "JFK",
  "departure_date": "2024-06-15",
  "accessibility_needs": ["wheelchair"]
}
```
### Health Check
```
GET /health
```
## ♿ Accessibility Features
### Scoring System (0-10 scale)
- Direct flights : +2 points
- Wheelchair accessible venues : +2 points
- Ground floor access : +1.5 points
- Accessible transportation : +1.5 points
- Short walking distances : +1 point
- Accessible parking : +1 point
- Medical facilities nearby : +0.5 points
### UI Accessibility
- Minimum font size: 18px
- Color contrast ratio: 4.5:1 minimum
- Clickable areas: 44px minimum
- Full keyboard navigation
- ARIA labels on all interactive elements
- Screen reader compatibility
## 🎨 Design Principles
### User Experience
- Skeleton-first development : Core features before advanced ones
- Accessibility-first design : Every component supports assistive technology
- Conversational interface : Natural language trip planning
- Visual clarity : Large fonts, high contrast, clean layouts
### Technical
- AI-powered intelligence : Gemini integration for smart recommendations
- Graceful degradation : Fallback to mock data if APIs fail
- Performance targets : <5 second API responses, <2 second page loads
- Error handling : User-friendly messages, no technical jargon
## 🚀 Performance Targets
- Chat response : <3 seconds
- API search : <5 seconds
- Itinerary generation : <10 seconds
- PDF export : <5 seconds
- Page load : <2 seconds
- Gemini API calls : <5 seconds with fallback
## 🎯 Target Users
- Primary : Travelers aged 55+ with mobility considerations
- Secondary : Family members planning for elderly relatives
- Tertiary : Travel agents specializing in accessible travel
## 🛠️ Development
### Project Structure
```
FastTrip/
├── travel-ai-backend/          # FastAPI 
backend
│   ├── app/
│   │   ├── api/               # API routes
│   │   ├── core/              # Core 
business logic
│   │   ├── models/            # Pydantic 
models
│   │   └── utils/             # Utilities
│   └── tests/                 # Backend tests
├── fast-trip-front-end/       # Next.js 
frontend
│   ├── src/
│   │   ├── app/               # App router 
pages
│   │   └── components/        # React 
components
│   └── cypress/               # E2E tests
└── ai-brain/                  # AI 
processing modules
    ├── ranker.py              # Place scoring
    ├── gen_iten.py            # Itinerary 
    generation
    └── chatbot.py             # Conversation 
    handling
```
### Commit Standards
- feat : New features
- fix : Bug fixes
- docs : Documentation updates
- test : Test additions/updates
Example: feat(gemini): add AI-powered place scoring

## 🔧 Environment Variables
### Backend (.env)
```
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_PLACES_API_KEY=your_google_places_key
SERAPI_API_KEY =your_serapi_key
```
### Frontend (.env.local)
```
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_google_ma
ps_key
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```
## 🤝 Contributing
1. Fork the repository
2. Create a feature branch ( git checkout -b feature/amazing-feature )
3. Commit your changes ( git commit -m 'feat: add amazing feature' )
4. Push to the branch ( git push origin feature/amazing-feature )
5. Open a Pull Request
### Development Guidelines
- Follow accessibility-first principles
- Write tests for new features
- Maintain high contrast and large fonts
- Test with screen readers
- Include ARIA labels
## 📄 License
This project is licensed under the MIT License

## 🙏 Acknowledgments
- Google Gemini AI for intelligent conversation processing
- Google Places API for comprehensive location data
- Serapi for flight search capabilities
- Material-UI for accessible React components
- Next.js for the robust frontend framework
## 📞 Support
For support, please open an issue on GitHub or contact the development team.

Built with ❤️ for accessible travel planning
