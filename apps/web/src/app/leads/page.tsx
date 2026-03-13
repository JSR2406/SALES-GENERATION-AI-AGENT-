"use client";

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Users, 
  Search, 
  Filter,
  ChevronDown,
  Star,
  Building2,
  Briefcase,
  ArrowUpRight,
  Loader2,
  UserPlus
} from 'lucide-react';
import { Shell } from '@/components/layout/Shell';
import { useLeads } from '@/hooks/useApi';

interface Lead {
  id: string;
  full_name: string;
  company_name: string;
  title: string;
  qualification_score: number;
  qualification_reason: string;
  status: string;
  created_at: string;
}

const fallbackLeads: Lead[] = [
  { id: '1', full_name: 'Sarah Chen', company_name: 'Fieldwork Labs', title: 'CTO', qualification_score: 9.2, qualification_reason: 'Strong ICP match — Series A SaaS company with 50+ engineers', status: 'qualified', created_at: '2m ago' },
  { id: '2', full_name: 'Marcus Lee', company_name: 'Orbit Analytics', title: 'VP Sales', qualification_score: 8.7, qualification_reason: 'High-growth analytics platform, actively hiring DevOps', status: 'qualified', created_at: '15m ago' },
  { id: '3', full_name: 'Jordan Walsh', company_name: 'DataOps Inc.', title: 'Head of Growth', qualification_score: 7.5, qualification_reason: 'Mid-stage company, expanding into enterprise', status: 'draft_ready', created_at: '1h ago' },
  { id: '4', full_name: 'Priya Sharma', company_name: 'CloudKraft', title: 'Engineering Lead', qualification_score: 6.2, qualification_reason: 'Small team, may not have budget yet', status: 'prospected', created_at: '2h ago' },
  { id: '5', full_name: 'Alex Rivera', company_name: 'Synapse AI', title: 'CEO', qualification_score: 9.0, qualification_reason: 'AI-first company, perfect use case alignment', status: 'qualified', created_at: '3h ago' },
  { id: '6', full_name: 'Emma Thompson', company_name: 'Nexus Cloud', title: 'VP Engineering', qualification_score: 8.1, qualification_reason: 'Enterprise cloud company scaling infrastructure team', status: 'draft_ready', created_at: '4h ago' },
];

const statusConfig: Record<string, { label: string; color: string; bg: string }> = {
  prospected: { label: 'Prospected', color: 'text-blue-400', bg: 'bg-blue-500/10' },
  qualified: { label: 'Qualified', color: 'text-emerald-400', bg: 'bg-emerald-500/10' },
  draft_ready: { label: 'Draft Ready', color: 'text-amber-400', bg: 'bg-amber-500/10' },
  contacted: { label: 'Contacted', color: 'text-violet-400', bg: 'bg-violet-500/10' },
  replied: { label: 'Replied', color: 'text-brand-400', bg: 'bg-brand-500/10' },
  replied_interested: { label: 'Interested', color: 'text-green-400', bg: 'bg-green-500/20' },
  replied_rejected: { label: 'Not Interested', color: 'text-pink-400', bg: 'bg-pink-500/10' },
};

export default function LeadsPage() {
  const { data: apiLeads, isLoading } = useLeads();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedLead, setSelectedLead] = useState<Lead | null>(null);

  const leads: Lead[] = apiLeads?.length ? apiLeads : fallbackLeads;

  const filtered = leads.filter((l: Lead) =>
    l.full_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    l.company_name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <Shell>
      <div className="space-y-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-end justify-between"
        >
          <div>
            <p className="text-white/40 mb-1 text-sm font-medium">Pipeline</p>
            <h1 className="text-3xl font-bold">Lead Explorer</h1>
          </div>
          <div className="flex gap-3">
            <button className="px-4 py-2.5 rounded-xl border border-white/10 glass hover:bg-white/10 transition-all text-sm font-medium flex items-center gap-2">
              <Filter className="w-4 h-4" />
              Filters
            </button>
            <button 
              onClick={() => window.location.href = '/campaigns/new'}
              className="px-4 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-700 transition-all shadow-lg shadow-brand-500/30 text-sm font-medium flex items-center gap-2"
            >
              <UserPlus className="w-4 h-4" />
              New Campaign
            </button>
          </div>
        </motion.div>

        {/* Search */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="relative"
        >
          <Search className="w-5 h-5 text-white/30 absolute left-5 top-1/2 -translate-y-1/2" />
          <input
            className="w-full h-14 pl-14 pr-6 bg-white/5 border border-white/10 rounded-2xl focus:border-brand-500/50 outline-none focus:ring-4 focus:ring-brand-500/10 transition-all text-base"
            placeholder="Search leads by name or company..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          {isLoading && (
            <Loader2 className="w-5 h-5 text-brand-400 animate-spin absolute right-5 top-1/2 -translate-y-1/2" />
          )}
        </motion.div>

        {/* Stats Bar */}
        <div className="grid grid-cols-4 gap-4">
          {[
            { label: 'Total', value: leads.length, color: 'text-white' },
            { label: 'Qualified', value: leads.filter(l => l.qualification_score >= 7).length, color: 'text-emerald-400' },
            { label: 'Draft Ready', value: leads.filter(l => l.status === 'draft_ready').length, color: 'text-amber-400' },
            { label: 'Avg Score', value: (leads.reduce((a, l) => a + l.qualification_score, 0) / leads.length).toFixed(1), color: 'text-brand-400' },
          ].map((s, i) => (
            <motion.div
              key={s.label}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.15 + i * 0.05 }}
              className="glass rounded-xl p-4 text-center"
            >
              <p className="text-[10px] font-bold text-white/30 uppercase tracking-widest">{s.label}</p>
              <p className={`text-2xl font-bold mt-1 ${s.color}`}>{s.value}</p>
            </motion.div>
          ))}
        </div>

        {/* Leads Table */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="glass rounded-3xl overflow-hidden"
        >
          {/* Table Header */}
          <div className="grid grid-cols-12 gap-4 px-6 py-4 border-b border-white/5 text-[10px] font-bold text-white/30 uppercase tracking-widest">
            <div className="col-span-3">Lead</div>
            <div className="col-span-2">Company</div>
            <div className="col-span-2">Title</div>
            <div className="col-span-2 text-center">Score</div>
            <div className="col-span-2">Status</div>
            <div className="col-span-1"></div>
          </div>

          {/* Table Rows */}
          <AnimatePresence>
            {filtered.map((lead: Lead, i: number) => {
              const status = statusConfig[lead.status] || statusConfig.prospected;
              return (
                <motion.div
                  key={lead.id}
                  initial={{ opacity: 0, y: 5 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ delay: i * 0.03 }}
                  onClick={() => setSelectedLead(selectedLead?.id === lead.id ? null : lead)}
                  className="grid grid-cols-12 gap-4 px-6 py-5 border-b border-white/5 hover:bg-white/5 cursor-pointer transition-all group items-center"
                >
                  <div className="col-span-3 flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-brand-500/20 to-violet-500/20 flex items-center justify-center flex-shrink-0">
                      <span className="text-sm font-bold text-brand-400">
                        {lead.full_name.split(' ').map(n => n[0]).join('')}
                      </span>
                    </div>
                    <p className="font-semibold text-sm truncate">{lead.full_name}</p>
                  </div>

                  <div className="col-span-2 flex items-center gap-2 text-sm text-white/60">
                    <Building2 className="w-3.5 h-3.5 flex-shrink-0" />
                    <span className="truncate">{lead.company_name}</span>
                  </div>

                  <div className="col-span-2 flex items-center gap-2 text-sm text-white/40">
                    <Briefcase className="w-3.5 h-3.5 flex-shrink-0" />
                    <span className="truncate">{lead.title}</span>
                  </div>

                  <div className="col-span-2 flex justify-center">
                    <div className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-bold ${
                      lead.qualification_score >= 8.5 ? 'bg-emerald-500/10 text-emerald-400' :
                      lead.qualification_score >= 7 ? 'bg-amber-500/10 text-amber-400' :
                      'bg-white/5 text-white/40'
                    }`}>
                      <Star className="w-3.5 h-3.5" />
                      {lead.qualification_score.toFixed(1)}
                    </div>
                  </div>

                  <div className="col-span-2">
                    <span className={`px-3 py-1.5 rounded-lg text-[10px] font-bold uppercase tracking-wider ${status.bg} ${status.color}`}>
                      {status.label}
                    </span>
                  </div>

                  <div className="col-span-1 flex justify-end">
                    <ArrowUpRight className="w-4 h-4 text-white/10 group-hover:text-brand-400 transition-colors" />
                  </div>
                </motion.div>
              );
            })}
          </AnimatePresence>

          {filtered.length === 0 && (
            <div className="p-12 text-center text-white/30">
              <Users className="w-8 h-8 mx-auto mb-3 opacity-50" />
              <p>No leads match your search.</p>
            </div>
          )}
        </motion.div>

        {/* Lead Detail Drawer */}
        <AnimatePresence>
          {selectedLead && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 20 }}
              className="glass rounded-3xl p-8 space-y-6"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-brand-500 to-violet-500 flex items-center justify-center shadow-lg shadow-brand-500/30">
                    <span className="text-lg font-bold text-white">
                      {selectedLead.full_name.split(' ').map(n => n[0]).join('')}
                    </span>
                  </div>
                  <div>
                    <h3 className="font-bold text-xl">{selectedLead.full_name}</h3>
                    <p className="text.sm text-white/40">{selectedLead.title} at {selectedLead.company_name}</p>
                  </div>
                </div>
                <button
                  onClick={() => setSelectedLead(null)}
                  className="px-4 py-2 rounded-xl border border-white/10 text-sm hover:bg-white/10 transition-all"
                >
                  Close
                </button>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 rounded-2xl bg-white/5 border border-white/5">
                  <p className="text-[10px] font-bold text-white/30 uppercase tracking-widest mb-2">AI Assessment</p>
                  <p className="text-sm text-white/70 leading-relaxed">{selectedLead.qualification_reason}</p>
                </div>
                <div className="p-4 rounded-2xl bg-white/5 border border-white/5">
                  <p className="text-[10px] font-bold text-white/30 uppercase tracking-widest mb-2">Qualification Score</p>
                  <div className="flex items-center gap-4">
                    <p className={`text-4xl font-black ${
                      selectedLead.qualification_score >= 8.5 ? 'text-emerald-400' :
                      selectedLead.qualification_score >= 7 ? 'text-amber-400' : 'text-red-400'
                    }`}>{selectedLead.qualification_score.toFixed(1)}</p>
                    <div className="flex-1">
                      <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${selectedLead.qualification_score * 10}%` }}
                          transition={{ duration: 0.8 }}
                          className={`h-full rounded-full ${
                            selectedLead.qualification_score >= 8.5 ? 'bg-emerald-500' :
                            selectedLead.qualification_score >= 7 ? 'bg-amber-500' : 'bg-red-500'
                          }`}
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </Shell>
  );
}
