"use client";

import React, { useEffect } from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { 
  LayoutDashboard, 
  PlusCircle, 
  CheckCircle2, 
  Settings, 
  Zap,
  Users,
  LogOut,
  Target
} from 'lucide-react';
import { cn } from '@/lib/utils';

const navItems = [
  { name: 'Mission Control', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Campaigns', href: '/campaigns', icon: Target },
  { name: 'New Campaign', href: '/campaigns/new', icon: PlusCircle },
  { name: 'Approvals', href: '/approvals', icon: CheckCircle2 },
  { name: 'Leads', href: '/leads', icon: Users },
  { name: 'Settings', href: '/settings', icon: Settings },
];

export function Shell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();

  // Redirect to login if not authenticated
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('auth_token');
      if (!token) {
        router.push('/login');
      }
    }
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem('auth_token');
    router.push('/login');
  };

  return (
    <div className="flex h-screen bg-surface-950 text-white overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 border-r border-white/10 bg-black/20 backdrop-blur-xl flex flex-col">
        <div className="p-6 flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-brand-600 flex items-center justify-center shadow-lg shadow-brand-500/20">
            <Zap className="w-5 h-5 text-white" />
          </div>
          <span className="font-bold text-xl tracking-tight">Sales.AI</span>
        </div>

        <nav className="flex-1 px-4 py-6 space-y-1">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link key={item.name} href={item.href}>
                <motion.div
                  whileHover={{ x: 4 }}
                  whileTap={{ scale: 0.98 }}
                  className={cn(
                    "flex items-center gap-3 px-4 py-3 rounded-xl transition-colors relative group",
                    isActive ? "text-white" : "text-white/40 hover:text-white/70"
                  )}
                >
                  {isActive && (
                    <motion.div 
                      layoutId="sidebar-active"
                      className="absolute inset-0 bg-brand-600/10 border border-brand-500/20 rounded-xl"
                    />
                  )}
                  <item.icon className={cn("w-5 h-5", isActive ? "text-brand-500" : "group-hover:text-white/60")} />
                  <span className="font-medium relative z-10">{item.name}</span>
                </motion.div>
              </Link>
            );
          })}
        </nav>

        <div className="p-4 border-t border-white/10">
          <div className="glass p-4 rounded-xl flex items-center gap-3 relative group">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-brand-500 to-violet-600 flex-shrink-0" />
            <div className="flex-1 min-w-0">
              <p className="text-sm font-semibold truncate">Janmejay Singh</p>
              <p className="text-xs text-white/40 truncate">Pro Account</p>
            </div>
            
            <button 
              onClick={handleLogout}
              className="absolute right-4 p-2 rounded-lg hover:bg-white/10 text-white/40 hover:text-red-400 transition-colors opacity-0 group-hover:opacity-100 focus:opacity-100"
              title="Logout"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto relative">
        {/* Top bar */}
        <header className="sticky top-0 z-30 h-16 border-b border-white/5 bg-black/20 backdrop-blur-sm px-8 flex items-center justify-between">
          <div className="flex items-center gap-2 text-sm text-white/40">
            <span>Workspace</span>
            <span>/</span>
            <span className="text-white">Main Organization</span>
          </div>
          <div className="flex items-center gap-4">
             <div className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
             <span className="text-xs font-medium text-green-500/80">Agents Active</span>
          </div>
        </header>

        <div className="p-8 max-w-7xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
}
