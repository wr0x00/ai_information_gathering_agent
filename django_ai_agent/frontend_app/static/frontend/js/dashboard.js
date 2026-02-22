// Dashboard JavaScript for the AI Information Gathering Agent

// Language translations
const translations = {
    en: {
        "total-scans-label": "Total Scans",
        "active-scans-label": "Active Scans",
        "generated-reports-label": "Generated Reports",
        "saved-configs-label": "Saved Configurations",
        "recent-activity-label": "Recent Activity",
        "loading-text": "Loading recent activity...",
        "no-activity": "No recent activity",
        "scan-action": "Started scan on",
        "report-action": "Generated report for",
        "config-action": "Updated configuration settings"
    },
    zh: {
        "total-scans-label": "总扫描数",
        "active-scans-label": "活动扫描",
        "generated-reports-label": "生成报告",
        "saved-configs-label": "保存配置",
        "recent-activity-label": "最近活动",
        "loading-text": "正在加载最近活动...",
        "no-activity": "没有最近活动",
        "scan-action": "开始扫描",
        "report-action": "生成报告给",
        "config-action": "更新配置设置"
    }
};

// Apply language translation
function applyLanguage(language) {
    // Update elements with translations
    const elements = Object.keys(translations.en);
    elements.forEach(elementId => {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = translations[language][elementId];
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    // Apply language on page load
    const preferredLanguage = localStorage.getItem('preferredLanguage') || 'en';
    applyLanguage(preferredLanguage);

    // Initialize dashboard
    initializeDashboard();

    // Set up event listeners for navigation
    setupNavigation();

    // Load initial data
    loadDashboardData();
});

function initializeDashboard() {
    console.log('Initializing AI Agent Dashboard...');

    // Set up any initial UI elements
    const dashboardRoot = document.getElementById('dashboard-root');
    if (dashboardRoot) {
        dashboardRoot.classList.add('loaded');
    }
}

function setupNavigation() {
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            navigateToSection(targetId);
        });
    });
}

function navigateToSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('main > section');
    sections.forEach(section => {
        section.style.display = 'none';
    });

    // Show the target section
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.style.display = 'block';
    }

    // Update active nav item
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').substring(1) === sectionId) {
            link.classList.add('active');
        }
    });
}

function loadDashboardData() {
    // Simulate loading data
    setTimeout(() => {
        updateStatistics({
            totalScans: 12,
            activeScans: 3,
            generatedReports: 8,
            savedConfigs: 5
        });

        // Get preferred language for activity list
        const preferredLanguage = localStorage.getItem('preferredLanguage') || 'en';

        updateActivityList([
            { time: '2026-02-23 01:30:00', action: translations[preferredLanguage]['scan-action'] + ' example.com' },
            { time: '2026-02-23 01:15:00', action: translations[preferredLanguage]['report-action'] + ' test.org' },
            { time: '2026-02-23 00:45:00', action: translations[preferredLanguage]['config-action'] }
        ]);
    }, 1000);
}

function updateStatistics(stats) {
    document.getElementById('total-scans').textContent = stats.totalScans;
    document.getElementById('active-scans').textContent = stats.activeScans;
    document.getElementById('generated-reports').textContent = stats.generatedReports;
    document.getElementById('saved-configs').textContent = stats.savedConfigs;
}

function updateActivityList(activities) {
    const activityList = document.getElementById('activity-list');
    const preferredLanguage = localStorage.getItem('preferredLanguage') || 'en';

    if (activities.length === 0) {
        activityList.innerHTML = `<p>${translations[preferredLanguage]['no-activity']}</p>`;
        return;
    }

    let html = '<ul>';
    activities.forEach(activity => {
        html += `<li><strong>${activity.time}</strong>: ${activity.action}</li>`;
    });
    html += '</ul>';

    activityList.innerHTML = html;
}

// Simulate real-time updates
setInterval(() => {
    // This would normally fetch real data from the server
    console.log('Refreshing dashboard data...');
}, 30000);