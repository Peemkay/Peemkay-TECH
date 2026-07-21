"""A small hand-rolled inline-SVG icon set.

Keeping icons inline (rather than an icon-font or CDN) means the site has
zero external runtime dependencies for its UI chrome — it keeps rendering
correctly even if a visitor's browser blocks third-party requests.
"""
from markupsafe import Markup

ICONS = {
    "shield": '<path d="M12 3l7 3v5c0 5-3 8.5-7 10-4-1.5-7-5-7-10V6z"/>',
    "layers": '<polygon points="12 3 21 8 12 13 3 8"/><polyline points="3 12 12 17 21 12"/><polyline points="3 16 12 21 21 16"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><line x1="3" y1="12" x2="21" y2="12"/>',
    "check-circle": '<circle cx="12" cy="12" r="9"/><polyline points="8 12.5 11 15.5 16 9"/>',
    "code": '<polyline points="9 8 4 12 9 16"/><polyline points="15 8 20 12 15 16"/>',
    "eye": '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/>',
    "database": '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
    "cpu": '<rect x="6" y="6" width="12" height="12" rx="2"/><rect x="10" y="10" width="4" height="4"/><line x1="12" y1="1" x2="12" y2="4"/><line x1="12" y1="20" x2="12" y2="23"/><line x1="1" y1="12" x2="4" y2="12"/><line x1="20" y1="12" x2="23" y2="12"/>',
    "tool": '<circle cx="7" cy="17" r="3"/><path d="M9.5 14.5 18 6a2.1 2.1 0 0 0-3-3l-8.5 8.5"/>',
    "shopping-bag": '<path d="M6 8h12l-1 12H7z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>',
    "smartphone": '<rect x="7" y="2" width="10" height="20" rx="2"/><line x1="11" y1="18" x2="13" y2="18"/>',
    "git-merge": '<circle cx="7" cy="6" r="2.5"/><circle cx="7" cy="18" r="2.5"/><circle cx="17" cy="6" r="2.5"/><path d="M7 8.5V15.5"/><path d="M17 8.5c0 5-6 5-8 7"/>',
    "life-buoy": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3.5"/><line x1="5" y1="5" x2="9" y2="9"/><line x1="15" y1="15" x2="19" y2="19"/><line x1="19" y1="5" x2="15" y2="9"/><line x1="9" y1="15" x2="5" y2="19"/>',
    "book-open": '<path d="M12 6c-2-1.5-5-2-8-1.5v13c3-0.5 6 0 8 1.5 2-1.5 5-2 8-1.5v-13c-3-0.5-6 0-8 1.5z"/><line x1="12" y1="6" x2="12" y2="19"/>',
    "briefcase": '<rect x="3" y="8" width="18" height="12" rx="2"/><path d="M8 8V6a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>',
    "music": '<circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/><path d="M9 18V5l12-2v13"/>',
    "activity": '<polyline points="2 12 7 12 9 18 14 6 16 12 22 12"/>',
    "credit-card": '<rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/>',
    "trending-up": '<polyline points="3 17 9 11 13 15 21 6"/><polyline points="15 6 21 6 21 12"/>',
    "menu": '<line x1="4" y1="7" x2="20" y2="7"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="17" x2="20" y2="17"/>',
    "x": '<line x1="6" y1="6" x2="18" y2="18"/><line x1="6" y1="18" x2="18" y2="6"/>',
    "arrow-right": '<line x1="4" y1="12" x2="20" y2="12"/><polyline points="13 5 20 12 13 19"/>',
    "arrow-up": '<line x1="12" y1="20" x2="12" y2="4"/><polyline points="5 11 12 4 19 11"/>',
    "external-link": '<path d="M14 4h6v6"/><line x1="20" y1="4" x2="10" y2="14"/><path d="M18 14v5a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h5"/>',
    "github": '<path d="M12 2C6.5 2 2 6.6 2 12.2c0 4.5 2.9 8.3 6.8 9.6.5.1.7-.2.7-.5v-1.8c-2.8.6-3.4-1.3-3.4-1.3-.4-1.1-1-1.4-1-1.4-.9-.6.1-.6.1-.6 1 .1 1.5 1 1.5 1 .9 1.5 2.3 1.1 2.9.8.1-.7.4-1.1.6-1.4-2.2-.2-4.6-1.1-4.6-5 0-1.1.4-2 1-2.7-.1-.2-.5-1.3.1-2.7 0 0 .8-.3 2.7 1a9.4 9.4 0 0 1 5 0c1.9-1.3 2.7-1 2.7-1 .6 1.4.2 2.5.1 2.7.6.7 1 1.6 1 2.7 0 3.9-2.4 4.8-4.6 5 .4.3.7.9.7 1.9v2.8c0 .3.2.6.7.5 3.9-1.3 6.8-5.1 6.8-9.6C22 6.6 17.5 2 12 2z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><polyline points="2 6 12 13 22 6"/>',
    "map-pin": '<path d="M12 22s7-6.5 7-12a7 7 0 1 0-14 0c0 5.5 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
    "send": '<line x1="21" y1="3" x2="10" y2="14"/><polygon points="21 3 14 21 10 14 3 10"/>',
    "chevron-down": '<polyline points="5 8 12 15 19 8"/>',
    "terminal": '<polyline points="5 7 10 12 5 17"/><line x1="12" y1="17" x2="19" y2="17"/>',
    "phone": '<path d="M6 3h4l1 5-2.5 2a12 12 0 0 0 5.5 5.5l2-2.5 5 1v4a2 2 0 0 1-2 2A17 17 0 0 1 4 5a2 2 0 0 1 2-2z"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><polyline points="12 7 12 12 16 14"/>',
    "award": '<circle cx="12" cy="8" r="5"/><polyline points="8.5 12.5 7 22 12 19 17 22 15.5 12.5"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2"/>',
    "lock": '<rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17" cy="9" r="2.6"/><path d="M15 14.2c2.3.4 4 2.3 4 4.8"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><line x1="3" y1="10" x2="21" y2="10"/><line x1="8" y1="3" x2="8" y2="7"/><line x1="16" y1="3" x2="16" y2="7"/>',
    "star": '<polygon points="12 2 15 9 22 9.5 17 14.5 18.5 22 12 18 5.5 22 7 14.5 2 9.5 9 9"/>',
}


def render_icon(name, css_class="icon", size=24):
    inner = ICONS.get(name, ICONS["star"])
    return Markup(
        '<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
        'stroke-linejoin="round" aria-hidden="true">{inner}</svg>'
    ).format(cls=css_class, size=size, inner=Markup(inner))
