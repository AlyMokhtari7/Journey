import { useState, useCallback, useRef } from "react";
import {
  ReactFlow,
  applyNodeChanges,
  applyEdgeChanges,
  addEdge,
  type NodeChange,
  type EdgeChange,
} from "@xyflow/react";
import type { nodeType, edgeType, nodeCategory, DataSetProfile } from "./types";
import {
  MousePointer2,
  Hand,
  ZoomIn,
  ZoomOut,
  Maximize2,
  Undo2,
  Redo2,
  Trash2,
  Save,
  Play,
  PanelRight,
  Settings,
  Plus,
} from "lucide-react";


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
  const [, setShowPanel] = useState(true);
  const [, setPanelData] = useState(
    "This is the content of the panel.",
  );
  const [, setShowDatasetProfilePanel] = useState(false);
  const [, setDatasetProfilePanelData] = useState<
    string | DataSetProfile
    >("");
  const [isNodeMenuOpen, setIsNodeMenuOpen] = useState(false);
  const rfInstance = useRef<any>(null);

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
         onInit={(instance: any) => {
           rfInstance.current = instance;
         }}

      >
        {/*<Controls />*/}
      </ReactFlow>
    </div>
  );

  // ------------------------------------- main visible ui code --------------------------------------

  const nodeSelector = (
    <span className="relative">
      <button
        className="border border-[#3f4043] px-5 py-2 text-sm"
        onClick={() => setIsNodeMenuOpen((open) => !open)}
      >
        + Add Node
      </button>

      {isNodeMenuOpen && (
        <div className="absolute left-0 bottom-full z-50 mt-1 mb-5 min-w-40 border border-[#3f4043] p-1 shadow-lg">
          {Object.entries(nodes_registery).map(([key, value]) => (
            <button
              key={key}
              className="block w-full px-3 py-2 text-left text-sm"
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

  const deleteSelected = () => {
    const selectedNodeIds = new Set(
      nodes.filter((n: any) => n.selected).map((n: any) => n.id),
    );
    setNodes((prev: any) =>
      prev.filter((n: any) => !selectedNodeIds.has(n.id)),
    );
    setEdges((prev: any) =>
      prev.filter(
        (e: any) =>
          !selectedNodeIds.has(e.source) && !selectedNodeIds.has(e.target),
      ),
    );
  };

  const saveWorkflow = () => {
    send_workflow(nodes, edges);
  };

  const runWorkflow = () => {
    send_workflow(nodes, edges);
  };

  const toolbarButtonClass =
    "flex h-10 w-10 items-center justify-center rounded-md text-gray-700 hover:bg-gray-100 focus:outline-none";

  const toolbar = (
    <div className="flex h-full w-full flex-col items-center gap-1 py-2">
      <button
        className={toolbarButtonClass}
        title="Select"
        onClick={() => rfInstance.current?.project?.({ x: 0, y: 0 })}
      >
        <MousePointer2 size={18} />
      </button>
      <button className={toolbarButtonClass} title="Pan">
        <Hand size={18} />
      </button>
      <div className="my-1 h-px w-8 bg-gray-300" />
      <button
        className={toolbarButtonClass}
        title="Zoom in"
        onClick={() => rfInstance.current?.zoomIn?.()}
      >
        <ZoomIn size={18} />
      </button>
      <button
        className={toolbarButtonClass}
        title="Zoom out"
        onClick={() => rfInstance.current?.zoomOut?.()}
      >
        <ZoomOut size={18} />
      </button>
      <button
        className={toolbarButtonClass}
        title="Fit view"
        onClick={() => rfInstance.current?.fitView?.()}
      >
        <Maximize2 size={18} />
      </button>
      <div className="my-1 h-px w-8 bg-gray-300" />
      <button className={toolbarButtonClass} title="Undo">
        <Undo2 size={18} />
      </button>
      <button className={toolbarButtonClass} title="Redo">
        <Redo2 size={18} />
      </button>
      <div className="my-1 h-px w-8 bg-gray-300" />
      <button
        className={toolbarButtonClass}
        title="Delete selected"
        onClick={deleteSelected}
      >
        <Trash2 size={18} />
      </button>
      <button
        className={toolbarButtonClass}
        title="Add node"
        onClick={() => setIsNodeMenuOpen((open) => !open)}
      >
        <Plus size={18} />
      </button>
      <div className="my-1 h-px w-8 bg-gray-300" />
      <button
        className={toolbarButtonClass}
        title="Save workflow"
        onClick={saveWorkflow}
      >
        <Save size={18} />
      </button>
      <button
        className={toolbarButtonClass}
        title="Run workflow"
        onClick={runWorkflow}
      >
        <Play size={18} />
      </button>
      <div className="my-1 h-px w-8 bg-gray-300" />
      <button
        className={toolbarButtonClass}
        title="Toggle panel"
        onClick={() => setShowPanel((s) => !s)}
      >
        <PanelRight size={18} />
      </button>
      <button className={toolbarButtonClass} title="Settings">
        <Settings size={18} />
      </button>
    </div>
  );

  const header = (<>
    <div className="flex">
      <span>Journey</span>
      <span>My Projects</span><span>/</span><span>Main</span>
    </div>
  </>);

  return (
    <div className="relative h-screen w-screen overflow-hidden">
      {/* Add Node button */}
      <div className="absolute left-5 bottom-5 z-50">
        {nodeSelector}
      </div>

      <div className="flex h-full w-full flex-col">
        {/* Navbar */}
        <header className="h-12 shrink-0 border-b border-[#3f4043]" >{header}</header>

        {/* Main workspace */}
        <main className="flex min-h-0 flex-1">
          <section className="h-full w-14 border-r border-[#3f4043]">{toolbar}</section>

          <section className="h-full w-full min-w-0 border-r border-[#3f4043]">
            {reactFlow}
          </section>

          {/*<section className="h-full w-1/2 min-w-0 overflow-auto">
            {showDatasetProfilePanel
              ? datasetProfilePanel
              : showPanel
                ? panel
                : null}
          </section>*/}
        </main>
      </div>
    </div>
  );

}
