"use client";
import FlightCard from "@/app/components/flightCard/FlightCard";
import Timeline from "@/app/components/timeline/Timeline";
import GoogleMap from "@/app/components/googleMaps/GoogleMaps";
import { useEffect, useState } from "react";
import { postData } from "@/app/lib/api";
import GroupButton from "@/app/components/groupButton/groupButton";
import { FlightsResponse } from "@/app/types/flight";

export default function Itinerary() {
  const [flights, setFlights] = useState<FlightsResponse | null>(null);
  const [selectedIndex, setSelectedIndex] = useState<number>(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchFlight() {
      try {
        const data = await postData("flights/search", {
          origin: "Boston",
          destination: "Brazil",
          departure_date: "2025-06-22",
          return_date: "2025-06-22",
          num_travelers: 4,
          budget: "medium",
          accessibility_requirements: true,
        });
        setFlights(data);
      } catch (err) {
        setError(err?.message || "Erro inesperado");
      } finally {
        setLoading(false);
      }
    }

    fetchFlight();
  }, []);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-[#0BC192]" />
        <p className="mt-4 text-gray-600 text-sm">
          Searching for the best flights...
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center h-screen text-red-600">
        <p className="text-lg font-semibold">Oops! {error}</p>
      </div>
    );
  }

  return (
    <>
      <GroupButton
        count={flights?.offers.length || 0}
        onSelect={setSelectedIndex}
        selectedIndex={selectedIndex}
      />

      {flights?.offers && (
        <div className="transition-opacity duration-500 opacity-100">
          <FlightCard offer={flights.offers[selectedIndex]} />
        </div>
      )}

      <Timeline />
      <GoogleMap />
    </>
  );
}
