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
