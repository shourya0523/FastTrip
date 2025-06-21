import ChatAction from "./components/chatAction/chatAction";
import ChatHeader from "./components/chatHeader/ChatHeader";
import ChatMessages from "./components/chatMessages/ChatMessages";

export default function ChatComponent() {
  return (
    <div className="flex-1 bg-[#f4f4f4] p-2 sm:p-6 justify-between flex flex-col h-screen">
      <ChatHeader />
      <div
        id="messages"
        className="flex flex-col space-y-4 p-3 overflow-y-auto scrollbar-thumb-blue scrollbar-thumb-rounded scrollbar-track-blue-lighter scrollbar-w-2 scrolling-touch"
      >
        <ChatMessages />
        <ChatMessages />
        <ChatMessages />
        <ChatMessages />
        <ChatMessages />
        <ChatMessages />
        <ChatMessages />
        <ChatMessages />
      </div>
      <ChatAction />
    </div>
  );
}
