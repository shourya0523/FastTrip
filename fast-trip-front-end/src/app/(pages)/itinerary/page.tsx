"use client";
import FlightCard from "@/app/components/flightCard/FlightCard";
import Timeline from "@/app/components/timeline/Timeline";
import GoogleMap from "@/app/components/googleMaps/GoogleMaps";
import { useEffect, useState } from "react";
import { getData, postData } from "@/app/lib/api";
import GroupButton from "@/app/components/groupButton/groupButton";
import { FlightsResponse } from "@/app/types/flight";
import { Typography } from "@mui/material";

export default function Itinerary() {
  const [flights, setFlights] = useState<FlightsResponse | null>(null);
  const [selectedIndex, setSelectedIndex] = useState<number | null>(0);
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
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
      } catch (err: any) {
        setError(err?.message || "Erro inesperado");
      } finally {
        setLoading(false);
      }
    }

    fetchFlight();
  }, []);

  console.log("selectIndex", selectedIndex);

  return (
    <>
      <GroupButton
        count={flights?.offers.length || 0}
        onSelect={setSelectedIndex}
      />

      {selectedIndex && (
        <div className="transition-opacity duration-500 opacity-100">
          <FlightCard />
        </div>
      )}
      <Timeline />
      <GoogleMap />
    </>
  );
}
