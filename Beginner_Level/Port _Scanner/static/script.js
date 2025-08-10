document.getElementById("scanBtn").addEventListener("click", function () {
    const target = document.getElementById("target").value;
    const startPort = document.getElementById("startPort").value;
    const endPort = document.getElementById("endPort").value;
    const resultsList = document.getElementById("resultsList");

    resultsList.innerHTML = "";
    if (!target) {
        alert("Please enter a target IP or domain.");
        return;
    }

    fetch("/scan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ target, startPort, endPort })
    })
    .then(response => response.json())
    .then(data => {
        const openPorts = data.open_ports;
        for (let port = startPort; port <= endPort; port++) {
            const li = document.createElement("li");
            if (openPorts.includes(parseInt(port))) {
                li.textContent = `Port ${port} is OPEN`;
                li.classList.add("open-port");
            } else {
                li.textContent = `Port ${port} is CLOSED`;
                li.classList.add("closed-port");
            }
            resultsList.appendChild(li);
        }
    })
    .catch(err => {
        console.error(err);
        alert("Error while scanning.");
    });
});
