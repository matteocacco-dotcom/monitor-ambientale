fetch('data.json')
  .then(res => {
    if (!res.ok) throw new Error('Risposta non valida: ' + res.status);
    return res.json();
  })
  .then(data => {
    const lastUpdate = document.getElementById('last-update');
    if (data.updated_at) {
      const date = new Date(data.updated_at);
      lastUpdate.textContent = 'Ultimo aggiornamento: ' + date.toLocaleString('it-IT');
    } else {
      lastUpdate.textContent = 'Nessun aggiornamento ancora disponibile.';
    }

    const container = document.getElementById('projects');
    container.innerHTML = '';

    if (!data.projects || data.projects.length === 0) {
      container.textContent = 'Nessun progetto trovato.';
      return;
    }

    data.projects.forEach(p => {
      const card = document.createElement('article');
      card.className = 'card';

      const title = document.createElement('h2');
      title.textContent = p.title;

      const summary = document.createElement('p');
      summary.textContent = p.summary;

      const link = document.createElement('a');
      link.href = p.url;
      link.target = '_blank';
      link.rel = 'noopener';
      link.textContent = "Leggi l'articolo";

      card.append(title, summary, link);
      container.appendChild(card);
    });
  })
  .catch(err => {
    document.getElementById('projects').textContent = 'Errore nel caricamento dei dati.';
    console.error(err);
  });