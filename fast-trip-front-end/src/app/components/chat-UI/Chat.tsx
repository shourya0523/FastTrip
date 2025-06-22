import { useEffect, useRef, useState } from "react";
import ChatAction from "./components/chatAction/chatAction";
import ChatHeader from "./components/chatHeader/ChatHeader";
import ChatMessages from "./components/chatMessages/ChatMessages";
import { postData } from "@/app/lib/api";

enum Message {
  allCollected = "Thank you! All information is collected.",
}

const initialMessages = [
  {
    id: 1,
    text: "Hey! Let's start? What is your Name?",
    isUser: false,
    avatarSrc: undefined,
  },
];

export default function ChatComponent() {
  const [messages, setMessages] = useState(initialMessages);
  const [sessionId, setSessionId] = useState("Random");
  const [allCollected, setAllCollected] = useState(false);

  async function handleSendMessage(userMessage: string) {
    const newUserMessage = {
      id: Date.now(),
      text: userMessage,
      isUser: true,
      avatarSrc: false,
    };
    setMessages((prev) => [...prev, newUserMessage]);

    const data = await postData("chat/chat", {
      message: userMessage,
      session_id: sessionId,
    });

    if (data.session_id && data.session_id !== sessionId) {
      setSessionId(data.session_id);
    }

    if (
      data.follow_up_questions &&
      data.follow_up_questions.length > 0 &&
      data.follow_up_questions?.[0] !== Message.allCollected &&
      data.conversation_complete === false
    ) {
      const newBotMessages = data.follow_up_questions.map(
        (text: string, i: number) => ({
          id: Date.now() + i + 1,
          text,
          isUser: false,
          avatarSrc: undefined,
        })
      );
      setMessages((prev) => [...prev, ...newBotMessages]);
    } else {
      setAllCollected(true);
    }
  }

  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollTop = messagesEndRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="flex-1 bg-[#f4f4f4] rounded p-2 sm:p-6 justify-between flex flex-col h-screen">
      <ChatHeader />
      <div
        id="messages"
        className="flex flex-col space-y-4 p-3 overflow-y-auto scrollbar-thumb-blue scrollbar-thumb-rounded scrollbar-track-blue-lighter scrollbar-w-2 scrolling-touch"
      >
        <div
          id="messages"
          ref={messagesEndRef}
          className="flex flex-col space-y-4 p-3 overflow-y-auto scrollbar-thumb-blue scrollbar-thumb-rounded scrollbar-track-blue-lighter scrollbar-w-2 scrolling-touch"
        >
          <ChatMessages messages={messages} />
        </div>
      </div>
      <ChatAction onSend={handleSendMessage} allCollected={allCollected} />
    </div>
  );
}
