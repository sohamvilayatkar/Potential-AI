/**
 * POTENTIAL AI - College Information Explorer Interactivity
 * Handles tab navigation, department filtering, document checklist searches,
 * and dynamic academic links.
 */

function switchCollegeTab(evt, tabId) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));
    if (evt && evt.currentTarget) {
        evt.currentTarget.classList.add('active');
    }
    const pane = document.getElementById(tabId);
    if (pane) {
        pane.classList.add('active');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Check if URL hash has a specific tab
    const hash = window.location.hash.replace('#', '');
    if (hash && document.getElementById(hash)) {
        const matchingBtn = document.querySelector(`[onclick*="${hash}"]`);
        if (matchingBtn) {
            matchingBtn.click();
        }
    }
});
