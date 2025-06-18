document.addEventListener('DOMContentLoaded', () => {
  // Находим все контейнеры, в которых указан data-content-url
  const bodies = document.querySelectorAll('.accordion-body[data-content-url]');

  bodies.forEach(body => {
    const url = body.getAttribute('data-content-url');
    const collapseEl = body.closest('.accordion-collapse');

    // Обработчик открытия аккордеона
    collapseEl.addEventListener('show.bs.collapse', async () => {
      // Если уже загружали — пропускаем
      if (body.dataset.loaded) return;

      try {
        const resp = await fetch(url);
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const html = await resp.text();
        body.innerHTML = html;
        body.dataset.loaded = 'true';
      } catch (err) {
        console.error('Error loading accordion content:', err);
        body.innerHTML = '<p class="text-danger">Не удалось загрузить контент.</p>';
      }
    });
  });
});
