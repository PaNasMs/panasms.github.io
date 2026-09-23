const viewer = document.querySelector(".lightbox");
let opener;
for (const link of document.querySelectorAll(".zoom")) {
  link.addEventListener("click", (event) => {
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey)
      return;
    event.preventDefault();
    opener = link;
    const image = link.querySelector("img");
    viewer.querySelector("img").src = image.src;
    viewer.querySelector("img").alt = image.alt;
    viewer.querySelector("p").textContent = image.alt;
    viewer.showModal();
  });
}
viewer.addEventListener("click", (event) => {
  if (event.target !== viewer) return;
  const bounds = viewer.getBoundingClientRect();
  if (
    event.clientX < bounds.left ||
    event.clientX > bounds.right ||
    event.clientY < bounds.top ||
    event.clientY > bounds.bottom
  )
    viewer.close();
});
viewer.addEventListener("close", () => opener?.focus());

for (const figure of document.querySelectorAll(".shot")) {
  const controls = figure.querySelector(".shot-themes");
  if (!controls) continue;
  controls.hidden = false;
  for (const button of controls.querySelectorAll("button")) {
    button.addEventListener("click", () => {
      const theme = button.dataset.showTheme;
      for (const view of figure.querySelectorAll("[data-theme]")) {
        view.hidden = view.dataset.theme !== theme;
      }
      for (const option of controls.querySelectorAll("button")) {
        option.setAttribute("aria-pressed", String(option === button));
      }
    });
  }
}
