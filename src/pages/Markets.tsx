import AppLayout from "@/components/AppLayout";
import { MapPin, Phone, Navigation, Search, Star } from "lucide-react";

const markets = [
  {
    name: "Wakulima Market",
    distance: "12 km",
    rating: 4.8,
    crops: [
      { name: "Tomatoes", price: "KSh 1,600/crate" },
      { name: "Maize", price: "KSh 3,850/bag" },
    ],
    phone: "+254 700 123 456",
    status: "Open",
    badge: "Best Prices",
  },
  {
    name: "City Market",
    distance: "8 km",
    rating: 4.5,
    crops: [
      { name: "Tomatoes", price: "KSh 1,480/crate" },
      { name: "Beans", price: "KSh 8,100/bag" },
    ],
    phone: "+254 700 234 567",
    status: "Open",
    badge: null,
  },
  {
    name: "Gikomba Market",
    distance: "15 km",
    rating: 4.2,
    crops: [
      { name: "Potatoes", price: "KSh 2,200/50kg" },
      { name: "Tomatoes", price: "KSh 1,380/crate" },
    ],
    phone: "+254 700 345 678",
    status: "Open",
    badge: null,
  },
  {
    name: "Ngong Road Market",
    distance: "6 km",
    rating: 4.0,
    crops: [
      { name: "Beans", price: "KSh 7,900/bag" },
      { name: "Maize", price: "KSh 3,700/bag" },
    ],
    phone: "+254 700 456 789",
    status: "Closes 6pm",
    badge: "Nearest",
  },
];

const Markets = () => {
  return (
    <AppLayout title="Nearby Markets">
      <div className="px-4 pt-4 pb-4 space-y-4">
        {/* Search */}
        <div className="flex items-center gap-2 bg-card rounded-2xl border border-border px-4 py-3 shadow-card">
          <Search size={18} className="text-muted-foreground flex-shrink-0" />
          <input
            placeholder="Search markets or crops..."
            className="flex-1 bg-transparent text-sm outline-none text-foreground placeholder:text-muted-foreground"
          />
          <button className="text-xs font-semibold text-primary px-2 py-1 bg-secondary rounded-xl">Near me</button>
        </div>

        {/* Map Placeholder */}
        <div className="card-soko overflow-hidden h-44 relative" style={{background: "var(--gradient-hero)"}}>
          <div className="absolute inset-0 opacity-10">
            {/* Grid lines */}
            {[...Array(6)].map((_, i) => (
              <div key={i} className="absolute w-full border-t border-white" style={{top: `${i * 20}%`}} />
            ))}
            {[...Array(6)].map((_, i) => (
              <div key={i} className="absolute h-full border-l border-white" style={{left: `${i * 20}%`}} />
            ))}
          </div>
          <div className="absolute inset-0 flex flex-col items-center justify-center text-center text-white px-4">
            <MapPin size={36} className="text-white/80 mb-2" />
            <p className="font-bold text-lg">Markets Near You</p>
            <p className="text-white/70 text-sm">4 markets found within 20km</p>
            <button className="mt-3 px-5 py-2 bg-white/20 backdrop-blur-sm border border-white/30 rounded-2xl text-sm font-semibold hover:bg-white/30 transition-colors">
              Open Full Map
            </button>
          </div>
          {/* Map pins */}
          <div className="absolute top-6 left-1/4 w-4 h-4 bg-accent rounded-full border-2 border-white shadow-lg animate-pulse-green" />
          <div className="absolute top-1/3 right-1/3 w-4 h-4 bg-accent rounded-full border-2 border-white shadow-lg" />
          <div className="absolute bottom-8 left-1/2 w-4 h-4 bg-earth rounded-full border-2 border-white shadow-lg" />
          <div className="absolute top-1/2 right-1/4 w-4 h-4 bg-accent rounded-full border-2 border-white shadow-lg" />
        </div>

        {/* Market Cards */}
        <div className="space-y-3">
          {markets.map((market, i) => (
            <div key={i} className="card-soko p-4 animate-fade-up" style={{animationDelay: `${i * 80}ms`}}>
              <div className="flex items-start justify-between mb-3">
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="font-bold text-foreground text-base">{market.name}</h3>
                    {market.badge && (
                      <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-secondary text-secondary-foreground">{market.badge}</span>
                    )}
                  </div>
                  <div className="flex items-center gap-3 mt-1">
                    <span className="flex items-center gap-1 text-xs text-muted-foreground">
                      <MapPin size={11} /> {market.distance}
                    </span>
                    <span className="flex items-center gap-1 text-xs text-amber-600">
                      <Star size={11} fill="currentColor" /> {market.rating}
                    </span>
                    <span className={`text-xs font-medium ${market.status === "Open" ? "text-emerald-600" : "text-amber-600"}`}>
                      ● {market.status}
                    </span>
                  </div>
                </div>
              </div>

              {/* Prices */}
              <div className="grid grid-cols-2 gap-2 mb-3">
                {market.crops.map((crop) => (
                  <div key={crop.name} className="bg-muted rounded-xl px-3 py-2">
                    <p className="text-xs text-muted-foreground">{crop.name}</p>
                    <p className="text-sm font-bold text-primary">{crop.price}</p>
                  </div>
                ))}
              </div>

              {/* Actions */}
              <div className="flex gap-2">
                <a
                  href={`tel:${market.phone}`}
                  className="flex-1 flex items-center justify-center gap-2 py-2.5 bg-secondary text-secondary-foreground rounded-xl text-sm font-semibold hover:bg-primary hover:text-primary-foreground transition-colors"
                >
                  <Phone size={15} /> Call Buyer
                </a>
                <button className="flex-1 flex items-center justify-center gap-2 py-2.5 btn-primary text-sm">
                  <Navigation size={15} /> Directions
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </AppLayout>
  );
};

export default Markets;
