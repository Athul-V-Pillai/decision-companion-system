/**
 * Decision Companion System - Frontend JavaScript
 * Handles form generation, API calls, and result display
 */

// State management
let state = {
    options: [],
    criteria: [],
    weights: [],
    criterionTypes: [],
    scores: {}
};

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
    inputSection.style.display = 'none';
    errorSection.style.display = 'none';
    resultsSection.style.display = 'block';

    const explanation = data.explanation;

    // Summary
    document.getElementById('summaryText').textContent = explanation.summary;

    // Recommendation
    document.getElementById('recommendationText').innerHTML = 
        explanation.recommendation.replace(/\n/g, '<br/>');

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

// Initialize with example data on page load
window.addEventListener('load', () => {
    // Optional: auto-generate form with example data
    // Uncomment the line below to auto-load example
    // generateForm();
});
