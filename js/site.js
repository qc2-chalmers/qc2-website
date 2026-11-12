// Shared behaviour for every page: button glow follows the cursor.
document.querySelectorAll('.sw-btn, .btn-qc2, .blog-more, .btn-profile, .btn-outline-primary, .btn-outline-secondary').forEach(btn => {
  btn.addEventListener('pointermove', e => {
    const r = btn.getBoundingClientRect()
    btn.style.setProperty('--mx', (e.clientX - r.left) + 'px')
    btn.style.setProperty('--my', (e.clientY - r.top) + 'px')
  })
})

// Desktop dropdowns open on hover; a click must not leave one stuck open next to another.
{
  const desktop = window.matchMedia('(min-width: 992px)')
  document.querySelectorAll('.nav-group').forEach(group => {
    const toggle = group.querySelector('.dropdown-toggle')
    const closeNow = () => {
      if (!desktop.matches || !window.bootstrap) return
      const dd = window.bootstrap.Dropdown.getInstance(toggle)
      if (dd) dd.hide()
      toggle.blur()
    }
    group.addEventListener('mouseleave', closeNow)
  })
  // on desktop the toggle is hover-driven: stop Bootstrap from toggling it on click
  document.querySelectorAll('.nav-group > .dropdown-toggle').forEach(toggle => {
    toggle.addEventListener('click', e => { if (desktop.matches) { e.preventDefault(); e.stopImmediatePropagation() } }, true)
  })
}

// Mobile menu: links to a section of the page (e.g. "Jobs") close the menu first,
// otherwise the open offcanvas keeps the page scroll locked and nothing seems to happen.
document.querySelectorAll('.site-menu a[href*="#"]:not(.dropdown-toggle)').forEach(link => {
  link.addEventListener('click', e => {
    const menu = document.querySelector('.site-menu.show')
    if (!menu || !window.bootstrap) return
    e.preventDefault()
    menu.addEventListener('hidden.bs.offcanvas', () => { window.location.href = link.href }, { once: true })
    window.bootstrap.Offcanvas.getOrCreateInstance(menu).hide()
  })
})
