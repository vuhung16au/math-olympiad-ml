import { X } from "lucide-react";

type SubstackPopupProps = {
  isOpen: boolean;
  onClose: () => void;
};

export default function SubstackPopup({ isOpen, onClose }: SubstackPopupProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/40 p-4 backdrop-blur-sm">
      <div className="relative w-full max-w-sm overflow-hidden rounded-[24px] bg-white p-6 shadow-2xl">
        <button
          onClick={onClose}
          className="absolute right-4 top-4 rounded-full p-1 text-gray-400 hover:bg-gray-100 hover:text-gray-600 transition"
          aria-label="Close"
        >
          <X className="h-5 w-5" />
        </button>
        <div className="mb-4">
          <h3 className="text-xl font-bold text-[var(--color-purple)]">Great job!</h3>
        </div>
        <p className="mb-6 text-sm text-gray-700 leading-relaxed">
          Thank you for reading the booklet cover to cover. Please join our Substack channel for updates to the HSC Math Hub, and receive tips, fully worked examples, and trial exams for HSC Math Extension 1 and Extension 2.
        </p>
        <a
          href="https://vuhung16.substack.com/"
          target="_blank"
          rel="noopener noreferrer"
          className="flex w-full items-center justify-center rounded-xl bg-[var(--color-purple)] px-4 py-3 font-semibold text-white! hover:text-white! transition hover:bg-[color:color-mix(in_srgb,var(--color-purple)_80%,black)] shadow-md"
          style={{ color: "#ffffff" }}
          onClick={onClose}
        >
          Join Substack Channel
        </a>
      </div>
    </div>
  );
}
