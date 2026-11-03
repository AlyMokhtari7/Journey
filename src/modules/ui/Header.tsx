export default function Header() {
  return (
    <header className="relative flex h-14 w-full items-center bg-[#fdfcfb] px-6 shadow-[0_1px_0_0_rgba(0,0,0,0.06)]">
      {/* Left: orange square */}
      <div className="flex items-center">
        <div className="h-9 w-9 rounded-[6px] bg-[#c46a2a] shadow-[0_2px_8px_rgba(196,106,42,0.3)]" />
      </div>

      {/* Center: title - absolutely centered */}
      <div className="absolute left-1/2 -translate-x-1/2">
        <h1 className="whitespace-nowrap text-[14px] font-medium tracking-[0.01em] text-[#4a4540]">
          <span className="text-[#2d2a26]">My Project</span>
          <span className="mx-2 text-[#c4b8a8]">/</span>
          <span>Sample One</span>
        </h1>
      </div>

      {/* Right: actions */}
      <div className="ml-auto flex items-center gap-3">
        <button
          aria-label="Play"
          className="flex h-9 w-9 items-center justify-center rounded-[8px] bg-[#3cb371] text-white shadow-[0_2px_8px_rgba(60,179,113,0.3)] transition-transform duration-150 hover:scale-105 hover:shadow-[0_4px_12px_rgba(60,179,113,0.4)] active:scale-95"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" stroke="none">
            <polygon points="5 3 19 12 5 21 5 3" />
          </svg>
        </button>
        <button className="flex h-9 items-center gap-2 rounded-[8px] bg-[#1a1816] px-4 text-[13px] font-medium text-[#f0ede8] shadow-[0_2px_8px_rgba(26,24,22,0.25)] transition-all duration-150 hover:bg-[#2d2a26] hover:shadow-[0_4px_12px_rgba(26,24,22,0.35)] active:scale-[0.97]">
          Export
        </button>
      </div>
    </header>
  );
}