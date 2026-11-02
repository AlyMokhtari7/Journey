import { Handle, Position } from '@xyflow/react';

import type { DataSetProfile, nodeCategory } from '../../journey/editor/types';

async function get_exec_res(node_id: string) {
  const response = await fetch(`http://localhost:8000/workflows/get_exec_res/${node_id}`)
  const res = await response.json()

  // console.log(typeof(res))
  // console.log(res.exec_res)

  return res.exec_res;
}

type NodesDataType = {
    label: string;
    category: nodeCategory;
    modify_ui: (mode: "show" | "hide", uiElement: "panel" | "DatasetProfile", data: DataSetProfile | any) => void;
};

export default function DataBaseExecutionNode({id, data}: {id: string, data: NodesDataType}) {



    async function handle_exec_res() {
      const exec_res: DataSetProfile = await get_exec_res(id);
      console.log(exec_res)
      data.modify_ui('show', 'DatasetProfile', exec_res);
    }

    return (
        <div className='bg-white border border-gray-200 rounded-md shadow-sm p-1 min-w-[160px] max-w-[200px]'>
            <div className='flex items-center gap-1 mb-1'>
                <div className='w-1.5 h-1.5 rounded-full bg-orange-400' />
                <span className='text-[10px] font-medium text-gray-800'>DB Execution</span>
            </div>
            <div className='text-[10px] font-medium text-gray-400 uppercase tracking-wider mb-0.5'>Logic</div>
            <button onClick={() => handle_exec_res()} className='w-full text-[10px] bg-orange-100 text-orange-700 px-1.5 py-0.5 rounded hover:bg-orange-200'>show exec res</button>
            <Handle type="target" position={Position.Left} />
            <Handle type="source" position={Position.Right} />
        </div>
    );
}
