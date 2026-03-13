"use client";

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  CheckCircle2, 
  XCircle, 
  Mail, 
  Clock, 
  User2,
  Building2,
  Sparkles,
  Loader2,
  AlertTriangle
} from 'lucide-react';
import { Shell } from '@/components/layout/Shell';
import { useApprovals, useApproveMessage, useRejectMessage } from '@/hooks/useApi';

interface Draft {
  id: string;
  lead_name: string;
  company: string;
  subject: string;
  body: string;
  score: number;
  status: string;
  created_at: string;
}

// Fallback drafts for when the backend is offline
const fallbackDrafts: Draft[] = [
  {
    id: '1',
    lead_name: 'Sarah Chen',
    company: 'Fieldwork Labs',
    subject: 'Quick question about your CI/CD pipeline',
    body: 'Hi Sarah,\n\nI noticed Fieldwork Labs recently raised Series A — congratulations! As you scale your engineering team, CI/CD bottlenecks often become the #1 velocity killer.\n\nWe help SaaS companies cut build times by 60% with intelligent caching. Would love to show you a 5-min demo.\n\nBest,\nThe Sales.AI Team',
    score: 9.2,
    status: 'pending',
    created_at: '2 min ago'
  },
  {
    id: '2',
    lead_name: 'Marcus Lee',
    company: 'Orbit Analytics',
    subject: 'Reducing your data pipeline costs by 40%',
    body: 'Hi Marcus,\n\nOrbit Analytics is doing incredible work in the analytics space. I imagine at your scale, data pipeline costs are a growing concern.\n\nOur platform has helped similar companies reduce infrastructure costs by 40% while improving query performance.\n\nWould a quick 10-min call make sense this week?\n\nCheers,\nThe Sales.AI Team',
    score: 8.7,
    status: 'pending',
    created_at: '15 min ago'
  },
  {
    id: '3',
    lead_name: 'Jordan Walsh',
    company: 'DataOps Inc.',
    subject: 'Loved your talk at DevCon',
    body: 'Hi Jordan,\n\nYour DevCon talk on observability was spot-on. We are building something that complements that vision — automated anomaly detection that plugs into existing monitoring stacks.\n\nWould love to get your take. Free for a quick chat?\n\nBest,\nThe Sales.AI Team',
    score: 7.5,
    status: 'pending',
    created_at: '1 hour ago'
  }
];

export default function ApprovalsPage() {
  const { data: apiDrafts, isLoading } = useApprovals();
  const approveMutation = useApproveMessage();
  const rejectMutation = useRejectMessage();

  const drafts: Draft[] = apiDrafts?.length ? apiDrafts : fallbackDrafts;
  const [selectedId, setSelectedId] = useState<string>(drafts[0]?.id);
  const [dismissed, setDismissed] = useState<Set<string>>(new Set());

  const activeDrafts = drafts.filter((d: Draft) => !dismissed.has(d.id));
  const selected = activeDrafts.find((d: Draft) => d.id === selectedId) ?? activeDrafts[0];

  const handleApprove = async (id: string) => {
    try {
      await approveMutation.mutateAsync(id);
    } catch {
      // Backend offline — just animate removal
    }
    setDismissed(prev => new Set(prev).add(id));
    const remaining = activeDrafts.filter((d: Draft) => d.id !== id);
    if (remaining.length > 0) setSelectedId(remaining[0].id);
  };

  const handleReject = async (id: string) => {
    try {
      await rejectMutation.mutateAsync(id);
    } catch {
      // Backend offline — just animate removal
    }
    setDismissed(prev => new Set(prev).add(id));
    const remaining = activeDrafts.filter((d: Draft) => d.id !== id);
    if (remaining.length > 0) setSelectedId(remaining[0].id);
  };

  return (
    <Shell>
      <div className="space-y-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="flex items-center gap-3 mb-2">
            <h1 className="text-3xl font-bold">Approval Queue</h1>
            {isLoading && <Loader2 className="w-5 h-5 animate-spin text-brand-400" />}
            <span className="px-3 py-1 bg-amber-500/10 text-amber-400 text-xs font-bold rounded-full">
              {activeDrafts.length} pending
            </span>
          </div>
          <p className="text-white/40 text-sm">Review and approve AI-generated outreach before sending.</p>
        </motion.div>

        {activeDrafts.length === 0 ? (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="glass rounded-3xl p-16 text-center"
          >
            <div className="w-16 h-16 bg-emerald-500/10 rounded-2xl mx-auto flex items-center justify-center mb-6">
              <CheckCircle2 className="w-8 h-8 text-emerald-400" />
            </div>
            <h2 className="text-2xl font-bold mb-2">All caught up!</h2>
            <p className="text-white/40 max-w-md mx-auto">No pending drafts to review. Your agents will generate new ones as campaigns run.</p>
          </motion.div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
            {/* Left: Draft List */}
            <div className="lg:col-span-2 space-y-3">
              <AnimatePresence>
                {activeDrafts.map((draft: Draft, i: number) => (
                  <motion.div
                    key={draft.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -40, height: 0, marginBottom: 0 }}
                    transition={{ delay: i * 0.05 }}
                    onClick={() => setSelectedId(draft.id)}
                    className={`glass rounded-2xl p-5 cursor-pointer transition-all border ${
                      selected?.id === draft.id 
                        ? 'border-brand-500/50 bg-brand-500/5 shadow-lg shadow-brand-500/10' 
                        : 'border-white/5 hover:border-white/10 hover:bg-white/5'
                    }`}
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-brand-500/20 to-violet-500/20 flex items-center justify-center">
                          <User2 className="w-5 h-5 text-brand-400" />
                        </div>
                        <div>
                          <p className="font-semibold text-sm">{draft.lead_name}</p>
                          <p className="text-xs text-white/30 flex items-center gap-1">
                            <Building2 className="w-3 h-3" /> {draft.company}
                          </p>
                        </div>
                      </div>
                      <div className={`px-2 py-0.5 rounded-md text-[10px] font-bold ${
                        draft.score >= 8.5 ? 'bg-emerald-500/20 text-emerald-400' :
                        draft.score >= 7 ? 'bg-amber-500/20 text-amber-400' :
                        'bg-red-500/20 text-red-400'
                      }`}>
                        {draft.score.toFixed(1)}
                      </div>
                    </div>
                    <p className="text-xs text-white/60 font-medium truncate">{draft.subject}</p>
                    <p className="text-[10px] text-white/20 mt-2 flex items-center gap-1">
                      <Clock className="w-3 h-3" /> {draft.created_at}
                    </p>
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>

            {/* Right: Email Preview */}
            {selected && (
              <motion.div
                key={selected.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="lg:col-span-3 glass rounded-3xl p-8 flex flex-col"
              >
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-brand-500 to-violet-500 flex items-center justify-center shadow-lg shadow-brand-500/30">
                      <Mail className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <h3 className="font-bold text-lg">{selected.lead_name}</h3>
                      <p className="text-xs text-white/40">{selected.company}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Sparkles className="w-4 h-4 text-brand-400" />
                    <span className="text-xs text-brand-400 font-medium">AI Generated</span>
                  </div>
                </div>

                {/* Subject */}
                <div className="mb-6 p-4 rounded-2xl bg-white/5 border border-white/5">
                  <p className="text-[10px] font-bold text-white/30 uppercase tracking-widest mb-1">Subject</p>
                  <p className="font-semibold">{selected.subject}</p>
                </div>

                {/* Body */}
                <div className="flex-1 mb-8 p-6 rounded-2xl bg-white/5 border border-white/5">
                  <p className="text-[10px] font-bold text-white/30 uppercase tracking-widest mb-3">Body</p>
                  <p className="text-sm text-white/70 leading-relaxed whitespace-pre-line">{selected.body}</p>
                </div>

                {/* Confidence */}
                <div className="mb-6 p-4 rounded-2xl bg-white/5 border border-white/5">
                  <div className="flex justify-between items-center mb-2">
                    <p className="text-[10px] font-bold text-white/30 uppercase tracking-widest">AI Confidence</p>
                    <span className={`text-sm font-bold ${
                      selected.score >= 8.5 ? 'text-emerald-400' : selected.score >= 7 ? 'text-amber-400' : 'text-red-400'
                    }`}>{selected.score.toFixed(1)}/10</span>
                  </div>
                  <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${selected.score * 10}%` }}
                      transition={{ duration: 0.8, ease: 'easeOut' }}
                      className={`h-full rounded-full ${
                        selected.score >= 8.5 ? 'bg-emerald-500' : selected.score >= 7 ? 'bg-amber-500' : 'bg-red-500'
                      }`}
                    />
                  </div>
                </div>

                {/* Actions */}
                <div className="flex gap-4">
                  <button
                    onClick={() => handleReject(selected.id)}
                    disabled={rejectMutation.isPending}
                    className="flex-1 h-14 rounded-2xl border border-red-500/30 text-red-400 font-bold hover:bg-red-500/10 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
                  >
                    {rejectMutation.isPending ? (
                      <Loader2 className="w-5 h-5 animate-spin" />
                    ) : (
                      <XCircle className="w-5 h-5" />
                    )}
                    Reject
                  </button>
                  <button
                    onClick={() => handleApprove(selected.id)}
                    disabled={approveMutation.isPending}
                    className="flex-[2] h-14 rounded-2xl bg-gradient-to-r from-emerald-600 to-emerald-500 font-bold shadow-lg shadow-emerald-500/30 hover:shadow-emerald-500/50 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
                  >
                    {approveMutation.isPending ? (
                      <Loader2 className="w-5 h-5 animate-spin" />
                    ) : (
                      <CheckCircle2 className="w-5 h-5" />
                    )}
                    Approve & Send
                  </button>
                </div>
              </motion.div>
            )}
          </div>
        )}
      </div>
    </Shell>
  );
}
