import { Handle, Position, useReactFlow } from '@xyflow/react';
import { useEffect, useState } from 'react';
import type { nodeCategory } from '../../journey/editor/types';

async function get_table_names() : Promise<Array<string>> {
    const response = await fetch('http://localhost:8000/SQL/get_all_tables_name', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    const res = await response.json();
    return res.tables;
}

async function get_table_column_names(table_name: string): Promise<Array<string>> {
    const response = await fetch(`http://localhost:8000/SQL/get_table_column_names/${table_name}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    const res = await response.json();
    return res.column_names;
}

async function get_exec_res(node_id: string) {
  const response = await fetch(`http://localhost:8000/workflows/get_exec_res/${node_id}`)
  const res = await response.json()

  return res.exec_res;
}

type NodesDataType = {
    label: string;
    category: nodeCategory;
    modify_ui: (mode: "show" | "hide", uiElement: "panel", data: any) => void;
};

export default function DataBaseNode({id, data}: {id: string, data: NodesDataType}) {
    const [tables, setTables] = useState<string[]>([]);
    const [columns, setColumns] = useState<string[]>([]);
    const [selectedTable, setSelectedTable] = useState<string>('');
    const [selectedColumns, setSelectedColumns] = useState<string[]>([]);
    const { updateNodeData } = useReactFlow();


    async function handle_exec_res() {
      const exec_res = await get_exec_res(id);
      console.log(exec_res)
      data.modify_ui('show', 'panel', exec_res);
    }

    useEffect(() => {
        get_table_names()
            .then((retrieved_tables) => {
                setTables(retrieved_tables);
                if (retrieved_tables.length > 0) {
                    setSelectedTable(retrieved_tables[0]);
                }
            })
            .catch(console.error);
    }, []);

    useEffect(() => {
        if (tables.length > 0) {
            get_table_column_names(tables[0])
                .then(setColumns)
                .catch(console.error);
        }
    }, [tables]);

    useEffect(() => {
        updateNodeData(id, {tableName: selectedTable, columns: selectedColumns});
    }, [selectedTable, selectedColumns, updateNodeData, id]);

    const tables_selection = (
        <>
            <label htmlFor="tables">Choose table:</label>
            <select name="tables" id="tables" value={selectedTable} onChange={(e) => setSelectedTable(e.target.value)}>
                {tables.map((table) =>
                    <option key={table} value={table}>{table}</option>
                )}
            </select>
        </>
    );

    const columns_selection = (
        <>
            <label htmlFor="columns">Choose column:</label>
            <fieldset name="columns" id="columns">
                {columns.map((column) =>
                    <div key={column}>
                        <input type="checkbox" value={column} id={column} checked={selectedColumns.includes(column)} onChange={(e) => {
                            if (e.target.checked) {
                                setSelectedColumns([...selectedColumns, column]);
                            } else {
                                setSelectedColumns(selectedColumns.filter((c) => c !== column));
                            }
                        }} />
                        <label htmlFor={column}>{column}</label>
                    </div>
                )}
            </fieldset>
        </>
    );

    return (
        <div className='bg-white border border-gray-200 rounded-md shadow-sm p-1 min-w-[180px] max-w-[240px]'>
            <div className='flex items-center gap-1 mb-1'>
                <div className='w-1.5 h-1.5 rounded-full bg-blue-400' />
                <span className='text-[10px] font-medium text-gray-800'>Database</span>
            </div>
            <div className='text-[10px] font-medium text-gray-400 uppercase tracking-wider mb-0.5'>Input</div>
            {tables_selection}
            <div className='mt-1 mb-0.5'>
                <div className='text-[10px] font-medium text-gray-400 uppercase tracking-wider mb-0.5'>Columns</div>
                {columns_selection}
            </div>
            <button onClick={() => handle_exec_res()} className='mt-0.5 text-[10px] bg-blue-100 text-blue-700 px-1.5 py-0.5 rounded hover:bg-blue-200'>show exec res</button>
            <Handle type="target" position={Position.Left} />
            <Handle type="source" position={Position.Right} />
        </div>
    );
}
