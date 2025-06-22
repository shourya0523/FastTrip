"use client";

import {
  GoogleMap,
  DirectionsRenderer,
  useJsApiLoader,
} from "@react-google-maps/api";
import { useEffect, useMemo, useState } from "react";
import { ItineraryDay } from "../../types/itinerary"; // ou ajustar o caminho

type Props = {
  itinerary: ItineraryDay[];
};

const containerStyle = {
  width: "100%",
  height: "80vh",
  borderRadius: "15px",
};

const ItineraryMap = ({ itinerary }: Props) => {
  const { isLoaded } = useJsApiLoader({
    googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY!,
    libraries: ["places"],
  });

  const [directions, setDirections] =
    useState<google.maps.DirectionsResult | null>(null);
  const [selectedDay, setSelectedDay] = useState(1);

  const selectedActivities = useMemo(() => {
    return itinerary.find((day) => day.day === selectedDay)?.activities ?? [];
  }, [selectedDay, itinerary]);

  useEffect(() => {
    const getDirections = async () => {
      if (selectedActivities.length < 2) return;

      const directionsService = new google.maps.DirectionsService();

      const origin = selectedActivities[0].address;
      const destination =
        selectedActivities[selectedActivities.length - 1].address;
      const waypoints = selectedActivities.slice(1, -1).map((a) => ({
        location: a.address,
        stopover: true,
      }));

      directionsService.route(
        {
          origin,
          destination,
          waypoints,
          travelMode: google.maps.TravelMode.DRIVING,
        },
        (result, status) => {
          if (status === "OK" && result) {
            setDirections(result);
          }
        }
      );
    };

    if (isLoaded) getDirections();
  }, [isLoaded, selectedActivities]);

  const center = {
    lat: 36.1627,
    lng: -86.7816, // Nashville
  };

  if (!isLoaded) return <p>Loading map...</p>;

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap gap-2">
        {itinerary.map((d) => (
          <button
            key={d.day}
            className={`cursor-pointer px-4 py-2 rounded-full text-sm ${
              d.day === selectedDay ? "bg-[#0BC192] text-white" : "bg-gray-100"
            }`}
            onClick={() => setSelectedDay(d.day)}
          >
            Day {d.day}
          </button>
        ))}
      </div>

      <GoogleMap
        mapContainerStyle={containerStyle}
        center={center}
        zoom={13}
        options={{ streetViewControl: false }}
      >
        {directions && <DirectionsRenderer directions={directions} />}
      </GoogleMap>
    </div>
  );
};

export default ItineraryMap;
