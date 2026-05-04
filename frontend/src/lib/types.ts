export interface User {
  id: string;
  email: string;
  name: string | null;
  is_active: boolean;
  created_at: string;
}

export interface JobPosting {
  id: string;
  url: string;
  title: string | null;
  company: string | null;
  company_url: string | null;
  location: string | null;
  description: string | null;
  source: string | null;
  salary_min: number | null;
  salary_max: number | null;
  salary_currency: string | null;
  trust_score: number | null;
  trust_score_updated_at: string | null;
  posted_date: string | null;
  is_active: boolean;
  created_at: string;
}

export interface TrustScoreDetail {
  freshness_score: number;
  feedback_score: number;
  company_score: number;
  quality_score: number;
  total: number;
  confidence: string;
}

export interface JobApplication {
  id: string;
  user_id: string;
  job_id: string;
  status: string;
  applied_date: string | null;
}

export interface JobFeedback {
  id: string;
  job_id: string;
  user_id: string;
  outcome: string;
  comment: string | null;
  tag: string | null;
  feedback_date: string | null;
}

export interface FeedbackAggregation {
  total_feedbacks: number;
  outcome_counts: Record<string, number>;
  confidence: string;
}

export interface OutreachTemplate {
  id: string;
  user_id: string;
  job_id: string;
  message: string;
  outreach_type: string | null;
  tone: string | null;
  provider: string | null;
  created_at: string | null;
}

export interface OutreachGenerateResponse {
  message: string;
  provider: string;
  model: string;
  tokens_used: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}
