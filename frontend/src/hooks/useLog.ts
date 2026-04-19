import { useState, useCallback } from 'react';

export type LogLevel = 'success' | 'error' | 'info';

export interface LogEntry {
  id: string;
  level: LogLevel;
  message: string;
  timestamp: Date;
}

const STORAGE_KEY = 'ai_clipper_logs';
const MAX_ENTRIES = 200;

function loadFromStorage(): LogEntry[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw) as Array<Omit<LogEntry, 'timestamp'> & { timestamp: string }>;
    return parsed.map((e) => ({ ...e, timestamp: new Date(e.timestamp) }));
  } catch {
    return [];
  }
}

function saveToStorage(entries: LogEntry[]) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(entries.slice(-MAX_ENTRIES)));
  } catch {
    // storage quota - ignore
  }
}

export function useLog() {
  const [entries, setEntries] = useState<LogEntry[]>(loadFromStorage);
  const [unread, setUnread] = useState(0);

  const addLog = useCallback((level: LogLevel, message: string) => {
    const entry: LogEntry = {
      id: `${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
      level,
      message,
      timestamp: new Date(),
    };
    setEntries((prev) => {
      const next = [...prev, entry].slice(-MAX_ENTRIES);
      saveToStorage(next);
      return next;
    });
    setUnread((n) => n + 1);
  }, []);

  const clearLog = useCallback(() => {
    setEntries([]);
    setUnread(0);
    localStorage.removeItem(STORAGE_KEY);
  }, []);

  const markRead = useCallback(() => {
    setUnread(0);
  }, []);

  return { entries, unread, addLog, clearLog, markRead };
}
