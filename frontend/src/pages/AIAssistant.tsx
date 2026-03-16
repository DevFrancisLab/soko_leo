import { useState, useRef, useEffect } from "react";
import AppLayout from "@/components/AppLayout";
import { Send, Mic, Bot, User } from "lucide-react";
import { useAuth } from "@/context/useAuth";

interface Message {
  id: number;
  role: "user" | "ai";
  text: string;
  time: string;
}

const suggestions = [
  "Where can I sell tomatoes today?",
  "Best price for maize near Nakuru?",
  "Should I harvest beans now?",
  "Weather forecast this week?",
];

const initialMessages: Message[] = [
  {
    id: 1,
    role: "ai",
    text: "Habari! 👋 I'm SokoLeo AI, your smart farming assistant.\n\nI can help you with:\n• 📊 Live commodity prices\n• 🏪 Best markets to sell\n• 🌤 Weather forecasts\n• 💰 Selling advice\n\nWhat would you like to know today?",
    time: "Now",
  },
];

const AIAssistant = () => {
  const { api } = useAuth();
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  const sendMessage = async (text: string) => {
    if (!text.trim()) return;
    const userMsg: Message = { id: Date.now(), role: "user", text, time: "Now" };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsTyping(true);

    try {
      const response = await api.post('/ai/chat/', { message: text });
      const aiText = response.data.response;
      const aiMsg: Message = { id: Date.now() + 1, role: "ai", text: aiText, time: "Now" };
      setMessages((prev) => [...prev, aiMsg]);
    } catch (error) {
      const errorMsg: Message = { id: Date.now() + 1, role: "ai", text: "Sorry, I'm having trouble connecting. Please try again.", time: "Now" };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsTyping(false);
    }
  };

  const renderText = (text: string) => {
    return text.split("\n").map((line, i) => {
      const boldLine = line.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
      return <p key={i} className="leading-relaxed" dangerouslySetInnerHTML={{ __html: boldLine || "&nbsp;" }} />;
    });
  };

  return (
    <AppLayout title="SokoLeo AI">
      <div className="flex flex-col h-[calc(100vh-130px)] lg:h-[calc(100vh-80px)]">
        {/* Chat messages */}
        <div className="flex-1 overflow-y-auto px-4 py-4 space-y-4">
          {messages.map((msg) => (
            <div key={msg.id} className={`flex gap-3 animate-fade-up ${msg.role === "user" ? "flex-row-reverse" : ""}`}>
              <div className={`w-9 h-9 rounded-2xl flex items-center justify-center flex-shrink-0 ${msg.role === "ai" ? "bg-primary" : "bg-earth"}`}>
                {msg.role === "ai" ? <Bot size={18} className="text-white" /> : <User size={18} className="text-white" />}
              </div>
              <div className={msg.role === "user" ? "chat-bubble-user" : "chat-bubble-ai"}>
                <div className="text-sm space-y-0.5">{renderText(msg.text)}</div>
              </div>
            </div>
          ))}
          {isTyping && (
            <div className="flex gap-3 animate-fade-up">
              <div className="w-9 h-9 rounded-2xl bg-primary flex items-center justify-center">
                <Bot size={18} className="text-white" />
              </div>
              <div className="chat-bubble-ai flex items-center gap-1.5 py-4">
                <span className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{animationDelay:"0ms"}} />
                <span className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{animationDelay:"150ms"}} />
                <span className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{animationDelay:"300ms"}} />
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {/* Suggestions */}
        {messages.length <= 2 && (
          <div className="px-4 pb-3">
            <p className="text-xs text-muted-foreground mb-2 font-medium">Try asking:</p>
            <div className="flex gap-2 overflow-x-auto pb-1 no-scrollbar">
              {suggestions.map((s) => (
                <button
                  key={s}
                  onClick={() => sendMessage(s)}
                  className="flex-shrink-0 text-xs font-medium px-3 py-2 rounded-xl bg-secondary text-secondary-foreground hover:bg-primary hover:text-primary-foreground transition-colors"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Input */}
        <div className="px-4 pb-4 pt-2 bg-background border-t border-border">
          <div className="flex items-center gap-2 bg-card rounded-2xl border border-border p-2 shadow-card">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage(input)}
              placeholder="Ask about prices, markets..."
              className="flex-1 bg-transparent text-sm px-3 py-2 outline-none text-foreground placeholder:text-muted-foreground"
            />
            <button className="p-2.5 rounded-xl text-muted-foreground hover:text-primary transition-colors hover:bg-muted">
              <Mic size={20} />
            </button>
            <button
              onClick={() => sendMessage(input)}
              disabled={!input.trim()}
              className="p-2.5 rounded-xl bg-primary text-primary-foreground disabled:opacity-40 transition-all active:scale-95"
            >
              <Send size={18} />
            </button>
          </div>
        </div>
      </div>
    </AppLayout>
  );
};

export default AIAssistant;
