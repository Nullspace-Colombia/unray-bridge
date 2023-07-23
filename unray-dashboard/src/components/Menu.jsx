// Side menu 

import "./Menu.css"

import {ReactComponent as Env}  from "../assets/SVG/env.svg"; 
import {ReactComponent as Agent}  from "../assets/SVG/agent.svg"; 
import {ReactComponent as Train}  from "../assets/SVG/train.svg"; 
import {ReactComponent as Learn}  from "../assets/SVG/learn.svg"; 


export const Menu = () => {
    return (
        <ul className="menu-list">
                <li>
                    <span><Env /></span>
                    <p>Environments </p>
                </li>
                <li>
                    <span><Agent /></span>
                    <p>Agents</p>
                </li>
                <li>
                    <span><Train /></span>
                    <p>training</p>
                </li>
                <li>
                    <span><Learn /></span>
                    <p>Learn</p>
                </li>
                
            </ul>
    )
}