/**
 * Custom hook for clip management
 */

import { useState, useCallback } from 'react';
import { Clip } from '../types/api';

export function useClips(initialClips: Clip[] = []) {
  const [clips, setClips] = useState<Clip[]>(initialClips);
  const [selectedClipId, setSelectedClipId] = useState<string | null>(null);

  const addClip = useCallback((clip: Clip) => {
    setClips(prev => [...prev, clip]);
  }, []);

  const removeClip = useCallback((clipId: string) => {
    setClips(prev => prev.filter(clip => clip.id !== clipId));
  }, []);

  const updateClip = useCallback((clipId: string, updates: Partial<Clip>) => {
    setClips(prev =>
      prev.map(clip =>
        clip.id === clipId ? { ...clip, ...updates } : clip
      )
    );
  }, []);

  const toggleClipEnabled = useCallback((clipId: string) => {
    setClips(prev =>
      prev.map(clip =>
        clip.id === clipId ? { ...clip, enabled: !clip.enabled } : clip
      )
    );
  }, []);

  const getClip = useCallback((clipId: string) => {
    return clips.find(clip => clip.id === clipId);
  }, [clips]);

  const getEnabledClips = useCallback(() => {
    return clips.filter(clip => clip.enabled);
  }, [clips]);

  const clearClips = useCallback(() => {
    setClips([]);
    setSelectedClipId(null);
  }, []);

  const setClipsBulk = useCallback((newClips: Clip[]) => {
    setClips(newClips);
    if (newClips.length > 0 && !selectedClipId) {
      setSelectedClipId(newClips[0].id);
    }
  }, [selectedClipId]);

  return {
    clips,
    selectedClipId,
    addClip,
    removeClip,
    updateClip,
    toggleClipEnabled,
    getClip,
    getEnabledClips,
    clearClips,
    setClipsBulk,
    setSelectedClipId,
  };
}
