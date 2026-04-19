import { useEffect, useRef, useCallback } from 'react';
import { WebSocketClient } from '../services/websocket';

export function useWebSocket(url: string) {
  const clientRef = useRef<WebSocketClient | null>(null);

  useEffect(() => {
    const client = new WebSocketClient(url);
    clientRef.current = client;

    client.connect();

    return () => {
      client.disconnect();
    };
  }, [url]);

  const subscribe = useCallback((event: string, handler: Function) => {
    const client = clientRef.current;
    if (!client) return () => {};

    client.on(event, (message: any) => handler(message));

    return () => {
      // Cleanup would go here
    };
  }, []);

  const on = useCallback((event: string, handler: Function) => {
    subscribe(event, handler);
  }, [subscribe]);

  const send = useCallback((message: any) => {
    const client = clientRef.current;
    if (client) {
      client.send(message);
    }
  }, []);

  const isConnected = useCallback(() => {
    const client = clientRef.current;
    return client?.isConnected() || false;
  }, []);

  return {
    client: clientRef.current,
    on,
    send,
    isConnected,
  };
}
