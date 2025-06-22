import Space from "@/app/components/space/Space";
import InsertEmoticonIcon from "@mui/icons-material/InsertEmoticon";
import Link from "next/link";
import { useState } from "react";

type ChatActionProps = {
  onSend: (message: string) => void;
  allCollected?: boolean;
};

export default function ChatAction({
  onSend,
  allCollected = false,
}: ChatActionProps) {
  const [input, setInput] = useState("");

  function handleSubmit(e?: React.FormEvent | React.MouseEvent) {
    e?.preventDefault();
    if (!input.trim()) return;
    onSend(input.trim());
    setInput("");
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  }

  return (
    <div className="border-t-2 border-gray-200 px-4 pt-4 mb-2 sm:mb-0">
      <div className="relative flex">
        {allCollected ? (
          <Link className="w-full" href="/itinerary">
            <button
              type="button"
              className=" w-full cursor-pointer inline-flex items-center justify-center rounded-lg px-4 py-3 transition duration-500 ease-in-out text-white bg-[#0BC187]  hover:opacity-70 focus:outline-none"
            >
              <span className="font-bold">View My Trip Plan</span>
              <Space left={4} />
              <InsertEmoticonIcon />
            </button>
          </Link>
        ) : (
          <>
            <span className="absolute inset-y-0 flex items-center">
              <button
                type="button"
                className=" cursor-pointer inline-flex items-center justify-center rounded-full h-12 w-12 transition duration-500 ease-in-out text-gray-500 hover:bg-gray-300 focus:outline-none"
              >
                {/* Ícone */}
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  className="h-6 w-6 text-gray-600"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
                  />
                </svg>
              </button>
            </span>

            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              type="text"
              placeholder="Write your message!"
              className="w-full focus:outline-none focus:placeholder-gray-400 text-gray-600 placeholder-gray-600 pl-12 bg-gray-200 rounded-md py-3"
            />

            <div className="absolute right-0 items-center inset-y-0  sm:flex">
              {/* Outros botões */}

              <button
                onClick={handleSubmit}
                type="button"
                className=" cursor-pointer inline-flex items-center justify-center rounded-lg px-4 py-3 transition duration-500 ease-in-out text-white bg-[#0BC187]  hover:opacity-70 focus:outline-none"
              >
                <span className="font-bold">Send</span>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  className="h-6 w-6 ml-2 transform rotate-90"
                >
                  <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
                </svg>
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
