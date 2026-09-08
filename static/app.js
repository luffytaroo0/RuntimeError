// State Management
let allCrops = [];
let currentCategory = 'all';
let cartCount = 0;
let userRole = 'consumer'; // or 'farmer'

// On Page Load
document.addEventListener('DOMContentLoaded', () => {
    fetchCrops();
});

// 1. Fetch crops from Flask API
async function fetchCrops() {
    try {
        const response = await fetch('/api/crops');
        const data = await response.json();
        allCrops = data.crops;
        renderCrops();
    } catch (error) {
        console.error("Error fetching crops:", error);
    }
}

// 2. Render Cards onto the UI (Direct Farmer vs Mandi Price)
function renderCrops() {
    const grid = document.getElementById('cropGrid');
    grid.innerHTML = '';

    const filtered = currentCategory === 'all' 
        ? allCrops 
        : allCrops.filter(c => c.category === currentCategory);

    filtered.forEach(crop => {
        const card = document.createElement('div');
        card.className = "bg-white border border-stone-200 rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition flex flex-col justify-between";
        card.innerHTML = `
            <div>
                <img src="${crop.image}" class="h-40 w-full object-cover">
                <div class="p-4">
                    <div class="flex justify-between items-start">
                        <h4 class="font-bold text-stone-800 text-base">${crop.name}</h4>
                        <span class="text-[10px] bg-stone-100 text-stone-600 px-2 py-0.5 rounded-full">${crop.qty}</span>
                    </div>
                    <p class="text-xs text-stone-500 mt-1"><i class="fa-solid fa-user-check text-emerald-600"></i> ${crop.farmer}</p>
                    
                    <div class="mt-3 p-2 bg-emerald-50 rounded-xl border border-emerald-100 flex justify-between items-center text-xs">
                        <div>
                            <span class="text-stone-400 line-through">₹${crop.mandi_price}/kg</span>
                            <span class="font-bold text-emerald-800 text-sm ml-1">₹${crop.price}/kg</span>
                        </div>
                        <span class="text-[10px] text-emerald-700 font-semibold bg-emerald-100 px-1.5 py-0.5 rounded">Save 30%</span>
                    </div>
                </div>
            </div>
            <div class="p-4 pt-0">
                <button onclick="buyCrop('${crop.name}', '${crop.farmer}', ${crop.price})" class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-semibold py-2 rounded-xl text-xs transition flex items-center justify-center gap-1.5">
                    <i class="fa-solid fa-basket-shopping"></i> Direct Buy
                </button>
            </div>
        `;
        grid.appendChild(card);
    });
}

// 3. Category Filter
function setCategory(cat) {
    currentCategory = cat;
    document.querySelectorAll('.category-btn').forEach(btn => {
        btn.classList.remove('bg-emerald-600', 'text-white');
        btn.classList.add('bg-white', 'text-stone-600');
    });
    event.target.classList.remove('bg-white', 'text-stone-600');
    event.target.classList.add('bg-emerald-600', 'text-white');
    renderCrops();
}

// 4. View Switching (SPA Navigation)
function showView(viewId) {
    document.getElementById('marketplaceView').classList.add('hidden');
    document.getElementById('profileView').classList.add('hidden');
    document.getElementById('ordersView').classList.add('hidden');

    if (viewId === 'marketplace') {
        document.getElementById('marketplaceView').classList.remove('hidden');
    } else if (viewId === 'profile') {
        document.getElementById('profileView').classList.remove('hidden');
    } else if (viewId === 'ordersView') {
        document.getElementById('ordersView').classList.remove('hidden');
    }
}

// 5. Auth Modal Controls
function openAuthModal(role) {
    document.getElementById('authModal').classList.remove('hidden');
}

function closeAuthModal() {
    document.getElementById('authModal').classList.add('hidden');
}

function sendOTP() {
    const aadhaar = document.getElementById('aadhaarInput').value;
    if (!aadhaar) return alert("Please enter Aadhaar ID");
    alert("Simulated OTP sent to registered mobile: 7492");
    document.getElementById('otpInput').value = "7492";
}

function loginUser(role) {
    userRole = role;
    closeAuthModal();
    if (role === 'farmer') {
        showView('profile');
    } else {
        alert("Logged in as Consumer!");
        showView('marketplace');
    }
}

function toggleProfileOrAuth() {
    if (userRole === 'farmer') {
        showView('profile');
    } else {
        openAuthModal('consumer');
    }
}

function handleLogout() {
    userRole = 'consumer';
    alert("Logged out successfully.");
    showView('marketplace');
}

// 6. AI Price & Demand Forecaster
async function runAIForecast() {
    const crop = document.getElementById('newCropName').value;
    if (!crop) return alert("Enter a crop name first!");

    const box = document.getElementById('aiSuggestionBox');
    box.innerText = "Analyzing regional market trends...";

    const res = await fetch('/api/ai-forecast', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ crop_name: crop })
    });
    const data = await res.json();

    document.getElementById('newCropPrice').value = data.recommended_price;
    box.innerHTML = `<strong>Suggested: ₹${data.recommended_price}/kg</strong> | <em>${data.demand_forecast}</em>`;
}

// 7. Add New Crop Listing
async function submitNewCrop() {
    const name = document.getElementById('newCropName').value;
    const price = document.getElementById('newCropPrice').value;
    const qty = document.getElementById('newCropQty').value;
    const category = document.getElementById('newCropCat').value;

    if (!name || !price || !qty) return alert("Please fill all fields");

    const res = await fetch('/api/crops', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, price, qty, category })
    });
    const data = await res.json();

    alert(data.message);
    closeAddCropModal();
    fetchCrops();
    showView('marketplace');
}

function openAddCropModal() {
    document.getElementById('addCropModal').classList.remove('hidden');
}

function closeAddCropModal() {
    document.getElementById('addCropModal').classList.add('hidden');
}

// 8. Buy & Logistics Simulation
async function buyCrop(cropName, farmer, price) {
    cartCount++;
    document.getElementById('cartCount').innerText = cartCount;

    const res = await fetch('/api/orders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ crop_name: cropName, farmer: farmer, price: price })
    });
    const data = await res.json();

    alert(`Order Placed for ${cropName}! Routed directly to ${farmer}.`);
    updateOrdersList(data.order);
}

function updateOrdersList(order) {
    const list = document.getElementById('ordersList');
    const item = document.createElement('div');
    item.className = "p-4 bg-white border border-stone-200 rounded-2xl shadow-sm flex justify-between items-center";
    item.innerHTML = `
        <div>
            <span class="text-xs font-mono font-bold text-emerald-800">${order.order_id}</span>
            <h4 class="font-bold text-stone-800">${order.crop_name}</h4>
            <p class="text-xs text-stone-500">Farmer: ${order.farmer}</p>
        </div>
        <div class="text-right">
            <span class="font-bold text-stone-800 text-sm">₹${order.amount}</span><br>
            <span class="text-[10px] bg-sky-100 text-sky-800 font-semibold px-2 py-0.5 rounded-full">${order.status}</span>
        </div>
    `;
    list.prepend(item);
}

function showInfoModal() {
    alert("Farmer Info:\nName: Sarah Jenkins\nAadhaar: XXXX-XXXX-4812\nFPO: Western UP Agri Cluster");
}