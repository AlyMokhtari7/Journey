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
import { Table2, ChartNoAxesColumn } from "lucide-react";
import type { nodeType, edgeType, nodeCategory, DataSetProfile } from "./types";
import DatasetProfile from "./components/DatasetProfile";
import Header from "../../modules/ui/Header";


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
  const [panel_data, setPanelData] = useState(
    "This is the content of the panel.",
  );
  const [showDatasetProfilePanel, setShowDatasetProfilePanel] = useState(false);
  const [datasetProfilePanelData, setDatasetProfilePanelData] = useState<
    string | DataSetProfile
    >("");
  const [isNodeMenuOpen, setIsNodeMenuOpen] = useState(false);

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

  function createNode(data: NodesDataType, type: any = "input") {
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
    modify_ui: (
      mode: "show" | "hide",
      uiElement: "panel" | "DatasetProfile",
      data: any,
    ) => void;
  };

  const nodes_registery: Record<string, { data: NodesDataType; type: string }> =
    {
      // what is Record ?
      CSV: {
        data: {
          label: "load CSV",
          category: "DataLoader/data/loadCSV",
          modify_ui: modifyUI,
        },
        type: "",
      },
      DB: {
        data: {
          label: "selection on DB",
          category: "SQL/Table/Select",
          modify_ui: modifyUI,
        },
        type: "dataBaseNode",
      },
      DBInstance: {
        data: {
          label: "DB instance",
          category: "SQL/DB/GetInstance",
          modify_ui: modifyUI,
        },
        type: "",
      },
      ExecuteQuery: {
        data: {
          label: "Execute Query",
          category: "SQL/ExecuteQuery",
          modify_ui: modifyUI,
        },
        type: "dataBaseExecutionNode",
      },
      SklearnDS: {
        data: {
          label: "Sklearn DS",
          category: "DataLoader/data/SkLearn",
          modify_ui: modifyUI,
        },
        type: "",
      },
      ShowDataInfo: {
        data: {
          label: "Show Data Info",
          category: "DataLoader/show_data_info",
          modify_ui: modifyUI,
        },
        type: "output",
      },
      SKLearnScale: {
        data: {
          label: "Sklearn Scale Data",
          category: "SkLearn/Scale",
          modify_ui: modifyUI,
        },
        type: "",
      },
      SKLearnSplit: {
        data: {
          label: "Sklearn Split Data",
          category: "SkLearn/DataSplit",
          modify_ui: modifyUI,
        },
        type: "",
      },
      SKLearnNormalize: {
        data: {
          label: "Sklearn Normalize Data",
          category: "SkLearn/Normalize",
          modify_ui: modifyUI,
        },
        type: "",
      },
      SKLearnEncode: {
        data: {
          label: "Sklearn Encode Data",
          category: "SkLearn/Encode",
          modify_ui: modifyUI,
        },
        type: "",
      },
      SKLearnDropNA: {
        data: {
          label: "Sklearn Drop NA",
          category: "SkLearn/DropMissingValues",
          modify_ui: modifyUI,
        },
        type: "",
      },
      SKLearnImpute: {
        data: {
          label: "Sklearn Impute Data",
          category: "SkLearn/Impute",
          modify_ui: modifyUI,
        },
        type: "",
      },
    };

  function modifyUI(
    mode: "show" | "hide",
    uiElement: "panel" | "DatasetProfile",
    data: DataSetProfile | any,
  ): void {
    if (mode === "show") {
      if (uiElement === "panel") {
        // show panel
        setShowPanel(true);
        setPanelData(data);
        console.log("show panel");
      } else if (uiElement === "DatasetProfile") {
        setDatasetProfilePanelData(data);
        console.log("data", data);
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

  if (typeof datasetProfilePanelData === "string") {
    panelContent = <p>{datasetProfilePanelData}</p>;
  } else {
    panelContent = <DatasetProfile profile={datasetProfilePanelData} />;
  }


  const reactFlow = (
    <div className="h-full w-full">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        nodeTypes={nodeTypes}
        colorMode="light"
        fitView
      >
        <Background variant="dots" />
      </ReactFlow>
    </div>
  );

  const panel = showPanel && (
    <div className="h-full w-full overflow-auto bg-[#313337] text-[#bfbdb6] p-4">
      <h3>Panel Content</h3>
      <p>{panel_data}</p>
    </div>
  );

  const datasetProfilePanel = showDatasetProfilePanel && (
    <div className="h-full w-full overflow-auto bg-[#313337] text-[#bfbdb6] p-4">
      <h3>Dataset Profile</h3>
      {panelContent}
    </div>
  );

  const nodeSelector = (
    <span className="relative">
      <button
        className="border border-[#3f4043] px-5 py-2 text-sm text-[#bfbdb6] hover:bg-gray-950"
        onClick={() => setIsNodeMenuOpen((open) => !open)}
      >
        + Add Node
      </button>

      {isNodeMenuOpen && (
        <div className="absolute left-0 bottom-full z-50 mt-1 mb-5 min-w-40 border border-[#3f4043] p-1 shadow-lg">
          {Object.entries(nodes_registery).map(([key, value]) => (
            <button
              key={key}
              className="block w-full px-3 py-2 text-left text-sm text-[#bfbdb6] hover:bg-gray-950"
              onClick={() => {
                createNode(value.data, value.type);
                setIsNodeMenuOpen(false);
              }}
            >
              {key}
            </button>
          ))}
        </div>
      )}
    </span>
  );

  return (
    <div className="relative flex h-screen w-screen flex-col overflow-hidden">
      <Header />

      <div className="flex min-h-0 flex-1">
        {/* Sidebar */}
        <aside className="w-12 h-full shrink-0 border-r border-[#bbb]" />

        <main className="flex flex-1 min-h-0">
          <section className={`h-full border-r border-[#3f4043] ${showDatasetProfilePanel ? 'w-1/2' : 'w-full'} flex-grow`}> 
              {reactFlow}
                  </section>
                  <section>
            {reactFlow}
              </section>

          <section className={`h-full min-w-0 overflow-auto flex-grow ${showDatasetProfilePanel ? 'w-1/2' : ''}`}> 
              {datasetProfilePanel}
          </section>

          <section className={`h-full min-w-0 overflow-auto flex-grow ${showPanel ? 'w-1/2' : ''}`}> 
              {panel}
          </section>
        </main>
      </div>

      {/* Status bar */}
      <div className="h-8 w-full shrink-0 border-t border-[#bbb] flex items-center justify-end px-2 gap-2">
        <button
          onClick={() => {
          setShowPanel((s) => {
             const newState = !s;
             console.log('New panel state:', newState);
             return newState;
          });
                  }
                  }
          className="text-[#bfbdb6] hover:text-white p-1"
          title="Toggle panel"
          aria-label="Toggle panel"
        >
          <Table2 color="black" width={16} height={16}/>
        </button>
        <button
          onClick={() => setShowDatasetProfilePanel((s) => !s)}
          className="text-[#bfbdb6] hover:text-white p-1"
          title="Toggle dataset profile"
          aria-label="Toggle dataset profile"
        >
          <ChartNoAxesColumn color="black" width={16} height={16}/>
        </button>
      </div>

      {/* Add Node button */}
      <div className="absolute left-5 bottom-5 z-50">
        {nodeSelector}
      </div>
    </div>
  );

}
