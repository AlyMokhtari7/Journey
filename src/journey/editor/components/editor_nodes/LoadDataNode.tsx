
import { Handle, Position } from '@xyflow/react';

export default function LoadData(){
    return (
        <div className='bg-white border border-gray-200 rounded-md shadow-sm p-1 min-w-[160px] max-w-[200px]'>
            <div className='flex items-center gap-1 mb-1'>
                <div className='w-1.5 h-1.5 rounded-full bg-blue-400' />
                <span className='text-[10px] font-medium text-gray-800'>Load Data</span>
            </div>
            <div className='text-[10px] font-medium text-gray-400 uppercase tracking-wider mb-0.5'>Input</div>
            <input type='file' className='text-[10px] w-full'/>
            <Handle type="target" position={Position.Left} />
            <Handle type="source" position={Position.Right} />
        </div>
    );
}