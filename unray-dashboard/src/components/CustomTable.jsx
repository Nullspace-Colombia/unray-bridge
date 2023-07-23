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
    const [filterQuery, setFilterQuery] = useState(props.filterQuery);


    // Effect Hooks     

    useEffect(() => {
        setData(props.data);
    }, [props.data])

    useEffect(() => {
        setFields(props.fields);
    }, [props.fields])


    useEffect(() => {
        setFilterQuery(props.filterQuery);
    }, [props.filterQuery])


    // Defined Functions 
    const getFields = () => {
        const fieldsElements = fields.map((e, idx) => {
            return (<th className={`text-start ${e.param == 'name' ? 'w-50' : ''}`}> {e.label} </th>)
        });
        return fieldsElements;
    }

    const getItems = () => {


        const filteredData = data.filter(e => !filterQuery || e.name.toLowerCase().includes(filterQuery.toLowerCase()));
        // console.log(test)
        const itemsForList = filteredData.map((e, idx) => {
            return (
                <tr key={idx}>
                    <td>
                        <div class="checkbox-wrapper-30">
                            <span class="checkbox">
                                <input type="checkbox" />
                                <svg>
                                    <use xlinkHref="#checkbox-30" class="checkbox"></use>
                                </svg>
                            </span>
                            <svg xmlns="http://www.w3.org/2000/svg" style={{display:"none"}}>
                                <symbol id="checkbox-30" viewBox="0 0 22 22">
                                    <path fill="none" stroke="currentColor" d="M5.5,11.3L9,14.8L20.2,3.3l0,0c-0.5-1-1.5-1.8-2.7-1.8h-13c-1.7,0-3,1.3-3,3v13c0,1.7,1.3,3,3,3h13 c1.7,0,3-1.3,3-3v-13c0-0.4-0.1-0.8-0.3-1.2" />
                                </symbol>
                            </svg>
                        </div>

                    </td>
                    {getFieldsForItem(e, idx)}
                </tr>
            )
        })
        return itemsForList
    }
    const getFieldsForItem = (rowItem, itemId) => {

        // Inner function 
        const typeChecker = (objField) => {
            if ("type" in objField) {
                switch (objField["type"]) {
                    case "dateTime":
                        const date = new Date(rowItem[objField.param]);
                        const currentDate = new Date(Date.now());
                        let result = new Date(date.getTime() - currentDate.getTime());

                        return date.getDate()
                        if (result.getMinutes() < 1) {
                            return "less than a minute";
                        } if (result.getHours() < 1) {
                            return "less than an hour";
                        } else {
                            return `${result.getHours()} hours ago`
                        }
                        break;
                    default:
                        return "no"
                        break;
                }
            } else {
                return rowItem[objField.param];
            }
        }
        const fieldsElements = fields.map((objField, idx) => {
            return (
                <td className="text-start" key={idx}>
                    {typeChecker(objField) || "-"}
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