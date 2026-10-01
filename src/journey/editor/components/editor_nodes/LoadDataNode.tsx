import { Position, Handle } from '@xyflow/react';

export default function LoadData(){
    return (
        <div>
            <p>load data</p>
            <Handle type="source" position={Position.Top}>
                <p>handle</p>
            </Handle>
            <Handle type="target" position={Position.Bottom} />
        </div>
    );
}