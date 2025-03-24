/**
 * Laptop Recommender Charts
 * 
 * Provides chart functionality for detailed laptop pages and comparison views.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize any charts on the page
    initBenchmarkCharts();
    initValueCharts();
});

/**
 * Initializes benchmark comparison charts
 */
function initBenchmarkCharts() {
    const benchmarkChart = document.getElementById('benchmarkChart');
    
    if (!benchmarkChart) return;
    
    // Get laptop data
    const laptopData = JSON.parse(benchmarkChart.dataset.laptop || '{}');
    const similarLaptops = JSON.parse(benchmarkChart.dataset.similarLaptops || '[]');
    
    if (!laptopData.id) return;
    
    // Combine main laptop with similar ones
    const allLaptops = [laptopData, ...similarLaptops];
    
    // Create chart data
    const labels = allLaptops.map(laptop => `${laptop.brand} ${laptop.model}`);
    
    // Create normalized scores (percentage of the maximum in each category)
    const maxCinebench = Math.max(...allLaptops.map(l => l.cinebench_score || 0));
    const maxGeekbench = Math.max(...allLaptops.map(l => l.geekbench_score || 0));
    const maxGamingFps = Math.max(...allLaptops.map(l => l.gaming_fps || 0));
    
    const cinebenchData = allLaptops.map(l => ((l.cinebench_score || 0) / maxCinebench * 100).toFixed(1));
    const geekbenchData = allLaptops.map(l => ((l.geekbench_score || 0) / maxGeekbench * 100).toFixed(1));
    const gamingFpsData = allLaptops.map(l => ((l.gaming_fps || 0) / maxGamingFps * 100).toFixed(1));
    
    new Chart(benchmarkChart, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Cinebench (CPU)',
                    data: cinebenchData,
                    backgroundColor: 'rgba(75, 192, 192, 0.7)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Geekbench (Overall)',
                    data: geekbenchData,
                    backgroundColor: 'rgba(153, 102, 255, 0.7)',
                    borderColor: 'rgba(153, 102, 255, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Gaming FPS',
                    data: gamingFpsData,
                    backgroundColor: 'rgba(255, 99, 132, 0.7)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Relative Performance (%)'
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const index = context.dataIndex;
                            const datasetIndex = context.datasetIndex;
                            
                            if (datasetIndex === 0) {
                                return `Cinebench: ${allLaptops[index].cinebench_score || 'N/A'} (${context.raw}%)`;
                            } else if (datasetIndex === 1) {
                                return `Geekbench: ${allLaptops[index].geekbench_score || 'N/A'} (${context.raw}%)`;
                            } else {
                                return `Gaming FPS: ${allLaptops[index].gaming_fps || 'N/A'} (${context.raw}%)`;
                            }
                        }
                    }
                }
            }
        }
    });
}

/**
 * Initializes price-to-performance ratio charts
 */
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
