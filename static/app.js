document.addEventListener('DOMContentLoaded', () => {
    addSpeedometerToBestMatch();
    addSimilarityMeters();
    animateOnScroll();
    setupFormAnimation();
    createBackgroundGrid();

    // ensure equal height AFTER layout settles
    setTimeout(equalizeResultHeights, 120);
});

/* ===============================
   BEST MATCH SPEEDOMETER (VISUAL)
================================ */
function addSpeedometerToBestMatch() {
    const li = document.querySelector('.best-match ul li');
    if (!li) return;

    const speedo = document.createElement('div');
    speedo.className = 'speedometer';
    speedo.innerHTML = `
        <svg viewBox="0 0 200 200">
            <path d="M30 100 A70 70 0 1 1 170 100"
                fill="none"
                stroke="rgba(255,255,255,0.08)"
                stroke-width="15"
                stroke-linecap="round"/>

            <path id="gaugeFill"
                d="M30 100 A70 70 0 1 1 170 100"
                fill="none"
                stroke="#ff3b3b"
                stroke-width="15"
                stroke-linecap="round"
                stroke-dasharray="0 440"
                style="transition: stroke-dasharray 1.6s ease-out"/>

            <line id="needle"
                x1="100" y1="100"
                x2="100" y2="42"
                stroke="#ffffff"
                stroke-width="3"
                style="transform-origin: 100px 100px;
                       transition: transform 1.6s ease-out"/>

            <circle cx="100" cy="100" r="6" fill="#ff3b3b"/>
        </svg>
    `;

    li.prepend(speedo);

    setTimeout(() => animateSpeedometer(88), 300);
}

function animateSpeedometer(value) {
    const fill = document.getElementById('gaugeFill');
    const needle = document.getElementById('needle');
    if (!fill || !needle) return;

    const arc = 440 * 0.75;
    fill.style.strokeDasharray = `${(value / 100) * arc} 440`;

    const rotation = -135 + (value / 100) * 270;
    needle.style.transform = `rotate(${rotation}deg)`;
}

/* ===============================
   RELATED MODELS — RING ONLY
================================ */
function addSimilarityMeters() {
    document.querySelectorAll('.related-models ul li').forEach((li, i) => {
        const strength = Math.max(60, 84 - i * 6);

        const meter = document.createElement('div');
        meter.className = 'mini-meter';
        meter.innerHTML = `
            <svg viewBox="0 0 70 70">
                <circle cx="35" cy="35" r="30"
                    fill="none"
                    stroke="rgba(255,59,59,0.2)"
                    stroke-width="6"/>
                <circle cx="35" cy="35" r="30"
                    fill="none"
                    stroke="#ff3b3b"
                    stroke-width="6"
                    stroke-dasharray="${(strength / 100) * 188} 188"
                    transform="rotate(-90 35 35)"
                    style="transition: stroke-dasharray 1.4s ease-out ${i * 0.12}s"/>
            </svg>
        `;

        li.prepend(meter);
        li.style.paddingLeft = '85px';
        li.style.position = 'relative';
    });
}

/* ===============================
   FORCE SAME HEIGHT
================================ */
function equalizeResultHeights() {
    const items = document.querySelectorAll(
        '.best-match ul li, .related-models ul li'
    );

    let max = 0;
    items.forEach(el => {
        el.style.height = 'auto';
        max = Math.max(max, el.offsetHeight);
    });

    items.forEach(el => {
        el.style.height = `${max}px`;
    });
}

/* ===============================
   EXISTING EFFECTS (UNCHANGED)
================================ */
function animateOnScroll() {
    const obs = new IntersectionObserver(entries => {
        entries.forEach(e => {
            if (e.isIntersecting) {
                e.target.style.opacity = '1';
                e.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.uploaded-model,.best-match,.related-models')
        .forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = '0.6s ease';
            obs.observe(el);
        });
}

function setupFormAnimation() {
    const form = document.querySelector('form');
    const btn = document.querySelector('button');
    if (!form || !btn) return;

    form.addEventListener('submit', () => {
        btn.innerHTML = '<span class="loading"></span> ANALYZING';
        btn.disabled = true;
    });
}

function createBackgroundGrid() {
    const grid = document.createElement('div');
    grid.style.cssText = `
        position:fixed; inset:0;
        pointer-events:none;
        opacity:0.03;
        z-index:0;
    `;
    document.body.prepend(grid);
}
