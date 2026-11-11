// Shared behaviour for every page: button glow follows the cursor.
document.querySelectorAll('.sw-btn, .btn-qc2, .blog-more, .btn-profile, .btn-outline-primary, .btn-outline-secondary').forEach(btn => {
  btn.addEventListener('pointermove', e => {
    const r = btn.getBoundingClientRect()
    btn.style.setProperty('--mx', (e.clientX - r.left) + 'px')
    btn.style.setProperty('--my', (e.clientY - r.top) + 'px')
  })
})
