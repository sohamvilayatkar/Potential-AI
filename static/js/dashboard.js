/**
 * POTENTIAL AI - Dashboard Auto-Refresh Logic
 */

document.addEventListener('DOMContentLoaded', () => {
    // Periodically fetch updated stats every 15 seconds
    setInterval(refreshDashboardData, 15000);
});

async function refreshDashboardData() {
    try {
        const res = await fetch('/api/dashboard/data');
        if (!res.ok) return;
        const data = await res.json();

        if (data.summary) {
            const s = data.summary;
            document.getElementById('statTotal').textContent = s.total_queries;
            document.getElementById('statSuccess').textContent = s.success_rate + '%';
            document.getElementById('statConf').textContent = s.average_confidence + '%';
            document.getElementById('statTop').textContent = s.top_intent;
        }

        if (data.chart_base64) {
            const chartImg = document.getElementById('dashboardChart');
            if (chartImg) {
                chartImg.src = `data:image/png;base64,${data.chart_base64}`;
            }
        }
    } catch (e) {
        console.warn("Dashboard auto-refresh paused:", e);
    }
}
