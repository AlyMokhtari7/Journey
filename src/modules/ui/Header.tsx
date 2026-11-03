export default function Header() {
  return (
    <header className="flex h-[72px] w-full items-center justify-between bg-[#fdfcfb] px-6 shadow-[0_1px_0_0_rgba(0,0,0,0.06)]">
      {/* Left: orange square */}
      <div className="flex w-[120px] items-center">
        <div className="h-11 w-11 rounded-[6px] bg-[#c46a2a] shadow-[0_2px_10px_rgba(196,106,42,0.3)]" />
      </div>

      {/* Center: title */}
      <div className="flex-1 text-center">
        <h1 className="text-[15px] font-medium tracking-[0.02em] text-[#3a3632]">
          <span className="text-[#2d2a26]">My Project</span>
          <span className="mx-2 text-[#c4b8a8]">/</span>
          <span>Sample One</span>
        </h1>
      </div>

      {/* Right: actions */}
      <div className="flex w-[220px] items-center justify-end gap-3">
        <button
          aria-label="Play"
          className="flex h-10 w-10 items-center justify-center rounded-[10px] bg-[#3cb371] text-white shadow-[0_2px_10px_rgba(60,179,113,0.35)] transition-transform duration-150 hover:scale-105 hover:shadow-[0_4px_14px_rgba(60,179,113,0.45)] active:scale-95"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" stroke="none">
            <polygon points="5 3 19 12 5 21 5 3" />
          </svg>
        </button>
        <button className="flex h-10 items-center gap-2 rounded-[10px] bg-[#1a1816] px-5 text-sm font-medium text-[#f0ede8] shadow-[0_2px_8px_rgba(26,24,22,0.25)] transition-all duration-150 hover:bg-[#2d2a26] hover:shadow-[0_4px_12px_rgba(26,24,22,0.35)] active:scale-[0.97]">
          Export
        </button>
      </div>
    </header>
  );
}
