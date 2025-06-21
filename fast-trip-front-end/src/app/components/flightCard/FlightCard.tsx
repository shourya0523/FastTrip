import React from "react";
import SyncIcon from "@mui/icons-material/Sync";
import FlightTakeoffIcon from "@mui/icons-material/FlightTakeoff";
import CardTravelIcon from "@mui/icons-material/CardTravel";
import ConnectingAirportsIcon from "@mui/icons-material/ConnectingAirports";

type TicketOption = {
  name: string;
  price: string;
  description: string;
  bgColor: string;
  textColor: string;
  icon: React.ReactNode;
  buttonBgColor: string;
  buttonTextColor: string;
};

type FlightCardProps = {
  departureDate?: string;
  flightClass?: string;
  airlineName?: string;
  airlineCode?: string;
  baggageInfo?: string;
  departureTime?: string;
  departureAirportCode?: string;
  departureAirportCity?: string;
  departureCountry?: string;
  arrivalTime?: string;
  arrivalAirportCode?: string;
  arrivalAirportCity?: string;
  arrivalCountry?: string;
  ticketOptions?: TicketOption[];
};

const FlightCard: React.FC<FlightCardProps> = ({
  departureDate = "Wednesday 18 Aug",
  flightClass = "Economy",
  airlineName = "Qatar Airways",
  airlineCode = "QR1456",
  baggageInfo = "2*23kg",
  departureTime = "18:25",
  departureAirportCode = "HRE",
  departureAirportCity = "Harare",
  departureCountry = "Zimbabwe",
  arrivalTime = "19:25",
  arrivalAirportCode = "LUN",
  arrivalAirportCity = "Lusaka",
  arrivalCountry = "Zambia",
  ticketOptions = [
    {
      name: "Standard Ticket",
      price: "$404.73",
      description: "Price per adult",
      bgColor: "bg-gray-400",
      textColor: "text-white",
      icon: <FlightTakeoffIcon />,
      buttonBgColor: "bg-white",
      buttonTextColor: "text-[rgb(105_114_130)]",
    },
    {
      name: "Flexible Ticket",
      price: "$605.43",
      description: "Price per adult",
      bgColor: "bg-[#0BC187]",
      textColor: "text-white",
      icon: <SyncIcon />,
      buttonBgColor: "bg-[#0BC187]",
      buttonTextColor: "text-white",
    },
  ],
}) => {
  return (
    <div className="p-10">
      <div className="max-w-full bg-white flex flex-col rounded overflow-hidden shadow-lg">
        {/* Header */}
        <div className="flex flex-row items-baseline bg-gray-100 p-2">
          <ConnectingAirportsIcon className="text-gray-500" />
          <h1 className="ml-2 uppercase font-bold text-gray-500">Departure</h1>
          <p className="ml-2 font-normal text-gray-500">{departureDate}</p>
        </div>

        {/* Flight Class */}
        <div className="mt-2 flex justify-start bg-white p-2">
          <div className="flex mx-2 ml-6 px-2 items-baseline rounded-full bg-gray-100 p-1">
            <svg
              viewBox="0 0 64 64"
              className="h-3 w-3 fill-gray-600"
              aria-hidden="true"
            >
              <path d="M43.389 38.269L29.222 61.34a1.152 1.152 0 01-1.064.615H20.99..." />
            </svg>
            <p className="ml-1 text-sm text-gray-500">{flightClass}</p>
          </div>
        </div>

        {/* Flight Info */}
        <div className="mt-2 flex flex-wrap sm:flex-nowrap justify-between mx-6">
          <div className="flex items-center p-2">
            <CardTravelIcon className="text-gray-500" />
            <div className="ml-2 flex flex-col">
              <p className="text-xs font-bold text-gray-500">{airlineName}</p>
              <p className="text-xs text-gray-500">{airlineCode}</p>
              <p className="text-xs text-gray-500">{baggageInfo}</p>
            </div>
          </div>

          <div className="flex flex-col p-2">
            <p className="font-bold">{departureTime}</p>
            <p className="text-gray-500">
              <span className="font-bold">{departureAirportCode}</span>{" "}
              {departureAirportCity}
            </p>
            <p className="text-gray-500">{departureCountry}</p>
          </div>

          <div className="flex flex-col p-2">
            <p className="font-bold">{arrivalTime}</p>
            <p className="text-gray-500">
              <span className="font-bold">{arrivalAirportCode}</span>{" "}
              {arrivalAirportCity}
            </p>
            <p className="text-gray-500">{arrivalCountry}</p>
          </div>
        </div>

        {/* Ticket Options */}
        <div className="mt-4 bg-gray-100 flex flex-wrap md:flex-nowrap justify-between items-baseline">
          {ticketOptions.map((ticket, i) => (
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
                className={`cursor-pointer w-32 h-11 rounded border mx-2 flex justify-center items-center ${ticket.buttonBgColor} ${ticket.buttonTextColor}`}
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
