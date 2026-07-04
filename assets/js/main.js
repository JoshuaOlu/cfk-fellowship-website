const menuButton = document.querySelector(".navbar__toggle");

menuButton.addEventListener("click", () => {
  menuButton.classList.toggle("is-open");

  const expanded =
    menuButton.getAttribute("aria-expanded") === "true";

  menuButton.setAttribute(
    "aria-expanded",
    !expanded
  );
});