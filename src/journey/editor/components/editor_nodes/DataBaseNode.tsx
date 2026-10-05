import { Position, Handle } from '@xyflow/react';
import type {nodeCategory} from '../../types'
import styles from './LoadDataNode.module.css'
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

async function load_data(table_name: string, columns: Array<string>): Promise<Array<any>> {
    await fetch(`http://localhost:8000/SQL/execute_query/${table_name}/${columns}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });
}

export default function LoadData(type: nodeCategory){

    const [tables, setTables] = useState<string[]>([]);
    const [columns, setColumns] = useState<string[]>([]);

    useEffect(() => {
        get_table_names()
            .then(setTables)
            .catch(console.error);
    }, []);

    useEffect(() => {
        if (tables.length > 0) {
            get_table_column_names(tables[0])
                .then(setColumns)
                .catch(console.error);
        }
    }, [tables]);

    const tables_selection = (
        <>
            <label htmlFor="tables">Choose table:</label>
            <select name="tables" id="tables">
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
                        <input type="checkbox" value={column} id={column} />
                        <label htmlFor={column}>{column}</label>
                    </div>
                )}        
            </fieldset>
        </>
    );

    function handleLoadData() {
        load_data(tables[0], columns)
    }

    return (
        <div className='bg-white rounded-md border-[0.5] p-2'>
            {tables_selection}
            <br/>
            {columns_selection}
            <br/>
            <button onClick={handleLoadData}>Load Data</button>
        </div>
    );
}