import React, { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { useAuth } from "@/contexts/AuthContext";

export type AppNotificationType = "eod_pnl" | "journal_reminder" | "server_email" | "system";

export interface AppNotification {
  id: string;
  type: AppNotificationType;
  title: string;
  body: string;
  createdAt: string;
  read: boolean;
}

interface NotificationContextValue {
  items: AppNotification[];
  unreadCount: number;
  upsert: (n: Omit<AppNotification, "read"> & { read?: boolean }) => void;
  markRead: (id: string) => void;
  markAllRead: () => void;
  clear: () => void;
}

const NotificationContext = createContext<NotificationContextValue | undefined>(undefined);

const storeKey = (userId: string) => `mind2profit_notifs_v1_${userId}`;

function loadStored(userId: string): AppNotification[] {
  try {
    const raw = localStorage.getItem(storeKey(userId));
    if (!raw) return [];
    const parsed = JSON.parse(raw) as AppNotification[];
    if (!Array.isArray(parsed)) return [];
    return parsed;
  } catch {
    return [];
  }
}

function saveStored(userId: string, items: AppNotification[]) {
  try {
    localStorage.setItem(storeKey(userId), JSON.stringify(items.slice(0, 200)));
  } catch {
    /* ignore quota */
  }
}

export const NotificationProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user } = useAuth();
  const userId = user?.id;
  const [items, setItems] = useState<AppNotification[]>([]);

  useEffect(() => {
    if (!userId) {
      setItems([]);
      return;
    }
    setItems(loadStored(userId));
  }, [userId]);

  useEffect(() => {
    if (!userId) return;
    saveStored(userId, items);
  }, [userId, items]);

  const upsert = useCallback(
    (n: Omit<AppNotification, "read"> & { read?: boolean }) => {
      if (!userId) return;
      setItems((prev) => {
        const next: AppNotification = {
          id: n.id,
          type: n.type,
          title: n.title,
          body: n.body,
          createdAt: n.createdAt,
          read: n.read ?? false,
        };
        const without = prev.filter((x) => x.id !== n.id);
        return [next, ...without].slice(0, 200);
      });
    },
    [userId]
  );

  const markRead = useCallback((id: string) => {
    setItems((prev) => prev.map((x) => (x.id === id ? { ...x, read: true } : x)));
  }, []);

  const markAllRead = useCallback(() => {
    setItems((prev) => prev.map((x) => ({ ...x, read: true })));
  }, []);

  const clear = useCallback(() => setItems([]), []);

  const unreadCount = useMemo(() => items.filter((i) => !i.read).length, [items]);

  const value = useMemo(
    () => ({
      items,
      unreadCount,
      upsert,
      markRead,
      markAllRead,
      clear,
    }),
    [items, unreadCount, upsert, markRead, markAllRead, clear]
  );

  return <NotificationContext.Provider value={value}>{children}</NotificationContext.Provider>;
};

export const useNotifications = () => {
  const ctx = useContext(NotificationContext);
  if (!ctx) {
    throw new Error("useNotifications must be used within NotificationProvider");
  }
  return ctx;
};
