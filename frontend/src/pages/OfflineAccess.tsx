import AppLayout from "@/components/AppLayout";
import { Phone, MessageSquare, Wifi, WifiOff, Download } from "lucide-react";

const methods = [
  {
    icon: "📱",
    title: "USSD Code",
    subtitle: "No internet needed",
    instruction: "Dial this number on any phone",
    action: "*384#",
    actionLabel: "Dial *384#",
    href: "tel:*384#",
    color: "bg-primary",
    tip: "Works on any phone, even basic feature phones. No airtime needed.",
  },
  {
    icon: "📞",
    title: "Voice Hotline",
    subtitle: "Talk to SokoLeo AI",
    instruction: "Call our free voice AI assistant",
    action: "0700 123 456",
    actionLabel: "Call Now",
    href: "tel:0700123456",
    color: "bg-earth",
    tip: "Available 6am – 9pm daily. Available in Swahili and English.",
  },
  {
    icon: "💬",
    title: "SMS Service",
    subtitle: "Text for prices",
    instruction: "Send a text message",
    action: "Send MAIZE NAIROBI to 22141",
    actionLabel: "Send SMS",
    href: "sms:22141?body=MAIZE NAIROBI",
    color: "bg-accent",
    tip: "Format: [CROP] [LOCATION] — e.g. TOMATOES NAKURU. Get reply in seconds.",
  },
];

const smsExamples = [
  { send: "MAIZE NAIROBI", reply: "Maize in Nairobi: KSh 3,800/bag. Best market: Wakulima. Call: +254700123456" },
  { send: "TOMATOES KISUMU", reply: "Tomatoes in Kisumu: KSh 1,200/crate. Selling fast today! Market: Kibuye." },
  { send: "WEATHER NAKURU", reply: "Nakuru forecast: Thu sunny 26°C, Fri rain 21°C, Sat partly cloudy 24°C." },
];

const OfflineAccess = () => {
  return (
    <AppLayout title="Offline Access">
      <div className="px-4 pt-4 pb-6 space-y-5">
        {/* Banner */}
        <div className="card-soko p-5" style={{background: "var(--gradient-hero)"}}>
          <div className="flex items-center gap-3 mb-3">
            <div className="w-12 h-12 rounded-2xl bg-white/20 flex items-center justify-center">
              <WifiOff size={24} className="text-white" />
            </div>
            <div>
              <h2 className="text-white font-bold text-lg">Works Without Internet</h2>
              <p className="text-white/70 text-sm">SokoLeo works even with no data</p>
            </div>
          </div>
          <div className="flex gap-3">
            <div className="flex-1 bg-white/10 rounded-xl px-3 py-2 text-center">
              <p className="text-white font-bold text-lg">*384#</p>
              <p className="text-white/70 text-xs">USSD</p>
            </div>
            <div className="flex-1 bg-white/10 rounded-xl px-3 py-2 text-center">
              <p className="text-white font-bold text-lg">22141</p>
              <p className="text-white/70 text-xs">SMS</p>
            </div>
            <div className="flex-1 bg-white/10 rounded-xl px-3 py-2 text-center">
              <p className="text-white font-bold text-lg">Free</p>
              <p className="text-white/70 text-xs">No cost</p>
            </div>
          </div>
        </div>

        {/* Methods */}
        <h2 className="font-bold text-foreground text-lg">How to Access Offline</h2>
        <div className="space-y-3">
          {methods.map((method, i) => (
            <div key={i} className="card-soko p-4">
              <div className="flex items-start gap-4">
                <div className={`w-12 h-12 rounded-2xl ${method.color} flex items-center justify-center text-2xl flex-shrink-0`}>
                  {method.icon}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <h3 className="font-bold text-foreground">{method.title}</h3>
                    <span className="text-xs px-2 py-0.5 bg-muted rounded-full text-muted-foreground">{method.subtitle}</span>
                  </div>
                  <p className="text-sm text-muted-foreground mt-1">{method.instruction}</p>
                  <p className="font-bold text-primary mt-1 text-sm">{method.action}</p>
                  <p className="text-xs text-muted-foreground mt-2 bg-muted px-3 py-2 rounded-xl">💡 {method.tip}</p>
                </div>
              </div>
              <a
                href={method.href}
                className="mt-3 w-full flex items-center justify-center gap-2 py-3 btn-primary text-sm"
              >
                {method.actionLabel}
              </a>
            </div>
          ))}
        </div>

        {/* SMS Examples */}
        <div>
          <h2 className="font-bold text-foreground text-lg mb-3">SMS Examples</h2>
          <div className="space-y-3">
            {smsExamples.map((ex, i) => (
              <div key={i} className="card-soko p-4">
                <div className="flex gap-3 mb-2">
                  <span className="text-xs font-semibold text-muted-foreground uppercase">You send:</span>
                  <span className="text-sm font-bold text-primary">{ex.send}</span>
                </div>
                <div className="bg-secondary rounded-xl px-3 py-2">
                  <p className="text-xs font-semibold text-muted-foreground mb-1">SokoLeo replies:</p>
                  <p className="text-sm text-secondary-foreground">{ex.reply}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Install PWA hint */}
        <div className="card-soko p-4 border-dashed border-2 border-primary/30">
          <div className="flex items-center gap-3 mb-2">
            <Download size={20} className="text-primary" />
            <h3 className="font-bold text-foreground">Install SokoLeo App</h3>
          </div>
          <p className="text-sm text-muted-foreground">Tap your browser menu → "Add to Home Screen" to install SokoLeo as an app. Works offline automatically!</p>
        </div>
      </div>
    </AppLayout>
  );
};

export default OfflineAccess;
