// State
let allCrops = [];
let currentCategory = 'Vegetables';
let searchQuery = '';

const CATEGORY_STYLES = {
    'Vegetables': 'bg-lime-100 text-lime-800',
    'Fruits': 'bg-rose-100 text-rose-700',
    'Dairy': 'bg-sky-100 text-sky-700',
    'Seeds': 'bg-violet-100 text-violet-700',
    'Seasonal': 'bg-emerald-100 text-emerald-700'
};

document.addEventListener('DOMContentLoaded', () => {
    fetchCrops();
    setupCategoryBar();
    setupSearch(); 
});

async function fetchCrops() {
    try {
        const response = await fetch('/api/crops');
        const data = await response.json();
        allCrops = data.crops;
        renderCrops();
    } catch (error) {
        console.error('Error fetching crops:', error);
    }
}

function renderCrops() {
    const grid = document.getElementById('cropGrid');
    grid.innerHTML = '';

    // If searching, ignore category. If not searching, use category.
    const filtered = allCrops.filter(c => {
        if (searchQuery !== '') {
            return c.name.toLowerCase().includes(searchQuery.toLowerCase());
        }
        return c.category === currentCategory;
    });

    if (filtered.length === 0) {
        grid.innerHTML = `<p class="col-span-full py-10 text-center text-stone-500 font-medium text-lg">No products found matching your search.</p>`;
        return;
    }

    filtered.forEach(crop => {
        const tagStyle = CATEGORY_STYLES[crop.category] || 'bg-stone-100 text-stone-700';
        const favorableBadge = crop.favorable 
            ? `<span class="ml-2 px-1.5 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-700 uppercase tracking-wide">Favorable</span>` 
            : '';

        const card = document.createElement('a');
        card.href = `/product/${crop.id}`;
        card.className = 'block bg-white border border-stone-200 rounded-2xl overflow-hidden hover:shadow-md transition cursor-pointer';
        card.innerHTML = `
            <img src="${crop.image}" class="h-44 w-full object-cover" alt="${crop.name}">
            <div class="p-4">
                <span class="inline-block text-[10px] font-bold uppercase tracking-wide px-2 py-1 rounded ${tagStyle}">${crop.category}</span>
                <h4 class="font-bold text-stone-800 mt-2">${crop.name}</h4>
                
                <div class="flex items-center mt-1">
                    <p class="text-sm font-medium text-stone-700">${crop.price} / ${crop.unit}</p>
                    ${favorableBadge}
                </div>

                <div class="flex items-center justify-between mt-3">
                    <span class="text-xs text-stone-500 flex items-center gap-1.5">
                        <i class="fa-solid fa-location-dot text-rose-500"></i> ${crop.nearest_farmer_km} km away
                    </span>
                    <button onclick="event.preventDefault(); event.stopPropagation();" class="h-7 w-7 flex items-center justify-center rounded-md bg-lime-100 border border-lime-300 text-lime-800 hover:bg-lime-200 transition">
                        <i class="fa-regular fa-bookmark text-xs"></i>
                    </button>
                </div>
            </div>
        `;
        grid.appendChild(card);
    });
}

// Robust Search Bar logic
function setupSearch() {
    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.getElementById('searchBtn');

    function executeSearch() {
        searchQuery = searchInput.value.trim();
        
        if (searchQuery !== '') {
            // Remove active style from categories when searching globally
            document.querySelectorAll('.cat-pill').forEach(b => b.classList.remove('active'));
            currentCategory = ''; 
        } else {
            // Re-activate Vegetables if search is cleared manually
            const vegPill = document.querySelector('.cat-pill[data-cat="Vegetables"]');
            if (vegPill && !currentCategory) {
                vegPill.classList.add('active');
                currentCategory = 'Vegetables';
            }
        }
        renderCrops();
    }

    if (searchInput) {
        searchInput.addEventListener('input', executeSearch); // Live search as you type
        searchInput.addEventListener('keypress', (e) => {     // Search on Enter
            if (e.key === 'Enter') executeSearch();
        });
    }

    if (searchBtn) {
        searchBtn.addEventListener('click', executeSearch);   // Search on icon click
    }
}

function setupCategoryBar() {
    const bar = document.getElementById('categoryBar');
    bar.addEventListener('click', (e) => {
        const btn = e.target.closest('.cat-pill');
        if (!btn) return;

        // Clear search when a category is clicked
        const searchInput = document.getElementById('searchInput');
        if (searchInput) searchInput.value = '';
        searchQuery = '';

        bar.querySelectorAll('.cat-pill').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        currentCategory = btn.dataset.cat;
        renderCrops();
    });
}