const API = "https://kisanconnect-production-1b79.up.railway.app";

// WEATHER
async function getWeather() {
    const location = document.getElementById("cityInput").value;
    if (!location) return alert("Please enter a location name");

    const box = document.getElementById("weatherResult");
    box.style.display = "block";
    box.innerHTML = `<p>⏳ Loading weather...</p>`;

    const res = await fetch(`${API}/weather/${encodeURIComponent(location)}`);
    const data = await res.json();

    if (res.ok) {
        box.innerHTML = `
            <h3>🌤️ ${data.found_location}</h3>
            <p style="color:#666; font-size:13px;">📍 Coordinates: ${data.latitude}, ${data.longitude}</p>
            <p>🌡️ Temperature: <strong>${data.temperature_c}°C</strong> (Feels like ${data.feels_like_c}°C)</p>
            <p>💧 Humidity: <strong>${data.humidity_percent}%</strong></p>
            <p>🌬️ Wind Speed: <strong>${data.wind_speed_ms} m/s</strong></p>
            <p>☁️ Weather: <strong>${data.weather}</strong></p>
            <p style="margin-top:16px; padding:12px; background:#f0fdf4; border-radius:8px;">
                🌾 <strong>Farming Advice:</strong> ${data.advice}
            </p>
        `;
    } else {
        box.innerHTML = `<p class="error">❌ ${data.detail}</p>`;
    }
}

// LOAD ALL CROPS
async function loadCrops() {
    const res = await fetch(`${API}/marketplace/crops`);
    const crops = await res.json();
    displayCrops(crops);
}

// SEARCH CROPS
async function searchCrops() {
    const q = document.getElementById("searchInput").value;
    if (!q) return loadCrops();
    const res = await fetch(`${API}/marketplace/search?q=${q}`);
    const crops = await res.json();
    displayCrops(crops);
}

// DISPLAY CROPS
function displayCrops(crops) {
    const grid = document.getElementById("cropsResult");
    if (!crops || crops.length === 0) {
        grid.innerHTML = `<p class="error">No crops found.</p>`;
        return;
    }
    grid.innerHTML = crops.map(c => `
        <div class="crop-card">
            <h3>🌱 ${c.name}</h3>
            <p>📦 Category: ${c.category}</p>
            <p>⚖️ Quantity: ${c.quantity_kg} kg</p>
            <p>🏅 Quality: ${c.quality}</p>
            <p class="crop-price">₹${c.price_per_kg}/kg</p>
        </div>
    `).join("");
}

// REGISTER FARMER
async function registerFarmer() {
    const data = {
        name: document.getElementById("regName").value,
        phone: document.getElementById("regPhone").value,
        email: document.getElementById("regEmail").value,
        password: document.getElementById("regPassword").value,
        village: document.getElementById("regVillage").value,
        district: document.getElementById("regDistrict").value,
        state: document.getElementById("regState").value,
        land_acres: parseFloat(document.getElementById("regLand").value)
    };

    const box = document.getElementById("registerResult");

    if (!data.name || !data.phone || !data.email || !data.password) {
        box.innerHTML = `<p class="error">❌ Please fill all required fields.</p>`;
        return;
    }

    const res = await fetch(`${API}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    const result = await res.json();

    if (res.ok) {
        box.innerHTML = `<p class="success">✅ Registered successfully! Welcome ${data.name}!</p>`;
    } else {
        box.innerHTML = `<p class="error">❌ ${result.detail}</p>`;
    }
}

// LOGIN FARMER
async function loginFarmer() {
    const data = {
        email: document.getElementById("loginEmail").value,
        password: document.getElementById("loginPassword").value
    };

    const box = document.getElementById("loginResult");

    if (!data.email || !data.password) {
        box.innerHTML = `<p class="error">❌ Please enter email and password.</p>`;
        return;
    }

    const res = await fetch(`${API}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    const result = await res.json();

    if (res.ok) {
        localStorage.setItem("token", result.access_token);
        box.innerHTML = `<p class="success">✅ Login successful! Welcome back!</p>`;
    } else {
        box.innerHTML = `<p class="error">❌ ${result.detail}</p>`;
    }
}

// Load crops on page load
window.onload = loadCrops;