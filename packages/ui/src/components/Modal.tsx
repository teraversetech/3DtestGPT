import * as React from "react";
import * as Dialog from "@radix-ui/react-dialog";
import { clsx } from "clsx";

export interface ModalProps {
  title: string;
  description?: string;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  children: React.ReactNode;
}

export const Modal: React.FC<ModalProps> = ({ title, description, open, onOpenChange, children }) => (
  <Dialog.Root open={open} onOpenChange={onOpenChange}>
    <Dialog.Portal>
      <Dialog.Overlay className="fixed inset-0 z-40 bg-black/50 backdrop-blur-sm" />
      <Dialog.Content className={clsx(
        "fixed left-1/2 top-1/2 z-50 w-full max-w-lg -translate-x-1/2 -translate-y-1/2 rounded-xl",
        "border border-neutral-200 bg-white p-6 shadow-2xl"
      )}>
        <div className="space-y-2">
          <Dialog.Title className="text-lg font-semibold text-neutral-900">{title}</Dialog.Title>
          {description ? (
            <Dialog.Description className="text-sm text-neutral-600">{description}</Dialog.Description>
          ) : null}
        </div>
        <div className="mt-4">{children}</div>
        <Dialog.Close className="absolute right-4 top-4 text-neutral-500 hover:text-neutral-700" aria-label="Close">
          ×
        </Dialog.Close>
      </Dialog.Content>
    </Dialog.Portal>
  </Dialog.Root>
);
