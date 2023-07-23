
import Container from 'react-bootstrap/Container';
import "./CustomNav.css"; 
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';


export const CustomNav = (props) => {

    return ( 
        <Navbar expand="lg" className="w-100" style = {{ background: "#000000", height: "40px", position: "static", zIndex: "2000"}}>
        <Container className='text-light'>
          <Navbar.Brand href="#home" className='text-light brand-text'>Unray Dashboard</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
        </Container>

      </Navbar>
    )
}