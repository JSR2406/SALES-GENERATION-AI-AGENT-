"use client";

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Shell } from '@/components/layout/Shell';
import { Mail, Shield, User, Bell, CheckCircle2 } from 'lucide-react';

export default function SettingsPage() {
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <Shell>
      <div className="max-w-4xl mx-auto space-y-8">
        <div>
          <h1 className="text-3xl font-black mb-2">Workspace Settings</h1>
          <p className="text-white/40">Manage your agent configurations, profile, and email providers.</p>
        </div>

        <div className="grid gap-6">
          {/* Email Provider Settings */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass rounded-3xl p-8 border-white/5"
          >
            <div className="flex items-center gap-4 mb-6">
              <div className="w-12 h-12 rounded-xl bg-brand-500/20 flex items-center justify-center">
                <Mail className="w-6 h-6 text-brand-400" />
              </div>
              <div>
                <h3 className="text-lg font-bold">Email Provider</h3>
                <p className="text-sm text-white/40">Configure Resend or SMTP settings for sending campaigns</p>
              </div>
            </div>

            <div className="space-y-4">
              <div className="space-y-2">
                <label className="text-xs font-bold uppercase tracking-widest text-white/40 ml-1">Provider Type</label>
                <select className="w-full h-12 px-4 bg-white/5 border border-white/10 rounded-xl focus:border-brand-500/50 outline-none appearance-none">
                  <option value="mock">Mock Sandbox (Local Dev)</option>
                  <option value="resend">Resend API</option>
                  <option value="smtp">Custom SMTP</option>
                </select>
              </div>
              
              <div className="space-y-2">
                <label className="text-xs font-bold uppercase tracking-widest text-white/40 ml-1">API Key</label>
                <input 
                  type="password" 
                  value="re_dummy_key_xxxxxxxxxxxxx"
                  readOnly
                  className="w-full h-12 px-4 bg-white/5 border border-white/10 rounded-xl focus:border-brand-500/50 outline-none font-mono text-sm text-white/60"
                />
              </div>
            </div>
          </motion.div>

          {/* Profile Settings */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="glass rounded-3xl p-8 border-white/5"
          >
            <div className="flex items-center gap-4 mb-6">
              <div className="w-12 h-12 rounded-xl bg-violet-500/20 flex items-center justify-center">
                <User className="w-6 h-6 text-violet-400" />
              </div>
              <div>
                <h3 className="text-lg font-bold">Account Profile</h3>
                <p className="text-sm text-white/40">Your personal and company details</p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
               <div className="space-y-2">
                <label className="text-xs font-bold uppercase tracking-widest text-white/40 ml-1">Full Name</label>
                <input 
                  type="text" 
                  defaultValue="Janmejay Singh"
                  className="w-full h-12 px-4 bg-white/5 border border-white/10 rounded-xl focus:border-brand-500/50 outline-none"
                />
              </div>
              <div className="space-y-2">
                <label className="text-xs font-bold uppercase tracking-widest text-white/40 ml-1">Company Name</label>
                <input 
                  type="text" 
                  defaultValue="Sales.AI Demo"
                  className="w-full h-12 px-4 bg-white/5 border border-white/10 rounded-xl focus:border-brand-500/50 outline-none"
                />
              </div>
            </div>
          </motion.div>

          <div className="flex justify-end pt-4">
             <button
               onClick={handleSave}
               className="h-12 px-8 bg-white text-black font-bold rounded-xl hover:bg-white/90 transition-colors flex items-center gap-2"
             >
               {saved ? (
                 <>
                   <CheckCircle2 className="w-5 h-5 text-green-500" />
                   Saved Successfully
                 </>
               ) : (
                 'Save Changes'
               )}
             </button>
          </div>
        </div>

      </div>
    </Shell>
  );
}
