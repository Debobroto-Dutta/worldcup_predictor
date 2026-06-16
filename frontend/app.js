// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

let currentUser = null;

// ============= Utility Functions =============

function showMessage(elementId, message, isError = false) {
    const element = document.getElementById(elementId);
    element.innerHTML = `<div class="alert ${isError ? 'alert-error' : 'alert-success'}">${message}</div>`;
    setTimeout(() => {
        element.innerHTML = '';
    }, 5000);
}

function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active class from all nav tabs
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(`${tabName}-tab`).classList.add('active');
    
    // Add active class to clicked nav tab
    event.target.classList.add('active');
    
    // Load data for the tab
    if (tabName === 'matches' && currentUser) {
        loadMatches();
    } else if (tabName === 'predictions' && currentUser) {
        loadMyPredictions();
    } else if (tabName === 'leaderboard') {
        loadLeaderboard();
    }
}

function formatDate(dateString) {
    const date = new Date(dateString);
    // Times are already stored in IST, just format them
    return date.toLocaleString('en-IN', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
    });
}

// ============= Authentication Functions =============

function showRegisterForm() {
    document.getElementById('login-form').parentElement.classList.add('hidden');
    document.getElementById('register-form-container').classList.remove('hidden');
}

function showLoginForm() {
    document.getElementById('register-form-container').classList.add('hidden');
    document.getElementById('login-form').parentElement.classList.remove('hidden');
}

async function login(username, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentUser = data.user;
            showMessage('login-message', 'Login successful!');
            setTimeout(() => {
                updateUIForLoggedInUser();
                showTab('matches');
            }, 1000);
        } else {
            showMessage('login-message', data.error || 'Login failed', true);
        }
    } catch (error) {
        showMessage('login-message', 'Network error. Please try again.', true);
        console.error('Login error:', error);
    }
}

async function register(username, email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showMessage('register-message', 'Registration successful! Please login.');
            setTimeout(() => {
                showLoginForm();
            }, 2000);
        } else {
            showMessage('register-message', data.error || 'Registration failed', true);
        }
    } catch (error) {
        showMessage('register-message', 'Network error. Please try again.', true);
        console.error('Registration error:', error);
    }
}

async function logout() {
    try {
        await fetch(`${API_BASE_URL}/logout`, {
            method: 'POST',
            credentials: 'include'
        });
        
        currentUser = null;
        updateUIForLoggedOutUser();
        showTab('login');
    } catch (error) {
        console.error('Logout error:', error);
    }
}

function updateUIForLoggedInUser() {
    document.getElementById('user-info').classList.remove('hidden');
    document.getElementById('username-display').textContent = currentUser.username;
    loadCurrentUser();
}

function updateUIForLoggedOutUser() {
    document.getElementById('user-info').classList.add('hidden');
    document.getElementById('login-username').value = '';
    document.getElementById('login-password').value = '';
}

async function loadCurrentUser() {
    try {
        const response = await fetch(`${API_BASE_URL}/current-user`, {
            credentials: 'include'
        });
        
        if (response.ok) {
            const data = await response.json();
            document.getElementById('points-display').textContent = data.total_points;
        }
    } catch (error) {
        console.error('Error loading user data:', error);
    }
}

// ============= Match Functions =============

async function loadMatches() {
    try {
        const response = await fetch(`${API_BASE_URL}/matches`);
        const matches = await response.json();
        
        // Also fetch user's predictions
        const predictionsResponse = await fetch(`${API_BASE_URL}/predictions/my`, {
            credentials: 'include'
        });
        const userPredictions = predictionsResponse.ok ? await predictionsResponse.json() : [];
        
        const matchesList = document.getElementById('matches-list');
        
        if (matches.length === 0) {
            matchesList.innerHTML = '<p>No matches available yet.</p>';
            return;
        }
        
        matchesList.innerHTML = matches.map(match => {
            const matchDate = new Date(match.match_date);
            const now = new Date();
            const hasStarted = matchDate <= now;
            const canPredict = !hasStarted && !match.is_finished;
            
            // Find existing prediction for this match
            const existingPrediction = userPredictions.find(p => p.match_id === match.id);
            
            return `
                <div class="match-card">
                    <div class="match-header">
                        <span class="badge ${match.is_finished ? 'badge-success' : hasStarted ? 'badge-danger' : 'badge-warning'}">
                            ${match.is_finished ? 'Finished' : hasStarted ? 'In Progress' : match.stage}
                        </span>
                        <span>${formatDate(match.match_date)}</span>
                    </div>
                    
                    <div class="match-teams">
                        <div class="team">${match.team_home}</div>
                        <div class="vs">VS</div>
                        <div class="team">${match.team_away}</div>
                    </div>
                    
                    ${match.is_finished ? `
                        <div style="text-align: center; font-size: 1.5em; font-weight: bold; color: #667eea;">
                            Final Score: ${match.home_score} - ${match.away_score}
                        </div>
                        ${existingPrediction ? `
                            <div style="text-align: center; margin-top: 10px; color: #666;">
                                Your Prediction: ${existingPrediction.predicted_home_score} - ${existingPrediction.predicted_away_score}
                                <span class="badge ${existingPrediction.points_earned === 3 ? 'badge-success' :
                                                   existingPrediction.points_earned === 1 ? 'badge-warning' : 'badge-danger'}">
                                    ${existingPrediction.points_earned === 3 ? '+3 points' :
                                      existingPrediction.points_earned === 1 ? '+1 point' : '0 points'}
                                </span>
                            </div>
                        ` : ''}
                    ` : canPredict ? `
                        ${existingPrediction ? `
                            <div style="text-align: center; margin-bottom: 10px; color: #667eea;">
                                Current Prediction: ${existingPrediction.predicted_home_score} - ${existingPrediction.predicted_away_score}
                                <br><small style="color: #999;">You can update until match starts</small>
                            </div>
                        ` : ''}
                        <div class="prediction-inputs">
                            <input type="number" class="score-input" id="home-score-${match.id}"
                                   min="0" max="20" placeholder="0"
                                   value="${existingPrediction ? existingPrediction.predicted_home_score : ''}">
                            <span style="font-size: 1.5em;">-</span>
                            <input type="number" class="score-input" id="away-score-${match.id}"
                                   min="0" max="20" placeholder="0"
                                   value="${existingPrediction ? existingPrediction.predicted_away_score : ''}">
                        </div>
                        <button class="btn" onclick="submitPrediction(${match.id})">
                            ${existingPrediction ? 'Update Prediction' : 'Submit Prediction'}
                        </button>
                    ` : `
                        <div style="text-align: center; color: #999;">
                            ${hasStarted ? 'Match has started - Predictions closed' : 'Predictions closed'}
                        </div>
                        ${existingPrediction ? `
                            <div style="text-align: center; margin-top: 10px; color: #667eea;">
                                Your Prediction: ${existingPrediction.predicted_home_score} - ${existingPrediction.predicted_away_score}
                            </div>
                        ` : ''}
                    `}
                </div>
            `;
        }).join('');
    } catch (error) {
        console.error('Error loading matches:', error);
        document.getElementById('matches-list').innerHTML =
            '<p class="alert alert-error">Error loading matches. Please try again.</p>';
    }
}

async function submitPrediction(matchId) {
    const homeScore = document.getElementById(`home-score-${matchId}`).value;
    const awayScore = document.getElementById(`away-score-${matchId}`).value;
    
    if (homeScore === '' || awayScore === '') {
        alert('Please enter both scores');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/predictions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({
                match_id: matchId,
                predicted_home_score: parseInt(homeScore),
                predicted_away_score: parseInt(awayScore)
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('Prediction submitted successfully!');
            loadMatches();
            loadCurrentUser();
        } else {
            alert(data.error || 'Failed to submit prediction');
        }
    } catch (error) {
        console.error('Error submitting prediction:', error);
        alert('Network error. Please try again.');
    }
}

// ============= Predictions Functions =============

async function loadMyPredictions() {
    try {
        const response = await fetch(`${API_BASE_URL}/predictions/my`, {
            credentials: 'include'
        });
        
        const predictions = await response.json();
        const predictionsList = document.getElementById('predictions-list');
        
        if (predictions.length === 0) {
            predictionsList.innerHTML = '<p>You haven\'t made any predictions yet.</p>';
            return;
        }
        
        predictionsList.innerHTML = predictions.map(pred => `
            <div class="match-card">
                <div class="match-teams">
                    <div class="team">${pred.team_home}</div>
                    <div class="vs">VS</div>
                    <div class="team">${pred.team_away}</div>
                </div>
                
                <div style="text-align: center; margin: 15px 0;">
                    <strong>Your Prediction:</strong> 
                    <span style="font-size: 1.3em; color: #667eea;">
                        ${pred.predicted_home_score} - ${pred.predicted_away_score}
                    </span>
                </div>
                
                ${pred.match_finished ? `
                    <div style="text-align: center;">
                        <span class="badge ${pred.points_earned === 3 ? 'badge-success' : 
                                           pred.points_earned === 1 ? 'badge-warning' : 'badge-danger'}">
                            ${pred.points_earned === 3 ? '🎯 Exact Score! +3 points' :
                              pred.points_earned === 1 ? '✓ Correct Winner! +1 point' :
                              '✗ No points'}
                        </span>
                    </div>
                ` : `
                    <div style="text-align: center; color: #999;">
                        Match not finished yet
                    </div>
                `}
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading predictions:', error);
        document.getElementById('predictions-list').innerHTML = 
            '<p class="alert alert-error">Error loading predictions. Please try again.</p>';
    }
}

// ============= Leaderboard Functions =============

async function loadLeaderboard() {
    try {
        const response = await fetch(`${API_BASE_URL}/leaderboard`);
        const leaderboard = await response.json();
        
        const leaderboardBody = document.getElementById('leaderboard-body');
        
        if (leaderboard.length === 0) {
            leaderboardBody.innerHTML = '<tr><td colspan="6" style="text-align: center;">No data yet</td></tr>';
            return;
        }
        
        leaderboardBody.innerHTML = leaderboard.map(entry => {
            let rankClass = '';
            if (entry.rank === 1) rankClass = 'rank-1';
            else if (entry.rank === 2) rankClass = 'rank-2';
            else if (entry.rank === 3) rankClass = 'rank-3';
            
            return `
                <tr class="${rankClass}">
                    <td><strong>${entry.rank}</strong></td>
                    <td>${entry.username}</td>
                    <td><strong>${entry.total_points}</strong></td>
                    <td>${entry.correct_winners}</td>
                    <td>${entry.exact_scores}</td>
                    <td>${entry.predictions_made}</td>
                </tr>
            `;
        }).join('');
    } catch (error) {
        console.error('Error loading leaderboard:', error);
        document.getElementById('leaderboard-body').innerHTML = 
            '<tr><td colspan="6" class="alert alert-error">Error loading leaderboard</td></tr>';
    }
}

// ============= Event Listeners =============

document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    await login(username, password);
});

document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    await register(username, email, password);
});

// ============= Initialize =============

// Load leaderboard on page load (public data)
loadLeaderboard();

// Made with Bob
