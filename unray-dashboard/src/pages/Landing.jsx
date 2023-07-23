// Landing.jsx

import "./Landing.css"
import axios from "axios";

import { CustomNav } from "../components/CustomNav"
import { Environments } from "./Environments";
import { useEffect, useState } from "react";

/**
 *  Landing Page
 * 
 *  @author Andrés Morales
 *  
 */

export const Landing = () => {
    // Constants 
    const REST_API_IP = "127.0.0.1"; // Local host 
    const REST_API_PORT = "8000"; // Defined for docker 
    const REFRESH_TIME = 250; // ms 

    // States 
    const [currentEnv, setCurrentEnv] = useState()

    useEffect(() => {
        setInterval(() => axios.get(`http://${REST_API_IP}:${REST_API_PORT}/api/current`).then(
            res => {
                setCurrentEnv(res.data)
            }
        ), REFRESH_TIME)
    }, [])


    return (
        <div className='d-flex flex-column text-light bg-white position-relative overflow-scroll w-100 d-block' style={{ overflowY: "scroll", height: "100vh" }}>
            {/* Custom Nav */}
            <CustomNav currentEnv={currentEnv} />

            {/* Main Section */}
            <section className="position-relative h-100 bg-white">
                <Environments />
            </section>

            <div className="w-100 position-absolute bg-info line-decoration-section d-flex justify-content-end px-5 align-items-center">
                <span>v0.1</span>
            </div>
        </div >

    )
}