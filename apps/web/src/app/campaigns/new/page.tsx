"use client";

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ChevronRight,
  Sparkles,
  Zap,
  Loader2
} from 'lucide-react';
import { Shell } from '@/components/layout/Shell';
import { useCreateCampaign } from '@/hooks/useApi';

const sectors = ['SaaS', 'Fintech', 'HR Tech', 'E-commerce', 'Cybersecurity', 'Logistics'];
const companySizes = ['1-50', '51-200', '201-500', '500+'];

export default function CreateCampaign() {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    name: '',
    industry: '',
    companySize: '',
    valueProp: '',
    offerSummary: ''
  });

  const createCampaign = useCreateCampaign();

  const nextStep = () => setStep((prev: number) => prev + 1);
  const prevStep = () => setStep((prev: number) => prev - 1);

  const deployAgents = async () => {
    try {
      await createCampaign.mutateAsync(formData);
    } catch (err) {
      console.error("Backend unreachable, navigating anyway:", err);
    }
    window.location.href = '/dashboard';
  };

  return (
    <Shell>
      <div className="max-w-4xl mx-auto space-y-12 pb-24">
        {/* Progress Bar */}
        <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden flex gap-2">
           {[1, 2, 3].map((s) => (
             <motion.div 
               key={s}
               initial={false}
               animate={{ 
                 width: step >= s ? '33.3%' : '20%',
                 backgroundColor: step >= s ? 'rgba(99, 102, 241, 1)' : 'rgba(255, 255, 255, 0.1)'
               }}
               className="h-full rounded-full transition-all"
             />
           ))}
        </div>

        <AnimatePresence mode="wait">
          {step === 1 && (
            <motion.div
              key="step1"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="space-y-8"
            >
              <div>
                 <h1 className="text-3xl font-bold mb-2">Campaign Identity</h1>
                 <p className="text-white/40">Define who you are targeting and why.</p>
              </div>

              <div className="space-y-6">
                 <div className="group space-y-2">
                    <label className="text-xs font-bold uppercase tracking-widest text-white/40 group-focus-within:text-brand-500 transition-colors">Campaign Name</label>
                    <input 
                      className="w-full h-14 px-6 bg-white/5 border border-white/10 rounded-2xl focus:border-brand-500/50 outline-none focus:ring-4 focus:ring-brand-500/10 transition-all text-lg font-medium"
                      placeholder="e.g. Q1 Growth - SaaS Founders"
                      value={formData.name}
                      onChange={(e: React.ChangeEvent<HTMLInputElement>) => setFormData({...formData, name: e.target.value})}
                    />
                 </div>

                 <div className="grid grid-cols-2 gap-6">
                    <div className="space-y-4">
                       <label className="text-xs font-bold uppercase tracking-widest text-white/40">Primary Sector</label>
                       <div className="grid grid-cols-2 gap-2">
                          {sectors.map(s => (
                            <button 
                              key={s} 
                              onClick={() => setFormData({...formData, industry: s})}
                              className={`px-4 py-3 rounded-xl border text-sm font-medium transition-all ${
                                formData.industry === s ? 'bg-brand-600 border-brand-500 shadow-lg shadow-brand-500/20' : 'bg-white/5 border-white/10 hover:border-white/20'
                              }`}
                            >
                               {s}
                            </button>
                          ))}
                       </div>
                    </div>

                    <div className="space-y-4">
                       <label className="text-xs font-bold uppercase tracking-widest text-white/40">Company Size</label>
                       <div className="grid grid-cols-2 gap-2">
                          {companySizes.map(s => (
                            <button 
                              key={s} 
                              onClick={() => setFormData({...formData, companySize: s})}
                              className={`px-4 py-3 rounded-xl border text-sm font-medium transition-all ${
                                formData.companySize === s ? 'bg-brand-600 border-brand-500 shadow-lg shadow-brand-500/20' : 'bg-white/5 border-white/10 hover:border-white/20'
                              }`}
                            >
                               {s}
                            </button>
                          ))}
                       </div>
                    </div>
                 </div>

                 <button 
                   onClick={nextStep}
                   className="w-full h-14 bg-brand-600 hover:bg-brand-700 rounded-2xl font-bold flex items-center justify-center gap-2 group transition-all"
                 >
                    Continue to Strategy
                    <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                 </button>
              </div>
            </motion.div>
          )}

          {step === 2 && (
            <motion.div
              key="step2"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="space-y-8"
            >
              <div>
                 <h1 className="text-3xl font-bold mb-2 text-transparent bg-clip-text bg-gradient-to-r from-brand-400 to-violet-400">Offer & Messaging</h1>
                 <p className="text-white/40">This will be used to calibrate your AI agents.</p>
              </div>

              <div className="space-y-6">
                 <div className="space-y-2">
                    <label className="text-xs font-bold uppercase tracking-widest text-white/40">Value Proposition</label>
                    <textarea 
                      rows={4}
                      className="w-full p-6 bg-white/5 border border-white/10 rounded-3xl focus:border-brand-500/50 outline-none focus:ring-4 focus:ring-brand-500/10 transition-all text-base resize-none"
                      placeholder="e.g. We provide 2x faster CI/CD pipelines for Kubernetes teams using unique caching..."
                      value={formData.valueProp}
                      onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setFormData({...formData, valueProp: e.target.value})}
                    />
                 </div>

                 <div className="space-y-2">
                    <label className="text-xs font-bold uppercase tracking-widest text-white/40">Offer Summary</label>
                    <textarea 
                      rows={3}
                      className="w-full p-6 bg-white/5 border border-white/10 rounded-3xl focus:border-brand-500/50 outline-none focus:ring-4 focus:ring-brand-500/10 transition-all text-base resize-none"
                      placeholder="e.g. Free 14-day trial with dedicated onboarding..."
                      value={formData.offerSummary}
                      onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setFormData({...formData, offerSummary: e.target.value})}
                    />
                 </div>

                 <div className="flex gap-4">
                   <button onClick={prevStep} className="flex-1 h-14 glass rounded-2xl font-bold hover:bg-white/10 transition-all">Back</button>
                   <button 
                     onClick={nextStep}
                     className="flex-[2] h-14 bg-brand-600 hover:bg-brand-700 rounded-2xl font-bold flex items-center justify-center gap-2"
                   >
                      Next Step
                   </button>
                 </div>
              </div>
            </motion.div>
          )}

          {step === 3 && (
            <motion.div
              key="step3"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="glass p-12 rounded-[40px] text-center space-y-8 border-brand-500/30"
            >
               <div className="w-20 h-20 bg-brand-600 rounded-3xl mx-auto flex items-center justify-center shadow-[0_0_50px_rgba(99,102,241,0.5)]">
                  <Sparkles className="w-10 h-10 text-white" />
               </div>
               
               <div>
                  <h2 className="text-4xl font-black mb-4">Ready to Launch?</h2>
                  <p className="text-white/40 max-w-md mx-auto">Our autonomous agents are primed and ready to start prospecting based on your strategy.</p>
               </div>

               <div className="grid grid-cols-3 gap-4 max-w-lg mx-auto">
                  <div className="p-4 rounded-2xl bg-white/5 border border-white/5 text-left">
                     <p className="text-[10px] font-bold text-white/30 uppercase tracking-widest mb-1">Campaign</p>
                     <p className="font-bold text-sm truncate">{formData.name || 'Undefined'}</p>
                  </div>
                  <div className="p-4 rounded-2xl bg-white/5 border border-white/5 text-left">
                     <p className="text-[10px] font-bold text-white/30 uppercase tracking-widest mb-1">Sector</p>
                     <p className="font-bold text-sm">{formData.industry || 'General'}</p>
                  </div>
                  <div className="p-4 rounded-2xl bg-white/5 border border-white/5 text-left">
                     <p className="text-[10px] font-bold text-white/30 uppercase tracking-widest mb-1">Size</p>
                     <p className="font-bold text-sm">{formData.companySize || 'Any'}</p>
                  </div>
               </div>

               <button 
                 onClick={deployAgents}
                 disabled={createCampaign.isPending}
                 className="w-full h-16 bg-gradient-to-r from-brand-600 to-violet-600 rounded-[20px] font-black text-lg shadow-xl hover:shadow-brand-500/40 transition-all flex items-center justify-center gap-3 disabled:opacity-50"
               >
                  {createCampaign.isPending ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      Deploying Agents...
                    </>
                  ) : (
                    <>
                      Deploy Agents Now
                      <Zap className="w-5 h-5 fill-white" />
                    </>
                  )}
               </button>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </Shell>
  );
}
