let map;
let marker;

function initMap(lat, lng) {
    if (!map) {
        map = L.map('map').setView([lat, lng], 15);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);
        marker = L.marker([lat, lng]).addTo(map);
    } else {
        map.setView([lat, lng], 15);
        marker.setLatLng([lat, lng]);
    }
}

function updateStatusDot(id, status) {
    const dot = document.getElementById(`${id}-dot`);
    if (dot) {
        dot.className = `status-dot ${status === 'ON' || status === 'Pass' ? 'active' : ''}`;
    }
}

function updateDashboard() {
    fetch('/api/sensor-data')
        .then(response => {
            if (!response.ok) throw new Error("No data available");
            return response.json();
        })
        .then(data => {
            document.getElementById('fingerprint-status').textContent = data.security_status.fingerprint;
            document.getElementById('intruder-status').textContent = data.security_status.intruder_detection;
            document.getElementById('theft-status').textContent = data.security_status.theft_detection;

            document.getElementById('ignition-status').textContent = data.vehicle_status.ignition;
            document.getElementById('towed-status').textContent = data.vehicle_status.towed_status;
            document.getElementById('accident-status').textContent = data.vehicle_status.accident_detection;

            document.getElementById('alcohol-status').textContent = data.safety_metrics.alcohol_detection;
            document.getElementById('temperature').textContent = data.safety_metrics.temperature;
            document.getElementById('speed-level').textContent = data.safety_metrics.speed_level;
            document.getElementById('gas-status').textContent = data.safety_metrics.gas_detection;
            document.getElementById('light-level').textContent = data.safety_metrics.light_level;

            document.getElementById('location-text').textContent = data.location_data.location_name;
            initMap(data.location_data.latitude, data.location_data.longitude);
        })
        .catch(error => {
            console.error("Error fetching data:", error);
            document.getElementById('fingerprint-status').textContent = "No Data";
        });
}


// Update dashboard every 5 seconds
updateDashboard();
setInterval(updateDashboard, 5000);