"use client";

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useParams } from 'next/navigation';
import { Shell } from '@/components/layout/Shell';
import { useCampaignLogs } from '@/hooks/useApi';
import { Loader2, Terminal, Activity, ArrowLeft, CheckCircle2, XCircle } from 'lucide-react';

interface LogEntry {
  id: string;
  node: string;
  status: string;
  details: any;
  created_at: string;
}

const mockLogs: LogEntry[] = [
  { id: '1', node: 'prospect', status: 'completed', details: { leads_count: 5, status: 'prospecting_complete' }, created_at: new Date(Date.now() - 60000).toISOString() },
  { id: '2', node: 'qualify', status: 'completed', details: { leads_count: 5, status: 'qualification_complete' }, created_at: new Date(Date.now() - 45000).toISOString() },
  { id: '3', node: 'draft', status: 'completed', details: { leads_count: 5, status: 'drafting_complete' }, created_at: new Date(Date.now() - 30000).toISOString() },
  { id: '4', node: 'send', status: 'completed', details: { leads_count: 5, status: 'sending_complete' }, created_at: new Date(Date.now() - 10000).toISOString() }
];

export default function AgentLogsPage() {
  const params = useParams();
  const campaignId = Array.isArray(params.id) ? params.id[0] : params.id;
  const { data: apiLogs, isLoading } = useCampaignLogs(campaignId || '');

  const logs = apiLogs?.length ? apiLogs : mockLogs;

  const getNodeIcon = (node: string) => {
    switch (node) {
      case 'prospect': return <SearchIcon className="w-5 h-5 text-blue-400" />;
      case 'qualify': return <TargetIcon className="w-5 h-5 text-amber-400" />;
      case 'draft': return <EditIcon className="w-5 h-5 text-violet-400" />;
      case 'send': return <SendIcon className="w-5 h-5 text-emerald-400" />;
      default: return <Activity className="w-5 h-5 text-brand-400" />;
    }
  };

  return (
    <Shell>
      <div className="space-y-8 max-w-4xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center gap-4"
        >
          <button 
            onClick={() => window.history.back()}
            className="p-3 bg-white/5 border border-white/10 rounded-2xl hover:bg-white/10 transition-all text-white/60 hover:text-white"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div>
            <p className="text-white/40 mb-1 text-sm font-medium flex items-center gap-2">
              <Terminal className="w-4 h-4" /> Agent Console
            </p>
            <h1 className="text-3xl font-bold">Execution Logs</h1>
          </div>
        </motion.div>

        {/* Console View */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="glass rounded-3xl overflow-hidden font-mono text-sm relative"
        >
          {/* Mac-like Header */}
          <div className="bg-black/40 px-6 py-3 border-b border-white/5 flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-red-500/50" />
            <div className="w-3 h-3 rounded-full bg-amber-500/50" />
            <div className="w-3 h-3 rounded-full bg-green-500/50" />
            <div className="ml-4 text-white/30 text-xs">LangGraph Executor • {campaignId}</div>
            {isLoading && (
              <div className="ml-auto text-brand-400 text-xs flex items-center gap-2">
                <Loader2 className="w-3 h-3 animate-spin" /> polling
              </div>
            )}
          </div>

          <div className="p-6 space-y-4 max-h-[600px] overflow-y-auto w-full">
            <AnimatePresence>
              {logs.map((log: LogEntry, index: number) => (
                <motion.div
                  key={log.id}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="flex items-start gap-4 p-4 rounded-xl hover:bg-white/5 transition-colors border border-transparent hover:border-white/5"
                >
                  <div className="mt-1">
                    {log.status === 'completed' ? (
                      <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                    ) : (
                      <XCircle className="w-5 h-5 text-red-400" />
                    )}
                  </div>
                  <div className="flex-1 space-y-2">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="text-brand-400 font-bold">[{log.node.toUpperCase()}]</span>
                        <span className="text-white/60">Node execution {log.status}</span>
                      </div>
                      <span className="text-white/30 text-xs">
                        {new Date(log.created_at).toLocaleTimeString()}
                      </span>
                    </div>
                    {/* JSON formatting */}
                    <div className="bg-black/30 p-4 rounded-xl text-white/70 overflow-x-auto border border-white/5">
                      <pre>
                        {JSON.stringify(log.details, null, 2)}
                      </pre>
                    </div>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
            {logs.length === 0 && !isLoading && (
              <div className="text-center p-10 text-white/30">
                <Terminal className="w-10 h-10 mx-auto mb-3 opacity-50" />
                <p>No execution logs found for this campaign.</p>
              </div>
            )}
            {/* Blinking cursor for effect */}
            {logs.length > 0 && (
              <motion.div 
                animate={{ opacity: [1, 0] }}
                transition={{ repeat: Infinity, duration: 0.8 }}
                className="w-2 h-4 bg-brand-400 ml-11 inline-block"
              />
            )}
          </div>
        </motion.div>
      </div>
    </Shell>
  );
}

// Minimal icon components for the switch statement
const SearchIcon = (props: any) => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>;
const TargetIcon = (props: any) => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>;
const EditIcon = (props: any) => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>;
const SendIcon = (props: any) => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg>;
