// Function to send POST requests
async function postData(url, data) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    return response.json();
}

// User Registration Form Submission
document.getElementById('user-registration-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const result = await postData('/register_user', { username, password });
    document.getElementById('user-registration-message').textContent = result.message;
});

// Driver Registration Form Submission
document.getElementById('driver-registration-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const name = document.getElementById('driver-name').value;
    const phone = document.getElementById('driver-phone').value;

    const result = await postData('/register_driver', { name, phone });
    document.getElementById('driver-registration-message').textContent = result.message;
});

// Parcel Creation Form Submission
document.getElementById('parcel-creation-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const user_id = document.getElementById('user-id').value;
    const driver_id = document.getElementById('driver-id').value;
    const pickup_location = document.getElementById('pickup-location').value;
    const dropoff_location = document.getElementById('dropoff-location').value;

    const result = await postData('/create_parcel', { user_id, driver_id, pickup_location, dropoff_location });
    document.getElementById('parcel-creation-message').textContent = result.message;
});

// Parcel Tracking Form Submission
document.getElementById('parcel-tracking-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const parcel_id = document.getElementById('parcel-id').value;

    const response = await fetch(`/track_parcel/${parcel_id}`);
    const result = await response.json();
    if (response.ok) {
        document.getElementById('parcel-tracking-result').textContent = `Status: ${result.status}, Pickup: ${result.pickup_location}, Dropoff: ${result.dropoff_location}`;
    } else {
        document.getElementById('parcel-tracking-result').textContent = result.message;
    }
});