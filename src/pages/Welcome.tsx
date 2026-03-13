import { useNavigate } from "react-router-dom";
import { WifiOff, Phone } from "lucide-react";
import farmerHero from "@/assets/farmer-hero.jpg";

const Welcome = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background flex flex-col lg:flex-row overflow-hidden">
      {/* Top info bar */}
      <div className="lg:hidden bg-primary px-5 py-3 flex items-center justify-between gap-4">
        <a href="tel:*384#" className="flex items-center gap-2 text-primary-foreground text-xs font-medium">
          <WifiOff size={14} />
          <span>Offline: *384#</span>
        </a>
        <a href="tel:+2541012345" className="flex items-center gap-2 text-primary-foreground text-xs font-medium">
          <Phone size={14} />
          <span>Hotline: +2541012345</span>
        </a>
      </div>

      {/* Hero Image Side */}
      <div className="relative lg:w-1/2 h-72 lg:h-screen overflow-hidden">
        <img
          src={farmerHero}
          alt="Happy farmer holding fresh vegetables in a maize field"
          className="w-full h-full object-cover object-top"
        />
        {/* Organic overlay */}
        <div className="absolute inset-0" style={{background: "linear-gradient(to bottom, transparent 40%, hsl(163 59% 20% / 0.6) 100%)"}} />

        {/* Logo on image */}
        <div className="absolute top-5 left-5 flex items-center gap-2.5">
          <div className="w-10 h-10 rounded-2xl flex items-center justify-center shadow-lg" style={{background: "var(--gradient-card)"}}>
            <span className="text-white font-bold text-xl">S</span>
          </div>
          <span className="text-white font-bold text-xl drop-shadow-md">SokoLeo</span>
        </div>

        {/* Curved bottom on mobile */}
        <div className="absolute bottom-0 left-0 right-0 h-10 bg-background lg:hidden" style={{borderRadius: "60% 60% 0 0 / 100% 100% 0 0"}} />
      </div>

      {/* Content Side */}
      <div className="flex-1 lg:w-1/2 px-6 pt-4 pb-10 lg:flex lg:flex-col lg:justify-center lg:px-16 animate-fade-up">
        {/* Desktop top bar */}
        <div className="hidden lg:flex items-center justify-between mb-12 text-sm text-muted-foreground">
          <a href="tel:*384#" className="flex items-center gap-2 hover:text-primary transition-colors font-medium">
            <WifiOff size={16} />
            <span>Offline Access: Dial *384#</span>
          </a>
          <a href="tel:+2541012345" className="flex items-center gap-2 hover:text-primary transition-colors font-medium">
            <Phone size={16} />
            <span>Voice AI: +254 101 2345</span>
          </a>
        </div>

        <div className="max-w-md">
          <span className="inline-block px-3 py-1 rounded-full text-xs font-semibold mb-4" style={{background: "hsl(var(--secondary))", color: "hsl(var(--secondary-foreground))"}}>
            🌱 AI-Powered Farm Assistant
          </span>
          <h1 className="text-4xl lg:text-5xl font-extrabold text-foreground leading-tight mb-4">
            Smart Farming{" "}
            <span className="text-primary">Assistant</span>
          </h1>
          <p className="text-lg text-muted-foreground leading-relaxed mb-8">
            Know <strong className="text-foreground">when and where</strong> to sell your crops before prices change. Real-time market intelligence for every farmer.
          </p>

          {/* Feature pills */}
          <div className="flex flex-wrap gap-2 mb-8">
            {["📊 Live Prices", "🌤 Weather", "🗺 Nearby Markets", "🤖 AI Advice"].map((f) => (
              <span key={f} className="px-3 py-1.5 bg-muted rounded-full text-sm font-medium text-muted-foreground">{f}</span>
            ))}
          </div>

          <button
            onClick={() => navigate("/dashboard")}
            className="btn-primary w-full text-center text-lg mb-4"
          >
            Get Started — It's Free
          </button>
          <p className="text-center text-sm text-muted-foreground">
            Works offline too. No expensive data needed.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Welcome;
