import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '@/lib/api';

// ─── Dashboard ───
export function useDashboardStats() {
  return useQuery({
    queryKey: ['dashboard', 'stats'],
    queryFn: async () => {
      const { data } = await api.get('/dashboard/stats');
      return data;
    },
    refetchInterval: 30_000, // live poll every 30s
  });
}

// ─── Campaigns ───
export function useCampaigns() {
  return useQuery({
    queryKey: ['campaigns'],
    queryFn: async () => {
      const { data } = await api.get('/campaigns');
      return data;
    },
  });
}

export function useCreateCampaign() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (payload: {
      name: string;
      industry: string;
      companySize: string;
      valueProp: string;
      offerSummary: string;
    }) => {
      const { data } = await api.post('/campaigns', {
        name: payload.name,
        target_industries: [payload.industry],
        offer_summary: payload.offerSummary,
        value_proposition: payload.valueProp,
        company_size: payload.companySize,
      });
      return data;
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['campaigns'] });
      qc.invalidateQueries({ queryKey: ['dashboard'] });
    },
  });
}

// ─── Leads ───
export function useLeads(campaignId?: string) {
  return useQuery({
    queryKey: ['leads', campaignId],
    queryFn: async () => {
      const url = campaignId ? `/leads?campaign_id=${campaignId}` : '/leads';
      const { data } = await api.get(url);
      return data;
    },
  });
}

// ─── Approvals (Pending Messages) ───
export function useApprovals() {
  return useQuery({
    queryKey: ['approvals'],
    queryFn: async () => {
      const { data } = await api.get('/campaigns/approvals');
      return data;
    },
    refetchInterval: 15_000, // poll every 15s for new drafts
  });
}

export function useApproveMessage() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (messageId: string) => {
      const { data } = await api.post(`/campaigns/approvals/${messageId}/approve`);
      return data;
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['approvals'] });
      qc.invalidateQueries({ queryKey: ['dashboard'] });
    },
  });
}

export function useRejectMessage() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (messageId: string) => {
      const { data } = await api.post(`/campaigns/approvals/${messageId}/reject`);
      return data;
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['approvals'] });
    },
  });
}

// ─── Auth ───
export function useLogin() {
  return useMutation({
    mutationFn: async (credentials: { email: string; password: string }) => {
      const { data } = await api.post('/auth/login', credentials);
      if (data.access_token) {
        if (typeof window !== 'undefined') {
          localStorage.setItem('auth_token', data.access_token);
        }
      }
      return data;
    },
  });
}

export function useRegister() {
  return useMutation({
    mutationFn: async (payload: { email: string; password: string; full_name?: string; company_name?: string }) => {
      const { data } = await api.post('/auth/register', payload);
      return data;
    },
  });
}

// ─── Logs ───
export function useCampaignLogs(campaignId: string) {
  return useQuery({
    queryKey: ['logs', campaignId],
    queryFn: async () => {
      const { data } = await api.get(`/agent-logs/${campaignId}`);
      return data.logs;
    },
    enabled: !!campaignId,
    refetchInterval: 10_000, // live poll every 10s
  });
}
