import '@xyflow/react/dist/style.css';
import LoadData from './components/editor_nodes/LoadDataNode';
import Editor from './Editor';
import type { nodeType, edgeType } from './types';
import DataBaseNode from '../../modules/database/DataBaseNode';

const nodeTypes = {
  loadData: LoadData,
  dataBaseNode: DataBaseNode
};

const initialNodes: Array<nodeType> = [
  // {
  //   id: 'n1',
  //   position: { x: 0, y: 0 },
  //   data: { label: 'Node 1' },
  // },
  // {
  //   id: 'n2',
  //   // type: 'loadData',
  //   position: { x: 100, y: 100 },
  //   data: { label: 'Node 2' },
  // },
];

const initialEdges: Array<edgeType> = [
  // {
  //   id: 'n1-n2',
  //   source: 'n1',
  //   target: 'n2',
  //   type: 'smoothstep',
  //   label: 'First-conn'
  // },
];

export default function App() {
  return (
    <>
      <Editor nodeTypes={nodeTypes} initialEdges={initialEdges} initialNodes={initialNodes} />
    </>
  );
}

