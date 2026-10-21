import { useState, useCallback, useEffect } from "react";
import {
  ReactFlow,
  applyNodeChanges,
  applyEdgeChanges,
  Background,
  Controls,
  addEdge,
  type NodeChange,
  type EdgeChange,
} from "@xyflow/react";
import type { nodeType, edgeType, nodeCategory, DataSetProfile } from "./types";
import DatasetProfile from "./components/DatasetProfile";



async function send_workflow(nodes: Array<nodeType>, edges: Array<edgeType>) {
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

  console.log(
    "sending workflow",
    JSON.stringify({
      nodes: nodes,
      edges: edges,
    }),
  );

  const res = await response.json();
  console.log(res);
}

export default function App({
  nodeTypes,
  initialNodes,
  initialEdges,
}: {
  nodeTypes: any;
  initialNodes: Array<nodeType>;
  initialEdges: Array<edgeType>;
}) {
  const [nodes, setNodes] = useState(initialNodes);
  const [edges, setEdges] = useState(initialEdges);
  const [showPanel, setShowPanel] = useState(true);
  const [panel_data, setPanelData] = useState('This is the content of the panel.');
  const [showDatasetProfilePanel, setShowDatasetProfilePanel] = useState(false);
  const [datasetProfilePanelData, setDatasetProfilePanelData] = useState<string | DataSetProfile>('');


  const onNodesChange = useCallback(
    (changes: NodeChange<nodeType>[]) =>
      setNodes((nodesSnapshot) =>
        applyNodeChanges<nodeType>(changes, nodesSnapshot),
      ),
    [],
  );

  const onEdgesChange = useCallback(
    (changes: EdgeChange<edgeType>[]) =>
      setEdges((edgesSnapshot) =>
        applyEdgeChanges<edgeType>(changes, edgesSnapshot),
      ),
    [],
  );

  const onConnect = useCallback(
    (params: any) =>
      setEdges((edgesSnapshot: any) => addEdge(params, edgesSnapshot)),
    [],
  );

  function createNode(
    data: NodesDataType,
    type: any = "input",
  ) {
    const id = crypto.randomUUID();

    setNodes([
      ...nodes,
      {
        id,
        position: { x: 10, y: 10 },
        type,
        data,
      },
    ]);
  }

    type NodesDataType = {
        label: string;
        category: nodeCategory;
        modify_ui: (mode: "show" | "hide", uiElement: "panel" | "DatasetProfile", data: any) => void;
    };

  const nodes_registery: Record<
    string,
    { data: NodesDataType; type: string }
  > = {
    // what is Record ?
    CSV: {
      data: { label: "load CSV", category: "DataLoader/data/loadCSV", modify_ui: modifyUI},
      type: "",
    },
    DB: {
      data: { label: "selection on DB", category: "SQL/Table/Select", modify_ui: modifyUI},
      type: "dataBaseNode",
    },
    DBInstance: {
      data: { label: "DB instance", category: "SQL/DB/GetInstance", modify_ui: modifyUI},
      type: "",
    },
    ExecuteQuery: {
      data: { label: "Execute Query", category: "SQL/ExecuteQuery", modify_ui: modifyUI},
      type: "dataBaseExecutionNode",
    },
    SklearnDS: {
      data: {
        label: "Sklearn DS",
        category: "DataLoader/data/SkLearn",
        modify_ui: modifyUI
      },
      type: "",
    },
    ShowDataInfo: {
      data: {
        label: "Show Data Info",
        category: "DataLoader/show_data_info",
        modify_ui: modifyUI
      },
      type: "output",
    },
    SKLearnScale: {
      data: {
        label: "Sklearn Scale Data",
        category: "SkLearn/Scale",
        modify_ui: modifyUI
      },
      type: "",
    },
    SKLearnSplit: {
      data: {
        label: "Sklearn Split Data",
        category: "SkLearn/DataSplit",
        modify_ui: modifyUI
      },
      type: "",
    },
    SKLearnNormalize: {
      data: {
        label: "Sklearn Normalize Data",
        category: "SkLearn/Normalize",
        modify_ui: modifyUI
      },
      type: "",
    },
    SKLearnEncode: {
      data: {
        label: "Sklearn Encode Data",
        category: "SkLearn/Encode",
        modify_ui: modifyUI
      },
      type: "",
    },
    SKLearnDropNA: {
      data: {
        label: "Sklearn Drop NA",
        category: "SkLearn/DropMissingValues",
        modify_ui: modifyUI
      },
      type: "",
    },
    SKLearnImpute: {
      data: {
        label: "Sklearn Impute Data",
        category: "SkLearn/Impute",
        modify_ui: modifyUI
      },
      type: "",
    },
  };

  function modifyUI(mode: "show" | "hide", uiElement: "panel" | 'DatasetProfile', data: DataSetProfile | any): void {
    if (mode === "show") {
      if (uiElement === "panel") {
        // show panel
        setShowPanel(true);
        setPanelData(data);
        console.log("show panel");
      } else if (uiElement === "DatasetProfile") {
        setDatasetProfilePanelData(data);
        console.log('data',data)
        setShowDatasetProfilePanel(true);
      }
    } else if (mode === "hide") {
      if (uiElement === "panel") {
        // hide panel
        console.log("hide panel");
        setShowPanel(false);
      } else if (uiElement === "DatasetProfile") {
        setShowDatasetProfilePanel(false);
      }
    }
  }

  let panelContent: React.ReactNode;

  if (typeof datasetProfilePanelData === 'string') {
    panelContent = <p>{datasetProfilePanelData}</p>;
  } else {
    panelContent = <DatasetProfile profile={datasetProfilePanelData} />;
  }

  return (
    <>
      <div className="flex">
        <div
          className="bg-amber-100"
          style={{ width: "30vw", height: "100vh" }}
        >
          {Object.entries(nodes_registery).map(([key, value]) => (
            <div key={key} onClick={() => createNode(value.data, value.type)}>
              {key}
            </div>
          ))}
          <hr />
          <div onClick={() => modifyUI("show", "panel", null)}>Show Panel</div>
          <div onClick={() => modifyUI("hide", "panel", null)}>Hide Panel</div>
          <hr />
          <div onClick={() => send_workflow(nodes, edges)}>Save</div>
        </div>
        <div style={{ width: "70vw", height: "100vh" }}>
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            nodeTypes={nodeTypes}
            colorMode="dark"
            fitView
          >
            <Controls />
          </ReactFlow>
        </div>
          {showPanel && (
            <div className="bg-amber-100" style={{ width: "30vw", height: "100vh" }}>
              <div>
                <h3>Panel Content</h3>
              <p>{panel_data}</p>
              </div>
            </div>
        )}
          {showDatasetProfilePanel && (
            <div className="bg-amber-100" style={{ width: "30vw", height: "100vh" }}>
              <div>
              <h3>Dataset Profile</h3>
                {panelContent}
              </div>
            </div>
          )}
      </div>
    </>
  );
}
