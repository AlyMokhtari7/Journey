export default function Header() {
  return (
    <header className="flex h-16 w-full items-center bg-[#f8f6f3] px-6 shadow-[0_1px_0_0_rgba(0,0,0,0.05)]">
      {/* Left: accent + title */}
      <div className="flex w-1/3 items-center gap-4">
        <div className="h-10 w-10 shrink-0 rounded-md bg-[#c46a2a] shadow-[0_2px_8px_rgba(196,106,42,0.35)]" />
        <div className="flex flex-col">
          <span className="text-[11px] font-medium uppercase tracking-[0.12em] text-[#8a8178]">
            My Project
          </span>
          <span className="text-sm font-semibold leading-none text-[#2d2a26] tracking-tight">
            Sample One
          </span>
        </div>
      </div>

      {/* Center: breadcrumb */}
      <nav aria-label="Breadcrumb" className="flex w-1/3 justify-center items-center gap-2.5 text-sm font-medium text-[#6b6358]">
        <span className="text-[#2d2a26]">My Project</span>
        <span className="text-[#c4b8a8]">/</span>
        <span>Sample One</span>
      </nav>

      {/* Right: actions */}
      <div className="flex w-1/3 justify-end items-center gap-3">
        <button
          aria-label="Play"
          className="flex h-10 w-10 items-center justify-center rounded-xl bg-[#3cb371] text-white shadow-[0_2px_10px_rgba(60,179,113,0.35)] transition-transform duration-150 hover:scale-105 hover:shadow-[0_4px_14px_rgba(60,179,113,0.45)] active:scale-95"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" stroke="none">
            <polygon points="5 3 19 12 5 21 5 3" />
          </svg>
        </button>
        <button className="flex h-10 items-center gap-2 rounded-xl bg-[#1a1816] px-4 text-sm font-medium text-[#f0ede8] shadow-[0_2px_8px_rgba(26,24,22,0.25)] transition-all duration-150 hover:bg-[#2d2a26] hover:shadow-[0_4px_12px_rgba(26,24,22,0.35)] active:scale-[0.97]">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <polyline points="7 10 12 15 17 10" />
            <line x1="12" x2="12" y1="15" y2="3" />
          </svg>
          Export
        </button>
      </div>
    </header>
  );
}
