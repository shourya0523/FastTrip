"use client";

import { Typography } from "@mui/material";
import Chat from "./components/chat-UI/Chat";
import Space from "./components/space/Space";

export default function Home() {
  return (
    <section
      className="flex flex-col pt-32 max-md:pt-2 justify-around items-center"
      aria-label="Seção de destaque para prospecção de clientes"
    >
      <Typography variant="title">
        Hey, ready to start personalizing your trip?
      </Typography>
      <Space top={20} />
      <div className="lg:w-[600px] flex justify-center">
        <div className="w-full relative rounded-xl p-1 bg-gradient-to-r from-[#0bc192] via-[#0dabc7] to-[#0bc192]">
          <div className="rounded-xl bg-white p-4">
            <Chat />
          </div>
        </div>
      </div>
    </section>
  );
}
