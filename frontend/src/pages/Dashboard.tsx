import AppLayout from "@/components/AppLayout";
import { TrendingUp, TrendingDown, Cloud, Sun, CloudRain, MessageCircle, Bell, ArrowRight } from "lucide-react";
import { useNavigate } from "react-router-dom";

const commodities = [
  { name: "Maize", unit: "per 90kg bag", price: "KSh 3,800", change: "+5%", trend: "up", icon: "🌽" },
  { name: "Beans", unit: "per 90kg bag", price: "KSh 8,200", change: "+2%", trend: "up", icon: "🫘" },
  { name: "Tomatoes", unit: "per crate", price: "KSh 1,450", change: "-8%", trend: "down", icon: "🍅" },
  { name: "Potatoes", unit: "per 50kg", price: "KSh 2,100", change: "+1%", trend: "up", icon: "🥔" },
];

const alerts = [
  { text: "Tomato prices dropping in Nairobi. Sell now!", type: "warn" },
  { text: "Maize demand high in Kisumu market", type: "info" },
];

const Dashboard = () => {
  const navigate = useNavigate();
  const hour = new Date().getHours();
  const greeting = hour < 12 ? "Good Morning" : hour < 17 ? "Good Afternoon" : "Good Evening";

  return (
    <AppLayout>
      <div className="px-4 pt-6 pb-4 space-y-5">
        {/* Header */}
        <div className="flex items-start justify-between">
          <div>
            <p className="text-muted-foreground text-sm font-medium">{greeting} 👋</p>
            <h1 className="text-2xl font-extrabold text-foreground mt-0.5">Hello, Farmer</h1>
            <p className="text-sm text-muted-foreground mt-1">Thursday, 26 Feb 2026 · Nairobi</p>
          </div>
          <button className="relative p-2.5 bg-card rounded-2xl shadow-card">
            <Bell size={22} className="text-foreground" />
            <span className="absolute top-1.5 right-1.5 w-2.5 h-2.5 bg-accent rounded-full border-2 border-card" />
          </button>
        </div>

        {/* Alert Banner */}
        {alerts.map((a, i) => (
          <div key={i} className={`flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-medium ${a.type === "warn" ? "bg-amber-50 text-amber-800 border border-amber-200" : "bg-secondary text-secondary-foreground"}`}>
            <span className="text-base">{a.type === "warn" ? "⚠️" : "💡"}</span>
            {a.text}
          </div>
        ))}

        {/* Weather Card */}
        <div className="card-soko p-5" style={{background: "var(--gradient-hero)"}}>
          <div className="flex items-center justify-between text-white">
            <div>
              <p className="text-white/70 text-sm font-medium">Today's Weather</p>
              <p className="text-3xl font-extrabold mt-1">24°C</p>
              <p className="text-white/80 text-sm mt-1">Partly cloudy · 40% rain</p>
            </div>
            <div className="text-right">
              <Cloud size={48} className="text-white/40 ml-auto mb-2" />
              <div className="flex gap-3 text-xs text-white/70">
                <div className="text-center"><p className="text-base">☀️</p><p>Mon</p><p className="font-semibold text-white">27°</p></div>
                <div className="text-center"><p className="text-base">🌧️</p><p>Tue</p><p className="font-semibold text-white">21°</p></div>
                <div className="text-center"><p className="text-base">⛅</p><p>Wed</p><p className="font-semibold text-white">25°</p></div>
              </div>
            </div>
          </div>
        </div>

        {/* AI Quick Access */}
        <button
          onClick={() => navigate("/assistant")}
          className="w-full card-soko p-4 flex items-center gap-4 text-left hover:shadow-hero transition-shadow active:scale-[0.98]"
        >
          <div className="w-12 h-12 rounded-2xl flex items-center justify-center flex-shrink-0 animate-pulse-green" style={{background: "var(--gradient-card)"}}>
            <MessageCircle size={24} className="text-white" />
          </div>
          <div className="flex-1">
            <p className="font-bold text-foreground">Ask SokoLeo AI</p>
            <p className="text-sm text-muted-foreground">"Where can I sell tomatoes today?"</p>
          </div>
          <ArrowRight size={20} className="text-muted-foreground flex-shrink-0" />
        </button>

        {/* Commodity Prices */}
        <div>
          <div className="flex items-center justify-between mb-3">
            <h2 className="font-bold text-foreground text-lg">Commodity Prices</h2>
            <span className="text-xs text-primary font-semibold bg-secondary px-2 py-1 rounded-full">Live</span>
          </div>
          <div className="grid grid-cols-2 gap-3">
            {commodities.map((c) => (
              <div key={c.name} className="card-soko p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-2xl">{c.icon}</span>
                  <span className={`text-xs font-bold px-2 py-0.5 rounded-full flex items-center gap-1 ${c.trend === "up" ? "bg-emerald-100 text-emerald-700" : "bg-red-100 text-red-600"}`}>
                    {c.trend === "up" ? <TrendingUp size={10} /> : <TrendingDown size={10} />}
                    {c.change}
                  </span>
                </div>
                <p className="font-bold text-foreground text-base">{c.name}</p>
                <p className="text-primary font-extrabold text-lg">{c.price}</p>
                <p className="text-xs text-muted-foreground mt-0.5">{c.unit}</p>
              </div>
            ))}
          </div>
        </div>

        {/* View Markets CTA */}
        <button
          onClick={() => navigate("/markets")}
          className="w-full btn-primary flex items-center justify-center gap-2"
        >
          <span>View Nearby Markets</span>
          <ArrowRight size={18} />
        </button>
      </div>
    </AppLayout>
  );
};

export default Dashboard;
