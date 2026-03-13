import { useNavigate, useLocation } from "react-router-dom";
import { LayoutDashboard, MessageCircle, MapPin, WifiOff, User } from "lucide-react";

const navItems = [
  { path: "/dashboard", icon: LayoutDashboard, label: "Home" },
  { path: "/assistant", icon: MessageCircle, label: "AI Chat" },
  { path: "/markets", icon: MapPin, label: "Markets" },
  { path: "/offline", icon: WifiOff, label: "Offline" },
  { path: "/profile", icon: User, label: "Profile" },
];

interface AppLayoutProps {
  children: React.ReactNode;
  title?: string;
  showBack?: boolean;
}

const AppLayout = ({ children, title, showBack }: AppLayoutProps) => {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <div className="min-h-screen bg-background flex flex-col max-w-lg mx-auto lg:max-w-none lg:flex-row">
      {/* Desktop Sidebar */}
      <aside className="hidden lg:flex lg:w-64 lg:flex-col lg:fixed lg:inset-y-0 lg:bg-card lg:border-r lg:border-border lg:p-6">
        <div className="flex items-center gap-3 mb-10">
          <div className="w-10 h-10 rounded-2xl flex items-center justify-center" style={{background: "var(--gradient-card)"}}>
            <span className="text-white font-bold text-lg">S</span>
          </div>
          <div>
            <p className="font-bold text-foreground text-lg leading-none">SokoLeo</p>
            <p className="text-muted-foreground text-xs">Smart Farming</p>
          </div>
        </div>
        <nav className="flex flex-col gap-2 flex-1">
          {navItems.map(({ path, icon: Icon, label }) => {
            const active = location.pathname === path;
            return (
              <button
                key={path}
                onClick={() => navigate(path)}
                className={`flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all ${
                  active ? "bg-primary text-primary-foreground shadow-btn" : "text-muted-foreground hover:bg-muted hover:text-foreground"
                }`}
              >
                <Icon size={20} />
                {label}
              </button>
            );
          })}
        </nav>
        <div className="mt-auto p-4 rounded-2xl bg-secondary">
          <p className="text-secondary-foreground text-xs font-medium">Offline access</p>
          <p className="text-secondary-foreground text-sm font-bold mt-1">Dial *384#</p>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 lg:ml-64 flex flex-col min-h-screen">
        {title && (
          <header className="sticky top-0 z-10 bg-background/90 backdrop-blur-sm border-b border-border px-4 py-4 flex items-center gap-3">
            {showBack && (
              <button onClick={() => navigate(-1)} className="p-2 rounded-xl hover:bg-muted transition-colors">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                  <path d="m15 18-6-6 6-6"/>
                </svg>
              </button>
            )}
            <h1 className="text-lg font-bold text-foreground">{title}</h1>
          </header>
        )}
        <div className="flex-1 overflow-y-auto pb-24 lg:pb-6">
          {children}
        </div>
      </main>

      {/* Mobile Bottom Nav */}
      <nav className="lg:hidden fixed bottom-0 left-0 right-0 bg-card border-t border-border safe-bottom z-20">
        <div className="max-w-lg mx-auto flex items-center justify-around px-2 py-1">
          {navItems.map(({ path, icon: Icon, label }) => {
            const active = location.pathname === path;
            return (
              <button
                key={path}
                onClick={() => navigate(path)}
                className={`bottom-nav-item ${active ? "active" : ""}`}
              >
                <div className={`p-1.5 rounded-xl transition-all ${active ? "bg-secondary" : ""}`}>
                  <Icon size={22} strokeWidth={active ? 2.5 : 1.8} />
                </div>
                <span className={`text-xs font-medium ${active ? "text-primary" : "text-muted-foreground"}`}>{label}</span>
              </button>
            );
          })}
        </div>
      </nav>
    </div>
  );
};

export default AppLayout;
