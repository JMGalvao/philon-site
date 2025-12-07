// initialization

const RESPONSIVE_WIDTH = 1024

let headerWhiteBg = false
let isHeaderCollapsed = window.innerWidth < RESPONSIVE_WIDTH
const collapseBtn = document.getElementById("collapse-btn")
const collapseHeaderItems = document.getElementById("collapsed-header-items")



function onHeaderClickOutside(e) {

    if (!collapseHeaderItems.contains(e.target)) {
        toggleHeader()
    }

}


function toggleHeader() {
    if (isHeaderCollapsed) {
        // collapseHeaderItems.classList.remove("max-md:tw-opacity-0")
        collapseHeaderItems.classList.add("opacity-100",)
        collapseHeaderItems.style.width = "60vw"
        collapseBtn.classList.remove("bi-list")
        collapseBtn.classList.add("bi-x", "max-lg:tw-fixed")
        isHeaderCollapsed = false

        setTimeout(() => window.addEventListener("click", onHeaderClickOutside), 1)

    } else {
        collapseHeaderItems.classList.remove("opacity-100")
        collapseHeaderItems.style.width = "0vw"
        collapseBtn.classList.remove("bi-x", "max-lg:tw-fixed")
        collapseBtn.classList.add("bi-list")
        isHeaderCollapsed = true
        window.removeEventListener("click", onHeaderClickOutside)

    }
}

function responsive() {
    if (window.innerWidth > RESPONSIVE_WIDTH) {
        collapseHeaderItems.style.width = ""

    } else {
        isHeaderCollapsed = true
    }
}

window.addEventListener("resize", responsive)


/**
 * Animations
 */

gsap.registerPlugin(ScrollTrigger)


gsap.to(".reveal-up", {
    opacity: 0,
    y: "100%",
})

gsap.to("#dashboard", {
    boxShadow: "0px 15px 25px -5px #7e22ceaa",
    duration: 0.3,
    scrollTrigger: {
        trigger: "#hero-section",
        start: "60% 60%",
        end: "80% 80%",
        // markers: true
    }

})

// straightens the slanting image
gsap.to("#dashboard", {

    scale: 1,
    translateY: 0,
    // translateY: "0%",
    rotateX: "0deg",
    scrollTrigger: {
        trigger: "#hero-section",
        start: window.innerWidth > RESPONSIVE_WIDTH ? "top 95%" : "top 70%",
        end: "bottom bottom",
        scrub: 1,
        // markers: true,
    }

})

const faqAccordion = document.querySelectorAll('.faq-accordion')

faqAccordion.forEach(function (btn) {
    btn.addEventListener('click', function () {
        this.classList.toggle('active')

        // Toggle 'rotate' class to rotate the arrow
        let content = this.nextElementSibling
        
        // content.classList.toggle('!tw-hidden')
        if (content.style.maxHeight === '200px') {
            content.style.maxHeight = '0px'
            content.style.padding = '0px 18px'

        } else {
            content.style.maxHeight = '200px'
            content.style.padding = '20px 18px'
        }
    })
})

// ------------- reveal section animations ---------------

const sections = gsap.utils.toArray("section")

sections.forEach((sec) => {

    const revealUptimeline = gsap.timeline({paused: true, 
                                            scrollTrigger: {
                                                            trigger: sec,
                                                            start: "10% 80%", // top of trigger hits the top of viewport
                                                            end: "20% 90%",
                                                            // markers: true,
                                                            // scrub: 1,
                                                        }})

    revealUptimeline.to(sec.querySelectorAll(".reveal-up"), {
        opacity: 1,
        duration: 0.8,
        y: "0%",
        stagger: 0.2,
    })


})


// Floating modal form handlers
(function () {
    const modalBackdrop = document.getElementById('modal-backdrop');
    const modalClose = document.getElementById('modal-close');
    const modalCancel = document.getElementById('modal-cancel');
    const leadForm = document.getElementById('lead-form');
    const openers = document.querySelectorAll('[data-open-form]');

    if (!modalBackdrop) return;

    function openModal() {
        modalBackdrop.classList.remove('tw-hidden');
        modalBackdrop.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
        const firstInput = modalBackdrop.querySelector('.lead-form .input');
        if (firstInput) firstInput.focus();
    }

    function closeModal() {
        modalBackdrop.classList.add('tw-hidden');
        modalBackdrop.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
    }

    openers.forEach(el => {
        el.addEventListener('click', (ev) => {
            // prevent default (anchors) and open modal
            ev.preventDefault();
            openModal();
        });
    });

    if (modalClose) modalClose.addEventListener('click', closeModal);
    if (modalCancel) modalCancel.addEventListener('click', closeModal);

    // click on backdrop outside the modal-card closes
    modalBackdrop.addEventListener('click', (ev) => {
        if (ev.target === modalBackdrop) closeModal();
    });

    // simple submit handler — change endpoint as needed
    if (leadForm) {
        leadForm.addEventListener('submit', async (ev) => {
            ev.preventDefault();
            const data = Object.fromEntries(new FormData(leadForm).entries());

            try {
                // Replace '/api/leads' with your actual server endpoint, or adapt to a service
                const res = await fetch('/api/leads', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data),
                });

                if (!res.ok) throw new Error('Network response was not ok');

                // success feedback then close
                alert('Thanks — we received your message!');
                closeModal();
                leadForm.reset();
            } catch (err) {
                console.error('Lead submit error:', err);
                alert('There was an error sending the form. Try again later.');
            }
        });
    }
})();
