const socket = io();

function updateDeviceTable(devices) {
    const tableBody = document.getElementById("device-table-body");
    tableBody.innerHTML = "";

    devices.forEach(device => {
        const row = document.createElement("tr");

        const infoCell = document.createElement("td");
        infoCell.textContent = device.info.trim();
        row.appendChild(infoCell);

        const busidCell = document.createElement("td");
        busidCell.textContent = device.busid;
        row.appendChild(busidCell);

        const statusCell = document.createElement("td");
        statusCell.textContent = device.bound ? "Bound" : "Unbound";
        statusCell.className = device.bound ? "status-bound" : "status-unbound";
        row.appendChild(statusCell);

        const actionCell = document.createElement("td");
        const button = document.createElement("button");
        button.textContent = device.bound ? "Unbind" : "Bind";
        button.className = device.bound ? "unbind-btn" : "bind-btn";
        button.onclick = () => {
            fetch(`/${device.bound ? "unbind" : "bind"}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ busid: device.busid })
            });
        };
        actionCell.appendChild(button);
        row.appendChild(actionCell);

        tableBody.appendChild(row);
    });
}

socket.on("update", devices => {
    updateDeviceTable(devices);
});

window.onload = () => {
    fetch("/devices")
        .then(res => res.json())
        .then(devices => updateDeviceTable(devices));
};
