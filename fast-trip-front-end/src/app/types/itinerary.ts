export type Activity = {
  time: string;
  type: string;
  name: string;
  address: string;
  duration: string;
};

export type ItineraryDay = {
  day: number;
  date?: string;
  activities: Activity[];
};
