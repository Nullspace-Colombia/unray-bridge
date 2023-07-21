import { useEffect, useState } from "react"
import "./ItemList.css"; 
import axios from 'axios'; 
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Container from "react-bootstrap/esm/Container";



export const ItemList = (props) => {
    const [envConfig, setEnvConfig] = useState(props.envConfig); 
    const [itemHeight, setItemHeight] = useState(false); 

    const onClickHandler = () => {
        setItemHeight(!itemHeight); 
    }

    return (
        <Container fluid className={`my-1  bg-body-tertiary p-2 px-4 justify-content-between align-items-center pe-auto ${itemHeight ? "selectedItem" : "notSelectedItem"}`}
        
        onClick={ onClickHandler }
                style={{
                    cursor: "pointer",
                    // height: itemHeight ? "300px" : "2.5rem", 
                    height: "fit-content",
                    transition: "0.6s ease"
                }}>
            <Row>
                <Col style={{textAlign: "left"}}><strong> Nombre: </strong> {envConfig.name }</Col>
                <Col style={{textAlign: "right"}}>Número de agentes: {envConfig.agents.length }</Col>
            </Row>
           
            <Row className="py-4"  style={{
                    cursor: "pointer",
                    // height: itemHeight ? "300px" : "2.5rem", 
                    display:  itemHeight ? "block" : "none",
                    transition: "2s ease"
                }}>
             
             <  Col> Lorem ipsum dolor sit amet consectetur adipisicing elit. Suscipit, numquam maiores molestiae perspiciatis magnam non in, ea nisi, doloremque libero provident reprehenderit voluptatem sapiente unde dolore fugiat quam voluptate tempore! </Col>
             
             </Row>
             
        </Container>
    )
}