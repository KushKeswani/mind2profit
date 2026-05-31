import { createClient, type SupabaseClient } from "@supabase/supabase-js";

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

export const isSupabaseConfigured = Boolean(
  supabaseUrl && supabaseAnonKey && String(supabaseUrl).startsWith("http")
);

if (!isSupabaseConfigured) {
  console.warn("Supabase auth env vars missing: set VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY.");
}

/** Null when env is missing — @supabase/supabase-js throws if createClient gets an empty URL. */
export const supabase: SupabaseClient | null = isSupabaseConfigured
  ? createClient(String(supabaseUrl), String(supabaseAnonKey))
  : null;
