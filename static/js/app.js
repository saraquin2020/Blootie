document.addEventListener('DOMContentLoaded', function () {
  const board = document.getElementById('memoryBoard');
  if (!board) return;
  const cards = Array.from(board.querySelectorAll('.memory-card'));
  cards.sort(() => Math.random() - 0.5);
  cards.forEach(card => board.appendChild(card));
  let opened = [];
  let lock = false;
  cards.forEach(card => {
    card.addEventListener('click', () => {
      if (lock || card.classList.contains('matched') || opened.includes(card)) return;
      card.textContent = card.dataset.value;
      card.classList.add('open');
      opened.push(card);
      if (opened.length === 2) {
        lock = true;
        const [a,b] = opened;
        if (a.dataset.value === b.dataset.value) {
          a.classList.add('matched');
          b.classList.add('matched');
          opened = [];
          lock = false;
        } else {
          setTimeout(() => {
            a.textContent = '?';
            b.textContent = '?';
            a.classList.remove('open');
            b.classList.remove('open');
            opened = [];
            lock = false;
          }, 700);
        }
      }
    });
  });
});
