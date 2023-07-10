import { useEffect, useState } from "react"

import axios from 'axios'; 

export const ItemList = (props) => {
    const [envConfig, setEnvConfig] = useState(props.envConfig); 
  
    return (
        <div className="my-1 d-flex bg-body-tertiary p-2 px-4 justify-content-between align-items-center pe-auto"
                style={{
                    cursor: "pointer"
                }}>
            <div><strong> Nombre: </strong> {envConfig.name }</div>
            <div>Número de agentes: {envConfig.agents.length }</div>
        </div>
    )
}