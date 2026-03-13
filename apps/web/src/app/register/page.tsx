"use client";

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Zap, Loader2, Mail, Lock, Building2, User, ArrowRight, CheckCircle2 } from 'lucide-react';
import Link from 'next/link';
import { useRegister, useLogin } from '@/hooks/useApi';

export default function RegisterPage() {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    full_name: '',
    company_name: '',
  });
  const [error, setError] = useState('');
  
  const registerMutation = useRegister();
  const loginMutation = useLogin();

  const handleNext = (e: React.FormEvent) => {
    e.preventDefault();
    if (step === 1 && formData.email && formData.password) {
      setStep(2);
    } else if (step === 2) {
      handleRegister();
    }
  };

  const handleRegister = async () => {
    setError('');
    try {
      await registerMutation.mutateAsync(formData);
      // Automatically log them in after register
      await loginMutation.mutateAsync({ email: formData.email, password: formData.password });
      window.location.href = '/dashboard';
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed');
    }
  };

  return (
    <div className="min-h-screen bg-surface-950 flex items-center justify-center p-6 relative overflow-hidden">
      <div className="absolute top-1/4 -right-1/4 w-96 h-96 bg-brand-600/20 rounded-full blur-[120px]" />
      <div className="absolute bottom-1/4 -left-1/4 w-96 h-96 bg-violet-600/20 rounded-full blur-[120px]" />

      <div className="w-full max-w-md z-10">
        <div className="text-center mb-10">
          <div className="w-16 h-16 bg-gradient-to-br from-brand-500 to-violet-600 rounded-2xl mx-auto flex items-center justify-center shadow-lg shadow-brand-500/20 mb-6">
            <Zap className="w-8 h-8 text-white fill-white" />
          </div>
          <h1 className="text-3xl font-black mb-2">Join Sales.AI</h1>
          <p className="text-white/40">Create an autonomous agent for your company</p>
        </div>

        {/* Step Indicator */}
        <div className="flex items-center justify-center gap-2 mb-8">
          <div className={`h-2 flex-1 rounded-full ${step >= 1 ? 'bg-brand-500' : 'bg-white/10'} transition-colors duration-500`} />
          <div className={`h-2 flex-1 rounded-full ${step >= 2 ? 'bg-brand-500' : 'bg-white/10'} transition-colors duration-500`} />
        </div>

        {error && (
          <div className="mb-6 p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm text-center">
            {error}
          </div>
        )}

        <form onSubmit={handleNext} className="glass p-10 rounded-[2rem] border-white/5 shadow-2xl overflow-hidden relative min-h-[400px]">
          <AnimatePresence mode="wait">
            {step === 1 ? (
              <motion.div
                key="step1"
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 50 }}
                className="space-y-5"
              >
                <div className="space-y-2">
                  <label className="text-xs font-bold uppercase tracking-widest text-white/40 ml-1">Work Email</label>
                  <div className="relative">
                    <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-white/30" />
                    <input
                      type="email"
                      required
                      className="w-full h-14 pl-12 pr-4 bg-white/5 border border-white/10 rounded-2xl focus:border-brand-500/50 outline-none focus:ring-4 focus:ring-brand-500/10 transition-all font-mono text-sm"
                      placeholder="founder@startup.com"
                      value={formData.email}
                      onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <label className="text-xs font-bold uppercase tracking-widest text-white/40 ml-1">Password</label>
                  <div className="relative">
                    <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-white/30" />
                    <input
                      type="password"
                      required
                      minLength={8}
                      className="w-full h-14 pl-12 pr-4 bg-white/5 border border-white/10 rounded-2xl focus:border-brand-500/50 outline-none focus:ring-4 focus:ring-brand-500/10 transition-all"
                      placeholder="••••••••"
                      value={formData.password}
                      onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  className="w-full h-14 mt-4 bg-white/10 hover:bg-white/20 border border-white/5 hover:border-white/20 rounded-2xl font-bold flex items-center justify-center gap-2 group transition-all"
                >
                  Continue
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </button>
              </motion.div>
            ) : (
              <motion.div
                key="step2"
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 50 }}
                className="space-y-5"
              >
                <div className="space-y-2">
                  <label className="text-xs font-bold uppercase tracking-widest text-white/40 ml-1">Full Name</label>
                  <div className="relative">
                    <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-white/30" />
                    <input
                      type="text"
                      className="w-full h-14 pl-12 pr-4 bg-white/5 border border-white/10 rounded-2xl focus:border-brand-500/50 outline-none focus:ring-4 focus:ring-brand-500/10 transition-all"
                      placeholder="Steve Jobs"
                      value={formData.full_name}
                      onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <label className="text-xs font-bold uppercase tracking-widest text-white/40 ml-1">Company Name</label>
                  <div className="relative">
                    <Building2 className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-white/30" />
                    <input
                      type="text"
                      className="w-full h-14 pl-12 pr-4 bg-white/5 border border-white/10 rounded-2xl focus:border-brand-500/50 outline-none focus:ring-4 focus:ring-brand-500/10 transition-all font-mono text-sm"
                      placeholder="Apple Inc."
                      value={formData.company_name}
                      onChange={(e) => setFormData({ ...formData, company_name: e.target.value })}
                    />
                  </div>
                </div>

                <div className="pt-4 flex gap-3">
                  <button
                    type="button"
                    onClick={() => setStep(1)}
                    className="w-14 h-14 shrink-0 bg-white/5 hover:bg-white/10 border border-white/10 rounded-2xl flex items-center justify-center transition-colors"
                  >
                    <ArrowRight className="w-5 h-5 rotate-180 text-white/60" />
                  </button>
                  <button
                    type="submit"
                    disabled={registerMutation.isPending || loginMutation.isPending}
                    className="flex-1 h-14 bg-gradient-to-r from-brand-600 to-violet-600 hover:from-brand-500 hover:to-violet-500 rounded-2xl font-bold flex items-center justify-center gap-2 group transition-all disabled:opacity-50 shadow-lg shadow-brand-500/25"
                  >
                    {registerMutation.isPending || loginMutation.isPending ? (
                      <Loader2 className="w-5 h-5 animate-spin" />
                    ) : (
                      <>
                        Launch Agent
                        <CheckCircle2 className="w-5 h-5" />
                      </>
                    )}
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </form>

        <p className="mt-8 text-center text-sm text-white/40">
          Already have an workspace?{' '}
          <Link href="/login" className="text-brand-400 font-semibold hover:text-brand-300 hover:underline transition-colors">
            Sign In
          </Link>
        </p>
      </div>
    </div>
  );
}
