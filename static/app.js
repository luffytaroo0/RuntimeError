// State
let allCrops = [];
let currentCategory = 'Vegetables';

// Category tag color styles
const CATEGORY_STYLES = {
    'Vegetables': 'bg-lime-100 text-lime-800',
    'Fruits': 'bg-rose-100 text-rose-700',
    'Dairy': 'bg-sky-100 text-sky-700',
    'Bakery': 'bg-violet-100 text-violet-700',
    'Beverages': 'bg-emerald-100 text-emerald-700'
};

document.addEventListener('DOMContentLoaded', () => {
    fetchCrops();
    setupCategoryBar();
});

// Fetch crops from Flask API
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

// Render featured produce cards
function renderCrops() {
    const grid = document.getElementById('cropGrid');
    grid.innerHTML = '';

    const filtered = allCrops.filter(c => c.category === currentCategory);

    filtered.forEach(crop => {
        const tagStyle = CATEGORY_STYLES[crop.category] || 'bg-stone-100 text-stone-700';

        const card = document.createElement('div');
        card.className = 'bg-white border border-stone-200 rounded-2xl overflow-hidden hover:shadow-md transition';
        card.innerHTML = `
            <img src="${crop.image}" class="h-44 w-full object-cover" alt="${crop.name}">
            <div class="p-4">
                <span class="inline-block text-[10px] font-bold uppercase tracking-wide px-2 py-1 rounded ${tagStyle}">${crop.category}</span>
                <h4 class="font-bold text-stone-800 mt-2">${crop.name}</h4>
                <p class="text-sm text-stone-600">${crop.price} / ${crop.unit}</p>
                <div class="flex items-center justify-between mt-2">
                    <span class="text-xs text-stone-500 flex items-center gap-1">
                        <i class="fa-solid fa-star text-amber-400"></i> ${crop.rating}
                    </span>
                    <button class="h-7 w-7 flex items-center justify-center rounded-md bg-lime-100 border border-lime-300 text-lime-800 hover:bg-lime-200 transition">
                        <i class="fa-regular fa-bookmark text-xs"></i>
                    </button>
                </div>
            </div>
        `;
        grid.appendChild(card);
    });
}

// Category pill click handling
function setupCategoryBar() {
    const bar = document.getElementById('categoryBar');
    bar.addEventListener('click', (e) => {
        const btn = e.target.closest('.cat-pill');
        if (!btn) return;

        bar.querySelectorAll('.cat-pill').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        currentCategory = btn.dataset.cat;
        renderCrops();
    });
}