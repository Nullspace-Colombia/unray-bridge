// Side menu 

import "./Menu.css"

import { ReactComponent as Env } from "../assets/SVG/env.svg";
import { ReactComponent as Agent } from "../assets/SVG/agent.svg";
import { ReactComponent as Train } from "../assets/SVG/train.svg";
import { ReactComponent as Learn } from "../assets/SVG/learn.svg";


export const Menu = () => {
    return (
        <div className="d-flex flex-column justify-content-between align-items-start h-100 pb-5">
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
                <hr />
            </ul>

            <div className="w-100 px-4">
              
                <a href="https://github.com/Nullspace-Colombia/unray-bridge" target="_blank">Support our GH!</a>
                
            </div>
        </div>
    )
}