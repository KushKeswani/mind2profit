-- Mind2Profit baseline Supabase schema
-- Run this in Supabase SQL Editor for the target project.

-- Waitlist table
create table if not exists public.waitlist (
  id uuid primary key default gen_random_uuid(),
  email text not null unique,
  subscribed_at timestamptz not null default now(),
  status text not null default 'active'
);

create index if not exists idx_waitlist_subscribed_at on public.waitlist (subscribed_at desc);

-- Beta applications table
create table if not exists public.beta_applications (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  first_name text not null default '',
  last_name text not null default '',
  email text not null default '',
  trading_experience text not null default '',
  trading_style text not null default '',
  current_tools text not null default '',
  pain_points text not null default '',
  expectations text not null default '',
  time_commitment text not null default '',
  social_media text not null default '',
  additional_info text not null default '',
  device_access jsonb not null default '[]'::jsonb
);

create index if not exists idx_beta_applications_created_at on public.beta_applications (created_at desc);
create index if not exists idx_beta_applications_email on public.beta_applications (email);

-- Optional RLS (disabled by default for current backend behavior).
-- Uncomment if/when you add proper auth policies.
-- alter table public.waitlist enable row level security;
-- alter table public.beta_applications enable row level security;
