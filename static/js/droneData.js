//function to create/update a data box for each drone
function updateDroneData(data) {
    const container = document.getElementById('drone-data-container');
    container.innerHTML = ''; //clear container before adding new data

    if (Array.isArray(data)) {
        data.forEach(drone => {
            const box = document.createElement('div');
            box.classList.add('drone-data-box');
            box.innerHTML = `
                <h3 class="drone-title">${drone.call_sign}</h3>
                <div class="drone-info">
                    <p><strong>Latitude:</strong> ${drone.latitude.toFixed(4)}</p>
                    <p><strong>Longitude:</strong> ${drone.longitude.toFixed(4)}</p>
                    <p><strong>Status:</strong> ${drone.status || 'Unknown'}</p>
                    <p><strong>Altitude:</strong> ${drone.altitude || 'N/A'}</p>
                </div>
            `;

            //hover effect for highlighting box when hovered
            box.addEventListener('mouseover', () => {
                box.classList.add('hovered');
            });
            box.addEventListener('mouseout', () => {
                box.classList.remove('hovered');
            });

            //add click event to nav to the specific drone page
            box.addEventListener('click', () => {
                const dronePage = getDronePage(drone.call_sign); //get the page based on callsign
                window.location.href = `/${dronePage}`; //nav to the drones specific page
            });

            //apend the new drone box to the container
            container.appendChild(box);
        });
    }
}

//map drone callsign to the url page(droneA, droneB, etc)
function getDronePage(callSign) {
    const dronePages = {
        'alpha': 'droneA',
        'bravo': 'droneB',
        'charlie': 'droneC',
        'juliet': 'droneJ' //add more drones if needed
    };
    return dronePages[callSign.toLowerCase()] || ''; //default to empty if not found
}

//fetch drone data and update the box
function fetchDroneDataForBoxes() {
    fetch('/drone-data')
        .then(res => res.json())
        .then(data => {
            updateDroneData(data); //update the drone boxes
        })
        .catch(err => console.error("Error fetching drone data for boxes:", err));
}

//fetch and update drone data every 4 seconds
setInterval(fetchDroneDataForBoxes, 4000);
fetchDroneDataForBoxes(); //init fetch
