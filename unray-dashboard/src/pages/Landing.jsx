import Container from "react-bootstrap/esm/Container"
import { CustomNav } from "../components/CustomNav"
import { ItemList } from "../components/ItemList"

import axios from 'axios'; 
import { useEffect, useState } from "react";
import { FloatingButton } from "../components/FloatingButton";

import Play  from "../assets/SVG/play.svg"; 

export const Landing =  () => {
    const [envData, setEnvData] = useState()
    const [currentEnv, setCurrentEnv] = useState()
    useEffect(()=> {
        console.log("as")
        setInterval(() =>   axios.get("http://127.0.0.1:8000/api/envs").then(
            (res)=> {
                console.log(res.data)
                setEnvData(res.data)
            }
        ),500); 
      
        
        setInterval(() =>  axios.get("http://127.0.0.1:8000/api/current").then(
            (res)=> {
                console.log(res.data)
                setCurrentEnv(res.data)
            }
        ), 250)
       
        

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
        <div className='text-light bg-body-tertiary position-relative overflow-scroll ' style={{height: "100vh", overflowY: "scroll"}}>
            <CustomNav currentEnv= {currentEnv}/> 
            <Container className="text-dark bg-white text-left mt-5 p-5 w-100 position-relative">
                    <article className="text-start">
                        <h2>Available Environments</h2>
                        <p>Comienza definiendo los entornos que quieras</p>
                    </article>

                {envData ?  <div className="d-flex flex-column">
                    {getItems(envData)}
                    
                </div> : "-"}
            </Container>


            <div className="d-flex flex-column position-fixed mb-2" style={ {right: "0px", bottom: "0px"}}>
                <FloatingButton Color = "blue" icon = {Play} /> 
                <FloatingButton Color = "red" icon = ""/> 
            </div>
        </div>
    )
}