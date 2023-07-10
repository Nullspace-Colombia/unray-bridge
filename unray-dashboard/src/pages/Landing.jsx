import Container from "react-bootstrap/esm/Container"
import { CustomNav } from "../components/CustomNav"
import { ItemList } from "../components/ItemList"

import axios from 'axios'; 
import { useEffect, useState } from "react";

export const Landing =  () => {
    const [envData, setEnvData] = useState()
    useEffect(()=> {
        console.log("as")
        axios.get("http://127.0.0.1:5000/api/envs").then(
            (res)=> {
                console.log(res.data)
                setEnvData(res.data)
            }
        )

    }, [])

    const getItems = (envData) => {
        console.log(envData)
        let a = envData.map((e)=>{
            return (<ItemList envConfig = {e}/>)
        })
        console.log(a)
        return a; 
    }
    return (
        <div className='text-light bg-body-tertiary position-relative overflow-hidden ' style={{height: "100vh"}}>
            <CustomNav/> 
            <Container className="text-dark bg-white text-left  h-100 p-5 w-100">
                    <article className="text-start">
                        <h2>Unray Dashboard</h2>
                        <p>Comienza definiendo los entornos que quieras</p>
                    </article>

                {envData ?  <div className="d-flex flex-column">
                    {getItems(envData)}
                    
                </div> : "-"}
            </Container>
        </div>
    )
}