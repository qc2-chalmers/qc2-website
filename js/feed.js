/* Grid / Feed view switch. A container with data-feed="<storage key>" turns into a
   full-screen snap-scrolling feed whose direct .feed-slide children are the posts. */
(function () {
  const feed = document.querySelector('[data-feed]');
  if (!feed) return;
  const key = feed.dataset.feed;
  const hadRow = feed.classList.contains('row');
  const buttons = document.querySelectorAll('.view-switch [data-view]');
  const slides = Array.from(feed.querySelectorAll(':scope > .feed-slide'));

  // Tag slides with the year of the preceding separator (used as a chip in the feed)
  let year = null;
  Array.from(feed.children).forEach(el => {
    if (el.classList.contains('year-separator')) year = el.textContent.trim();
    else if (year && el.firstElementChild) el.firstElementChild.dataset.year = year;
  });

  const ui = document.createElement('div');
  ui.className = 'feed-ui';
  ui.innerHTML = '<div class="feed-counter"></div>' +
    '<div class="feed-arrows"><button type="button" data-dir="-1" aria-label="Previous">▲</button>' +
    '<button type="button" data-dir="1" aria-label="Next">▼</button></div>';
  document.body.appendChild(ui);
  const counter = ui.querySelector('.feed-counter');

  const isOn = () => feed.classList.contains('feed-on');
  const move = dir => feed.scrollBy({ top: dir * feed.clientHeight, behavior: 'smooth' });
  const updateCounter = () => {
    const i = Math.min(slides.length - 1, Math.round(feed.scrollTop / feed.clientHeight));
    counter.textContent = (i + 1) + ' / ' + slides.length;
  };

  function setView(view) {
    const on = view === 'feed';
    feed.classList.toggle('feed-on', on);
    if (hadRow) feed.classList.toggle('row', !on);
    document.body.classList.toggle('feed-open', on);
    buttons.forEach(b => b.classList.toggle('active', b.dataset.view === view));
    feed.scrollTop = 0;
    if (on) { feed.focus(); updateCounter(); }
    try { localStorage.setItem(key, view); } catch (e) {}
  }

  buttons.forEach(b => b.addEventListener('click', () => setView(b.dataset.view)));
  ui.querySelectorAll('[data-dir]').forEach(b => b.addEventListener('click', () => move(+b.dataset.dir)));
  feed.addEventListener('scroll', () => { if (isOn()) updateCounter(); }, { passive: true });
  document.addEventListener('keydown', e => {
    if (!isOn()) return;
    if (e.key === 'Escape') setView('grid');
    else if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); move(e.key === 'ArrowDown' ? 1 : -1); }
  });

  feed.tabIndex = 0;
  let saved = null;
  try { saved = localStorage.getItem(key); } catch (e) {}
  if (saved === 'feed') setView('feed');
})();
