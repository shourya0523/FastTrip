import { Divider } from "@mui/material";
import { useState } from "react";
import Space from "../space/Space";

const faqs = [
  {
    id: 1,
    question: "Can I cancel or change my trip later?",
    answer:
      "Yes! You can modify or cancel your trip anytime. We recommend saving your link or logging in to access your plan later.",
  },
  {
    id: 2,
    question: "Is Fast Trip free to use?",
    answer:
      "Yes, Fast Trip is completely free for users. We're here to help you plan accessible trips without extra cost.",
  },
  {
    id: 3,
    question: "How does Fast Trip create my itinerary?",
    answer:
      "We use AI to analyze your preferences, accessibility needs, and budget to create a custom itinerary that's inclusive and stress-free.",
  },
  {
    id: 4,
    question: "Is Fast Trip accessible for screen readers?",
    answer:
      "Absolutely. We've designed Fast Trip to be compatible with assistive technologies, including screen readers and keyboard navigation.",
  },
  {
    id: 5,
    question: "What types of disabilities does Fast Trip support?",
    answer:
      "We aim to support a wide range of needs — including mobility, visual, auditory, and cognitive accommodations — and are always improving.",
  },
  {
    id: 6,
    question: "Can I share my trip plan with someone else?",
    answer:
      "Yes! After your itinerary is generated, you can share it easily via link or download it for offline access.",
  },
];

export default function FAQSection() {
  const [openId, setOpenId] = useState<number | null>(1);

  const toggle = (id: number) => {
    setOpenId((prev) => (prev === id ? null : id));
  };

  return (
    <div className="w-full px-4 py-10 sm:px-6 lg:px-8 lg:py-14 mx-auto">
      <Space bottom={10} />
      <Divider />
      <Space bottom={10} />
      <div className="w-full mx-auto text-center mb-10 lg:mb-14">
        <h2 className="text-2xl font-bold md:text-4xl md:leading-tight">FAQ</h2>
        <p className="mt-1 text-gray-600">
          Answers to the most frequently asked questions.
        </p>
      </div>
      {/* Accordion */}
      <div className="w-full mx-auto space-y-4">
        {faqs.map(({ id, question, answer }) => (
          <div
            key={id}
            className={`rounded-xl p-6 transition bg-gray-50 ${
              openId === id ? "bg-gray-100" : ""
            }`}
          >
            <button
              onClick={() => toggle(id)}
              className="w-full text-start pb-3 flex justify-between items-center gap-x-3 md:text-lg font-semibold text-gray-800 hover:text-gray-500 focus:outline-none"
              aria-expanded={openId === id}
            >
              {question}
              <svg
                className={`w-5 h-5 text-gray-600 transition-transform duration-300 transform ${
                  openId === id ? "rotate-180" : "rotate-0"
                }`}
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </button>
            {openId === id && (
              <div className="mt-2 text-gray-800 transition duration-300">
                <p>{answer}</p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
