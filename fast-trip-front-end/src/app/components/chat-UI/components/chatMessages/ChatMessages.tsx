import Image from "next/image";
import defaultUser from "../../../../../../public/default-user.png";

interface Message {
  id: string | number;
  text: string;
  isUser: boolean; // true if message is from the current user (right side)
  avatarSrc?: string; // optional avatar image URL
}

interface ChatMessagesProps {
  messages: Message[];
}

export default function ChatMessages({ messages }: ChatMessagesProps) {
  return (
    <>
      {messages?.map(({ id, text, isUser, avatarSrc }) => (
        <div key={id} className="chat-message">
          <div className={`flex items-end ${isUser ? "justify-end" : ""}`}>
            <div
              className={`flex flex-col space-y-2 text-xs max-w-xs mx-2 ${
                isUser ? "order-1 items-end" : "order-2 items-start"
              }`}
            >
              <div>
                <span
                  className={`px-4 py-2 rounded-lg inline-block ${
                    isUser
                      ? "rounded-br-none bg-[#0BC187] text-white"
                      : "rounded-bl-none bg-gray-300 text-gray-600"
                  }`}
                >
                  {text}
                </span>
              </div>
            </div>
            <Image
              src={avatarSrc || defaultUser}
              alt="User avatar"
              width={20}
              height={20}
              className={`rounded-full ${isUser ? "order-2" : "order-1"}`}
            />
          </div>
        </div>
      ))}
    </>
  );
}
