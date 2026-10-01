export type nodeType = {
    id: string,
    position: { x: number, y: number },
    type?: string,
    data: { label: string }
}

export type edgeType = {
    id: string,
    source: string,
    target: string,
    // type: "smoothstep" | "step",
    type: string,
    label: string
}