import { WebSocketMessage, ProcessingProgress, Clip } from '../types/api';

type MessageHandler = (message: WebSocketMessage) => void;
type ErrorHandler = (error: Event) => void;

export class WebSocketClient {
  private ws: WebSocket | null = null;
  private url: string;
  private reconnectAttempts: number = 0;
  private maxReconnectAttempts: number = 5;
  private reconnectDelay: number = 3000;
  private handlers: Map<string, MessageHandler[]> = new Map();
  private errorHandlers: ErrorHandler[] = [];
  private connectionHandlers: Array<() => void> = [];
  private disconnectHandlers: Array<() => void> = [];

  constructor(url: string) {
    this.url = url;
  }

  connect(): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      return;
    }

    try {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        console.log('WebSocket connected');
        this.reconnectAttempts = 0;
        this.connectionHandlers.forEach(handler => handler());
      };

      this.ws.onclose = (event: CloseEvent) => {
        console.log('WebSocket disconnected', event);
        this.disconnectHandlers.forEach(handler => handler());

        if (!event.wasClean && this.reconnectAttempts < this.maxReconnectAttempts) {
          this.reconnectAttempts++;
          console.log(`Reconnecting... (attempt ${this.reconnectAttempts})`);
          setTimeout(() => this.connect(), this.reconnectDelay);
        }
      };

      this.ws.onerror = (error: Event) => {
        console.error('WebSocket error:', error);
        this.errorHandlers.forEach(handler => handler(error));
      };

      this.ws.onmessage = (event: MessageEvent) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data);
          this.handleMessage(message);
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error);
        }
      };
    } catch (error) {
      console.error('Failed to create WebSocket connection:', error);
    }
  }

  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  private handleMessage(message: WebSocketMessage): void {
    const type = message.type;
    const handlers = this.handlers.get(type) || [];
    handlers.forEach(handler => handler(message));
  }

  on(event: string, handler: MessageHandler): void {
    if (!this.handlers.has(event)) {
      this.handlers.set(event, []);
    }
    this.handlers.get(event)!.push(handler);
  }

  onError(handler: ErrorHandler): void {
    this.errorHandlers.push(handler);
  }

  onConnect(handler: () => void): void {
    this.connectionHandlers.push(handler);
  }

  onDisconnect(handler: () => void): void {
    this.disconnectHandlers.push(handler);
  }

  send(message: any): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    } else {
      console.warn('WebSocket is not connected. Message not sent:', message);
    }
  }

  isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN;
  }
}

// Convenience functions for common event types
export function onProgress(client: WebSocketClient, handler: (progress: ProcessingProgress) => void): void {
  client.on('progress', (message: WebSocketMessage) => {
    if (message.type === 'progress' && message.data) {
      handler(message.data as ProcessingProgress);
    }
  });
}

export function onClipGenerated(client: WebSocketClient, handler: (clip: Clip) => void): void {
  client.on('clip_generated', (message: WebSocketMessage) => {
    if (message.type === 'clip_generated' && message.data) {
      handler(message.data as Clip);
    }
  });
}

export function onError(client: WebSocketClient, handler: (error: string) => void): void {
  client.on('error', (message: WebSocketMessage) => {
    if (message.type === 'error' && message.data) {
      handler((message.data as any).error || 'Unknown error');
    }
  });
}

export function onComplete(client: WebSocketClient, handler: (data: any) => void): void {
  client.on('complete', (message: WebSocketMessage) => {
    if (message.type === 'complete' && message.data) {
      handler(message.data);
    }
  });
}
