(function () {
  const tocLinks = document.querySelectorAll(".toc a");
  const headings = [
    ...document.querySelectorAll(".article h2[id], .article h3[id]"),
  ];

  document.querySelectorAll(".heading-anchor").forEach((anchor) => {
    anchor.addEventListener("click", (event) => {
      event.preventDefault();
      const hash = anchor.getAttribute("href");
      if (!hash) return;

      const url = `${location.origin}${location.pathname}${hash}`;
      history.replaceState(null, "", hash);

      const target = document.querySelector(hash);
      target?.scrollIntoView({ behavior: "smooth", block: "start" });

      const copy = () => {
        anchor.classList.add("is-copied");
        anchor.setAttribute("aria-label", "已複製連結");
        window.setTimeout(() => {
          anchor.classList.remove("is-copied");
          anchor.setAttribute("aria-label", "複製此段連結");
        }, 2000);
      };

      if (navigator.clipboard?.writeText) {
        navigator.clipboard.writeText(url).then(copy).catch(copy);
      } else {
        copy();
      }
    });
  });

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

  headings.forEach((heading) => observer.observe(heading));
})();
