import React from "react";
import SyncIcon from "@mui/icons-material/Sync";
import FlightTakeoffIcon from "@mui/icons-material/FlightTakeoff";

import { FlightOffer } from "../../types/flight";
import AirplanemodeActiveOutlinedIcon from "@mui/icons-material/AirplanemodeActiveOutlined";
import Airport from "../../../../public/airport.png";
import Image from "next/image";
type FlightCardProps = {
  offer: FlightOffer;
};

const FlightCard: React.FC<FlightCardProps> = ({ offer }) => {
  const {
    airline,
    flight_number,
    departure_time,
    arrival_time,
    origin,
    destination,
    price,
    currency,
  } = offer;

  const departureDate = new Date(departure_time).toLocaleDateString(undefined, {
    weekday: "long",
    day: "numeric",
    month: "short",
  });

  const departureHour = new Date(departure_time).toLocaleTimeString(undefined, {
    hour: "2-digit",
    minute: "2-digit",
  });

  const arrivalHour = new Date(arrival_time).toLocaleTimeString(undefined, {
    hour: "2-digit",
    minute: "2-digit",
  });

  return (
    <div className="p-10">
      <div className="max-w-full bg-white flex flex-col rounded overflow-hidden shadow-lg">
        {/* Header */}
        <div className="flex  items-center flex-row items-baseline bg-gray-100 p-2">
          <AirplanemodeActiveOutlinedIcon className="text-gray-500" />
          <h1 className="ml-2 uppercase font-bold text-gray-500">Departure</h1>
          <p className="ml-2 font-normal text-gray-500">{departureDate}</p>
        </div>

        {/* Flight Class (fixo por enquanto) */}
        <div className="mt-2 flex justify-start bg-white p-2">
          <div className="flex items-center mx-2 ml-6 px-2 items-baseline rounded-full bg-gray-100 p-1">
            <AirplanemodeActiveOutlinedIcon
              className="text-gray-500"
              style={{ fontSize: 18 }}
            />
            <p className="ml-1 text-sm text-gray-500">Economy</p>
          </div>
        </div>

        <div className="mt-2 flex flex-wrap sm:flex-nowrap justify-between mx-6">
          <div className="flex items-center p-2">
            <Image src={Airport} alt="" width={50} />
            <div className="ml-2 flex flex-col">
              <p className="text-xs font-bold text-gray-500">{airline}</p>
              <p className="text-xs text-gray-500">{flight_number}</p>
              <p className="text-xs text-gray-500">1 carry-on, 1 checked</p>
            </div>
          </div>

          <div className="flex flex-col p-2">
            <p className="font-bold">{departureHour}</p>
            <p className="text-gray-500">
              <span className="font-bold">XXX</span> {origin}
            </p>
            <p className="text-gray-500">Country A</p>
          </div>

          <div className="flex flex-col p-2">
            <p className="font-bold">{arrivalHour}</p>
            <p className="text-gray-500">
              <span className="font-bold">YYY</span> {destination}
            </p>
            <p className="text-gray-500">Country B</p>
          </div>
        </div>

        {/* Ticket Options */}
        <div className="mt-4 bg-gray-100 flex flex-wrap md:flex-nowrap justify-between items-baseline">
          {[
            {
              name: "Standard Ticket",
              price: `$${price.toFixed(2)} ${currency}`,
              description: "Non-refundable",
              bgColor: "bg-gray-400",
              textColor: "text-white",
              icon: <FlightTakeoffIcon />,
              buttonBgColor: "bg-white",
              buttonTextColor: "text-[rgb(105_114_130)]",
            },
            {
              name: "Flexible Ticket",
              price: `$${(price * 1.5).toFixed(2)} ${currency}`,
              description: "Refundable",
              bgColor: "bg-[#0BC187]",
              textColor: "text-white",
              icon: <SyncIcon />,
              buttonBgColor: "bg-[#0BC187]",
              buttonTextColor: "text-white",
            },
          ].map((ticket, i) => (
            <div key={i} className="flex mx-6 py-4 flex-wrap items-center">
              <div
                className={`w-12 h-10 p-2 rounded-full flex justify-center items-center ${ticket.bgColor} ${ticket.textColor}`}
              >
                {ticket.icon}
              </div>
              <div className="text-sm mx-2 flex flex-col">
                <p>{ticket.name}</p>
                <p className="font-bold">{ticket.price}</p>
                <p className="text-xs text-gray-500">{ticket.description}</p>
              </div>
              <button
                className={`cursor-pointer w-32 h-11 rounded border border-[#e3e3e3] mx-2 flex justify-center items-center ${ticket.buttonBgColor} ${ticket.buttonTextColor}`}
              >
                Book
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default FlightCard;
