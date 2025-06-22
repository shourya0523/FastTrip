type FlightOffer = {
  flight_id: string;
  airline: string;
  flight_number: string;
  origin: string;
  destination: string;
  departure_time: string; // ISO date string
  arrival_time: string; // ISO date string
  duration_minutes: number;
  price: number;
  currency: string;
  accessibility_score: number;
  accessibility_features: string[];
  is_direct: boolean;
  stops: number;
  aircraft_type: string;
};

type SearchSummary = {
  origin: string;
  destination: string;
  departure_date: string; // yyyy-mm-dd
  num_travelers: number;
  budget: string;
  accessibility_requirements: boolean;
};

export type FlightsResponse = {
  search_id: string;
  offers: FlightOffer[];
  total_results: number;
  search_summary: SearchSummary;
};
