(function () {
  const tocLinks = document.querySelectorAll(".toc a");
  const headings = [...document.querySelectorAll(".article h2[id]")];

  if (!tocLinks.length || !headings.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const id = entry.target.getAttribute("id");
        tocLinks.forEach((link) => {
          link.classList.toggle(
            "is-active",
            link.getAttribute("href") === `#${id}`,
          );
        });
      });
    },
    { rootMargin: "-20% 0px -65% 0px", threshold: 0 },
  );

  headings.forEach((h) => observer.observe(h));
})();
