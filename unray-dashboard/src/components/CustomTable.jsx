import { useEffect, useState } from "react"
import Table from "react-bootstrap/Table";

// css 
import "./CustomTable.css";


/**
 * Custom Table
 * 
 * @author Andrés Morales
 */

export const CustomTable = (props) => {
    // states 
    const [fields, setFields] = useState(props.fields);
    const [data, setData] = useState(props.data);

    // Effect Hooks     

    useEffect(() => {
        setData(props.data);
    }, [props.data])

    useEffect(() => {
        setFields(props.fields);
    }, [props.fields])

    // Defined Functions 
    const getFields = () => {
        const fieldsElements = fields.map((e, idx) => {
            return (<th className="text-start"> {e.label} </th>)
        });
        return fieldsElements;
    }

    const getItems = () => {
        const itemsForList = data.map((e, idx) => {
            return (
                <tr>
                    <td> <input type="checkbox" /></td>
                    {getFieldsForItem(e, idx)}
                </tr>
            )
        })
        return itemsForList
    }
    const getFieldsForItem = (rowItem, itemId) => {
        
        console.log(rowItem)
        const fieldsElements = fields.map((e, idx) => {
            return (<td className="text-start">
                { rowItem[e.param] || "-" }
            </td>)
        });
        return fieldsElements;
    }

    return (
        <Table responsive condensed hover >
            <thead>
                <th><input type="checkbox" className="check" name="" id="" /></th>
                {getFields()}
            </thead>
            <tbody>
                {getItems()}
            </tbody>
        </Table>

    )
}