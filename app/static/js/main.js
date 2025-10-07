const appState = {
    currentScreen: 'home',
    selectedCategory: null,
    selectedSubcategory: null,
    currentItem: null,
    history: []
};

const screens = {
    loading: document.getElementById('loadingScreen'),
    home: document.getElementById('homeScreen'),
    subcategory: document.getElementById('subcategoryScreen'),
    result: document.getElementById('resultScreen'),
    error: document.getElementById('errorScreen')
};

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    loadCategories();
});

// Initialize Navigation
function initializeApp() {
    document.getElementById('backFromSubcategory').addEventListener('click', goBack);
    document.getElementById('backFromResult').addEventListener('click', goBack);
    document.getElementById('tryAgainBtn').addEventListener('click', reRandomize);
}

async function fetchAPI(endpoint) {
    try {
        showLoading(true);
        const response = await fetch(endpoint);
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        showLoading(false);
        // await new Promise(resolve => setTimeout(resolve, 100));
        return data;
    } catch (error) {
        showLoading(false);
        showError('Failed to load data. Please try again.');
        console.error('API Error:', error);
        return null;
    }
}

async function loadCategories() {
    const data = await fetchAPI('/api/categories');
    if (data && data.categories) {
        const container = document.getElementById('categoryButtons');
        container.innerHTML = '';
        data.categories.forEach(category => {
            const button = createButton(category.display, () => selectCategory(category.id));
            container.appendChild(button);
        });
        showScreen('home');
    }
}

async function selectCategory(categoryId) {
    appState.selectedCategory = categoryId;
    appState.history.push('home');
    const data = await fetchAPI(`/api/subcategories/${categoryId}`);
    if (data && data.subcategories) {
        const container = document.getElementById('subcategoryButtons');
        const title = document.getElementById('categoryTitle');
        title.textContent = categoryId === 'dapur_time' ? 'Pilih Kategori' : 'Pilih Kategori';
        container.innerHTML = '';
        data.subcategories.forEach(sub => {
            const button = createButton(sub.display, () => selectSubcategory(sub.id));
            container.appendChild(button);
        });
        showScreen('subcategory');
    }
}

async function selectSubcategory(subcategoryId) {
    appState.selectedSubcategory = subcategoryId;
    appState.history.push('subcategory');
    await getRandomItem();
}

async function getRandomItem() {
    const { selectedCategory, selectedSubcategory } = appState;
    const data = await fetchAPI(`/api/random-item/${selectedCategory}/${selectedSubcategory}`);
    if (data && data.item) {
        appState.currentItem = data.item;
        displayResult(data.item);
    }
}

function displayResult(item) {
    const img = document.getElementById('resultImage');
    img.src = item.image || '/static/images/placeholder.jpg';
    img.alt = item.name;
    
    // Update title with subcategory display name
    const subcategoryDisplay = appState.selectedSubcategory.replace('_', ' ').split(' ').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
    document.getElementById('resultTitle').textContent = subcategoryDisplay;
    document.getElementById('resultName').textContent = item.name;
    document.getElementById('resultDescription').textContent = item.description || '';

    // Youtube dynamic href
    const recipeBtn = document.getElementById('recipeBtn');
    if (appState.selectedCategory == 'tapau'){
        recipeBtn.style.display = 'none';
    } else {
        recipeBtn.style.display = 'inline-block';
        const searchQuery = `Cara buat ${item.name}`;
        const encodedQuery = encodeURIComponent(searchQuery);
        recipeBtn.href = `https://www.youtube.com/results?search_query=${encodedQuery}`;
        recipeBtn.target = '_blank';    
    }
    
    showScreen('result');
}

async function reRandomize() {
    await getRandomItem();
}

function goBack() {
    if (appState.history.length === 0) return;
    
    const previousScreen = appState.history.pop();
    
    if (previousScreen === 'home') {
        showScreen('home');
        appState.selectedCategory = null;
        appState.selectedSubcategory = null;
    } else if (previousScreen === 'subcategory') {
        showScreen('subcategory');
        appState.selectedSubcategory = null;
    }
}

function showScreen(screenName) {
    Object.values(screens).forEach(screen => {
        if (screen) screen.classList.add('hidden');
    });
    if (screens[screenName]) {
        screens[screenName].classList.remove('hidden');
        appState.currentScreen = screenName;
    }

    // test
    const container = document.querySelector('.container');
    if (screenName === 'result') {
        container.classList.add('result-active');
    } else {
        container.classList.remove('result-active');
    }
}

function showLoading(show) {
    if (show) {
        screens.loading.classList.remove('hidden');
    } else {
        screens.loading.classList.add('hidden');
    }
}

function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    showScreen('error');
}

function createButton(text, onClick) {
    const button = document.createElement('button');
    button.className = 'choice-button';
    button.textContent = text;
    button.addEventListener('click', onClick);
    return button;
}

document.addEventListener('DOMContentLoaded', () => {
    // Handle Image Errors (original and placeholder)
    const img = document.getElementById('resultImage');
    if (img) {
        img.addEventListener('error', function onError() {
            if (this.src.endsWith('/static/images/placeholder.jpg')) {
                this.removeEventListener('error', onError);
                return;
            }
            this.src = '/static/images/placeholder.jpg';
        });
    }
});