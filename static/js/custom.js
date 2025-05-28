window.addEventListener("load", function() {
    document.getElementById("preloader").style.display = "none";
    document.getElementById("main-content").style.display = "";
});

document.addEventListener("DOMContentLoaded", function () {

    // Show and auto-hide messages
    var toastElements = document.querySelectorAll('.msg-toast');
    toastElements.forEach(function (toastElement) {
      if (!toastElement.classList.contains('bg-danger-subtle')) {
          new bootstrap.Toast(toastElement, { autohide: true, delay: 5000 }).show();
      }else{
          new bootstrap.Toast(toastElement, { autohide: true, delay: 600000 }).show();
      }
    });

    const navbarToggler = document.querySelector('.navbar-toggler');
    const originalContent = navbarToggler.innerHTML;
    const colseContent = '<i class="bi bi-x-lg px-2" style="font-size: 1.5rem;" ></i>';
    const navbarCollapse = document.querySelector('#navbarToggler');

    // Listen for the collapse toggle events
    navbarCollapse.addEventListener('show.bs.collapse', function () {
        navbarToggler.innerHTML = colseContent;
    });

    navbarCollapse.addEventListener('hide.bs.collapse', function () {
      navbarToggler.innerHTML = originalContent;
    });

    document.querySelectorAll('.nav-section').forEach(link => {
      link.addEventListener('click', function (event) {
        const navbarCollapse = document.querySelector('.navbar-collapse');

        // Check if the navbar is expanded
        if (navbarCollapse.classList.contains('show')) {
          // Collapse the navbar using Bootstrap's Collapse API
          const bootstrapCollapse = bootstrap.Collapse.getInstance(navbarCollapse) || new bootstrap.Collapse(navbarCollapse);
          bootstrapCollapse.hide();
        }

        // Wait for the collapse animation to finish, then scroll
        navbarCollapse.addEventListener('hidden.bs.collapse', () => {
          const targetId = this.getAttribute('href').slice(1); // Extract the target ID
          const targetElement = document.getElementById(targetId);

          if (targetElement) {
            targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        }, { once: true }); // Ensure the event runs only once
      });
    });

    // Show loader on link click
    document.querySelectorAll('.btn-preload').forEach(link => {
        link.addEventListener('click', function (event) {
            if (event.ctrlKey || event.metaKey || event.which === 2) { return; /*Do nothing*/  }
            document.getElementById("preloader").style.display = "flex";
        });
    });

    // Hide preloader when the page is fully loaded
    window.addEventListener("load", function () {
        document.getElementById("preloader").style.display = "none";
    });

    // Show loader on form submission
    document.querySelectorAll("form").forEach(form => {
        form.addEventListener("submit", function () {
            document.getElementById("preloader").style.display = "flex";
        });
    });

    // Show loader when selecting an option
    document.querySelectorAll("select.sel-preload").forEach(select => {
        select.addEventListener("change", function () {
            document.getElementById("preloader").style.display = "flex";
        });
    });

    // Hide preloader whenever the page is shown (including back/forward navigation)
    window.addEventListener("pageshow", function () {
        document.getElementById("preloader").style.display = "none";
    });

    var toastElements = document.querySelectorAll('.msg-toast');
    toastElements.forEach(function (toastElement) {
      if (!toastElement.classList.contains('bg-danger-subtle')) {
          new bootstrap.Toast(toastElement, { autohide: true, delay: 5000 }).show();
      }else{
          new bootstrap.Toast(toastElement, { autohide: true, delay: 600000 }).show();
      }
    });
});


document.addEventListener("visibilitychange", function () {
    if (!document.hidden) {
        document.getElementById("preloader").style.display = "none";
    }
});


// JavaScript to handle the navbar shrinking effect
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    if (window.scrollY > 0) { // Adjust scroll threshold as needed
        navbar.classList.add('shrink', 'shadow', 'shadow-md');
        navbar.classList.remove('pt-3', 'pb-4');
    } else {
        navbar.classList.remove('shrink', 'shadow', 'shadow-md');
        navbar.classList.add('pt-3', 'pb-4');
    }
});