// EduGenius - Hebrew RTL Educational Platform

// Show/hide loading indicator
function showLoading(show) {
    document.getElementById('loading').classList.toggle('show', show);
}

// Display result
function showResult(content, isError = false) {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = content;
    resultDiv.classList.add('show');
    if (isError) {
        resultDiv.classList.add('error');
    } else {
        resultDiv.classList.remove('error');
    }
    // Scroll to results
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Generate validation info HTML in Hebrew
function generateValidationHTML(validation) {
    if (!validation) return '';

    const confidenceColor = {
        'high': '#4caf50',
        'medium': '#ff9800',
        'low': '#f44336'
    }[validation.confidence_level] || '#757575';

    const confidenceText = {
        'high': 'גבוה',
        'medium': 'בינוני',
        'low': 'נמוך'
    }[validation.confidence_level] || 'לא ידוע';

    let html = `
        <div class="validation-info" style="background: #f5f5f5; padding: 20px; border-radius: 10px; margin: 20px 0; border-right: 4px solid ${confidenceColor};">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; flex-wrap: wrap;">
                <div style="margin-bottom: 10px;">
                    <strong>רמת אמינות התוכן:</strong>
                    <span style="color: ${confidenceColor}; font-weight: bold; font-size: 1.2em;">
                        ${confidenceText}
                    </span>
                    (${(validation.confidence_score * 100).toFixed(0)}%)
                </div>
                ${validation.has_reference_material ?
                    '<span style="color: #4caf50; font-weight: 600;">✓ אומת עם מקורות מהימנים</span>' :
                    '<span style="color: #ff9800; font-weight: 600;">⚠️ לא נמצאו מקורות התייחסות</span>'}
            </div>
    `;

    // Add warnings
    if (validation.validation_warnings && validation.validation_warnings.length > 0) {
        html += '<div style="margin-top: 15px; background: white; padding: 15px; border-radius: 8px;">';
        html += '<strong style="color: #ff9800;">⚠️ הערות חשובות:</strong>';
        validation.validation_warnings.forEach(warning => {
            // Translate common warnings to Hebrew
            let hebrewWarning = warning;
            if (warning.includes('AI-generated')) {
                hebrewWarning = '🤖 תוכן זה נוצר על ידי בינה מלאכותית ועלול להכיל שגיאות';
            } else if (warning.includes('No reference material')) {
                hebrewWarning = '📚 לא נמצא חומר התייחסות. מומלץ לבדוק מול מקורות נוספים';
            } else if (warning.includes('Low confidence')) {
                hebrewWarning = '⚠️ אמינות נמוכה: אנא אמתו את המידע מול מקורות אחרים';
            } else if (warning.includes('Medium confidence')) {
                hebrewWarning = '💡 אמינות בינונית: מומלץ לאמת עובדות מפתח';
            } else if (warning.includes('Always consult')) {
                hebrewWarning = '📖 תמיד התייעצו עם מקורות מרובים לתוכן חינוכי חשוב';
            }
            html += `<div style="font-size: 0.95em; color: #666; margin: 8px 0; padding: 5px 10px; background: #f9f9f9; border-radius: 5px;">• ${hebrewWarning}</div>`;
        });
        html += '</div>';
    }

    // Add references if available
    if (validation.references && validation.references.length > 0) {
        html += `
            <details style="margin-top: 15px;">
                <summary style="cursor: pointer; font-weight: 600; padding: 12px; background: white; border-radius: 8px; color: #667eea;">
                    📚 צפה במקורות המידע (${validation.references.length})
                </summary>
                <div style="margin-top: 15px; padding: 10px;">
        `;
        validation.references.forEach(ref => {
            html += `
                <div style="margin: 12px 0; padding: 15px; background: white; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                    <strong style="color: #333; font-size: 1.1em;">${ref.title}</strong><br>
                    <span style="font-size: 0.95em; color: #666; line-height: 1.5; display: block; margin: 8px 0;">${ref.summary}</span><br>
                    <a href="${ref.url}" target="_blank" style="color: #667eea; font-weight: 600; text-decoration: none;">קרא עוד ב-Wikipedia ←</a>
                </div>
            `;
        });
        html += '</div></details>';
    }

    html += '</div>';
    return html;
}

// Load provider information on page load
async function loadProviderInfo() {
    try {
        const response = await fetch('/api/providers');
        const data = await response.json();

        const availableProviders = Object.entries(data.providers)
            .filter(([_, available]) => available)
            .map(([name, _]) => name)
            .join(', ');

        const providerNames = {
            'deepseek': 'DeepSeek',
            'openai': 'OpenAI',
            'anthropic': 'Anthropic'
        };

        const providerInfo = document.getElementById('provider-info');
        providerInfo.innerHTML = `
            <strong>ספק ברירת המחדל:</strong> ${providerNames[data.default] || data.default.toUpperCase()} |
            <strong>ספקים זמינים:</strong> ${availableProviders || 'לא הוגדרו ספקים'}
        `;
    } catch (error) {
        console.error('Error loading provider info:', error);
    }
}

// Learning Unit Form Handler
document.getElementById('learning-unit-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    showLoading(true);

    const learningPrompt = document.getElementById('learning-prompt').value;
    const provider = document.getElementById('provider').value || null;

    const data = {
        prompt: learningPrompt,
        provider: provider
    };

    try {
        const response = await fetch('/api/learning-unit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || 'שגיאה ביצירת יחידת הלימוד');
        }

        // Build Hebrew results HTML
        let html = `
            <div class="provider-badge">נוצר על ידי: ${result.provider || 'לא ידוע'}</div>
            <h2 style="color: #667eea; margin-bottom: 20px;">📚 ${result.topic || 'יחידת לימוד'}</h2>
        `;

        // Add validation info
        if (result.validation) {
            html += generateValidationHTML(result.validation);
        }

        // Section 1: Explanation
        if (result.explanation) {
            html += `
                <div class="section-title">📖 הסבר מפורט</div>
                <div class="section-content" style="white-space: pre-wrap; line-height: 1.8;">
                    ${result.explanation}
                </div>
            `;
        }

        // Section 2: Quiz
        if (result.quiz && result.quiz.questions && result.quiz.questions.length > 0) {
            html += `<div class="section-title">✍️ מבחן (${result.quiz.questions.length} שאלות)</div>`;
            result.quiz.questions.forEach((q, index) => {
                html += `
                    <div class="quiz-question">
                        <h4>שאלה ${index + 1}: ${q.question}</h4>
                        <div class="options">
                            ${q.options.map(opt => `<div class="quiz-option">${opt}</div>`).join('')}
                        </div>
                        <div class="explanation" id="quiz-exp-${index}">
                            <strong>תשובה נכונה:</strong> ${q.correct_answer}<br>
                            <strong>הסבר:</strong> ${q.explanation}
                        </div>
                        <button class="btn-primary" onclick="toggleQuizAnswer(${index})" style="margin-top: 10px; padding: 10px 20px; font-size: 1em; width: auto;">הצג תשובה</button>
                    </div>
                `;
            });
        }

        // Section 3: Practice Problems
        if (result.practice && result.practice.length > 0) {
            html += `<div class="section-title">🎯 תרגילי תרגול (${result.practice.length})</div>`;
            result.practice.forEach((problem, index) => {
                html += `
                    <div class="practice-problem">
                        <h4>תרגיל ${index + 1}</h4>
                        <p style="font-size: 1.1em; line-height: 1.6;">${problem.problem}</p>
                `;

                if (problem.hints && problem.hints.length > 0) {
                    html += `
                        <div class="hints">
                            <h5>💡 רמזים:</h5>
                            <ul>${problem.hints.map(h => `<li>${h}</li>`).join('')}</ul>
                        </div>
                    `;
                }

                html += `
                        <div class="solution" id="practice-sol-${index}" style="display: none;">
                            <h5>✅ פתרון:</h5>
                            <p style="white-space: pre-wrap; line-height: 1.6;">${problem.solution}</p>
                        </div>
                        <button class="btn-primary" onclick="togglePracticeSolution(${index})" style="margin-top: 10px; padding: 10px 20px; font-size: 1em; width: auto;">הצג פתרון</button>
                    </div>
                `;
            });
        }

        // Section 4: Study Plan
        if (result.study_plan && result.study_plan.weeks && result.study_plan.weeks.length > 0) {
            html += `
                <div class="section-title">📅 תוכנית לימוד (${result.study_plan.weeks.length} שבועות)</div>
            `;

            result.study_plan.weeks.forEach(week => {
                html += `
                    <div class="section-content">
                        <h3 style="color: #667eea; margin-bottom: 15px;">שבוע ${week.week}: ${week.focus}</h3>
                        <div style="margin-bottom: 15px;">
                            <strong>נושאים:</strong>
                            <ul>${week.topics.map(t => `<li>${t}</li>`).join('')}</ul>
                        </div>
                        <div style="margin-bottom: 15px;">
                            <strong>פעילויות:</strong>
                            <ul>${week.activities.map(a => `<li>${a}</li>`).join('')}</ul>
                        </div>
                        <div>
                            <strong>יעדים:</strong>
                            <ul>${week.goals.map(g => `<li>${g}</li>`).join('')}</ul>
                        </div>
                    </div>
                `;
            });

            // Add resources and tips if available
            if (result.study_plan.resources && result.study_plan.resources.length > 0) {
                html += `
                    <div class="section-content">
                        <h4 style="color: #667eea; margin-bottom: 10px;">📚 מקורות מומלצים</h4>
                        <ul>${result.study_plan.resources.map(r => `<li>${r}</li>`).join('')}</ul>
                    </div>
                `;
            }

            if (result.study_plan.tips && result.study_plan.tips.length > 0) {
                html += `
                    <div class="section-content" style="background: #e8f5e9;">
                        <h4 style="color: #4caf50; margin-bottom: 10px;">💡 טיפים ללימוד</h4>
                        <ul>${result.study_plan.tips.map(t => `<li>${t}</li>`).join('')}</ul>
                    </div>
                `;
            }
        }

        showResult(html);
    } catch (error) {
        showResult(`
            <div style="text-align: center; padding: 30px;">
                <h3 style="color: #f44336; margin-bottom: 15px;">❌ שגיאה</h3>
                <p style="font-size: 1.1em;">${error.message}</p>
                <p style="margin-top: 15px; color: #666;">אנא בדוק את הגדרות ה-API ונסה שנית</p>
            </div>
        `, true);
    } finally {
        showLoading(false);
    }
});

// Toggle quiz answer visibility
function toggleQuizAnswer(index) {
    const explanation = document.getElementById(`quiz-exp-${index}`);
    const button = event.target;
    explanation.classList.toggle('show');
    button.textContent = explanation.classList.contains('show') ? 'הסתר תשובה' : 'הצג תשובה';
}

// Toggle practice solution visibility
function togglePracticeSolution(index) {
    const solution = document.getElementById(`practice-sol-${index}`);
    const button = event.target;
    if (solution.style.display === 'none') {
        solution.style.display = 'block';
        button.textContent = 'הסתר פתרון';
    } else {
        solution.style.display = 'none';
        button.textContent = 'הצג פתרון';
    }
}

// Load provider info when page loads
window.addEventListener('load', loadProviderInfo);
