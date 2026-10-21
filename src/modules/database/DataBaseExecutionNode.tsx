import { Handle, Position, useReactFlow } from '@xyflow/react';
import { useEffect, useState } from 'react';
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
    const { updateNodeData } = useReactFlow();


    async function handle_exec_res() {
      const exec_res: DataSetProfile = await get_exec_res(id);
      console.log(exec_res)
      data.modify_ui('show', 'DatasetProfile', exec_res);
    }

    return (
        <div className='bg-white rounded-md border-[0.5] p-2'>
          <Handle type="target" position={Position.Top} />
          <Handle type="source" position={Position.Bottom} />

        <br />
        <button onClick={() => handle_exec_res()}>show exec res</button>
        </div>
    );
}
