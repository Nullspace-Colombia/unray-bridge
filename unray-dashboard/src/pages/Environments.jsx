import Row from "react-bootstrap/esm/Row";
import Col from "react-bootstrap/esm/Col";
import { Menu } from "../components/Menu";
import Form from 'react-bootstrap/Form';
import Modal from 'react-bootstrap/Modal';

import Container from "react-bootstrap/esm/Container"
import Table from 'react-bootstrap/Table'
import { CustomTable } from "../components/CustomTable";
import { Alert, Badge, Button, Card } from "react-bootstrap";
import ProgressBar from 'react-bootstrap/ProgressBar';


// charjs 
import React from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import { faker } from '@faker-js/faker'

import Tab from 'react-bootstrap/Tab';
import Tabs from 'react-bootstrap/Tabs';

import axios from 'axios';
import { useEffect, useState } from "react";


ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);


export const options = {
    responsive: false,

    plugins: {

        legend: {
            position: 'top',
        },
        title: {
            display: true,
            text: 'Accuracy',
        },
    },
};



const labels = new Array(5).fill(0).map((e, idx) => (idx * 25).toString())// ['25', '50', 'March', 'April', 'May', 'June', 'July'];

export const data = {
    labels,
    datasets: [
        {
            label: 'Dataset 1',
            data: labels.map(() => faker.datatype.number({ min: 0, max: 100 })),
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(255, 99, 132, 0.5)',
        }
    ],
};



export const Environments = () => {
    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    // Parameters 
    // TODO: If no param added just the label, the label will be used as the param to search. 
    const ENVS_TABLE_FIELDS = [
        // { "label": "ID", "param": "id" },
        { label: "Name", param: "name" },
        { label: "Amount of Agents", param: "amountOfAgents" },
        { label: "Created At", param: "created_at", type: "dateTime" },
        { label: "Status", param: "status" },
        { "label": "Current", "param": "created_at", type: "dateTime" },
    ]

    // States 
    const [envData, setEnvData] = useState()
    const [filterQuery, setFilterQuery] = useState()

    useEffect(() => {
        setInterval(() => axios.get("http://127.0.0.1:8000/api/envs").then(
            (res) => {
                setEnvData(res.data)
            }
        ), 500)
    });

    // Hooks 
    const setFilter = (e) => {
        const textQuery = e.target.value;
        setFilterQuery(textQuery);
    }


    const trainHandler = () => {

        axios.post("http://localhost:8000/train/start?env=2").then((e) => {
            console.log(e);
        }).catch((e) => {
            alert("none")
        }).finally(console.log("enf"))
    }

    return (
        <Row className=" position-absolute" style={{ height: "100%", width: "100%" }} noGutters={true}>
            {/* Menu Lateral */}
            <Col xs={2} className="bg-dark pt-4" noGutters={true}>
                <Menu />
            </Col>

            <Col noGutters={true}>
                <Container fluid className="text-dark bg-white text-left pt-5 px-4 w-100 position-relative">
                    <article className="text-start mb-4">
                        <div className="d-flex justify-content-between">
                            <h3 ><strong>Environments</strong> <Badge>envs</Badge></h3>
                            <div>
                                <Button variant="outline-success"  onClick={handleShow} >New</Button>{' '}
                                <Button variant="danger" onClick={trainHandler}> Train</Button>{' '}
                            </div>
                        </div>
                        <hr />

                        <Alert bsStyle="warning">
                            <strong>What is an environment?</strong> Defines a set of parameters to be extracted from the UE5 scene!
                        </Alert>

                        <Tabs
                            defaultActiveKey="profile"
                            id="uncontrolled-tab-example"
                            className="mb-3"
                        >
                            <Tab eventKey="home" title="Environments">

                                {/* Search Bar  */}
                                <div className="d-flex">
                                    <input type="text" name="" placeholder="search" className="w-25" id="" onChange={setFilter} />
                                </div>

                                {envData ? <div className="">
                                    <CustomTable fields={ENVS_TABLE_FIELDS} data={envData} filterQuery={filterQuery} />
                                </div> : "-"}
                            </Tab>


                            <Tab eventKey="profile" title="Training">
                                <Row>
                                    <Col>

                                        <Card className="">
                                            <Card.Header>Status</Card.Header>
                                            <Card.Body>
                                                {/* <Card.Title>Status</Card.Title> */}
                                                <h3 className="mb-3"><strong>60%</strong> of training</h3>
                                                <ProgressBar now={60} />

                                            </Card.Body>
                                        </Card>
                                        <Card className="mt-4">
                                            <Card.Header>Ray Dashboard</Card.Header>
                                            <Card.Body>
                                                {/* <Card.Title>Status</Card.Title> */}
                                                Ray includes their own dashboard for resources. <a href="https://localhost:18283" style={{ color: "gray" }}>Ray Dashboard</a>

                                            </Card.Body>
                                        </Card>

                                    </Col>


                                    <Col>
                                        <Card>
                                            <Card.Header>Accuracy</Card.Header>
                                            <Card.Body>

                                                <Line className="container" height={200} width={600} options={options} data={data} />;

                                            </Card.Body>
                                        </Card>
                                    </Col>
                                </Row>



                            </Tab>
                        </Tabs>



                    </article>


                </Container>

            </Col>


            <Modal show={show} onHide={handleClose}
            size="lg"
            aria-labelledby="contained-modal-title-vcenter"
            centered>
                <Modal.Header closeButton>
                    <Modal.Title>Env Creator</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
                            <Form.Label>Env name</Form.Label>
                            <Form.Control
                                type="text"
                                placeholder="gorgeous name"
                                autoFocus
                            />
                        </Form.Group>
                        <Form.Group
                            className="mb-3"
                            controlId="exampleForm.ControlTextarea1"
                        >
                            <Form.Label>Amount of agents</Form.Label>
                            <Form.Control as="input" rows={3} />
                        </Form.Group>
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="danger" onClick={handleClose}>
                        Cancel
                    </Button>
                    <Button variant="success" onClick={handleClose}>
                        Add env
                    </Button>
                </Modal.Footer>
            </Modal>
        </Row>
    )
}
