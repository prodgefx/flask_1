document.addEventListener("DOMContentLoaded", () => {
  // Automatic Copyright Year
  const yearSpan = document.getElementById("copyright-year");
  if (yearSpan) {
    yearSpan.textContent = new Date().getFullYear();
  }

  // Your existing Fade-in Observer Code
  const sections = document.querySelectorAll('.fade-in');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) entry.target.classList.add('visible');
    });
  }, { threshold: 0.2 });
  sections.forEach(s => observer.observe(s));
});