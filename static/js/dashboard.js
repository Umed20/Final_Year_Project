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
        .then(response => response.json())
        .then(data => {
            // Update Security Status
            document.getElementById('fingerprint-status').textContent = data.security_status.fingerprint;
            document.getElementById('intruder-status').textContent = data.security_status.intruder_detection;
            document.getElementById('theft-status').textContent = data.security_status.theft_detection;
            
            updateStatusDot('fingerprint', data.security_status.fingerprint);
            updateStatusDot('intruder', data.security_status.intruder_detection);
            updateStatusDot('theft', data.security_status.theft_detection);

            // Update Vehicle Status
            document.getElementById('ignition-status').textContent = data.vehicle_status.ignition;
            document.getElementById('brake-status').textContent = data.vehicle_status.brake;
            document.getElementById('towed-status').textContent = data.vehicle_status.towed_status;
            document.getElementById('accident-status').textContent = data.vehicle_status.accident_detection;
            
            updateStatusDot('ignition', data.vehicle_status.ignition);
            updateStatusDot('brake', data.vehicle_status.brake);
            updateStatusDot('towed', data.vehicle_status.towed_status);
            updateStatusDot('accident', data.vehicle_status.accident_detection);

            // Update Safety Metrics
            document.getElementById('alcohol-status').textContent = data.safety_metrics.alcohol_detection;
            document.getElementById('temperature').textContent = data.safety_metrics.temperature;
            document.getElementById('speed-level').textContent = data.safety_metrics.speed_level;
            document.getElementById('gas-status').textContent = data.safety_metrics.gas_detection;
            document.getElementById('light-level').textContent = data.safety_metrics.light_level;
            
            updateStatusDot('alcohol', data.safety_metrics.alcohol_detection);
            updateStatusDot('gas', data.safety_metrics.gas_detection);

            // Update Location
            document.getElementById('location-text').textContent = data.location_data.location_name;
            initMap(data.location_data.latitude, data.location_data.longitude);
        })
        .catch(error => console.error('Error fetching sensor data:', error));
}

// Update dashboard every 5 seconds
updateDashboard();
setInterval(updateDashboard, 5000);