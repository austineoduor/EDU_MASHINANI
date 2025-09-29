document.addEventListener("DOMContentLoaded", () => {
    const container = document.querySelector(".form_container");
    const signInBtn = document.querySelector("#sign-in-btn");
    const signUpBtn = document.querySelector("#sign-up-btn");
    const signInBtn2 = document.querySelector("#sign-in-btn2");
    const signUpBtn2 = document.querySelector("#sign-up-btn2");

    /* -------------------
       Sign In / Sign Up switch
    ------------------- */
    if (container) {
        // Panel buttons
        signUpBtn?.addEventListener("click", () => {
            container.classList.add("form-register-mode");
        });
        signInBtn?.addEventListener("click", () => {
            container.classList.remove("form-register-mode");
        });

        // Inline links
        signUpBtn2?.addEventListener("click", (e) => {
            e.preventDefault();
            container.classList.add("form-register-mode");
        });
        signInBtn2?.addEventListener("click", (e) => {
            e.preventDefault();
            container.classList.remove("form-register-mode");
        });

        // Backend auto-switch
        if (container.dataset.showRegister === "true") {
            container.classList.add("form-register-mode");
        }
    }

    /* -------------------
       Password visibility toggle
    ------------------- */
    document.querySelectorAll('.pw-toggle, .pw-toggle-log').forEach(btn => {
        btn.addEventListener('click', () => {
            const wrapper = btn.closest('.pw-field');
            const input = wrapper?.querySelector('input[type="password"], input[type="text"]');
            if (!input) return;

            const show = input.type === 'password';
            input.type = show ? 'text' : 'password';

            btn.setAttribute('aria-pressed', show ? 'true' : 'false');
            btn.setAttribute('aria-label', show ? 'Hide password' : 'Show password');

            const icon = btn.querySelector('i.fa');
            if (icon) {
                icon.classList.toggle('fa-eye', !show);
                icon.classList.toggle('fa-eye-slash', show);
            }
        });
    });

    /* -------------------
       Course details toggle
    ------------------- */
    document.querySelectorAll(".toggle-details").forEach(title => {
    title.setAttribute("role", "button");
    title.setAttribute("aria-expanded", "false");
    title.setAttribute("tabindex", "0");

    title.addEventListener("click", toggleCourseDetails);
    title.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            toggleCourseDetails.call(title);
        }
    });
});

function toggleCourseDetails() {
    const details = this.parentElement.querySelector(".course-details");
    if (!details) return;

    const isOpen = details.classList.contains("open");

    if (isOpen) {
        details.style.maxHeight = null;
        details.classList.remove("open");
        this.classList.remove("open");
        this.setAttribute("aria-expanded", "false");
    } else {
        details.style.maxHeight = details.scrollHeight + "px";
        details.classList.add("open");
        this.classList.add("open");
        this.setAttribute("aria-expanded", "true");
    }
}
    const navToggle = document.getElementById("nav-toggle");
            const navMenu = document.getElementById("nav-menu");

            navToggle.addEventListener("click", () => {
                navMenu.classList.toggle("active");
            });
});