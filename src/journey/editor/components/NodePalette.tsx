import { useState } from "react";
import { ChevronDown, ChevronRight } from "lucide-react";

export type NodePaletteItem = {
  key: string;
  label: string;
  category: string;
  type: string;
};

type NodePaletteProps = {
  items: Array<NodePaletteItem>;
  onAdd: (key: string) => void;
  open: boolean;
};

export default function NodePalette({ items, onAdd, open }: NodePaletteProps) {
  const grouped = items.reduce<Record<string, Array<NodePaletteItem>>>(
    (acc, item) => {
      const category = item.category.split("/")[0] || "Other";
      if (!acc[category]) acc[category] = [];
      acc[category].push(item);
      return acc;
    },
    {},
  );

  const [expanded, setExpanded] = useState<Record<string, boolean>>(() =>
    Object.fromEntries(Object.keys(grouped).map((key) => [key, true])),
  );

  if (!open) return null;

  return (
    <div className="absolute left-14 top-16 z-40 w-64 max-h-[calc(100vh-8rem)] overflow-auto rounded-2xl border border-[#bbb] bg-white p-3 text-gray-800 shadow-xl">
      <div className="mb-2 text-sm font-semibold text-gray-700">Nodes</div>
      {Object.entries(grouped).map(([category, categoryItems]) => (
        <div key={category} className="mb-2">
          <button
            type="button"
            onClick={() =>
              setExpanded((prev) => ({ ...prev, [category]: !prev[category] }))
            }
            className="flex w-full items-center justify-between rounded-lg px-2 py-1 text-xs font-semibold uppercase tracking-wide text-gray-500 hover:bg-gray-100"
          >
            <span>{category}</span>
            {expanded[category] ? (
              <ChevronDown size={14} />
            ) : (
              <ChevronRight size={14} />
            )}
          </button>

          {expanded[category] && (
            <div className="mt-1 flex flex-col gap-1">
              {categoryItems.map((item) => (
                <button
                  key={item.key}
                  type="button"
                  onClick={() => onAdd(item.key)}
                  className="rounded-xl border border-gray-200 px-3 py-2 text-left text-sm text-gray-800 shadow-sm transition hover:bg-gray-100"
                >
                  <div className="font-medium">{item.label}</div>
                  <div className="text-xs text-gray-500">{item.category}</div>
                </button>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}