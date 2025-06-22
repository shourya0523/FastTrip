"use client";

import { Typography } from "@mui/material";

import Chat from "./components/chat-UI/Chat";
import Space from "./components/space/Space";
import FAQSection from "./components/faq/Faq";

export default function Home() {
  return (
    <section
      className="flex flex-col pt-32 max-md:pt-2 justify-around items-center"
      aria-label="Seção de destaque para prospecção de clientes"
    >
      <div className="lg:w-[600px] ">
        <Typography variant="hero" lineHeight="50px" fontWeight="bold">
          Inclusive Travel Starts Here —{" "}
          <span className="text-[#0BC192]"> Built for You</span>
        </Typography>
        <Typography variant="titleSmall">
          Smart travel planning for people with disabilities. Create
          personalized and accessible itineraries: no stress, no barriers.
        </Typography>
      </div>
      <Space top={10} />
      <div className="lg:w-[600px] flex justify-center">
        <div className="w-full relative rounded-xl p-1 bg-gradient-to-r from-[#0bc192] via-[#0dabc7] to-[#0bc192]">
          <div className="rounded-xl bg-white p-4">
            <Chat />
          </div>
        </div>
      </div>

      <FAQSection />
    </section>
  );
}
