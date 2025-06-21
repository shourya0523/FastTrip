import pytest
import asyncio
from datetime import date, timedelta
from unittest.mock import AsyncMock, patch

from app.models.travel_models import FlightSearchRequest, BudgetLevel
from app.flights.flight_search import FlightSearchService
from app.flights.serpapi_adapter import SerpApiAdapter
from app.utils.mock_data import get_mock_flights


class TestFlightSearch:
    """Test flight search functionality"""
    
    @pytest.fixture
    def search_service(self):
        return FlightSearchService()
    
    @pytest.fixture
    def sample_request(self):
        return FlightSearchRequest(
            origin="JFK",
            destination="LAX",
            departure_date=date(2024, 6, 15),
            return_date=date(2024, 6, 22),
            num_travelers=2,
            budget=BudgetLevel.MEDIUM,
            accessibility_requirements=True
        )
    
    @pytest.mark.asyncio
    async def test_search_flights_mock(self, search_service, sample_request):
        """Test flight search with mock data"""
        response = await search_service.search_flights(sample_request)
        
        assert response.search_id is not None
        assert len(response.offers) > 0
        assert response.total_results > 0
        
        # Check first offer
        first_offer = response.offers[0]
        assert first_offer.origin == "JFK"
        assert first_offer.destination == "LAX"
        assert first_offer.price > 0
        assert 0 <= first_offer.accessibility_score <= 10
    
    @pytest.mark.asyncio
    async def test_search_flights_serpapi_success(self, search_service, sample_request):
        """Test flight search with SerpAPI success"""
        # Mock SerpAPI response
        mock_flights = [
            {
                "id": "test_flight_1",
                "airline": "American Airlines",
                "price": 299.99,
                "departure": {"at": "2024-06-15T10:00:00Z", "iataCode": "JFK"},
                "arrival": {"at": "2024-06-15T13:30:00Z", "iataCode": "LAX"},
                "duration": 210,
                "stops": 0
            }
        ]
        
        with patch.object(SerpApiAdapter, 'search_flights', new_callable=AsyncMock) as mock_search:
            mock_search.return_value = mock_flights
            
            # Mock settings to use SerpAPI
            with patch('app.config.settings.USE_MOCK_DATA', False):
                with patch('app.config.settings.SERPAPI_KEY', 'test_key'):
                    response = await search_service.search_flights(sample_request)
        
        assert response.search_id is not None
        assert len(response.offers) == 1
        assert response.offers[0].airline == "American Airlines"
        assert response.offers[0].price == 299.99
    
    @pytest.mark.asyncio
    async def test_search_flights_serpapi_fallback(self, search_service, sample_request):
        """Test flight search with SerpAPI failure fallback to mock"""
        with patch.object(SerpApiAdapter, 'search_flights', new_callable=AsyncMock) as mock_search:
            mock_search.side_effect = Exception("API Error")
            
            # Mock settings to use SerpAPI
            with patch('app.config.settings.USE_MOCK_DATA', False):
                with patch('app.config.settings.SERPAPI_KEY', 'test_key'):
                    response = await search_service.search_flights(sample_request)
        
        # Should fallback to mock data
        assert response.search_id is not None
        assert len(response.offers) > 0
    
    @pytest.mark.asyncio
    async def test_sort_flights_accessibility(self, search_service, sample_request):
        """Test flight sorting with accessibility requirements"""
        response = await search_service.search_flights(sample_request)
        
        # Should be sorted by accessibility score first
        scores = [offer.accessibility_score for offer in response.offers]
        assert scores == sorted(scores, reverse=True)
    
    @pytest.mark.asyncio
    async def test_sort_flights_price_only(self, search_service):
        """Test flight sorting without accessibility requirements"""
        request = FlightSearchRequest(
            origin="JFK",
            destination="LAX",
            departure_date=date(2024, 6, 15),
            return_date=date(2024, 6, 22),
            num_travelers=2,
            budget=BudgetLevel.MEDIUM,
            accessibility_requirements=False  # No accessibility requirements
        )
        
        response = await search_service.search_flights(request)
        
        # Should be sorted by price only
        prices = [offer.price for offer in response.offers]
        assert prices == sorted(prices)


class TestSerpApiAdapter:
    """Test SerpAPI adapter"""
    
    @pytest.fixture
    def adapter(self):
        return SerpApiAdapter()
    
    @pytest.mark.asyncio
    async def test_search_flights_no_api_key(self, adapter):
        """Test SerpAPI search without API key"""
        request = FlightSearchRequest(
            origin="JFK",
            destination="LAX",
            departure_date=date(2024, 6, 15),
            return_date=date(2024, 6, 22),
            num_travelers=2,
            budget=BudgetLevel.MEDIUM,
            accessibility_requirements=True
        )
        
        with patch('app.config.settings.SERPAPI_KEY', ''):
            with pytest.raises(Exception, match="No SerpAPI key"):
                await adapter.search_flights(request)
    
    def test_extract_price(self, adapter):
        """Test price extraction from various formats"""
        test_cases = [
            ("$299.99", 299.99),
            ("1,299.50", 1299.50),
            ("500", 500.0),
            ("invalid", 0.0)
        ]
        
        for price_str, expected in test_cases:
            result = adapter._extract_price(price_str)
            assert result == expected
    
    def test_parse_duration(self, adapter):
        """Test duration parsing"""
        test_cases = [
            ("5h 30m", 330),  # 5 hours 30 minutes
            ("2h", 120),      # 2 hours
            ("45m", 45),      # 45 minutes
            ("invalid", 0)    # Invalid format
        ]
        
        for duration_str, expected in test_cases:
            result = adapter._parse_duration(duration_str)
            assert result == expected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
