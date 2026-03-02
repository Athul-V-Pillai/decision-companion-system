/**
 * Decision Companion System - Frontend JavaScript
 * Handles form generation, API calls, result display, and chart visualizations
 */

// State management
let state = {
    options: [],
    criteria: [],
    weights: [],
    criterionTypes: [],
    scores: {}
};

// Chart instances for cleanup
window.scoresBarChart = null;
window.criteriaRadarChart = null;

// Store last evaluation result for export
let lastEvaluationResult = null;

// DOM Elements
const optionsInput = document.getElementById('optionsInput');
const criteriaInput = document.getElementById('criteriaInput');
const generateBtn = document.getElementById('generateBtn');
const evaluateBtn = document.getElementById('evaluateBtn');
const resetBtn = document.getElementById('resetBtn');
const weightsContainer = document.getElementById('weightsContainer');
const scoresContainer = document.getElementById('scoresContainer');

const inputSection = document.querySelector('.input-section');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');

// Event Listeners
generateBtn.addEventListener('click', generateForm);
evaluateBtn.addEventListener('click', evaluateDecision);
resetBtn.addEventListener('click', resetForm);
document.getElementById('backBtn').addEventListener('click', backToInput);
document.getElementById('errorBackBtn').addEventListener('click', backToInput);

// Add listeners for new buttons if they exist
const exportPdfBtn = document.getElementById('exportPdfBtn');
const viewHistoryBtn = document.getElementById('viewHistoryBtn');
if (exportPdfBtn) exportPdfBtn.addEventListener('click', exportPDF);
if (viewHistoryBtn) viewHistoryBtn.addEventListener('click', toggleHistory);

/**
 * Parse comma-separated input and trim whitespace
 */
function parseInput(input) {
    return input
        .split(',')
        .map(item => item.trim())
        .filter(item => item.length > 0);
}

/**
 * Generate dynamic form based on options and criteria
 */
function generateForm() {
    // Parse inputs
    state.options = parseInput(optionsInput.value);
    state.criteria = parseInput(criteriaInput.value);

    // Validate
    if (state.options.length === 0) {
        showError('Please enter at least one option');
        return;
    }
    if (state.criteria.length === 0) {
        showError('Please enter at least one criterion');
        return;
    }

    // Initialize weights and types
    state.weights = Array(state.criteria.length).fill(1);
    state.criterionTypes = Array(state.criteria.length).fill('max');

    // Initialize scores
    state.scores = {};
    state.options.forEach(option => {
        state.scores[option] = Array(state.criteria.length).fill(5);
    });

    hideError();
    renderWeightsSection();
    renderScoresSection();
    evaluateBtn.disabled = false;
}

/**
 * Render weights and criterion type inputs
 */
function renderWeightsSection() {
    weightsContainer.innerHTML = '';

    state.criteria.forEach((criterion, index) => {
        const div = document.createElement('div');
        div.className = 'weight-input-group';

        const label = document.createElement('label');
        label.textContent = criterion;

        const typeSelect = document.createElement('select');
        typeSelect.value = state.criterionTypes[index];
        typeSelect.innerHTML = `
            <option value="max">↑ Max (Higher is better)</option>
            <option value="min">↓ Min (Lower is better)</option>
        `;
        typeSelect.addEventListener('change', (e) => {
            state.criterionTypes[index] = e.target.value;
        });

        const weightInput = document.createElement('input');
        weightInput.type = 'number';
        weightInput.min = '0.1';
        weightInput.step = '0.1';
        weightInput.value = state.weights[index];
        weightInput.placeholder = 'Weight';
        weightInput.addEventListener('change', (e) => {
            state.weights[index] = parseFloat(e.target.value) || 1;
        });

        const weightLabel = document.createElement('span');
        weightLabel.className = 'weight-label';
        weightLabel.textContent = 'Weight:';

        div.appendChild(label);
        div.appendChild(typeSelect);
        div.appendChild(weightLabel);
        div.appendChild(weightInput);

        weightsContainer.appendChild(div);
    });
}

/**
 * Render scores input table
 */
function renderScoresSection() {
    scoresContainer.innerHTML = '';

    // Create table
    const table = document.createElement('table');
    table.className = 'scores-input-table';

    // Header row
    const headerRow = document.createElement('tr');
    const emptyHeader = document.createElement('th');
    emptyHeader.textContent = 'Option';
    headerRow.appendChild(emptyHeader);

    state.criteria.forEach(criterion => {
        const th = document.createElement('th');
        th.textContent = criterion;
        headerRow.appendChild(th);
    });

    table.appendChild(headerRow);

    // Option rows
    state.options.forEach((option, optionIndex) => {
        const row = document.createElement('tr');

        const optionCell = document.createElement('td');
        optionCell.textContent = option;
        optionCell.className = 'option-name';
        row.appendChild(optionCell);

        state.criteria.forEach((criterion, criterionIndex) => {
            const td = document.createElement('td');
            const input = document.createElement('input');
            input.type = 'number';
            input.min = '0';
            input.max = '10';
            input.step = '0.1';
            input.value = state.scores[option][criterionIndex];
            input.className = 'score-input';

            input.addEventListener('change', (e) => {
                state.scores[option][criterionIndex] = parseFloat(e.target.value) || 0;
            });

            td.appendChild(input);
            row.appendChild(td);
        });

        table.appendChild(row);
    });

    scoresContainer.appendChild(table);
}

/**
 * Send evaluation request to backend
 */
async function evaluateDecision() {
    evaluateBtn.disabled = true;
    evaluateBtn.textContent = 'Evaluating...';

    try {
        const payload = {
            options: state.options,
            criteria: state.criteria,
            weights: state.weights,
            criterion_types: state.criterionTypes,
            scores: state.scores
        };

        const response = await fetch('/api/evaluate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (result.success) {
            displayResults(result.data);
        } else {
            showError(result.error || 'Evaluation failed');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to communicate with server');
    } finally {
        evaluateBtn.disabled = false;
        evaluateBtn.textContent = 'Evaluate Decision';
    }
}

/**
 * Display evaluation results
 */
function displayResults(data) {
    // Store evaluation result for PDF export
    lastEvaluationResult = data;
    console.log('displayResults called with data:', data);
    
    inputSection.style.display = 'none';
    errorSection.style.display = 'none';
    resultsSection.style.display = 'block';

    const explanation = data.explanation;

    // Summary
    document.getElementById('summaryText').textContent = explanation.summary;

    // Recommendation
    document.getElementById('recommendationText').innerHTML = 
        explanation.recommendation.replace(/\n/g, '<br/>');

    // Confidence Score
    const confidenceData = data.confidence;
    const confidenceContainer = document.getElementById('confidenceContainer');
    console.log('Confidence data:', confidenceData);
    if (confidenceContainer) {
        confidenceContainer.innerHTML = `
            <p><strong>Confidence Score:</strong> ${confidenceData.score.toFixed(4)}</p>
            <p><strong>Level:</strong> <span class="confidence-${confidenceData.level.toLowerCase()}">${confidenceData.level}</span></p>
            <p><em>${confidenceData.interpretation}</em></p>
        `;
        console.log('Confidence container updated');
    } else {
        console.error('Confidence container not found');
    }

    // Scores table
    const tbody = document.getElementById('scoresTableBody');
    tbody.innerHTML = '';
    data.ranked_options.forEach((option, index) => {
        const row = document.createElement('tr');
        if (index === 0) row.classList.add('best-option');

        const rankCell = document.createElement('td');
        rankCell.textContent = `#${index + 1}`;

        const optionCell = document.createElement('td');
        optionCell.textContent = option;

        const scoreCell = document.createElement('td');
        scoreCell.textContent = data.scores[option].toFixed(4);
        scoreCell.className = 'score-value';

        row.appendChild(rankCell);
        row.appendChild(optionCell);
        row.appendChild(scoreCell);
        tbody.appendChild(row);
    });

    // Details breakdown
    const detailsContainer = document.getElementById('detailsContainer');
    detailsContainer.innerHTML = '';
    
    data.ranked_options.forEach(option => {
        const details = data.details[option];
        const div = document.createElement('div');
        div.className = 'detail-item';

        let html = `<h4>${option}</h4>`;
        html += `<p class="detail-score">Total Score: ${details.total_score}</p>`;
        html += '<table class="detail-table"><thead><tr>';
        html += '<th>Criterion</th><th>Raw Score</th><th>Normalized</th><th>Weight</th><th>Contribution</th>';
        html += '</tr></thead><tbody>';

        details.criteria_breakdown.forEach(cb => {
            html += `<tr>
                <td>${cb.criterion}</td>
                <td>${cb.raw_score}</td>
                <td>${cb.normalized_score.toFixed(4)}</td>
                <td>${cb.weight.toFixed(4)}</td>
                <td>${cb.contribution.toFixed(4)}</td>
            </tr>`;
        });

        html += '</tbody></table>';
        div.innerHTML = html;
        detailsContainer.appendChild(div);
    });

    // Methodology
    document.getElementById('methodologyText').innerHTML = 
        explanation.methodology.replace(/\n/g, '<br/>');

    // Ranking explanation
    const rankingDiv = document.getElementById('rankingExplanation');
    rankingDiv.innerHTML = '';
    explanation.ranking_explanation.forEach(item => {
        const div = document.createElement('div');
        div.className = 'ranking-item';
        if (item.rank === 1) div.classList.add('top-ranked');
        
        div.innerHTML = `
            <h4>${item.summary}</h4>
            <p><strong>${item.strengths}</strong></p>
            <p>${item.weaknesses}</p>
        `;
        rankingDiv.appendChild(div);
    });

    // Create visualizations after DOM has updated
    console.log('Creating charts...');
    setTimeout(() => {
        console.log('Timeout callback: Creating charts');
        try {
            createScoresBarChart(data);
            createCriteriaRadarChart(data);
        } catch (err) {
            console.error('Chart creation error:', err);
        }
    }, 200);
}

/**
 * Create bar chart showing total scores per option
 */
function createScoresBarChart(data) {
    try {
        console.log('=== BAR CHART START ===');
        console.log('Data:', data);
        
        // Destroy existing chart if it exists
        if (window.scoresBarChart) {
            console.log('Destroying existing bar chart');
            window.scoresBarChart.destroy();
        }

        // Get canvas element
        const canvas = document.getElementById('scoresBarChart');
        if (!canvas) {
            console.error('❌ Canvas element scoresBarChart not found');
            return;
        }
        console.log('✓ Canvas found:', canvas);

        const options = data.ranked_options;
        const scores = options.map(opt => data.scores[opt]);
        
        console.log('Options:', options);
        console.log('Scores:', scores);

        // Define colors
        const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#06b6d4'];
        const backgroundColor = options.map((_, i) => colors[i % colors.length]);
        const borderColor = backgroundColor.map(c => c.replace(')', ', 0.8)'));

        // Create chart
        window.scoresBarChart = new Chart(canvas, {
            type: 'bar',
            data: {
                labels: options,
                datasets: [{
                    label: 'Total Score',
                    data: scores,
                    backgroundColor: backgroundColor,
                    borderColor: borderColor,
                    borderWidth: 2,
                    borderRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                indexAxis: 'x',
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 1,
                        ticks: {
                            stepSize: 0.2
                        }
                    }
                }
            }
        });
        
        console.log('✓ Bar chart created successfully');
        console.log('=== BAR CHART END ===');
    } catch (error) {
        console.error('❌ Error creating bar chart:', error);
        console.error('Stack:', error.stack);
    }
}

/**
 * Create radar chart comparing criteria performance across top options
 */
function createCriteriaRadarChart(data) {
    try {
        console.log('=== RADAR CHART START ===');
        
        // Destroy existing chart if it exists
        if (window.criteriaRadarChart) {
            console.log('Destroying existing radar chart');
            window.criteriaRadarChart.destroy();
        }

        // Get canvas element
        const canvas = document.getElementById('criteriaRadarChart');
        if (!canvas) {
            console.error('❌ Canvas element criteriaRadarChart not found');
            return;
        }
        console.log('✓ Canvas found:', canvas);

        // Get top 3 options
        const topOptions = data.ranked_options.slice(0, 3);
        console.log('Top options:', topOptions);

        // Extract criteria
        const firstDetails = data.details[topOptions[0]];
        const criteria = firstDetails.criteria_breakdown.map(cb => cb.criterion);
        console.log('Criteria:', criteria);

        // Define colors
        const colors = ['#3b82f6', '#10b981', '#f59e0b'];

        // Helper function to convert hex to rgba
        function hexToRgba(hex, alpha) {
            const r = parseInt(hex.slice(1, 3), 16);
            const g = parseInt(hex.slice(3, 5), 16);
            const b = parseInt(hex.slice(5, 7), 16);
            return `rgba(${r}, ${g}, ${b}, ${alpha})`;
        }

        // Create datasets for each option
        const datasets = topOptions.map((option, idx) => {
            const details = data.details[option];
            const normalizedScores = details.criteria_breakdown.map(cb => cb.normalized_score);
            const color = colors[idx];
            
            console.log(`Option ${option}:`, normalizedScores);

            return {
                label: option,
                data: normalizedScores,
                borderColor: color,
                backgroundColor: hexToRgba(color, 0.15),
                borderWidth: 2.5,
                fill: true,
                tension: 0.4,
                pointRadius: 6,
                pointBackgroundColor: color,
                pointBorderColor: '#fff',
                pointBorderWidth: 2.5,
                pointHoverRadius: 8
            };
        });

        // Create chart
        window.criteriaRadarChart = new Chart(canvas, {
            type: 'radar',
            data: {
                labels: criteria,
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                layout: {
                    padding: {
                        top: 30,
                        bottom: 30,
                        left: 30,
                        right: 30
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            font: {
                                size: 14,
                                weight: 'bold',
                                family: 'Arial, sans-serif'
                            },
                            padding: 20,
                            boxWidth: 15,
                            boxHeight: 12,
                            usePointStyle: true,
                            color: '#333'
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.85)',
                        padding: 14,
                        titleFont: { size: 14, weight: 'bold' },
                        bodyFont: { size: 13 },
                        cornerRadius: 6,
                        displayColors: true,
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' + (context.raw * 100).toFixed(1) + '%';
                            }
                        }
                    }
                },
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 1,
                        ticks: {
                            stepSize: 0.2,
                            font: {
                                size: 12,
                                weight: 'bold'
                            },
                            callback: function(value) {
                                return (value * 100).toFixed(0) + '%';
                            },
                            color: '#666',
                            backdropColor: 'transparent'
                        },
                        pointLabels: {
                            font: {
                                size: 13,
                                weight: 'bold',
                                family: 'Arial, sans-serif'
                            },
                            padding: 12,
                            color: '#333'
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.08)',
                            drawBorder: true,
                            lineWidth: 1.5
                        },
                        angleLines: {
                            color: 'rgba(0, 0, 0, 0.1)',
                            lineWidth: 1
                        }
                    }
                }
            }
        });
        
        console.log('✓ Radar chart created successfully');
        console.log('=== RADAR CHART END ===');
    } catch (error) {
        console.error('❌ Error creating radar chart:', error);
        console.error('Stack:', error.stack);
    }
}

/**
 * Display error message
 */
function showError(message) {
    inputSection.style.display = 'none';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'block';
    document.getElementById('errorText').textContent = message;
}

/**
 * Hide error section
 */
function hideError() {
    errorSection.style.display = 'none';
}

/**
 * Navigate back to input section
 */
function backToInput() {
    inputSection.style.display = 'block';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
}

/**
 * Reset form to initial state
 */
function resetForm() {
    optionsInput.value = '';
    criteriaInput.value = '';
    weightsContainer.innerHTML = '';
    scoresContainer.innerHTML = '';
    evaluateBtn.disabled = true;
    state = {
        options: [],
        criteria: [],
        weights: [],
        criterionTypes: [],
        scores: {}
    };
    backToInput();
}

/**
 * Export current evaluation as PDF Report
 */
async function exportPDF() {
    try {
        console.log('=== PDF EXPORT START ===');
        
        // Check if evaluation has been run
        if (!lastEvaluationResult) {
            alert('Please evaluate options first before exporting.');
            return;
        }
        
        // Show loading state
        const btn = document.getElementById('exportPdfBtn');
        const originalText = btn.textContent;
        btn.textContent = 'Generating PDF...';
        btn.disabled = true;

        // Prepare export data from last evaluation result
        const exportData = {
            title: 'Decision Analysis Report',
            options: state.options,
            criteria: state.criteria,
            weights: Object.fromEntries(state.criteria.map((c, i) => [c, state.weights[i]])),
            scores: lastEvaluationResult.scores || {},
            ranked_options: lastEvaluationResult.ranked_options || [],
            details: lastEvaluationResult.details || {},
            confidence: lastEvaluationResult.confidence || {},
            explanation: lastEvaluationResult.explanation || {}
        };

        console.log('Export data prepared:', exportData);

        // Call export endpoint
        const response = await fetch('/api/export-report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(exportData)
        });

        console.log('Export response status:', response.status);

        if (!response.ok) {
            const errorText = await response.text();
            console.error('Error response:', errorText);
            throw new Error('PDF export failed: ' + response.statusText);
        }

        // Get the blob and trigger download
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'decision_report.pdf';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();

        console.log('✓ PDF exported successfully');
        
        // Restore button
        btn.textContent = originalText;
        btn.disabled = false;
        
    } catch (error) {
        console.error('❌ Error exporting PDF:', error);
        alert('Error exporting PDF: ' + error.message);
        const btn = document.getElementById('exportPdfBtn');
        btn.textContent = '📄 Export PDF Report';
        btn.disabled = false;
    }
}

/**
 * Toggle history section visibility and load data if needed
 */
async function toggleHistory() {
    const historySection = document.getElementById('historySection');
    const historyContainer = document.getElementById('historyContainer');
    
    try {
        if (historySection.style.display === 'none' || historySection.style.display === '') {
            // Show history section and load data
            const viewBtn = document.getElementById('viewHistoryBtn');
            viewBtn.textContent = 'Loading...';
            viewBtn.disabled = true;
            
            const response = await fetch('/api/history');
            if (!response.ok) {
                throw new Error('Failed to load history');
            }

            const data = await response.json();
            console.log('History data:', data);
            console.log('Data length:', data.data ? data.data.length : 0);

            if (!data.data || data.data.length === 0) {
                historyContainer.innerHTML = '<p style="color: #999; padding: 20px;">No decisions saved yet. Evaluate some options to build your history.</p>';
            } else {
                // Build history HTML
                let historyHTML = '';
                data.data.forEach((item, index) => {
                    const itemId = item.id || index + 1;
                    const options = Array.isArray(item.options) ? item.options.join(', ') : item.options;
                    const bestChoice = item.best_choice || 'N/A';
                    const score = item.best_score ? (parseFloat(item.best_score) * 100).toFixed(1) : '0';
                    const timestamp = item.timestamp ? new Date(item.timestamp).toLocaleString() : 'Unknown';
                    
                    historyHTML += `
                        <div class="history-item" style="display: block; margin-bottom: 15px; padding: 15px; background: white; border-left: 4px solid #3b82f6; border-radius: 5px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);">
                            <h4 style="color: #3b82f6; margin: 0 0 10px 0; font-size: 1em;">Decision #${itemId}</h4>
                            <div class="history-item-info" style="font-size: 0.9em; color: #666; line-height: 1.6;">
                                <div><strong>Options:</strong> ${options}</div>
                                <div><strong>Best Choice:</strong> ${bestChoice}</div>
                                <div><strong>Score:</strong> ${score}%</div>
                                <div><strong>Saved:</strong> ${timestamp}</div>
                            </div>
                            <div style="margin-top: 10px;">
                                <button class="btn btn-danger" onclick="deleteHistoryItem('${itemId}')" style="padding: 6px 12px; font-size: 0.85em;">🗑️ Delete</button>
                            </div>
                        </div>
                    `;
                });
                historyContainer.innerHTML = historyHTML;
            }

            historySection.style.display = 'block';
            historySection.classList.add('visible');
            viewBtn.textContent = '📋 Hide History';
            viewBtn.disabled = false;
        } else {
            // Hide history section
            historySection.style.display = 'none';
            historySection.classList.remove('visible');
            document.getElementById('viewHistoryBtn').textContent = '📋 View History';
        }
    } catch (error) {
        console.error('❌ Error loading history:', error);
        historyContainer.innerHTML = '<p style="color: #e74c3c; padding: 20px;">Error loading history: ' + error.message + '</p>';
        if (historySection.style.display === 'none' || historySection.style.display === '') {
            historySection.style.display = 'block';
        }
        document.getElementById('viewHistoryBtn').textContent = '📋 View History';
    }
}

/**
 * Delete a history item
 */
async function deleteHistoryItem(itemId) {
    if (!confirm('Are you sure you want to delete this decision record?')) {
        return;
    }

    try {
        console.log('Deleting history item:', itemId);
        
        const response = await fetch(`/api/history/${itemId}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error('Failed to delete history');
        }

        console.log('✓ History item deleted');
        // Refresh history display
        await toggleHistory();
        await toggleHistory();
        
    } catch (error) {
        console.error('❌ Error deleting history:', error);
        alert('Error deleting history: ' + error.message);
    }
}

// Initialize with example data on page load
window.addEventListener('load', () => {
    // Optional: auto-generate form with example data
    // Uncomment the line below to auto-load example
    // generateForm();
});
