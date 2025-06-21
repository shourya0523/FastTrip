"use client";
import FlightCard from "@/app/components/flightCard/FlightCard";
import Timeline from "@/app/components/timeline/Timeline";
import GoogleMap from "@/app/components/googleMaps/GoogleMaps";

export default function Itinerary() {
  return (
    <>
      <FlightCard />
      <Timeline />
      <GoogleMap />
    </>
  );
}
