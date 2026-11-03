import { Play, CircleUser } from "lucide-react";

export default function Header() {
    return (
        <header className="relative flex h-12 w-full items-center bg-[#fdfcfb] shadow-[0_1px_0_0_rgba(0,0,0,0.06)]">
            {/* Left: orange square */}
            <div className="flex items-center">
                <div className="h-12 w-12 bg-[#d87551] shadow-[0_2px_8px_rgba(196,106,42,0.3)]" />
            </div>

            {/* Center: title - absolutely centered */}
            <div className="absolute left-1/2 -translate-x-1/2">
                <h1 className="whitespace-nowrap text-[14px] font-medium tracking-[0.01em] text-[#4a4540]">
                    <span className="text-[#949494]">My Project</span>
                    <span className="text-[#c4b8a8]">/</span>
                    <span className="ml-1 text-black">Sample One</span>
                </h1>
            </div>

            {/* Right: actions */}
            <div className="ml-auto mr-4 flex items-center gap-2">
              <span className="text-[13px] mr-2 flex flex-row items-center justify-center"><CircleUser className="mr-2"/><span>User One</span></span>
                <button
                    aria-label="Play"
                    className="flex h-9 w-9 items-center justify-center rounded-lg  text-white border-[#bbb] border-4"
                >
                  <Play color="rgb(52, 165, 91)" fill="rgb(52, 165, 91)"/>
                </button>
                <button className="flex h-9 items-center gap-2 rounded-lg bg-[black] px-8 text-[13px] font-medium text-[#f0ede8] border-[black] border-4">
                  Export
                </button>
            </div>
        </header>
    );
}
