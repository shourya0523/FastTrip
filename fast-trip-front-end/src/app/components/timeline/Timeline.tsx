export type Activity = {
  time: string;
  type: string;
  name: string;
  address: string;
  duration: string;
};

export type ItineraryDay = {
  day: number;
  date: string;
  activities: Activity[];
};

type ItineraryTimelineProps = {
  itinerary: ItineraryDay[];
};

export default function ItineraryTimeline({
  itinerary,
}: ItineraryTimelineProps) {
  return (
    <div className="max-w-6xl px-4 py-10 sm:px-6 lg:px-8 mx-auto">
      <div className="grid gap-8 md:grid-cols-2">
        {itinerary.map(({ day, date, activities }) => (
          <div
            key={day}
            className="relative pl-6 border-l-2 border-[#0BC192] bg-white rounded-xl p-6 shadow-md"
          >
            <div className="absolute -left-3 top-6 w-6 h-6 bg-[#0BC192] rounded-full text-white text-sm font-semibold flex items-center justify-center shadow-md">
              {day}
            </div>
            <h3 className="text-lg font-semibold text-gray-800 mb-6">
              Day {day} –
              {new Date(date).toLocaleDateString(undefined, {
                weekday: "long",
                month: "long",
                day: "numeric",
              })}
            </h3>
            <ul className="space-y-6">
              {activities.map((activity, index) => (
                <li key={index} className="relative ml-2">
                  <div className="absolute left-[-11px] top-2.5 w-2 h-2 bg-[#0BC192] rounded-full" />
                  <div className="ml-4">
                    <p className="text-sm text-gray-500">
                      {activity.time} •{" "}
                      {activity.type.charAt(0).toUpperCase() +
                        activity.type.slice(1)}
                    </p>
                    <p className="text-base font-medium text-gray-800">
                      {activity.name}
                    </p>
                    <p className="text-sm text-gray-600">{activity.address}</p>
                    <p className="text-sm text-gray-500 italic">
                      Duration: {activity.duration}
                    </p>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}
