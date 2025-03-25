/**
 * Laptop Comparison Page JavaScript
 * Handles the dynamic comparison features and chart generation.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Enable tooltips
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => {
        new bootstrap.Tooltip(tooltip);
    });
    
    // Handle highlighting best specs
    highlightBestSpecs();
    
    // Initialize comparison charts
    initPerformanceChart();
    initPricePerformanceChart();
    
    // Add to comparison functionality
    setupComparisonButtons();
});

/**
 * Highlights the best specification in each row of the comparison table
 */
function highlightBestSpecs() {
    const specRows = document.querySelectorAll('.spec-row');
    
    specRows.forEach(row => {
        const isHigherBetter = row.dataset.higherBetter === 'true';
        const specCells = row.querySelectorAll('.spec-value');
        let bestValue = isHigherBetter ? -Infinity : Infinity;
        let bestCells = [];
        
        // Find the best value
        specCells.forEach(cell => {
            const numValue = parseFloat(cell.dataset.rawValue || 0);
            
            if (!isNaN(numValue)) {
                if ((isHigherBetter && numValue > bestValue) || 
                    (!isHigherBetter && numValue < bestValue)) {
                    bestValue = numValue;
                    bestCells = [cell];
                } else if (numValue === bestValue) {
                    bestCells.push(cell);
                }
            }
        });
        
        // Highlight the best cells
        bestCells.forEach(cell => {
            cell.classList.add('best-spec');
        });
    });
}

/**
 * Initializes the performance comparison chart
 */
function initPerformanceChart() {
    const performanceChart = document.getElementById('performanceChart');
    
    if (!performanceChart) return;
    
    const laptops = JSON.parse(performanceChart.dataset.laptops || '[]');
    
    if (laptops.length === 0) return;
    
    const labels = laptops.map(laptop => `${laptop.brand} ${laptop.model}`);
    const cinebenchData = laptops.map(laptop => laptop.cinebench_score);
    const geekbenchData = laptops.map(laptop => laptop.geekbench_score);
    const gamingFpsData = laptops.map(laptop => laptop.gaming_fps * 100); // Scale for visibility
    
    new Chart(performanceChart, {
        type: 'radar',
        data: {
            labels: ['CPU (Cinebench)', 'Multi-Core (Geekbench)', 'Gaming Performance'],
            datasets: laptops.map((laptop, index) => ({
                label: `${laptop.brand} ${laptop.model}`,
                data: [
                    laptop.cinebench_score / 100, // Scale down for better visualization
                    laptop.geekbench_score / 100,
                    laptop.gaming_fps
                ],
                fill: true,
                backgroundColor: `rgba(${index * 100}, ${255 - index * 50}, ${index * 80}, 0.2)`,
                borderColor: `rgba(${index * 100}, ${255 - index * 50}, ${index * 80}, 1)`,
                pointBackgroundColor: `rgba(${index * 100}, ${255 - index * 50}, ${index * 80}, 1)`,
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: `rgba(${index * 100}, ${255 - index * 50}, ${index * 80}, 1)`
            }))
        },
        options: {
            elements: {
                line: {
                    borderWidth: 3
                }
            },
            scales: {
                r: {
                    angleLines: {
                        display: true
                    },
                    suggestedMin: 0
                }
            }
        }
    });
}

/**
 * Initializes the price-to-performance chart
 */
function initPricePerformanceChart() {
    const pricePerformanceChart = document.getElementById('pricePerformanceChart');
    
    if (!pricePerformanceChart) return;
    
    const laptops = JSON.parse(pricePerformanceChart.dataset.laptops || '[]');
    
    if (laptops.length === 0) return;
    
    const ctx = pricePerformanceChart.getContext('2d');
    
    new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: laptops.map((laptop, index) => ({
                label: `${laptop.brand} ${laptop.model}`,
                data: [{
                    x: laptop.price,
                    y: (laptop.cinebench_score + laptop.geekbench_score/10) / 100 // Simplified performance score
                }],
                backgroundColor: `rgba(${index * 100}, ${255 - index * 50}, ${index * 80}, 0.7)`,
                borderColor: `rgba(${index * 100}, ${255 - index * 50}, ${index * 80}, 1)`,
                pointRadius: 10,
                pointHoverRadius: 12
            }))
        },
        options: {
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    title: {
                        display: true,
                        text: 'Price (₹)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Performance Score'
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const laptop = laptops[context.datasetIndex];
                            return [
                                `${laptop.brand} ${laptop.model}`,
                                `Price: $${laptop.price}`,
                                `Cinebench: ${laptop.cinebench_score}`,
                                `Geekbench: ${laptop.geekbench_score}`,
                                `Gaming FPS: ${laptop.gaming_fps}`
                            ];
                        }
                    }
                }
            }
        }
    });
}

/**
 * Sets up the "Add to Comparison" buttons functionality
 */
function setupComparisonButtons() {
    const addToCompareButtons = document.querySelectorAll('.add-to-compare');
    const compareButton = document.getElementById('compare-selected');
    const selectedLaptops = new Set();
    
    // Update the compare button state
    function updateCompareButtonState() {
        if (selectedLaptops.size >= 2) {
            compareButton.disabled = false;
        } else {
            compareButton.disabled = true;
        }
        
        // Update counter if it exists
        const counter = document.getElementById('comparison-count');
        if (counter) {
            counter.textContent = selectedLaptops.size;
        }
    }
    
    // Add event listeners to comparison buttons
    addToCompareButtons.forEach(button => {
        button.addEventListener('click', function() {
            const laptopId = this.dataset.laptopId;
            
            if (selectedLaptops.has(laptopId)) {
                selectedLaptops.delete(laptopId);
                this.classList.remove('btn-success');
                this.classList.add('btn-outline-success');
                this.innerHTML = '<i class="fas fa-plus"></i> Add to Comparison';
            } else {
                if (selectedLaptops.size < 4) { // Limit to 4 laptops
                    selectedLaptops.add(laptopId);
                    this.classList.remove('btn-outline-success');
                    this.classList.add('btn-success');
                    this.innerHTML = '<i class="fas fa-check"></i> Added to Comparison';
                } else {
                    alert('You can compare up to 4 laptops at a time.');
                }
            }
            
            updateCompareButtonState();
        });
    });
    
    // Handle the compare button click
    if (compareButton) {
        compareButton.addEventListener('click', function() {
            if (selectedLaptops.size >= 2) {
                const laptopIds = Array.from(selectedLaptops);
                const queryString = laptopIds.map(id => `laptop_id=${id}`).join('&');
                window.location.href = `/comparison?${queryString}`;
            }
        });
    }
    
    // Initialize button state
    updateCompareButtonState();
}
