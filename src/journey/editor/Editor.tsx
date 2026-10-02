import { useState, useCallback, useEffect } from 'react';
import { ReactFlow, applyNodeChanges, applyEdgeChanges, Background, Controls, addEdge, type NodeChange, type EdgeChange } from '@xyflow/react';
import type { nodeType, edgeType } from './types';


async function send_workflow(nodes: Array<nodeType>, edges: Array<edgeType>){
  const response = await fetch("http://127.0.0.1:8000/workflows/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      nodes: nodes,
      edges: edges,
    }),
  });

  const res = await response.json();
  console.log(res)
}

export default function App({nodeTypes, initialNodes, initialEdges}: {nodeTypes: any, initialNodes: Array<nodeType>, initialEdges: Array<edgeType>}) {
  const [nodes, setNodes] = useState(initialNodes)
  const [edges, setEdges] = useState(initialEdges)

  const onNodesChange = useCallback(
    (changes: NodeChange<{ id: string; position: { x: number; y: number; }; data: { label: string; }; }>[]) => setNodes((nodesSnapshot) => applyNodeChanges(changes, nodesSnapshot)),
    [],
  );

  const onEdgesChange = useCallback(
    (changes: EdgeChange<{ id: string; source: string; target: string; type: string; label: string; }>[]) => setEdges((edgesSnapshot) => applyEdgeChanges(changes, edgesSnapshot)),
    [],
  );

  const onConnect = useCallback(
    (params: any) => setEdges((edgesSnapshot: any) => addEdge(params, edgesSnapshot)),
    [],
  );

  function createNode(data: {label: string, category: nodeCategory}, type: "" | "input" | "output" = "input") {
    const id = crypto.randomUUID();

    setNodes([...nodes, {
      id,
      position: { x: 10, y: 10 }, // temporary
      type: type,
      data,
    }])
  }

  type nodeCategory = "DataLoader/data" | "DataLoader/show_data_info" | "DataLoader/aggregate_data" | "DataLoader/data/loadCSV" | "DataLoader/data/loadDB" | "DataLoader/data/SkLearn"

  return (
    <>
      <div className='flex'>
        <div className='bg-amber-100' style={{width: '30vw', height: '100vh'}}>
          <div onClick={() => createNode({label: "new CSV node", category: "DataLoader/data/loadCSV"})}>Add CSV Data</div>
          <div onClick={() => createNode({label: "new DB node", category: "DataLoader/data/loadDB"})}>Add DataBase</div>
          <div onClick={() => createNode({label: "new Sklearn DS node", category: "DataLoader/data/SkLearn"})}>Add sklearn DS</div>
          <div onClick={() => createNode({label: "new Show Data Info node", category: "DataLoader/show_data_info"}, "output")}>Add Show Data Info</div>
          <div onClick={() => createNode({label: "new Aggregate Data node", category: "DataLoader/aggregate_data"}, "")}>Add Aggregate Data</div>
          <div onClick={() => send_workflow(nodes, edges)}>Save</div>
        </div>
        <div style={{ width: '70vw', height: '100vh' }}>
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            nodeTypes={nodeTypes}
            colorMode='dark'
            fitView
          >
            <Controls />
            <Background />
          </ReactFlow>
        </div>
      </div>
    </>
  );
}

