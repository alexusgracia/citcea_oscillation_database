document.addEventListener("DOMContentLoaded", function () {
    const map = L.map('map').setView([20, 0], 2);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    fetch('data.json') // Asegúrate de que el JSON esté accesible desde este path
        .then(response => response.json())
        .then(data => {
            data.data.forEach(point => {
                const marker = L.marker([point.Latitude, point.Longitude]).addTo(map);

                marker.on('click', function () {
                    L.popup()
                        .setLatLng([point.Latitude, point.Longitude])
                        .setContent(`
                            <strong>${point.Ref}</strong><br>
                            <strong>Year:</strong> ${point.Year}<br>
                            <strong>Grid:</strong> ${point.Grid}<br>
                            <strong>Frequency:</strong> ${point["f (Hz)"]} Hz<br>
                            <strong>Duration:</strong> ${point.Duration}
                        `)
                        .openOn(map);

                    L.circle([point.Latitude, point.Longitude], {
                        color: 'blue',
                        fillColor: 'blue',
                        fillOpacity: 0.2,
                        radius: point.Propagation["Total distance"] * 1000 // Convertir km a metros
                    }).addTo(map);
                });
            });
        })
        .catch(error => console.error('Error loading JSON:', error));
});
