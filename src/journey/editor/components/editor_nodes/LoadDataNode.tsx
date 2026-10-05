import { Position, Handle } from '@xyflow/react';
import type {nodeCategory} from '../../types'
import styles from './LoadDataNode.module.css'

export default function LoadData(type: nodeCategory){
    return (
        <div className='bg-white rounded-md border-[0.5] p-2'>
            <input type='file'/>
        </div>
    );
}