// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

let currentUser = null;
let editingMatchId = null;

// ============= Utility Functions =============

function showMessage(message, isError = false) {
    const messageArea = document.getElementById('message-area');
    messageArea.innerHTML = `<div class="alert ${isError ? 'alert-error' : 'alert-success'}">${message}</div>`;
    setTimeout(() => {
        messageArea.innerHTML = '';
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
    if (tabName === 'dashboard') {
        loadDashboard();
    } else if (tabName === 'matches') {
        loadMatches();
    } else if (tabName === 'results') {
        loadMatchesForResults();
    } else if (tabName === 'users') {
        loadUsers();
    }
}

function formatDate(dateString) {
    const date = new Date(dateString);
    // Times are already stored in IST, just format them
    return date.toLocaleString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
    });
}

function formatDateForInput(dateString) {
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${year}-${month}-${day}T${hours}:${minutes}`;
}

// ============= Authentication Check =============

async function checkAuth() {
    try {
        const response = await fetch(`${API_BASE_URL}/current-user`, {
            credentials: 'include'
        });
        
        if (response.ok) {
            const data = await response.json();
            currentUser = data;
            
            // Check if user is admin
            if (!currentUser.is_admin) {
                alert('Access denied. Admin privileges required.');
                window.location.href = 'index.html';
                return false;
            }
            return true;
        } else {
            alert('Please login first');
            window.location.href = 'index.html';
            return false;
        }
    } catch (error) {
        console.error('Auth check error:', error);
        alert('Error checking authentication');
        window.location.href = 'index.html';
        return false;
    }
}

// ============= Dashboard Functions =============

async function loadDashboard() {
    try {
        // Load statistics
        const [usersRes, matchesRes, leaderboardRes] = await Promise.all([
            fetch(`${API_BASE_URL}/leaderboard`),
            fetch(`${API_BASE_URL}/matches`),
            fetch(`${API_BASE_URL}/leaderboard`)
        ]);
        
        const users = await usersRes.json();
        const matches = await matchesRes.json();
        const leaderboard = await leaderboardRes.json();
        
        const completedMatches = matches.filter(m => m.is_finished).length;
        const totalPredictions = leaderboard.reduce((sum, user) => sum + user.predictions_made, 0);
        
        document.getElementById('total-users').textContent = users.length;
        document.getElementById('total-matches').textContent = matches.length;
        document.getElementById('completed-matches').textContent = completedMatches;
        document.getElementById('total-predictions').textContent = totalPredictions;
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showMessage('Error loading dashboard data', true);
    }
}

// ============= Match Management Functions =============

async function loadMatches() {
    try {
        const response = await fetch(`${API_BASE_URL}/matches`);
        const matches = await response.json();
        
        const matchesList = document.getElementById('matches-list');
        
        if (matches.length === 0) {
            matchesList.innerHTML = '<p>No matches found. Add your first match!</p>';
            return;
        }
        
        matchesList.innerHTML = matches.map(match => `
            <div class="match-card">
                <div class="match-header">
                    <div class="match-info">
                        <h3>${match.team_home} vs ${match.team_away}</h3>
                        <p>${formatDate(match.match_date)} - ${match.stage}</p>
                        <span class="badge ${match.is_finished ? 'badge-success' : 'badge-warning'}">
                            ${match.is_finished ? `Finished: ${match.home_score}-${match.away_score}` : 'Upcoming'}
                        </span>
                    </div>
                    <div class="match-actions">
                        <button class="btn btn-small" onclick="editMatch(${match.id})">Edit</button>
                        <button class="btn btn-small btn-danger" onclick="deleteMatch(${match.id})">Delete</button>
                    </div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading matches:', error);
        showMessage('Error loading matches', true);
    }
}

function showAddMatchModal() {
    editingMatchId = null;
    document.getElementById('modal-title').textContent = 'Add New Match';
    document.getElementById('match-form').reset();
    document.getElementById('match-id').value = '';
    document.getElementById('match-modal').classList.add('active');
}

function closeMatchModal() {
    document.getElementById('match-modal').classList.remove('active');
}

async function editMatch(matchId) {
    try {
        const response = await fetch(`${API_BASE_URL}/matches/${matchId}`);
        const match = await response.json();
        
        editingMatchId = matchId;
        document.getElementById('modal-title').textContent = 'Edit Match';
        document.getElementById('match-id').value = matchId;
        document.getElementById('team-home').value = match.team_home;
        document.getElementById('team-away').value = match.team_away;
        document.getElementById('match-date').value = formatDateForInput(match.match_date);
        document.getElementById('match-stage').value = match.stage;
        
        document.getElementById('match-modal').classList.add('active');
    } catch (error) {
        console.error('Error loading match:', error);
        showMessage('Error loading match details', true);
    }
}

async function deleteMatch(matchId) {
    if (!confirm('Are you sure you want to delete this match? This will also delete all predictions for this match.')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/matches/${matchId}`, {
            method: 'DELETE',
            credentials: 'include'
        });
        
        if (response.ok) {
            showMessage('Match deleted successfully');
            loadMatches();
        } else {
            const data = await response.json();
            showMessage(data.error || 'Failed to delete match', true);
        }
    } catch (error) {
        console.error('Error deleting match:', error);
        showMessage('Error deleting match', true);
    }
}

// ============= Match Form Submission =============

document.getElementById('match-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const matchId = document.getElementById('match-id').value;
    const matchData = {
        team_home: document.getElementById('team-home').value,
        team_away: document.getElementById('team-away').value,
        match_date: new Date(document.getElementById('match-date').value).toISOString(),
        stage: document.getElementById('match-stage').value
    };
    
    try {
        let response;
        if (matchId) {
            // Update existing match
            response = await fetch(`${API_BASE_URL}/matches/${matchId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(matchData)
            });
        } else {
            // Create new match
            response = await fetch(`${API_BASE_URL}/matches`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(matchData)
            });
        }
        
        if (response.ok) {
            showMessage(matchId ? 'Match updated successfully' : 'Match created successfully');
            closeMatchModal();
            loadMatches();
        } else {
            const data = await response.json();
            showMessage(data.error || 'Failed to save match', true);
        }
    } catch (error) {
        console.error('Error saving match:', error);
        showMessage('Error saving match', true);
    }
});

// ============= Results Management Functions =============

async function loadMatchesForResults() {
    try {
        const response = await fetch(`${API_BASE_URL}/matches`);
        const matches = await response.json();
        
        const resultsList = document.getElementById('results-list');
        
        // Filter to show only matches that haven't been finished or can be updated
        const relevantMatches = matches.filter(m => new Date(m.match_date) <= new Date());
        
        if (relevantMatches.length === 0) {
            resultsList.innerHTML = '<p>No matches available for result updates yet.</p>';
            return;
        }
        
        resultsList.innerHTML = relevantMatches.map(match => `
            <div class="match-card">
                <div class="match-header">
                    <div class="match-info">
                        <h3>${match.team_home} vs ${match.team_away}</h3>
                        <p>${formatDate(match.match_date)} - ${match.stage}</p>
                        ${match.is_finished ? `
                            <span class="badge badge-success">
                                Result: ${match.home_score}-${match.away_score}
                            </span>
                        ` : `
                            <span class="badge badge-warning">No result yet</span>
                        `}
                    </div>
                    <div class="match-actions">
                        <button class="btn btn-small" onclick="showResultModal(${match.id}, '${match.team_home}', '${match.team_away}', ${match.home_score}, ${match.away_score})">
                            ${match.is_finished ? 'Update Result' : 'Add Result'}
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading matches:', error);
        showMessage('Error loading matches', true);
    }
}

function showResultModal(matchId, teamHome, teamAway, homeScore, awayScore) {
    document.getElementById('result-match-id').value = matchId;
    document.getElementById('result-match-info').innerHTML = `
        <h3>${teamHome} vs ${teamAway}</h3>
    `;
    document.getElementById('home-team-label').textContent = `${teamHome} Score`;
    document.getElementById('away-team-label').textContent = `${teamAway} Score`;
    
    if (homeScore !== null && awayScore !== null) {
        document.getElementById('home-score').value = homeScore;
        document.getElementById('away-score').value = awayScore;
    } else {
        document.getElementById('home-score').value = '';
        document.getElementById('away-score').value = '';
    }
    
    document.getElementById('result-modal').classList.add('active');
}

function closeResultModal() {
    document.getElementById('result-modal').classList.remove('active');
}

document.getElementById('result-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const matchId = document.getElementById('result-match-id').value;
    const resultData = {
        home_score: parseInt(document.getElementById('home-score').value),
        away_score: parseInt(document.getElementById('away-score').value)
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/matches/${matchId}/result`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(resultData)
        });
        
        if (response.ok) {
            showMessage('Result updated and points calculated successfully!');
            closeResultModal();
            loadMatchesForResults();
            loadDashboard(); // Refresh stats
        } else {
            const data = await response.json();
            showMessage(data.error || 'Failed to update result', true);
        }
    } catch (error) {
        console.error('Error updating result:', error);
        showMessage('Error updating result', true);
    }
});

// ============= User Management Functions =============

async function loadUsers() {
    try {
        const response = await fetch(`${API_BASE_URL}/admin/users`, {
            credentials: 'include'
        });
        
        if (!response.ok) {
            throw new Error('Failed to load users');
        }
        
        const users = await response.json();
        
        const usersTableBody = document.getElementById('users-table-body');
        
        if (users.length === 0) {
            usersTableBody.innerHTML = '<tr><td colspan="7" style="text-align: center;">No users found</td></tr>';
            return;
        }
        
        usersTableBody.innerHTML = users.map(user => `
            <tr>
                <td><strong>${user.username}</strong></td>
                <td>${user.email}</td>
                <td>${user.is_admin ? '✓ Admin' : 'User'}</td>
                <td><strong>${user.total_points}</strong></td>
                <td>${user.predictions_count}</td>
                <td>${user.created_at ? formatDate(user.created_at) : 'N/A'}</td>
                <td>
                    <button class="btn btn-small" onclick="editUser(${user.id})">Edit</button>
                    <button class="btn btn-small" onclick="sendPasswordResetEmail(${user.id}, '${user.username}', '${user.email}')" style="background: #ffc107; color: black;">Reset Password</button>
                    <button class="btn btn-small btn-danger" onclick="deleteUser(${user.id})">Delete</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading users:', error);
        showMessage('Error loading users', true);
    }
}

async function editUser(userId) {
    try {
        const response = await fetch(`${API_BASE_URL}/admin/users/${userId}`, {
            credentials: 'include'
        });
        
        if (!response.ok) {
            throw new Error('Failed to load user');
        }
        
        const user = await response.json();
        
        const newUsername = prompt('Enter new username:', user.username);
        if (newUsername === null) return; // Cancelled
        
        const newEmail = prompt('Enter new email:', user.email);
        if (newEmail === null) return; // Cancelled
        
        const makeAdmin = confirm(`Make ${newUsername} an admin?`);
        
        const updateResponse = await fetch(`${API_BASE_URL}/admin/users/${userId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({
                username: newUsername,
                email: newEmail,
                is_admin: makeAdmin
            })
        });
        
        if (updateResponse.ok) {
            showMessage('User updated successfully');
            loadUsers();
        } else {
            const data = await updateResponse.json();
            showMessage(data.error || 'Failed to update user', true);
        }
    } catch (error) {
        console.error('Error updating user:', error);
        showMessage('Error updating user', true);
    }
}

async function deleteUser(userId) {
    if (!confirm('Are you sure you want to delete this user? This will also delete all their predictions.')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/admin/users/${userId}`, {
            method: 'DELETE',
            credentials: 'include'
        });
        
        if (response.ok) {
            showMessage('User deleted successfully');
            loadUsers();
            loadDashboard(); // Refresh stats
        } else {
            const data = await response.json();
            showMessage(data.error || 'Failed to delete user', true);
        }
    } catch (error) {
        console.error('Error deleting user:', error);
        showMessage('Error deleting user', true);
    }

async function sendPasswordResetEmail(userId, username, email) {
    if (!confirm(`Send password reset email to ${username} (${email})?`)) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/admin/users/${userId}/send-reset-email`, {
            method: 'POST',
            credentials: 'include'
        });
        
        if (response.ok) {
            const data = await response.json();
            showMessage(data.message || 'Password reset email sent successfully!');
        } else {
            const data = await response.json();
            showMessage(data.error || 'Failed to send reset email', true);
        }
    } catch (error) {
        console.error('Error sending reset email:', error);
        showMessage('Error sending reset email. Check email configuration.', true);
    }
}
}

async function resetUserPassword(userId) {
    const newPassword = prompt('Enter new password for user:');
    if (!newPassword) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/admin/users/${userId}/reset-password`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({ new_password: newPassword })
        });
        
        if (response.ok) {
            showMessage('Password reset successfully');
        } else {
            const data = await response.json();
            showMessage(data.error || 'Failed to reset password', true);
        }
    } catch (error) {
        console.error('Error resetting password:', error);
        showMessage('Error resetting password', true);
    }
}

// ============= Initialize =============

async function init() {
    const isAuthenticated = await checkAuth();
    if (isAuthenticated) {
        loadDashboard();
    }
}

// Run initialization
init();

// Made with Bob
