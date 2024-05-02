import React from "react";
import ReactDom from "react-dom";

const navbar = (
    <nav>
        <h1>Bob's Bistro</h1>
        <ul>
            <li>Menu</li>
            <li>About</li>
            <li>Contact</li>
        </ul>
    </nav>
);

console.log(navbar);
console.log(document.getElementById("root"));

ReactDom.render(navbar, document.getElementById("root"));