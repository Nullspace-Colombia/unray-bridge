
import Container from 'react-bootstrap/Container';
import "./CustomNav.css"; 
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';


export const CustomNav = (props) => {

    return ( 
        <Navbar expand="lg" className="bg-dark">
        <Container className='text-light'>
          <Navbar.Brand href="#home" className='text-light'>Unray Dashboard</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav" className='text-light'>
            <Nav className="me-auto">
              <Nav.Link href="#home" className='text-light'>envs</Nav.Link>
              <Nav.Link href="#link" className='text-light'>agents</Nav.Link>
              <NavDropdown className='text-light' title="Config" id="basic-nav-dropdown">
                <NavDropdown.Item href="#action/3.1" >set folders</NavDropdown.Item>
                <NavDropdown.Item href="#action/3.2">
                  set config
                </NavDropdown.Item>
                
                <NavDropdown.Divider />
                <NavDropdown.Item href="#action/3.4">
                  Contribute
                </NavDropdown.Item>
              </NavDropdown>
            </Nav>
          </Navbar.Collapse>
          <span className={`selected-environment p-1 ${ props.currentEnv == "-1" ? 'bg-warning' : 'bg-success'} px-5`}>
            {props.currentEnv == "-1" ?  "none" : props.currentEnv}
          </span>
        </Container>

      </Navbar>
    )
}