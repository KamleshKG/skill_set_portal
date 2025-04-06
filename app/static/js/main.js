document.addEventListener('DOMContentLoaded', function() {
    // Flash message auto-hide
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            alert.style.transition = 'opacity 1s';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 1000);
        });
    }, 3000);

    // Skill level selector enhancement
    document.querySelectorAll('.skill-level-select').forEach(select => {
        select.addEventListener('change', function() {
            const badge = this.parentElement.querySelector('.level-badge');
            badge.textContent = `Level ${this.value}`;
            badge.className = `badge bg-${this.value > 3 ? 'success' : 'warning'}`;
        });
    });
});