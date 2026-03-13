"use client";

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Zap, Loader2, Mail, Lock, ArrowRight } from 'lucide-react';
import Link from 'next/link';
import { useLogin } from '@/hooks/useApi';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const loginMutation = useLogin();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      await loginMutation.mutateAsync({ email, password });
      window.location.href = '/dashboard';
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to login');
    }
  };

  return (
    <div className="min-h-screen bg-surface-950 flex items-center justify-center p-6 relative overflow-hidden">
      {/* Background elements */}
      <div className="absolute top-1/4 -left-1/4 w-96 h-96 bg-brand-600/20 rounded-full blur-[120px]" />
      <div className="absolute bottom-1/4 -right-1/4 w-96 h-96 bg-violet-600/20 rounded-full blur-[120px]" />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-md glass p-10 rounded-[2rem] border-white/5 shadow-2xl z-10"
      >
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-gradient-to-br from-brand-500 to-violet-600 rounded-2xl mx-auto flex items-center justify-center shadow-lg shadow-brand-500/20 mb-6">
            <Zap className="w-8 h-8 text-white fill-white" />
          </div>
          <h1 className="text-3xl font-black mb-2">Welcome Back</h1>
          <p className="text-white/40">Sign in to your Sales.AI workspace</p>
        </div>

        {error && (
          <div className="mb-6 p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm text-center">
            {error}
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-5">
          <div className="space-y-2">
            <label className="text-xs font-bold uppercase tracking-widest text-white/40 ml-1">Email</label>
            <div className="relative">
              <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-white/30" />
              <input
                type="email"
                required
                className="w-full h-14 pl-12 pr-4 bg-white/5 border border-white/10 rounded-2xl focus:border-brand-500/50 outline-none focus:ring-4 focus:ring-brand-500/10 transition-all"
                placeholder="you@company.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
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
                className="w-full h-14 pl-12 pr-4 bg-white/5 border border-white/10 rounded-2xl focus:border-brand-500/50 outline-none focus:ring-4 focus:ring-brand-500/10 transition-all"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loginMutation.isPending}
            className="w-full h-14 mt-4 bg-gradient-to-r from-brand-600 to-violet-600 hover:from-brand-500 hover:to-violet-500 rounded-2xl font-bold flex items-center justify-center gap-2 group transition-all disabled:opacity-50 shadow-lg shadow-brand-500/25"
          >
            {loginMutation.isPending ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <>
                Sign In
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </>
            )}
          </button>
        </form>

        <p className="mt-8 text-center text-sm text-white/40">
          Don't have an account?{' '}
          <Link href="/register" className="text-brand-400 font-semibold hover:text-brand-300 hover:underline transition-colors">
            Create one
          </Link>
        </p>
      </motion.div>
    </div>
  );
}
