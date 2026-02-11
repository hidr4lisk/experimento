document.addEventListener('DOMContentLoaded', () => {
    const langToggle = document.getElementById('langToggle');
    let currentLang = 'es';

    const updateContent = (lang) => {
        document.querySelectorAll('[data-es]').forEach(el => {
            el.textContent = lang === 'es' ? el.getAttribute('data-es') : el.getAttribute('data-en');
        });
        
        // Handle images/placeholders if needed
        document.querySelectorAll('img[data-es]').forEach(img => {
            img.src = lang === 'es' ? img.getAttribute('data-es') : img.getAttribute('data-en');
        });
    };

    langToggle.addEventListener('click', (e) => {
        e.preventDefault();
        currentLang = currentLang === 'es' ? 'en' : 'es';
        langToggle.textContent = currentLang === 'es' ? 'English' : 'Español';
        updateContent(currentLang);
    });

    // Initial load
    updateContent(currentLang);
});
