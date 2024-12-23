'use client';

import * as React from 'react';
import { 
  ToastProvider, 
  ToastViewport, 
  Toast, 
  ToastTitle, 
  ToastDescription, 
  ToastClose, 
  ToastAction 
} from '@/components/ui/toast';

interface ToastOptions {
  title?: string;
  description?: string;
  action?: React.ReactNode;
  variant?: 'default' | 'destructive';
}

export function useToast() {
  const [toastState, setToastState] = React.useState<ToastOptions | null>(null);
  const [isOpen, setIsOpen] = React.useState(false);

  const toast = React.useCallback((options: ToastOptions) => {
    setToastState(options);
    setIsOpen(true);

    // Auto-dismiss after 3 seconds
    const timer = setTimeout(() => {
      setIsOpen(false);
    }, 3000);

    return () => clearTimeout(timer);
  }, []);

  const ToastComponent = isOpen && toastState ? (
    <ToastProvider>
      <Toast 
        open={isOpen} 
        onOpenChange={setIsOpen} 
        variant={toastState.variant || 'default'}
      >
        {toastState.title && <ToastTitle>{toastState.title}</ToastTitle>}
        {toastState.description && <ToastDescription>{toastState.description}</ToastDescription>}
        {toastState.action && <ToastAction altText="Try again">{toastState.action}</ToastAction>}
        <ToastClose />
      </Toast>
      <ToastViewport />
    </ToastProvider>
  ) : null;

  return { 
    toast, 
    ToastComponent 
  };
}

export { ToastAction };
