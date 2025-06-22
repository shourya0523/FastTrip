"use client";
import FlightCard from "@/app/components/flightCard/FlightCard";
import Timeline from "@/app/components/timeline/Timeline";
import GoogleMap from "@/app/components/googleMaps/GoogleMaps";
import { useEffect, useState } from "react";
import { postData } from "@/app/lib/api";
import GroupButton from "@/app/components/groupButton/groupButton";
import { FlightsResponse } from "@/app/types/flight";
import { Typography } from "@mui/material";
import Space from "@/app/components/space/Space";
import Divider from "@mui/material/Divider";
import DownloadButton from "@/app/components/download-button/DownloadButton";
import trip_itinerary from "../../mocks/trip_itinerary.json";

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
      <div className="lg:w-[600px] text-center m-auto   flex flex-col justify-center items-center ">
        <Typography variant="hero" lineHeight="50px" fontWeight="bold">
          Your Accessible Itinerary is Ready —{" "}
          <span className="text-[#0BC192]">Enjoy the Journey</span>
        </Typography>
        <Typography variant="titleSmall">
          We’ve crafted a thoughtful travel plan just for you, fully
          personalized, accessible, and ready to explore at your own pace.
        </Typography>
      </div>
      <Space bottom={10} />
      <Divider />
      <Space bottom={10} />
      <Typography className="flex justify-center" variant="overline">
        *Save your itinerary for easy access during your trip.
      </Typography>
      <Space bottom={2} />
      <DownloadButton />
      <Space bottom={10} />
      <Divider />
      <Space bottom={10} />
      <Typography
        className="flex justify-center"
        variant="title"
        lineHeight="50px"
        fontWeight="bold"
      >
        Flights
      </Typography>
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
      <Typography
        className="flex justify-center"
        variant="title"
        lineHeight="50px"
        fontWeight="bold"
      >
        Timeline
      </Typography>
      <Typography className="flex justify-center" variant="overline">
        *Your Personalized Itinerary
      </Typography>
      <Space bottom={10} />
      <Timeline itinerary={trip_itinerary.itinerary} />
      <Space bottom={10} />
      <Typography
        className="flex justify-center"
        variant="title"
        lineHeight="50px"
        fontWeight="bold"
      >
        Maps
      </Typography>
      <Typography className="flex justify-center" variant="overline">
        *Your Trip on the Map
      </Typography>
      <Space bottom={10} />
      <GoogleMap />
    </>
  );
}
