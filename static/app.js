// EduGenius Frontend JavaScript

// Tab switching
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-button').forEach(button => {
        button.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(`${tabName}-tab`).classList.add('active');
    event.target.classList.add('active');
}

// Show/hide loading indicator
function showLoading(show) {
    document.getElementById('loading').classList.toggle('show', show);
}

// Display result
function showResult(elementId, content, isError = false) {
    const resultDiv = document.getElementById(elementId);
    resultDiv.innerHTML = content;
    resultDiv.classList.add('show');
    if (isError) {
        resultDiv.classList.add('error');
    } else {
        resultDiv.classList.remove('error');
    }
}

// Generate validation info HTML
function generateValidationHTML(validation) {
    if (!validation) return '';

    const confidenceColor = {
        'high': '#4caf50',
        'medium': '#ff9800',
        'low': '#f44336'
    }[validation.confidence_level] || '#757575';

    let html = `
        <div class="validation-info" style="background: #f5f5f5; padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 4px solid ${confidenceColor};">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div>
                    <strong>Content Confidence:</strong>
                    <span style="color: ${confidenceColor}; font-weight: bold; text-transform: uppercase;">
                        ${validation.confidence_level}
                    </span>
                    (${(validation.confidence_score * 100).toFixed(0)}%)
                </div>
                ${validation.has_reference_material ?
                    '<span style="color: #4caf50;">✓ Verified with references</span>' :
                    '<span style="color: #ff9800;">⚠️ No references found</span>'}
            </div>
    `;

    // Add warnings
    if (validation.validation_warnings && validation.validation_warnings.length > 0) {
        html += '<div style="margin-top: 10px;">';
        validation.validation_warnings.forEach(warning => {
            html += `<div style="font-size: 0.9em; color: #666; margin: 5px 0;">• ${warning}</div>`;
        });
        html += '</div>';
    }

    // Add references if available
    if (validation.references && validation.references.length > 0) {
        html += `
            <details style="margin-top: 10px;">
                <summary style="cursor: pointer; font-weight: 500; color: #667eea;">
                    📚 View Reference Sources (${validation.references.length})
                </summary>
                <div style="margin-top: 10px; padding-left: 10px;">
        `;
        validation.references.forEach(ref => {
            html += `
                <div style="margin: 8px 0; padding: 8px; background: white; border-radius: 4px;">
                    <strong>${ref.title}</strong><br>
                    <span style="font-size: 0.9em; color: #666;">${ref.summary}</span><br>
                    <a href="${ref.url}" target="_blank" style="color: #667eea; font-size: 0.9em;">Read more →</a>
                </div>
            `;
        });
        html += '</div></details>';
    }

    html += '</div>';
    return html;
}

// Fetch provider information on load
async function loadProviderInfo() {
    try {
        const response = await fetch('/api/providers');
        const data = await response.json();

        const availableProviders = Object.entries(data.providers)
            .filter(([_, available]) => available)
            .map(([name, _]) => name)
            .join(', ');

        const providerInfo = document.getElementById('provider-info');
        providerInfo.innerHTML = `
            <strong>Default Provider:</strong> ${data.default.toUpperCase()} |
            <strong>Available:</strong> ${availableProviders || 'None configured'}
        `;
    } catch (error) {
        console.error('Error loading provider info:', error);
    }
}

// Quiz Form Handler
document.getElementById('quiz-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    showLoading(true);

    const data = {
        topic: document.getElementById('quiz-topic').value,
        num_questions: parseInt(document.getElementById('quiz-questions').value),
        difficulty: document.getElementById('quiz-difficulty').value,
        provider: document.getElementById('quiz-provider').value || null
    };

    try {
        const response = await fetch('/api/quiz', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || 'Error generating quiz');
        }

        let html = `<div class="provider-badge">Generated by: ${result.provider || 'Unknown'}</div>`;
        html += `<h3>Quiz: ${result.topic}</h3>`;
        html += `<p><strong>Difficulty:</strong> ${result.difficulty}</p>`;

        // Add validation info
        if (result.validation) {
            html += generateValidationHTML(result.validation);
        }

        if (result.questions && result.questions.length > 0) {
            result.questions.forEach((q, index) => {
                html += `
                    <div class="quiz-question">
                        <h4>Question ${index + 1}: ${q.question}</h4>
                        <div class="options">
                            ${q.options.map(opt => `<div class="quiz-option">${opt}</div>`).join('')}
                        </div>
                        <div class="explanation">
                            <strong>Correct Answer:</strong> ${q.correct_answer}<br>
                            <strong>Explanation:</strong> ${q.explanation}
                        </div>
                        <button class="btn-primary" onclick="toggleExplanation(this)" style="margin-top: 10px; padding: 8px 15px; font-size: 0.9em;">Show Answer</button>
                    </div>
                `;
            });
        } else if (result.error) {
            html += `<p class="error">Error: ${result.error}</p>`;
        }

        showResult('quiz-result', html);
    } catch (error) {
        showResult('quiz-result', `<p>Error: ${error.message}</p>`, true);
    } finally {
        showLoading(false);
    }
});

// Toggle explanation visibility
function toggleExplanation(button) {
    const explanation = button.previousElementSibling;
    explanation.classList.toggle('show');
    button.textContent = explanation.classList.contains('show') ? 'Hide Answer' : 'Show Answer';
}

// Explain Concept Form Handler
document.getElementById('explain-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    showLoading(true);

    const data = {
        concept: document.getElementById('explain-concept').value,
        level: document.getElementById('explain-level').value,
        provider: document.getElementById('explain-provider').value || null
    };

    try {
        const response = await fetch('/api/explain', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || 'Error explaining concept');
        }

        let html = `
            <div class="provider-badge">Generated by: ${result.provider}</div>
            <h3>${result.concept}</h3>
            <p><strong>Level:</strong> ${result.level}</p>
        `;

        // Add validation info
        if (result.validation) {
            html += generateValidationHTML(result.validation);
        }

        html += `<div style="margin-top: 20px; white-space: pre-wrap; line-height: 1.6;">${result.explanation}</div>`;

        showResult('explain-result', html);
    } catch (error) {
        showResult('explain-result', `<p>Error: ${error.message}</p>`, true);
    } finally {
        showLoading(false);
    }
});

// Study Plan Form Handler
document.getElementById('study-plan-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    showLoading(true);

    const data = {
        subject: document.getElementById('study-subject').value,
        duration_weeks: parseInt(document.getElementById('study-weeks').value),
        hours_per_week: parseInt(document.getElementById('study-hours').value),
        provider: document.getElementById('study-provider').value || null
    };

    try {
        const response = await fetch('/api/study-plan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || 'Error creating study plan');
        }

        let html = `<div class="provider-badge">Generated by: ${result.provider || 'Unknown'}</div>`;
        html += `<h3>Study Plan: ${result.subject}</h3>`;
        html += `<p><strong>Duration:</strong> ${result.duration_weeks} weeks | <strong>Time:</strong> ${result.hours_per_week} hours/week</p>`;

        // Add validation info
        if (result.validation) {
            html += generateValidationHTML(result.validation);
        }

        if (result.weeks && result.weeks.length > 0) {
            result.weeks.forEach(week => {
                html += `
                    <div class="study-week">
                        <h4>Week ${week.week}: ${week.focus}</h4>
                        <div><strong>Topics:</strong>
                            <ul>${week.topics.map(t => `<li>${t}</li>`).join('')}</ul>
                        </div>
                        <div><strong>Activities:</strong>
                            <ul>${week.activities.map(a => `<li>${a}</li>`).join('')}</ul>
                        </div>
                        <div><strong>Goals:</strong>
                            <ul>${week.goals.map(g => `<li>${g}</li>`).join('')}</ul>
                        </div>
                    </div>
                `;
            });

            if (result.resources && result.resources.length > 0) {
                html += `
                    <div class="study-week">
                        <h4>Recommended Resources</h4>
                        <ul>${result.resources.map(r => `<li>${r}</li>`).join('')}</ul>
                    </div>
                `;
            }

            if (result.tips && result.tips.length > 0) {
                html += `
                    <div class="study-week">
                        <h4>Study Tips</h4>
                        <ul>${result.tips.map(t => `<li>${t}</li>`).join('')}</ul>
                    </div>
                `;
            }
        } else if (result.error) {
            html += `<p class="error">Error: ${result.error}</p>`;
        }

        showResult('study-plan-result', html);
    } catch (error) {
        showResult('study-plan-result', `<p>Error: ${error.message}</p>`, true);
    } finally {
        showLoading(false);
    }
});

// Homework Help Form Handler
document.getElementById('homework-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    showLoading(true);

    const data = {
        question: document.getElementById('homework-question').value,
        subject: document.getElementById('homework-subject').value || null,
        provider: document.getElementById('homework-provider').value || null
    };

    try {
        const response = await fetch('/api/homework-help', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || 'Error getting homework help');
        }

        const html = `
            <div class="provider-badge">Generated by: ${result.provider}</div>
            <h3>Homework Help${result.subject ? ': ' + result.subject : ''}</h3>
            <div style="background: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
                <strong>Your Question:</strong><br>
                ${result.question}
            </div>
            <div style="margin-top: 20px; white-space: pre-wrap; line-height: 1.6;">${result.help}</div>
        `;

        showResult('homework-result', html);
    } catch (error) {
        showResult('homework-result', `<p>Error: ${error.message}</p>`, true);
    } finally {
        showLoading(false);
    }
});

// Practice Problems Form Handler
document.getElementById('practice-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    showLoading(true);

    const data = {
        topic: document.getElementById('practice-topic').value,
        num_problems: parseInt(document.getElementById('practice-count').value),
        difficulty: document.getElementById('practice-difficulty').value,
        provider: document.getElementById('practice-provider').value || null
    };

    try {
        const response = await fetch('/api/practice', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || 'Error generating practice problems');
        }

        let html = `<div class="provider-badge">Generated by: ${result.provider}</div>`;
        html += `<h3>Practice Problems: ${result.topic}</h3>`;
        html += `<p><strong>Difficulty:</strong> ${result.difficulty}</p>`;

        if (result.problems && result.problems.length > 0) {
            result.problems.forEach((problem, index) => {
                html += `
                    <div class="practice-problem">
                        <h4>Problem ${index + 1}</h4>
                        <p>${problem.problem}</p>
                        ${problem.hints && problem.hints.length > 0 ? `
                            <div class="hints">
                                <h5>Hints:</h5>
                                <ul>${problem.hints.map(h => `<li>${h}</li>`).join('')}</ul>
                            </div>
                        ` : ''}
                        <div class="solution" id="solution-${index}" style="display: none;">
                            <h5>Solution:</h5>
                            <p>${problem.solution}</p>
                        </div>
                        <button class="btn-primary" onclick="toggleSolution(${index})" style="margin-top: 10px; padding: 8px 15px; font-size: 0.9em;">Show Solution</button>
                    </div>
                `;
            });
        } else {
            html += '<p>No practice problems generated. Please try again.</p>';
        }

        showResult('practice-result', html);
    } catch (error) {
        showResult('practice-result', `<p>Error: ${error.message}</p>`, true);
    } finally {
        showLoading(false);
    }
});

// Toggle solution visibility
function toggleSolution(index) {
    const solution = document.getElementById(`solution-${index}`);
    const button = event.target;
    if (solution.style.display === 'none') {
        solution.style.display = 'block';
        button.textContent = 'Hide Solution';
    } else {
        solution.style.display = 'none';
        button.textContent = 'Show Solution';
    }
}

// Load provider info when page loads
window.addEventListener('load', loadProviderInfo);
