import React from "react";
import { Typography } from "@mui/material";

type TimelineItem = {
  time: string;
  place: string;
  description: string;
  type: string[];
};

type TimelineProps = {
  timelineData?: TimelineItem[];
};

const defaultTimelineData: TimelineItem[] = [
  {
    time: "08:30 AM",
    place: "Downtown Bakery",
    description:
      "Start your day with fresh artisan bread and natural juices in a cozy environment.",
    type: ["restaurant", "wheelChair Accessible"],
  },
  {
    time: "10:00 AM",
    place: "Modern Art Museum",
    description:
      "Explore contemporary art exhibitions and interactive installations.",
    type: ["attraction", "wheelChair Accessible"],
  },
  {
    time: "12:30 PM",
    place: "Vista Gourmet Restaurant",
    description:
      "Enjoy a panoramic view of the city while tasting traditional local dishes.",
    type: ["restaurant"],
  },
  {
    time: "2:00 PM",
    place: "Water Garden Park",
    description:
      "Relax with a peaceful walk through natural springs and lush gardens.",
    type: ["attraction", "outdoor"],
  },
  {
    time: "4:00 PM",
    place: "Square Café",
    description:
      "Take a break for coffee and try local desserts before the final activity.",
    type: ["restaurant", "wheelChair Accessible"],
  },
  {
    time: "5:30 PM",
    place: "Sunset Viewpoint",
    description:
      "Wrap up the day watching the sunset and capturing beautiful memories.",
    type: ["attraction", "viewpoint"],
  },
];

const Timeline: React.FC<TimelineProps> = ({
  timelineData = defaultTimelineData,
}) => {
  return (
    <section className="relative py-10 px-4 max-w-screen-lg mx-auto">
      {/* Vertical line */}
      <div className="absolute left-6 sm:left-1/2 transform sm:-translate-x-1/2 top-0 bottom-0 w-1 bg-[#0BC192BF]" />

      {timelineData.map((item, index) => {
        const isEven = index % 2 === 0;

        return (
          <div
            key={index}
            className="relative my-8 flex flex-col sm:flex-row sm:items-center"
          >
            {/* Timeline Dot */}
            <div className="absolute top-2 sm:top-1 left-6 sm:left-1/2 sm:-translate-x-1/2 w-5 h-5 rounded-full border-4 border-[#0BC187] bg-white z-10" />

            {/* Timeline Content */}
            <div
              className={`mt-6 sm:mt-0 sm:w-1/2 px-4 ${
                isEven
                  ? "sm:pr-12 sm:text-right"
                  : "sm:pl-12 sm:text-left sm:ml-auto"
              }`}
            >
              <Typography>{item.time}</Typography>
              <div className="bg-[#333C42] text-white p-4 rounded shadow-md">
                <h2 className="text-lg font-semibold mb-2">{item.place}</h2>
                {item.place && (
                  <div className="bg-[#2B343A] text-xs text-gray-300 rounded px-2 py-1 mb-2 inline-block">
                    <i
                      className="fa fa-certificate mr-1"
                      aria-hidden="true"
                    ></i>
                    {item.place}
                  </div>
                )}

                <p className="text-sm leading-relaxed text-gray-300 mb-2">
                  {item.description}
                </p>
                {item.type && (
                  <ul className="flex flex-wrap gap-1 text-xs">
                    {item.type.map((typeItem, i) => (
                      <li
                        key={i}
                        className="bg-[#40484D] text-gray-300 rounded px-2 py-1"
                      >
                        {typeItem}
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
          </div>
        );
      })}
    </section>
  );
};

export default Timeline;
