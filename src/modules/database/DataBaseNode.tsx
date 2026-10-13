import { Handle, Position, useReactFlow } from '@xyflow/react';
import { useEffect, useState } from 'react';

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

export default function DataBaseNode({id}: {id: string}) {
    const [tables, setTables] = useState<string[]>([]);
    const [columns, setColumns] = useState<string[]>([]);
    const [selectedTable, setSelectedTable] = useState<string>('');
    const [selectedColumns, setSelectedColumns] = useState<string[]>([]);
    const {updateNodeData} = useReactFlow();

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
        <div className='bg-white rounded-md border-[0.5] p-2'>
            {tables_selection}
            <br/>
            {columns_selection}
            <br />
            <Handle type="source" position={Position.Bottom} />
        </div>
    );
}
