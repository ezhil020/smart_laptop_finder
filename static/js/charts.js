/**
 * Laptop Recommender Charts
 * 
 * Provides chart functionality for detailed laptop pages and comparison views.
 */


document.addEventListener('DOMContentLoaded', function () {
    // Initialize all charts
    initBenchmarkCharts();
    initValueCharts();
    initRamStorageChart();
    initPriceBatteryChart();
});

/**
 * Initializes the RAM and Storage Comparison Chart
 */
function initRamStorageChart() {
    const ramStorageChart = document.getElementById('ramStorageChart');
    if (!ramStorageChart) return;

    const laptops = JSON.parse(ramStorageChart.dataset.laptops || '[]');
    if (laptops.length === 0) return;

    const labels = laptops.map(laptop => `${laptop.brand} ${laptop.model}`);
    const ramData = laptops.map(laptop => laptop.ram || 0);
    const storageData = laptops.map(laptop => laptop.storage_capacity || 0);

    new Chart(ramStorageChart, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'RAM (GB)',
                    data: ramData,
                    backgroundColor: 'rgba(54, 162, 235, 0.7)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Storage (GB)',
                    data: storageData,
                    backgroundColor: 'rgba(75, 192, 192, 0.7)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Capacity (GB)'
                    }
                }
            }
        }
    });
}

/**
 * Initializes the Price vs. Battery Life Scatter Plot
 */
function initPriceBatteryChart() {
    const priceBatteryChart = document.getElementById('priceBatteryChart');
    if (!priceBatteryChart) return;

    const laptops = JSON.parse(priceBatteryChart.dataset.laptops || '[]');
    if (laptops.length === 0) return;

    const datasets = laptops.map((laptop, index) => ({
        label: `${laptop.brand} ${laptop.model}`,
        data: [{ x: laptop.price, y: laptop.battery_life }],
        backgroundColor: `rgba(${index * 50}, ${255 - index * 50}, ${index * 100}, 0.7)`,
        borderColor: `rgba(${index * 50}, ${255 - index * 50}, ${index * 100}, 1)`,
        pointRadius: 10
    }));

    new Chart(priceBatteryChart, {
        type: 'scatter',
        data: { datasets: datasets },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Price (₹)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Battery Life (hours)'
                    }
                }
            }
        }
    });
}

/**
 * Initializes the RAM and Storage Comparison Chart
 */
function initRamStorageChart() {
    const ramStorageChart = document.getElementById('ramStorageChart');
    if (!ramStorageChart) return;

    const laptops = JSON.parse(ramStorageChart.dataset.laptops || '[]');
    if (laptops.length === 0) return;

    const labels = laptops.map(laptop => `${laptop.brand} ${laptop.model}`);
    const ramData = laptops.map(laptop => laptop.ram || 0);
    const storageData = laptops.map(laptop => laptop.storage_capacity || 0);

    new Chart(ramStorageChart, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'RAM (GB)',
                    data: ramData,
                    backgroundColor: 'rgba(54, 162, 235, 0.7)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Storage (GB)',
                    data: storageData,
                    backgroundColor: 'rgba(75, 192, 192, 0.7)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Capacity (GB)'
                    }
                }
            }
        }
    });
}

/**
 * Initializes the Price vs. Battery Life Scatter Plot
 */
function initPriceBatteryChart() {
    const priceBatteryChart = document.getElementById('priceBatteryChart');
    if (!priceBatteryChart) return;

    const laptops = JSON.parse(priceBatteryChart.dataset.laptops || '[]');
    if (laptops.length === 0) return;

    const datasets = laptops.map((laptop, index) => ({
        label: `${laptop.brand} ${laptop.model}`,
        data: [{ x: laptop.price, y: laptop.battery_life }],
        backgroundColor: `rgba(${index * 50}, ${255 - index * 50}, ${index * 100}, 0.7)`,
        borderColor: `rgba(${index * 50}, ${255 - index * 50}, ${index * 100}, 1)`,
        pointRadius: 10
    }));

    new Chart(priceBatteryChart, {
        type: 'scatter',
        data: { datasets: datasets },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Price (₹)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Battery Life (hours)'
                    }
                }
            }
        }
    });
}
/**
 * Initializes benchmark comparison charts
 */

function initBenchmarkCharts() {
    const performanceChart = document.getElementById('performanceChart');
    const pricePerformanceChart = document.getElementById('pricePerformanceChart');

    if (!performanceChart || !pricePerformanceChart) return;

    // Get laptop data
    const laptops = JSON.parse(performanceChart.dataset.laptops || '[]');
    console.log(laptops);

    if (laptops.length === 0) return;

    // Create chart data for performance chart
    const labels = laptops.map(laptop => `${laptop.brand} ${laptop.model}`);
    const cinebenchData = laptops.map(laptop => laptop.cinebench_score || 0);
    const geekbenchData = laptops.map(laptop => laptop.geekbench_score || 0);
    const gamingFpsData = laptops.map(laptop => laptop.gaming_fps || 0);

    // Render the performance radar chart
    new Chart(performanceChart, {
        type: 'radar',
        data: {
            labels: ['Cinebench (CPU)', 'Geekbench (Overall)', 'Gaming FPS'],
            datasets: laptops.map((laptop, index) => ({
                label: `${laptop.brand} ${laptop.model}`,
                data: [
                    laptop.cinebench_score || 0,
                    laptop.geekbench_score || 0,
                    laptop.gaming_fps || 0,
                ],
                backgroundColor: `rgba(${index * 50}, ${index * 100}, ${index * 150}, 0.2)`,
                borderColor: `rgba(${index * 50}, ${index * 100}, ${index * 150}, 1)`,
                borderWidth: 1,
            })),
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
            },
        },
    });

    // Create chart data for price-performance chart
    const pricePerformanceLabels = laptops.map(laptop => `${laptop.brand} ${laptop.model}`);
    const pricePerformanceData = laptops.map(laptop => laptop.price_performance_ratio || 0);

    // Render the price-performance bar chart
    new Chart(pricePerformanceChart, {
        type: 'bar',
        data: {
            labels: pricePerformanceLabels,
            datasets: [
                {
                    label: 'Price-Performance Ratio',
                    data: pricePerformanceData,
                    backgroundColor: 'rgba(75, 192, 192, 0.7)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                },
            ],
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                },
            },
        },
    });
}
function initValueCharts() {
    const valueChart = document.getElementById('valueChart');
    
    if (!valueChart) return;
    
    // Get laptop data
    const laptopData = JSON.parse(valueChart.dataset.laptop || '{}');
    const similarLaptops = JSON.parse(valueChart.dataset.similarLaptops || '[]');
    
    if (!laptopData.id) return;
    
    // Combine main laptop with similar ones
    const allLaptops = [laptopData, ...similarLaptops];
    
    // Create labels and data for price-performance ratio
    const labels = allLaptops.map(laptop => `${laptop.brand} ${laptop.model}`);
    const ratioData = allLaptops.map(laptop => laptop.price_performance_ratio || 0);
    
    // Create colors with the first one (main laptop) highlighted
    const backgroundColors = allLaptops.map((_, index) => 
        index === 0 ? 'rgba(54, 162, 235, 0.8)' : 'rgba(201, 203, 207, 0.8)'
    );
    const borderColors = allLaptops.map((_, index) => 
        index === 0 ? 'rgba(54, 162, 235, 1)' : 'rgba(201, 203, 207, 1)'
    );
    
    new Chart(valueChart, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Price-Performance Ratio',
                    data: ratioData,
                    backgroundColor: backgroundColors,
                    borderColor: borderColors,
                    borderWidth: 1
                }
            ]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            scales: {
                x: {
                    beginAtZero: true,
                    max: 1,
                    title: {
                        display: true,
                        text: 'Value Score (higher is better)'
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const index = context.dataIndex;
                            const laptop = allLaptops[index];
                            return [
                                `Value Score: ${laptop.price_performance_ratio?.toFixed(2) || 'N/A'}`,
                                `Price: $${laptop.price}`,
                                `Performance Rating: ${((laptop.price_performance_ratio || 0) * laptop.price).toFixed(0)}`
                            ];
                        }
                    }
                }
            }
        }
    });
}

/**
 * Creates a gauge chart for laptop rating visualization
 */
function createRatingGauge(elementId, value, maxValue = 5, title = 'Rating') {
    const gaugeElement = document.getElementById(elementId);
    
    if (!gaugeElement) return;
    
    const percentage = (value / maxValue) * 100;
    
    new Chart(gaugeElement, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [percentage, 100 - percentage],
                backgroundColor: [
                    getColorForRating(value, maxValue),
                    'rgba(220, 220, 220, 0.5)'
                ],
                borderWidth: 0
            }]
        },
        options: {
            circumference: 180,
            rotation: 270,
            cutout: '75%',
            plugins: {
                tooltip: {
                    enabled: false
                },
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: title,
                    position: 'bottom',
                    padding: {
                        top: 10
                    }
                }
            },
            layout: {
                padding: 10
            }
        },
        plugins: [{
            id: 'centerText',
            afterDraw: function(chart) {
                const ctx = chart.ctx;
                const width = chart.width;
                const height = chart.height;
                
                ctx.restore();
                ctx.font = 'bold 24px Arial';
                ctx.textBaseline = 'middle';
                ctx.textAlign = 'center';
                ctx.fillStyle = getColorForRating(value, maxValue);
                ctx.fillText(value.toFixed(1), width / 2, height / 2 - 15);
                
                ctx.font = '16px Arial';
                ctx.fillStyle = '#666';
                ctx.fillText(`out of ${maxValue}`, width / 2, height / 2 + 10);
                ctx.save();
            }
        }]
    });
}

/**
 * Helper function to get color based on rating value
 */
function getColorForRating(value, maxValue) {
    const ratio = value / maxValue;
    
    if (ratio >= 0.8) {
        return 'rgba(75, 192, 192, 0.8)'; // Good (teal)
    } else if (ratio >= 0.6) {
        return 'rgba(54, 162, 235, 0.8)'; // Above average (blue)
    } else if (ratio >= 0.4) {
        return 'rgba(255, 206, 86, 0.8)'; // Average (yellow)
    } else if (ratio >= 0.2) {
        return 'rgba(255, 159, 64, 0.8)'; // Below average (orange)
    } else {
        return 'rgba(255, 99, 132, 0.8)'; // Poor (red)
    }
}
