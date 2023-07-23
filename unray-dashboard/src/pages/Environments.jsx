import Row from "react-bootstrap/esm/Row";
import Col from "react-bootstrap/esm/Col";
import { Menu } from "../components/Menu";
import Container from "react-bootstrap/esm/Container"
import Table from 'react-bootstrap/Table'
import { CustomTable } from "../components/CustomTable";
import { Alert, Badge } from "react-bootstrap";

import axios from 'axios';
import { useEffect, useState } from "react";

export const Environments = () => {
    // Parameters 
    // TODO: If no param added just the label, the label will be used as the param to search. 
    const ENVS_TABLE_FIELDS = [
        { "label": "ID", "param": "id" },
        { "label": "Name", "param": "name" },
        { "label": "Amount of Agents", "param": "amountOfAgents" },
        { "label": "Created At", "param": "created_at" },
        { "label": "Current", "param": "created_at" },
    ]

    // States 
    const [envData, setEnvData] = useState()

    useEffect(() => {
        setInterval(() => axios.get("http://127.0.0.1:8000/api/envs").then(
            (res) => {
                // console.log(res.data); 
                // console.log(envData)
                try {
                    if (res.data.length != envData.length) {
                        // alert("New data!");
                    }
                }catch{

                }
                setEnvData(res.data)
            }
        ), 500)
    });


    return (
        <Row className=" position-absolute" style={{ height: "100%", width: "100%" }} noGutters={true}>
            {/* Menu Lateral */}
            <Col xs={2} className="bg-dark pt-4" noGutters={true}>
                <Menu />
            </Col>

            <Col noGutters={true}>
                <Container fluid className="text-dark bg-white text-left pt-5 px-4 w-100 position-relative">
                    <article className="text-start mb-4">
                        <h3 ><strong>Environments</strong> <Badge>envs</Badge></h3>
                        <hr />

                        <Alert bsStyle="warning">
                            <strong>What is an environment?</strong> Defines a set of parameters to be extracted from the UE5 scene!
                        </Alert>

                        {/* Search Bar  */}
                        <div className="d-flex">
                            <input type="text" name="" placeholder="search" className="w-25" id="" />
                        </div>
                    </article>

                    {envData ? <div className="">
                        <CustomTable fields={ENVS_TABLE_FIELDS} data={envData} />
                    </div> : "-"}
                </Container>

            </Col>
        </Row>
    )
}
