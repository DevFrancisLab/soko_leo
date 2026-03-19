import AppLayout from "@/components/AppLayout";
import { MapPin, ChevronRight, Bell, Globe, Shield, HelpCircle, LogOut, Star } from "lucide-react";

const crops = ["Maize", "Tomatoes", "Beans", "Potatoes"];
const regions = ["Nairobi", "Kisumu", "Nakuru", "Mombasa"];

const menuItems = [
  { icon: Bell, label: "Price Alerts", desc: "Get notified when prices change", badge: "3 active" },
  { icon: Globe, label: "Language", desc: "English / Kiswahili", badge: null },
  { icon: Shield, label: "Privacy", desc: "Data & permissions", badge: null },
  { icon: HelpCircle, label: "Help & Support", desc: "Chat, call or FAQ", badge: null },
];

const Profile = () => {
  return (
    <AppLayout title="My Profile">
      <div className="px-4 pt-4 pb-6 space-y-5">
        {/* Farmer Profile Card */}
        <div className="card-soko p-5" style={{background: "var(--gradient-hero)"}}>
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-3xl bg-white/20 border-2 border-white/30 flex items-center justify-center text-3xl">
              👩‍🌾
            </div>
            <div className="flex-1">
              <h2 className="text-white font-bold text-xl">Amina Wanjiku</h2>
              <div className="flex items-center gap-2 text-white/70 text-sm mt-1">
                <MapPin size={13} />
                <span>Kiambu County, Kenya</span>
              </div>
              <div className="flex items-center gap-1.5 mt-2">
                <Star size={13} className="text-amber-300" fill="currentColor" />
                <span className="text-white text-sm font-medium">Verified Farmer</span>
              </div>
            </div>
          </div>
          <div className="mt-4 grid grid-cols-3 gap-2">
            <div className="bg-white/10 rounded-xl px-2 py-2.5 text-center">
              <p className="text-white font-bold text-lg">12</p>
              <p className="text-white/60 text-xs">Queries</p>
            </div>
            <div className="bg-white/10 rounded-xl px-2 py-2.5 text-center">
              <p className="text-white font-bold text-lg">4</p>
              <p className="text-white/60 text-xs">Markets</p>
            </div>
            <div className="bg-white/10 rounded-xl px-2 py-2.5 text-center">
              <p className="text-white font-bold text-lg">3</p>
              <p className="text-white/60 text-xs">Alerts</p>
            </div>
          </div>
        </div>

        {/* My Crops */}
        <div className="card-soko p-4">
          <h3 className="font-bold text-foreground mb-3">My Crops</h3>
          <div className="flex flex-wrap gap-2">
            {crops.map((c) => (
              <span key={c} className="px-3 py-1.5 bg-secondary text-secondary-foreground rounded-xl text-sm font-medium">{c}</span>
            ))}
            <button className="px-3 py-1.5 border border-dashed border-border rounded-xl text-sm text-muted-foreground hover:text-primary hover:border-primary transition-colors">
              + Add crop
            </button>
          </div>
        </div>

        {/* Location */}
        <div className="card-soko p-4">
          <h3 className="font-bold text-foreground mb-3">My Regions</h3>
          <div className="flex flex-wrap gap-2">
            {regions.map((r) => (
              <span key={r} className={`px-3 py-1.5 rounded-xl text-sm font-medium ${r === "Nairobi" ? "bg-primary text-primary-foreground" : "bg-muted text-muted-foreground"}`}>{r}</span>
            ))}
          </div>
        </div>

        {/* Menu Items */}
        <div className="card-soko overflow-hidden divide-y divide-border">
          {menuItems.map(({ icon: Icon, label, desc, badge }) => (
            <button key={label} className="w-full flex items-center gap-4 px-4 py-4 hover:bg-muted transition-colors text-left">
              <div className="w-10 h-10 rounded-xl bg-muted flex items-center justify-center flex-shrink-0">
                <Icon size={19} className="text-foreground" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-semibold text-foreground text-sm">{label}</p>
                <p className="text-xs text-muted-foreground">{desc}</p>
              </div>
              {badge && <span className="text-xs font-semibold px-2 py-0.5 bg-secondary text-secondary-foreground rounded-full">{badge}</span>}
              <ChevronRight size={16} className="text-muted-foreground flex-shrink-0" />
            </button>
          ))}
        </div>

        {/* Version */}
        <div className="text-center">
          <p className="text-xs text-muted-foreground">SokoLeo v1.0 · Made for African Farmers 🌱</p>
          <p className="text-xs text-muted-foreground mt-1">Works offline · PWA Ready</p>
        </div>
      </div>
    </AppLayout>
  );
};

export default Profile;
