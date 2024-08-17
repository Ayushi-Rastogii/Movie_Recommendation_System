        window.onload= function() {
    fetch('/api/data')  // Fetching data from the correct API endpoint
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {

            const select = document.querySelector("#ret");
            data.forEach(item => {
                const option = document.createElement('option');
                option.value = item.title;
                option.textContent = item.title;
                select.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching data:', error));
}
        document.getElementById('ret').addEventListener('focus', function() {
            this.style.zIndex = 1000; // Make sure dropdown is above other elements
        });

function getRecommendation() {
    // Get the selected movie from the select box
    const movie = document.getElementById('ret').value;
    // Prepare the data to be sent to the server
    const requestData = { movie: movie };

    // Send the POST request to the server
    fetch('/recommend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Read and return the entire response as text
        return response.text();
    })
    .then(data => {
        // Parse the data into a JSON object
        const parsedData = JSON.parse(data);

        // Update the posters with the new data
        for (let i = 0; i < parsedData.length; i++) {
            const poster = document.getElementById(`poster${i + 1}`);
            if (poster && parsedData[i]) {
                poster.src = parsedData[i].url;
                poster.alt = parsedData[i].title;
            }
        }
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}
