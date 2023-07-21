// floating button 
import "./FloatingButton.css"


export const FloatingButton = (props) => {
    const clickHandler = () => {
        alert("on click"); 
    }
    return(
        <span className="floatingButton my-1 mx-3" onClick={clickHandler} style = {{
            background: props.Color || "red"
        }}>
            <props.Icon/> 
            
        </span>
    )
}