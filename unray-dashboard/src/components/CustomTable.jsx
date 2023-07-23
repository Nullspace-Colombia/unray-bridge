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
            return (<th className={`text-start ${e.param == 'name' ? 'w-50' : ''}`}> {e.label} </th>)
        });
        return fieldsElements;
    }

    const getItems = () => {
        const itemsForList = data.map((e, idx) => {
            return (
                <tr key={idx}>
                    <td> <input type="checkbox" /></td>
                    {getFieldsForItem(e, idx)}
                </tr>
            )
        })
        return itemsForList
    }
    const getFieldsForItem = (rowItem, itemId) => {

        // Inner function 
        const typeChecker = (objField) => {
            if("type" in objField){
                switch(objField["type"]){
                    case "dateTime": 
                        const date = new Date(rowItem[objField.param]); 
                        const currentDate = new Date(Date.now()); 
                        let result = new Date(date.getTime() - currentDate.getTime()); 

                        return date.getDate()
                        if(result.getMinutes() < 1){
                            return "less than a minute"; 
                        }if(result.getHours() < 1){
                            return "less than an hour"; 
                        }else{
                            return `${result.getHours()} hours ago`
                        }
                    break; 
                    default: 
                        return "no"
                    break; 
                }
            }else{
                return rowItem[objField.param]; 
            }
        }
        const fieldsElements = fields.map((objField, idx) => {
            return (
                <td className="text-start" key={idx}>
                    { typeChecker(objField) || "-" }
                </td>
            )
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