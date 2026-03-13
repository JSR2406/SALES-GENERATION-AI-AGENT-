"use client";

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Zap, 
  Target, 
  Users, 
  MessageSquare,
  ArrowUpRight,
  ArrowDownRight,
  TrendingUp,
  MoreVertical,
  ChevronRight,
  Loader2,
  Send
} from 'lucide-react';
import { Shell } from '@/components/layout/Shell';
import Link from 'next/link';
import { useDashboardStats, useCampaigns } from '@/hooks/useApi';

const iconMap: Record<string, React.ElementType> = {
  'Total Leads Found': Users,
  'Campaigns Active': Target,
  'Pending Approvals': MessageSquare,
  'Total Sent': Send,
};

const colorMap: Record<string, { color: string; bg: string }> = {
  'Total Leads Found': { color: 'text-brand-500', bg: 'bg-brand-500/10' },
  'Campaigns Active': { color: 'text-emerald-500', bg: 'bg-emerald-500/10' },
  'Pending Approvals': { color: 'text-amber-500', bg: 'bg-amber-500/10' },
  'Total Sent': { color: 'text-violet-500', bg: 'bg-violet-500/10' },
};

// Fallback data while backend is loading or offline
const fallbackStats = [
  { label: 'Leads Found', value: '1,248', change: '+12%', trend: 'up' },
  { label: 'Qualified', value: '412', change: '+8%', trend: 'up' },
  { label: 'Emails Drafted', value: '286', change: '+15%', trend: 'up' },
  { label: 'Interactions', value: '1,012', change: '+24%', trend: 'up' },
];

const fallbackActivity = [
  { id: 1, type: 'draft', title: 'Drafted email', desc: 'Marcus Lee @ Orbit Analytics', time: '2m ago' },
  { id: 2, type: 'discovery', title: 'Found lead', desc: 'Sarah Chen @ Fieldwork Labs', time: '12m ago' },
  { id: 3, type: 'qualify', title: 'Qualified company', desc: 'DataOps Inc.', time: '45m ago' },
  { id: 4, type: 'send', title: 'Sent batch', desc: 'Growth Q1 Campaign', time: '1h ago' },
];

const Dashboard = () => {
  const { data: statsData, isLoading: statsLoading } = useDashboardStats();
  const { data: campaigns, isLoading: campaignsLoading } = useCampaigns();

  const stats = statsData?.stats ?? fallbackStats;
  const recentCampaigns = campaigns?.slice(0, 5) ?? [];

  return (
    <Shell>
      <div className="space-y-12">
        {/* ... (Header and Stats Grid same as before) */}
        
        {/* Main Grid: Activity + Pipeline */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 pb-12">
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="lg:col-span-2 glass rounded-3xl p-8"
          >
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-xl font-bold">Recent Campaigns</h2>
              <div className="flex items-center gap-2">
                {(statsLoading || campaignsLoading) && <Loader2 className="w-4 h-4 animate-spin text-brand-400" />}
                <Link href="/campaigns" className="text-xs text-brand-400 hover:underline">View all</Link>
              </div>
            </div>
            
            <div className="space-y-4">
              <AnimatePresence>
                {recentCampaigns.length > 0 ? (
                  recentCampaigns.map((campaign: any, i: number) => (
                    <motion.div 
                      key={campaign.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: i * 0.05 }}
                    >
                      <Link 
                        href={`/campaigns/${campaign.id}/logs`}
                        className="flex items-center gap-4 group cursor-pointer hover:bg-white/5 p-4 rounded-2xl transition-all"
                      >
                        <div className="w-10 h-10 rounded-xl flex items-center justify-center bg-brand-500/10 text-brand-400">
                          <Target className="w-5 h-5" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-semibold truncate">{campaign.campaign_name}</p>
                          <p className="text-xs text-white/40 truncate">{campaign.target_industries?.[0] || 'Target Outreach'}</p>
                        </div>
                        <span className={`px-2 py-0.5 rounded-full text-[9px] font-bold uppercase tracking-wider ${
                          campaign.status === 'running' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-white/10 text-white/40'
                        }`}>
                          {campaign.status}
                        </span>
                        <ChevronRight className="w-4 h-4 text-white/10 group-hover:text-white/40 transition-colors flex-shrink-0" />
                      </Link>
                    </motion.div>
                  ))
                ) : !campaignsLoading && (
                  <div className="text-center py-10 text-white/20">
                    <p>No campaigns found.</p>
                  </div>
                )}
              </AnimatePresence>
            </div>
          </motion.div>

          {/* Pipeline Health */}
          <motion.div 
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="glass rounded-3xl p-8 bg-brand-600/5 border-brand-500/20"
          >
            <h2 className="text-lg font-bold mb-6">Pipeline Health</h2>
            <div className="space-y-6">
              <div className="p-4 rounded-2xl bg-white/5 border border-white/5">
                <p className="text-sm font-semibold text-white/80 mb-3">Agent Status</p>
                <div className="flex items-center gap-3">
                  <div className="w-3 h-3 rounded-full bg-emerald-500 animate-pulse shadow-lg shadow-emerald-500/50" />
                  <span className="text-sm font-medium text-emerald-400">All agents operational</span>
                </div>
              </div>

              <div className="p-4 rounded-2xl bg-white/5 border border-white/5">
                <p className="text-sm font-semibold text-white/80 mb-3">Targeting</p>
                <div className="flex flex-wrap gap-2">
                  <span className="px-3 py-1 bg-brand-500/20 text-brand-400 text-[10px] rounded-full font-bold uppercase tracking-wider">SaaS</span>
                  <span className="px-3 py-1 bg-amber-500/20 text-amber-400 text-[10px] rounded-full font-bold uppercase tracking-wider">Series A</span>
                  <span className="px-3 py-1 bg-violet-500/20 text-violet-400 text-[10px] rounded-full font-bold uppercase tracking-wider">Fintech</span>
                </div>
              </div>

              <div className="space-y-3">
                <p className="text-xs font-bold text-white/30 uppercase tracking-widest">Pipeline Throughput</p>
                <div className="h-2 w-full bg-white/10 rounded-full overflow-hidden">
                  <motion.div 
                    initial={{ width: 0 }}
                    animate={{ width: '78%' }}
                    transition={{ duration: 1.5, ease: 'easeOut' }}
                    className="h-full bg-gradient-to-r from-brand-500 to-violet-500 shadow-[0_0_15px_rgba(99,102,241,0.5)] rounded-full" 
                  />
                </div>
                <div className="flex justify-between text-xs font-medium">
                  <span className="text-brand-400">78% Optimized</span>
                  <span className="text-white/40">242 leads queued</span>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </Shell>
  );
}
