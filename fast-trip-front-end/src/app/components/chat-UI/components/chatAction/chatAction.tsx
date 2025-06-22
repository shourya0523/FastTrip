/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";
import Space from "@/app/components/space/Space";
import InsertEmoticonIcon from "@mui/icons-material/InsertEmoticon";
import Link from "next/link";
import { useRef, useState } from "react";

type ChatActionProps = {
  onSend: (message: string) => void;
  allCollected?: boolean;
};

export default function ChatAction({
  onSend,
  allCollected = false,
}: ChatActionProps) {
  const [input, setInput] = useState("");
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef<any>(null);

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

  const toggleListening = () => {
    if (!("webkitSpeechRecognition" in window)) {
      alert("Seu navegador não suporta reconhecimento de voz.");
      return;
    }

    if (!recognitionRef.current) {
      const SpeechRecognition = (window as any).webkitSpeechRecognition;
      const recognition = new SpeechRecognition();
      recognition.lang = "en-US";
      recognition.interimResults = false;
      recognition.maxAlternatives = 1;

      recognition.onresult = (event: any) => {
        const text = event.results[0][0].transcript;
        setInput((prev) => prev + " " + text);
      };

      recognition.onerror = (event: any) => {
        console.error("Erro de voz:", event.error);
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognitionRef.current = recognition;
    }

    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      recognitionRef.current.start();
      setIsListening(true);
    }
  };

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
                onClick={toggleListening}
                className={`cursor-pointer inline-flex items-center justify-center rounded-full h-12 w-12 transition duration-500 ease-in-out text-white ${
                  isListening ? "bg-red-500" : "bg-gray-500"
                } focus:outline-none`}
                title="Click to talk"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  className="h-6 w-6"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 1a3 3 0 00-3 3v6a3 3 0 006 0V4a3 3 0 00-3-3zm0 12a7 7 0 01-7-7m14 0a7 7 0 01-7 7v4m0 0H8m4 0h4"
                  />
                </svg>
              </button>
            </span>

            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              type="text"
              placeholder="Write or Talk!"
              className="w-full focus:outline-none focus:placeholder-gray-400 text-gray-600 placeholder-gray-600 pl-15 bg-gray-200 rounded-md py-3"
            />

            <div className="absolute right-0 items-center inset-y-0  sm:flex">
              <button
                onClick={handleSubmit}
                type="button"
                className="cursor-pointer inline-flex items-center justify-center rounded-lg px-4 py-3 transition duration-500 ease-in-out text-white bg-[#0BC187] hover:opacity-70 focus:outline-none"
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
