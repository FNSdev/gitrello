export class Renderer {
    render(element, html) {
        element.innerHTML = html;

        // TODO it is vulnerable to XSS attacks. Should be removed probably.
        Array.from(element.querySelectorAll("script")).forEach( oldScript => {
            const newScript = document.createElement("script");
            Array.from(oldScript.attributes).forEach(attr => newScript.setAttribute(attr.name, attr.value));
            newScript.appendChild(document.createTextNode(oldScript.innerHTML));
            oldScript.parentNode.replaceChild(newScript, oldScript);
        });
    }
}
