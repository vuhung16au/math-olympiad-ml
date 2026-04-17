export default function LoadingSpinner({ label = "Loading" }: { label?: string }) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 py-10 text-[var(--color-purple)]">
      <div className="h-10 w-10 animate-spin rounded-full border-4 border-[color:color-mix(in_srgb,var(--color-purple)_15%,white)] border-t-[var(--color-red)]" />
      <p className="text-sm font-medium text-[color:color-mix(in_srgb,var(--color-charcoal)_78%,white)]">
        {label}
      </p>
    </div>
  );
}
