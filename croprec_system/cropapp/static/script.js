// Utility: Select helpers
const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

// Mobile navigation toggle
(() => {
  const toggle = $("#navToggle");
  const menu = $("#navMenu");
  if (!toggle || !menu) return;

  toggle.addEventListener("click", () => {
    const expanded = toggle.getAttribute("aria-expanded") === "true";
    toggle.setAttribute("aria-expanded", String(!expanded));
    menu.classList.toggle("open");
  });

  // Close menu when a link is clicked (mobile UX)
  $$("#navMenu .nav-link").forEach((link) =>
    link.addEventListener("click", () => {
      toggle.setAttribute("aria-expanded", "false");
      menu.classList.remove("open");
    })
  );
})();

// Footer year
(() => {
  const yearSpan = $("#year");
  if (yearSpan) {
    yearSpan.textContent = new Date().getFullYear();
  }
})();

// Predict form submission is handled by the server; no client interception

// Display results on results page
(() => {
  const cropEl = document.querySelector("#cropName");
  if (!cropEl) return;

  // If server already rendered a prediction, do not override with client data
  const serverRendered = (cropEl.textContent && cropEl.textContent.trim() !== "—");
  if (serverRendered) return;

  const dataRaw = sessionStorage.getItem("predict_data");
  if (!dataRaw) return;

  try {
    const data = JSON.parse(dataRaw);
    const { N, P, K, crop, score, warnings } = data;
    cropEl.textContent = crop || "—";

    const box = document.querySelector("#warningsBox");
    const list = document.querySelector("#warningList");

    if (box && list) {
      list.innerHTML = "";
      if (warnings && warnings.length) {
        warnings.forEach((w) => {
          const li = document.createElement("li");
          li.textContent = w;
          list.appendChild(li);
        });
        box.classList.remove("hidden");
      } else {
        box.classList.add("hidden");
      }
    }
  } catch (err) {
    console.error("Error parsing prediction data:", err);
  }
})();

// Avatar dropdown toggle
(() => {
  const avatarBtn = document.getElementById('avatarBtn');
  const avatarDropdown = document.getElementById('avatarDropdown');

  if (avatarBtn && avatarDropdown) {
    avatarBtn.addEventListener('click', function(e) {
      e.stopPropagation();
      avatarDropdown.classList.toggle('active');
    });

    document.addEventListener('click', function(e) {
      if (!e.target.closest('.nav-user')) {
        avatarDropdown.classList.remove('active');
      }
    });
  }
})();
document.addEventListener("DOMContentLoaded", () => {
    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", () => {
            window.location.href = "/logout/";
        });
    }
    const toggleLoginPassword = document.getElementById('toggleLoginPassword');
    const loginPasswordInput = document.getElementById('password');
    if (toggleLoginPassword && loginPasswordInput) {
        toggleLoginPassword.addEventListener('click', () => {
            const isPassword = loginPasswordInput.type === 'password';
            loginPasswordInput.type = isPassword ? 'text' : 'password';
            toggleLoginPassword.setAttribute('aria-label', isPassword ? 'Hide password' : 'Show password');
            const eyeOn = toggleLoginPassword.querySelector('.eye-on');
            const eyeOff = toggleLoginPassword.querySelector('.eye-off');
            if (eyeOn && eyeOff) {
                eyeOn.style.display = isPassword ? 'none' : 'inline';
                eyeOff.style.display = isPassword ? 'inline' : 'none';
            }
        });
    }
    
    const okBtn = document.getElementById('messageOkBtn');
const messageModal = document.getElementById('messageModal');

// SHOW the popup if Django sent a message
if (messageModal) {
    messageModal.classList.remove("hidden");
    messageModal.style.display = "flex";
}

// OK button closes popup
if (okBtn && messageModal) {
  okBtn.addEventListener('click', () => {
    messageModal.remove();
  });
}
    const alertModal = document.getElementById('alertModal');
    const alertContent = document.getElementById('alertContent');
    const alertOkBtn = document.getElementById('alertOkBtn');
    const showAlert = (items) => {
      if (!alertModal || !alertContent) return;
      const list = Array.isArray(items) ? items : [String(items || 'Invalid input')];
      alertContent.innerHTML = `<ul>${list.map((m) => `<li>${m}</li>`).join('')}</ul>`;
      alertModal.classList.remove('hidden');
    };
    if (alertOkBtn && alertModal) {
      alertOkBtn.addEventListener('click', () => {
        alertModal.classList.add('hidden');
      });
    }
    const loginForm = document.querySelector('form.auth-form[action$="login/"]') || (document.querySelector('#userType') ? document.querySelector('form.auth-form') : null);
    if (loginForm) {
      loginForm.addEventListener('submit', (e) => {
        const invalids = Array.from(loginForm.querySelectorAll(':invalid')).map((el) => el.validationMessage || 'Invalid field');
        if (invalids.length) {
          e.preventDefault();
          showAlert(invalids);
        }
      });
    }
    const registerForm = document.querySelector('form.auth-form[action$="register/"]') || (document.querySelector('#userTypeReg') ? document.querySelector('form.auth-form') : null);
    const mobileInput = document.getElementById('mobile');
    if (mobileInput) {
      mobileInput.setAttribute('pattern', '^\\d{10}$');
      mobileInput.setAttribute('title', 'Enter exactly 10 digits');
      mobileInput.setAttribute('inputmode', 'numeric');
      const updateMobileState = () => {
        const v = (mobileInput.value || '').replace(/\s/g, '');
        const ok = /^\d{10}$/.test(v);
        mobileInput.classList.toggle('field-error', !ok && v.length > 0);
        mobileInput.setCustomValidity(ok ? '' : 'Enter exactly 10 digits');
        mobileInput.setAttribute('title', 'Enter exactly 10 digits');
      };
      mobileInput.addEventListener('input', updateMobileState);
      mobileInput.addEventListener('blur', updateMobileState);
      mobileInput.addEventListener('mouseenter', updateMobileState);
      updateMobileState();
    }
    if (registerForm) {
      registerForm.addEventListener('submit', (e) => {
        const invalids = Array.from(registerForm.querySelectorAll(':invalid')).map((el) => el.validationMessage || 'Invalid field');
        if (invalids.length) {
          e.preventDefault();
          showAlert(invalids);
        }
      });
    }
    const flashes = document.querySelectorAll('.flash');
    if (flashes.length) {
      setTimeout(() => {
        flashes.forEach((f) => f.remove());
      }, 4000);
    }
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});
(() => {
  const items = Array.from(document.querySelectorAll('.reveal'));
  if (!items.length) return;
  const showIfInView = () => {
    items.forEach((el) => {
      if (el.classList.contains('visible')) return;
      const r = el.getBoundingClientRect();
      if (r.top < (window.innerHeight * 0.9)) {
        el.classList.add('visible');
      }
    });
  };

  showIfInView();

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });
    items.forEach((el) => observer.observe(el));
  } else {
    items.forEach((el) => el.classList.add('visible'));
  }

  let pending = true;
  const onScroll = () => {
    if (!pending) return;
    pending = false;
    requestAnimationFrame(() => {
      showIfInView();
      pending = true;
      if (items.every((el) => el.classList.contains('visible'))) {
        window.removeEventListener('scroll', onScroll);
        window.removeEventListener('resize', onScroll);
      }
    });
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
})();
