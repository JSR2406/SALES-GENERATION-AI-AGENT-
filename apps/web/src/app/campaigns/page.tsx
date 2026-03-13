"use client";

import React from 'react';
import { motion } from 'framer-motion';
import { Shell } from '@/components/layout/Shell';
import { useCampaigns } from '@/hooks/useApi';
import { 
  Plus, 
  Target, 
  Activity, 
  Clock, 
  ChevronRight, 
  Loader2,
  AlertCircle
} from 'lucide-react';
import Link from 'next/link';

export default function CampaignsPage() {
  const { data: campaigns, isLoading, error } = useCampaigns();

  return (
    <Shell>
      <div className="space-y-8">
        <div className="flex justify-between items-end">
          <div>
            <h1 className="text-3xl font-bold font-display tracking-tight">Campaigns</h1>
            <p className="text-white/40 mt-1">Manage and monitor your active outreach missions.</p>
          </div>
          <Link 
            href="/campaigns/new"
            className="px-5 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-700 transition-all shadow-lg shadow-brand-500/30 text-white font-medium text-sm flex items-center gap-2"
          >
            <Plus className="w-4 h-4" />
            Create New
          </Link>
        </div>

        {isLoading ? (
          <div className="flex flex-col items-center justify-center py-20 text-white/20">
            <Loader2 className="w-10 h-10 animate-spin mb-4" />
            <p>Loading your campaigns...</p>
          </div>
        ) : error ? (
          <div className="glass rounded-3xl p-12 text-center border-red-500/20 bg-red-500/5">
            <AlertCircle className="w-12 h-12 text-red-400 mx-auto mb-4" />
            <h2 className="text-xl font-bold mb-2">Failed to load campaigns</h2>
            <p className="text-white/40 mb-6">There was an error connecting to the mission control server.</p>
            <button 
              onClick={() => window.location.reload()}
              className="px-6 py-2 bg-white/10 hover:bg-white/20 rounded-xl transition-all"
            >
              Retry
            </button>
          </div>
        ) : campaigns?.length === 0 ? (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass rounded-3xl p-16 text-center"
          >
            <div className="w-20 h-20 bg-brand-500/10 rounded-full flex items-center justify-center mx-auto mb-6">
              <Target className="w-10 h-10 text-brand-400" />
            </div>
            <h2 className="text-2xl font-bold mb-3">No active campaigns</h2>
            <p className="text-white/40 max-w-sm mx-auto mb-8">
              Launch your first campaign to start discovering leads and automating your B2B outreach.
            </p>
            <Link 
              href="/campaigns/new"
              className="px-8 py-3 rounded-2xl bg-brand-600 hover:bg-brand-700 transition-all text-white font-bold"
            >
              Start Mission
            </Link>
          </motion.div>
        ) : (
          <div className="grid grid-cols-1 gap-4">
            {campaigns.map((campaign: any, i: number) => (
              <motion.div
                key={campaign.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.05 }}
              >
                <Link 
                  href={`/campaigns/${campaign.id}/logs`}
                  className="group block glass rounded-[2rem] p-6 hover:bg-white/5 transition-all border border-white/5 hover:border-brand-500/30"
                >
                  <div className="flex items-center gap-6">
                    <div className="w-14 h-14 rounded-2xl bg-brand-500/10 flex items-center justify-center text-brand-400 group-hover:scale-110 transition-transform">
                      <Target className="w-7 h-7" />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-1">
                        <h3 className="text-lg font-bold">{campaign.campaign_name}</h3>
                        <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider ${
                          campaign.status === 'running' ? 'bg-emerald-500/20 text-emerald-400' :
                          campaign.status === 'draft' ? 'bg-amber-500/20 text-amber-400' :
                          'bg-white/10 text-white/40'
                        }`}>
                          {campaign.status}
                        </span>
                      </div>
                      <div className="flex items-center gap-4 text-sm text-white/30 font-medium">
                        <span className="flex items-center gap-1.5">
                          <Activity className="w-4 h-4" />
                          {campaign.target_industries?.[0] || 'Multiple Industries'}
                        </span>
                        <span className="flex items-center gap-1.5">
                          <Clock className="w-4 h-4" />
                          Created {new Date(campaign.created_at).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                    <div className="flex items-center gap-4">
                      <div className="text-right mr-4 hidden md:block">
                        <p className="text-xs font-bold text-white/20 uppercase tracking-widest mb-1">Execution</p>
                        <p className="text-brand-400 font-mono text-sm group-hover:underline">View Logs</p>
                      </div>
                      <ChevronRight className="w-6 h-6 text-white/10 group-hover:text-white group-hover:translate-x-1 transition-all" />
                    </div>
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </Shell>
  );
}
