/**
 * CropMind AI - Intelligent Farming Platform
 * Frontend Application with Charts, Maps, and AI Features
 */

// =============================================================================
// CONFIGURATION
// =============================================================================

const API_BASE = '';

// Chart color palette
const COLORS = {
    green: '#10b981',
    blue: '#3b82f6',
    orange: '#f59e0b',
    purple: '#8b5cf6',
    red: '#ef4444',
    cyan: '#06b6d4',
    pink: '#ec4899',
    yellow: '#eab308'
};

// =============================================================================
// NAVIGATION
// =============================================================================

function showPage(pageId) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });

    // Show selected page
    const page = document.getElementById(`page-${pageId}`);
    if (page) {
        page.classList.add('active');
    }

    // Update nav
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
        if (item.dataset.page === pageId) {
            item.classList.add('active');
        }
    });

    // Initialize map if needed
    if (pageId === 'map' && !window.farmMapInitialized) {
        setTimeout(initializeMap, 100);
    }
}

// Initialize navigation
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', () => {
        showPage(item.dataset.page);
    });
});

// =============================================================================
// UTILITIES
// =============================================================================

function showLoading() {
    document.getElementById('loading-overlay').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loading-overlay').classList.add('hidden');
}

function formatDate(date) {
    return new Intl.DateTimeFormat('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(date);
}

function escapeHtml(text) {
    if (typeof text !== 'string') return text;
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// =============================================================================
// API FUNCTIONS
// =============================================================================

async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: { 'Content-Type': 'application/json' }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    const response = await fetch(`${API_BASE}${endpoint}`, options);

    if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
    }

    return response.json();
}

// =============================================================================
// ANIMATED COUNTERS
// =============================================================================

function animateCounter(element, target, duration = 2000) {
    const start = 0;
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);

        // Easing function
        const easeOutQuart = 1 - Math.pow(1 - progress, 4);
        const current = Math.floor(start + (target - start) * easeOutQuart);

        element.textContent = current.toLocaleString();

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

function initializeCounters() {
    const counters = document.querySelectorAll('.metric-value[data-target]');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = parseInt(entry.target.dataset.target);
                animateCounter(entry.target, target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => observer.observe(counter));
}

// =============================================================================
// GAUGE CHARTS
// =============================================================================

function initializeGauges() {
    const gauges = document.querySelectorAll('.gauge');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const gauge = entry.target;
                const value = parseInt(gauge.dataset.value);
                const color = gauge.dataset.color;
                const fill = gauge.querySelector('.gauge-fill');

                // Calculate stroke-dashoffset
                // Circumference = 2 * PI * r = 2 * 3.14159 * 40 = 251.2
                const circumference = 251.2;
                const offset = circumference - (value / 100) * circumference;

                fill.style.stroke = color;
                fill.style.strokeDashoffset = offset;

                observer.unobserve(gauge);
            }
        });
    }, { threshold: 0.5 });

    gauges.forEach(gauge => observer.observe(gauge));
}

// =============================================================================
// CHART.JS CHARTS
// =============================================================================

let yieldChart, envChart, cropChart;

function initializeCharts() {
    // Yield Forecast Chart
    const yieldCtx = document.getElementById('yieldChart');
    if (yieldCtx) {
        yieldChart = new Chart(yieldCtx, {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Actual Yield',
                    data: [4.2, 4.5, 4.3, 4.8, 4.6, 4.9, 5.1],
                    borderColor: COLORS.green,
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    fill: true,
                    tension: 0.4,
                    borderWidth: 3,
                    pointBackgroundColor: COLORS.green,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }, {
                    label: 'Predicted',
                    data: [4.0, 4.3, 4.5, 4.6, 4.8, 5.0, 5.2],
                    borderColor: COLORS.blue,
                    backgroundColor: 'transparent',
                    borderDash: [5, 5],
                    tension: 0.4,
                    borderWidth: 2,
                    pointRadius: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 20
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        min: 3.5,
                        max: 5.5,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        },
                        ticks: {
                            callback: value => value + ' t/ha'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'index'
                }
            }
        });
    }

    // Environmental Conditions Chart
    const envCtx = document.getElementById('envChart');
    if (envCtx) {
        envChart = new Chart(envCtx, {
            type: 'bar',
            data: {
                labels: ['Temp', 'Humidity', 'Soil pH', 'Moisture'],
                datasets: [{
                    label: 'Current',
                    data: [28, 65, 6.5, 45],
                    backgroundColor: [
                        COLORS.orange,
                        COLORS.blue,
                        COLORS.green,
                        COLORS.cyan
                    ],
                    borderRadius: 8,
                    borderSkipped: false
                }, {
                    label: 'Optimal',
                    data: [25, 60, 6.8, 55],
                    backgroundColor: [
                        'rgba(245, 158, 11, 0.3)',
                        'rgba(59, 130, 246, 0.3)',
                        'rgba(16, 185, 129, 0.3)',
                        'rgba(6, 182, 212, 0.3)'
                    ],
                    borderRadius: 8,
                    borderSkipped: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 20
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    // Crop Distribution Chart
    const cropCtx = document.getElementById('cropChart');
    if (cropCtx) {
        cropChart = new Chart(cropCtx, {
            type: 'doughnut',
            data: {
                labels: ['Wheat', 'Rice', 'Maize', 'Cotton', 'Tomatoes', 'Others'],
                datasets: [{
                    data: [30, 25, 15, 12, 10, 8],
                    backgroundColor: [
                        COLORS.green,
                        COLORS.blue,
                        COLORS.orange,
                        COLORS.purple,
                        COLORS.red,
                        COLORS.cyan
                    ],
                    borderWidth: 0,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '65%',
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });

        // Generate legend
        const legendContainer = document.getElementById('cropLegend');
        if (legendContainer) {
            const data = cropChart.data;
            const colors = data.datasets[0].backgroundColor;
            const labels = data.labels;

            legendContainer.innerHTML = labels.map((label, i) => `
                <div class="legend-item">
                    <span class="legend-color" style="background: ${colors[i]};"></span>
                    <span>${label}</span>
                </div>
            `).join('');
        }
    }
}

// =============================================================================
// LEAFLET MAP
// =============================================================================

let farmMap;

function initializeMap() {
    if (window.farmMapInitialized) return;

    const mapContainer = document.getElementById('farmMap');
    if (!mapContainer) return;

    // Initialize map centered on a farm location
    farmMap = L.map('farmMap').setView([28.6139, 77.2090], 14);

    // Add tile layer (OpenStreetMap)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(farmMap);

    // Define farm zones
    const zones = [
        {
            name: 'Zone A - Wheat',
            coords: [[28.618, 77.200], [28.618, 77.210], [28.612, 77.210], [28.612, 77.200]],
            color: '#10b981',
            health: 95
        },
        {
            name: 'Zone B - Rice',
            coords: [[28.612, 77.200], [28.612, 77.210], [28.606, 77.210], [28.606, 77.200]],
            color: '#f59e0b',
            health: 72
        },
        {
            name: 'Zone C - Tomatoes',
            coords: [[28.618, 77.210], [28.618, 77.220], [28.612, 77.220], [28.612, 77.210]],
            color: '#ef4444',
            health: 58
        },
        {
            name: 'Zone D - Maize',
            coords: [[28.612, 77.210], [28.612, 77.220], [28.606, 77.220], [28.606, 77.210]],
            color: '#10b981',
            health: 98
        }
    ];

    // Add zone polygons
    zones.forEach(zone => {
        const polygon = L.polygon(zone.coords, {
            color: zone.color,
            fillColor: zone.color,
            fillOpacity: 0.3,
            weight: 2
        }).addTo(farmMap);

        polygon.bindPopup(`
            <div style="text-align: center; padding: 8px;">
                <strong>${zone.name}</strong><br>
                <span style="color: ${zone.color}; font-size: 24px; font-weight: bold;">${zone.health}%</span><br>
                <small>Health Score</small>
            </div>
        `);
    });

    // Add markers for key points
    const markers = [
        { pos: [28.615, 77.205], icon: '🌾', label: 'Wheat Storage' },
        { pos: [28.609, 77.215], icon: '💧', label: 'Water Tank' },
        { pos: [28.617, 77.215], icon: '🚜', label: 'Equipment Shed' }
    ];

    markers.forEach(m => {
        const customIcon = L.divIcon({
            html: `<div style="font-size: 24px; text-align: center;">${m.icon}</div>`,
            className: 'custom-marker',
            iconSize: [30, 30]
        });

        L.marker(m.pos, { icon: customIcon })
            .addTo(farmMap)
            .bindPopup(`<strong>${m.label}</strong>`);
    });

    window.farmMapInitialized = true;

    // Handle map resize
    setTimeout(() => farmMap.invalidateSize(), 100);
}

// =============================================================================
// DASHBOARD
// =============================================================================

async function loadDashboard() {
    // Set current date
    const dateEl = document.getElementById('current-date');
    if (dateEl) {
        dateEl.textContent = formatDate(new Date());
    }

    // Initialize counters, gauges, and charts
    initializeCounters();
    initializeGauges();
    initializeCharts();

    // Load tips
    try {
        const tipsData = await apiCall('/api/quick/today-tips');
        const tipsContainer = document.getElementById('tips-container');

        if (tipsContainer) {
            tipsContainer.innerHTML = tipsData.tips.map(tip => `
                <div class="tip-item">
                    <span class="tip-icon">${tip.icon}</span>
                    <div class="tip-content">
                        <div class="tip-category">${tip.category}</div>
                        <div class="tip-text">${tip.tip}</div>
                    </div>
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Failed to load tips:', error);
        const tipsContainer = document.getElementById('tips-container');
        if (tipsContainer) {
            tipsContainer.innerHTML = `
                <div class="tip-item">
                    <span class="tip-icon">💡</span>
                    <div class="tip-content">
                        <div class="tip-category">General</div>
                        <div class="tip-text">Check soil moisture before irrigating to avoid overwatering.</div>
                    </div>
                </div>
            `;
        }
    }
}

// =============================================================================
// YIELD PREDICTION
// =============================================================================

document.getElementById('yield-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    showLoading();

    const formData = new FormData(e.target);
    const data = {
        crop: formData.get('crop'),
        farm_area_ha: parseFloat(formData.get('farm_area_ha')),
        temperature: parseFloat(formData.get('temperature')),
        rainfall: parseFloat(formData.get('rainfall')),
        soil_ph: parseFloat(formData.get('soil_ph')),
        irrigation_type: formData.get('irrigation_type'),
        nitrogen: parseFloat(formData.get('nitrogen')),
        phosphorus: parseFloat(formData.get('phosphorus')),
        potassium: parseFloat(formData.get('potassium'))
    };

    try {
        const result = await apiCall('/api/predict/yield', 'POST', data);
        displayYieldResult(result);
    } catch (error) {
        alert('Error predicting yield. Please try again.');
        console.error(error);
    } finally {
        hideLoading();
    }
});

function displayYieldResult(result) {
    const container = document.getElementById('yield-result');
    const content = document.getElementById('yield-result-content');
    const details = result.details;

    content.innerHTML = `
        <div class="result-main">
            <span class="result-icon">🌾</span>
            <div>
                <div class="result-value">${details.yield_per_hectare_tons} tons/ha</div>
                <div class="result-label">Predicted Yield</div>
            </div>
        </div>

        <div class="result-section">
            <h4>Yield Summary</h4>
            <div class="result-grid">
                <div class="result-item">
                    <span class="result-item-label">Crop</span>
                    <span class="result-item-value">${details.crop.charAt(0).toUpperCase() + details.crop.slice(1)}</span>
                </div>
                <div class="result-item">
                    <span class="result-item-label">Total Expected</span>
                    <span class="result-item-value">${details.total_expected_yield_tons} tons</span>
                </div>
                <div class="result-item">
                    <span class="result-item-label">Yield Range</span>
                    <span class="result-item-value">${details.yield_range}</span>
                </div>
                <div class="result-item">
                    <span class="result-item-label">Confidence</span>
                    <span class="result-item-value">${(result.confidence * 100).toFixed(0)}%</span>
                </div>
            </div>
        </div>

        <div class="result-section">
            <h4>Factor Analysis</h4>
            <div class="result-grid">
                <div class="result-item">
                    <span class="result-item-label">Temperature Effect</span>
                    <span class="result-item-value">${(details.factors.temperature_effect * 100).toFixed(0)}%</span>
                </div>
                <div class="result-item">
                    <span class="result-item-label">Rainfall Effect</span>
                    <span class="result-item-value">${(details.factors.rainfall_effect * 100).toFixed(0)}%</span>
                </div>
                <div class="result-item">
                    <span class="result-item-label">Soil pH Effect</span>
                    <span class="result-item-value">${(details.factors.soil_ph_effect * 100).toFixed(0)}%</span>
                </div>
                <div class="result-item">
                    <span class="result-item-label">Irrigation Effect</span>
                    <span class="result-item-value">${(details.factors.irrigation_effect * 100).toFixed(0)}%</span>
                </div>
            </div>
        </div>

        <div class="result-section">
            <h4>Recommendations</h4>
            <ul class="recommendations-list">
                ${details.recommendations.map(rec => `<li>${escapeHtml(rec)}</li>`).join('')}
            </ul>
        </div>
    `;

    container.style.display = 'block';
}

// =============================================================================
// DISEASE DETECTION
// =============================================================================

document.getElementById('disease-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    showLoading();

    const formData = new FormData(e.target);
    const data = {
        crop: formData.get('crop'),
        affected_area_pct: parseFloat(formData.get('affected_area_pct')),
        spot_density: parseFloat(formData.get('spot_density')),
        leaf_color_g: parseInt(formData.get('leaf_color_g')),
        temperature: parseFloat(formData.get('temperature')),
        humidity: parseFloat(formData.get('humidity'))
    };

    try {
        const result = await apiCall('/api/predict/disease', 'POST', data);
        displayDiseaseResult(result);
    } catch (error) {
        alert('Error detecting disease. Please try again.');
        console.error(error);
    } finally {
        hideLoading();
    }
});

function displayDiseaseResult(result) {
    const container = document.getElementById('disease-result');
    const content = document.getElementById('disease-result-content');
    const details = result.details;

    const urgencyClass = `urgency-${details.urgency}`;

    content.innerHTML = `
        <div class="result-main">
            <span class="result-icon">🔬</span>
            <div>
                <div class="result-value">${result.prediction}</div>
                <div class="result-label">
                    <span class="urgency-badge ${urgencyClass}">${details.urgency} urgency</span>
                </div>
            </div>
        </div>

        <div class="result-section">
            <h4>Disease Details</h4>
            <div class="result-grid">
                <div class="result-item">
                    <span class="result-item-label">Severity</span>
                    <span class="result-item-value">${details.severity_label} (${details.severity}/5)</span>
                </div>
                <div class="result-item">
                    <span class="result-item-label">Affected Area</span>
                    <span class="result-item-value">${details.affected_area_pct}%</span>
                </div>
                <div class="result-item">
                    <span class="result-item-label">Confidence</span>
                    <span class="result-item-value">${(result.confidence * 100).toFixed(0)}%</span>
                </div>
                <div class="result-item">
                    <span class="result-item-label">Yield Impact</span>
                    <span class="result-item-value">${details.estimated_yield_impact}</span>
                </div>
            </div>
        </div>

        <div class="result-section">
            <h4>Treatment</h4>
            <div class="result-item" style="display: block; padding: 14px;">
                ${escapeHtml(details.treatment)}
            </div>
        </div>

        <div class="result-section">
            <h4>Prevention Tips</h4>
            <ul class="recommendations-list">
                ${details.prevention_tips.map(tip => `<li>${escapeHtml(tip)}</li>`).join('')}
            </ul>
        </div>
    `;

    container.style.display = 'block';
}

// =============================================================================
// PEST PREDICTION
// =============================================================================

document.getElementById('pest-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    showLoading();

    const formData = new FormData(e.target);
    const data = {
        crop: formData.get('crop'),
        season: formData.get('season'),
        temperature: parseFloat(formData.get('temperature')),
        humidity: parseFloat(formData.get('humidity'))
    };

    try {
        const result = await apiCall('/api/predict/pest', 'POST', data);
        displayPestResult(result);
    } catch (error) {
        alert('Error predicting pest risk. Please try again.');
        console.error(error);
    } finally {
        hideLoading();
    }
});

function displayPestResult(result) {
    const container = document.getElementById('pest-result');
    const content = document.getElementById('pest-result-content');
    const details = result.details;

    content.innerHTML = `
        <div class="result-main">
            <span class="result-icon">🛡️</span>
            <div>
                <div class="result-value">${result.prediction} Risk</div>
                <div class="result-label">
                    Highest risk: ${details.highest_risk_pest}
                </div>
            </div>
        </div>

        <div class="result-section">
            <h4>Pest Risk Scores</h4>
            <div class="result-grid">
                ${Object.entries(details.all_pest_risks).map(([pest, score]) => `
                    <div class="result-item">
                        <span class="result-item-label">${pest}</span>
                        <span class="result-item-value">${(score * 100).toFixed(0)}%</span>
                    </div>
                `).join('')}
            </div>
        </div>

        <div class="result-section">
            <h4>Recommendations</h4>
            <ul class="recommendations-list">
                ${details.recommendations.map(rec => `<li>${escapeHtml(rec)}</li>`).join('')}
            </ul>
        </div>
    `;

    container.style.display = 'block';
}

// =============================================================================
// IRRIGATION
// =============================================================================

document.getElementById('irrigation-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    showLoading();

    const formData = new FormData(e.target);
    const data = {
        crop: formData.get('crop'),
        irrigation_type: formData.get('irrigation_type'),
        soil_moisture: parseFloat(formData.get('soil_moisture')),
        last_irrigation_hours: parseInt(formData.get('last_irrigation_hours')),
        temperature: parseFloat(formData.get('temperature')),
        humidity: parseFloat(formData.get('humidity'))
    };

    try {
        const result = await apiCall('/api/predict/irrigation', 'POST', data);
        displayIrrigationResult(result);
    } catch (error) {
        alert('Error getting irrigation advice. Please try again.');
        console.error(error);
    } finally {
        hideLoading();
    }
});

function displayIrrigationResult(result) {
    const container = document.getElementById('irrigation-result');
    const content = document.getElementById('irrigation-result-content');
    const details = result.details;

    const urgencyClass = `urgency-${details.urgency}`;

    content.innerHTML = `
        <div class="result-main">
            <span class="result-icon">💧</span>
            <div>
                <div class="result-value">${details.action}</div>
                <div class="result-label">
                    <span class="urgency-badge ${urgencyClass}">${details.urgency}</span>
                </div>
            </div>
        </div>

        <div class="result-section">
            <h4>Irrigation Details</h4>
            <div class="result-grid">
                <div class="result-item">
                    <span class="result-item-label">Water Needed</span>
                    <span class="result-item-value">${details.water_amount_mm} mm</span>
                </div>
                <div class="result-item">
                    <span class="result-item-label">Best Time</span>
                    <span class="result-item-value">${details.best_time}</span>
                </div>
                <div class="result-item">
                    <span class="result-item-label">Current Moisture</span>
                    <span class="result-item-value">${details.current_conditions.soil_moisture_pct}%</span>
                </div>
                <div class="result-item">
                    <span class="result-item-label">Optimal Moisture</span>
                    <span class="result-item-value">${details.current_conditions.optimal_moisture_pct}%</span>
                </div>
            </div>
        </div>

        <div class="result-section">
            <h4>Water Saving Tips</h4>
            <ul class="recommendations-list">
                ${details.water_saving_tips.map(tip => `<li>${escapeHtml(tip)}</li>`).join('')}
            </ul>
        </div>
    `;

    container.style.display = 'block';
}

// =============================================================================
// MARKET PRICES
// =============================================================================

document.getElementById('market-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    showLoading();

    const formData = new FormData(e.target);
    const data = {
        commodity: formData.get('commodity'),
        days_ahead: parseInt(formData.get('days_ahead'))
    };

    try {
        const result = await apiCall('/api/predict/price', 'POST', data);
        displayMarketResult(result);
    } catch (error) {
        alert('Error predicting price. Please try again.');
        console.error(error);
    } finally {
        hideLoading();
    }
});

function displayMarketResult(result) {
    const container = document.getElementById('market-result');
    const content = document.getElementById('market-result-content');
    const details = result.details;

    const sentimentColors = {
        'Bullish': 'color: #10b981',
        'Bearish': 'color: #ef4444',
        'Neutral': 'color: #64748b'
    };

    content.innerHTML = `
        <div class="result-main">
            <span class="result-icon">📈</span>
            <div>
                <div class="result-value">₹${details.predicted_price_per_quintal}</div>
                <div class="result-label">per quintal (${details.commodity})</div>
            </div>
        </div>

        <div class="result-section">
            <h4>Price Details</h4>
            <div class="result-grid">
                <div class="result-item">
                    <span class="result-item-label">Price Range</span>
                    <span class="result-item-value">${details.price_range}</span>
                </div>
                <div class="result-item">
                    <span class="result-item-label">Prediction Period</span>
                    <span class="result-item-value">${details.prediction_period_days} days</span>
                </div>
                <div class="result-item">
                    <span class="result-item-label">Market Sentiment</span>
                    <span class="result-item-value" style="${sentimentColors[details.market_sentiment]}">${details.market_sentiment}</span>
                </div>
                <div class="result-item">
                    <span class="result-item-label">Confidence</span>
                    <span class="result-item-value">${(result.confidence * 100).toFixed(0)}%</span>
                </div>
            </div>
        </div>

        <div class="result-section">
            <h4>Recommendation</h4>
            <div class="result-item" style="display: block; padding: 14px;">
                💡 ${escapeHtml(details.recommendation)}
            </div>
        </div>
    `;

    container.style.display = 'block';
}

// =============================================================================
// CHATBOT
// =============================================================================

const chatMessages = document.getElementById('chat-messages');
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');

chatForm?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const message = chatInput.value.trim();
    if (!message) return;

    // Add user message
    addChatMessage('user', message);
    chatInput.value = '';

    // Get bot response
    try {
        const result = await apiCall('/api/chat', 'POST', { message });
        addChatMessage('bot', result.response);
    } catch (error) {
        addChatMessage('bot', 'Sorry, I encountered an error. Please try again.');
        console.error(error);
    }
});

function addChatMessage(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${role}`;

    const avatar = role === 'user' ? '👤' : '🤖';
    const avatarClass = role === 'bot' ? 'bot-avatar' : '';

    // Convert markdown-like formatting
    let formattedContent = content
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n/g, '<br>')
        .replace(/• /g, '&bull; ');

    messageDiv.innerHTML = `
        <div class="message-avatar ${avatarClass}">${avatar}</div>
        <div class="message-content">
            <div class="message-text">${formattedContent}</div>
        </div>
    `;

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Suggestion chips
document.querySelectorAll('.suggestion-chip').forEach(chip => {
    chip.addEventListener('click', () => {
        if (chatInput) {
            chatInput.value = chip.dataset.text;
            chatForm.dispatchEvent(new Event('submit'));
        }
    });
});

// =============================================================================
// INITIALIZATION
// =============================================================================

document.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
});

// Make showPage available globally for onclick handlers
window.showPage = showPage;
