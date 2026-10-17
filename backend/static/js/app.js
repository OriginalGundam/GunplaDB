const form = document.querySelector("#search-form");
const searchInput = document.querySelector("#kit-search");
const grid = document.querySelector("#kit-grid");
const message = document.querySelector("#results-message");
const count = document.querySelector("#result-count");
const filterButtons = [...document.querySelectorAll(".filter-button")];
const results = document.querySelector(".results");
const detailPanel = document.querySelector("#kit-detail");
const detailContent = document.querySelector("#detail-content");
const detailMessage = document.querySelector("#detail-message");
const detailClose = document.querySelector("#detail-close");

let selectedCategory = "";
let requestNumber = 0;
let detailRequestNumber = 0;
let selectedCard = null;

function addTextElement(parent, tag, className, text) {
  const element = document.createElement(tag);
  element.className = className;
  element.textContent = text || "";
  parent.append(element);
  return element;
}

function renderKits(kits) {
  grid.replaceChildren();
  count.textContent = kits.length ? `${kits.length} ${kits.length === 1 ? "kit" : "kits"}` : "";

  if (!kits.length) {
    addTextElement(grid, "p", "empty-state", "No kits found. Try another search or grade.");
    return;
  }
  
  for (const kit of kits) {
    const card = addTextElement(grid, "button", "kit-card", "");
    card.type = "button";
    card.setAttribute("aria-label", `View details for ${kit.name}`);
    const meta = addTextElement(card, "span", "kit-meta", "");
    addTextElement(meta, "span", "grade-badge", kit.grade || kit.category || "Gunpla");
    if (kit.status) addTextElement(meta, "span", "status-badge", kit.status);
    addTextElement(card, "span", "kit-title", kit.name);
    card.addEventListener("click", () => openKitDetails(kit, card));
  }
}

function renderKitDetails(kit) {
  detailContent.replaceChildren();
  addTextElement(detailContent, "h2", "detail-title", kit.name || "Kit details");

  const facts = addTextElement(detailContent, "div", "detail-facts", "");
  for (const [label, value] of [
    ["Grade", kit.grade],
    ["Category", kit.category],
    ["Status", kit.status]
  ]) {
    if (!value) continue;
    const fact = addTextElement(facts, "span", "detail-fact", "");
    const strong = addTextElement(fact, "strong", "", `${label}: `);
    strong.append(document.createTextNode(value));
  }

  addTextElement(detailContent, "h3", "price-heading", "Retailer listings");
  
  const prices = Array.isArray(kit.prices) ? kit.prices : [];
  if (!prices.length) {
    addTextElement(detailContent, "p", "detail-empty", "No retailer price listings are available for this kit yet.");
    return;
  }

  const list = addTextElement(detailContent, "div", "price-list", "");
  for (const listing of prices) {
    const item = addTextElement(list, "article", "price-item", "");
    const info = addTextElement(item, "div", "", "");
    addTextElement(info, "p", "price-store", listing.store || "Retailer");

    if (listing.updated_at) {
      const updatedDate = new Date(listing.updated_at);

      if (!Number.isNaN(updatedDate.getTime())) {
        addTextElement(
          info,
          "span",
          "last-updated",
          `Last updated: ${updatedDate.toLocaleDateString("en-US", {
            year: "numeric",
            month: "long",
            day: "numeric"
          })}`
        );
      }
    }

    const metadata = addTextElement(info, "div", "price-meta", "");
    if (listing.availability) addTextElement(metadata, "span", "", `Availability: ${listing.availability}`);
    if (listing.stock !== null && listing.stock !== undefined) {
      addTextElement(metadata, "span", "", `Stock: ${listing.stock}`);
    }

    const price = Number(listing.price);
    addTextElement(
        item,
        "span",
        "price-value",
        Number.isFinite(price) ? `Price: $${price.toFixed(2)}` : "Price unavailable"
    );

    const shippingFee = listing.shipping_fee;
    addTextElement(
        item,
        "span",
        "shipping-value",
        shippingFee !== null && shippingFee !== undefined
            ? `Shipping: $${Number(shippingFee).toFixed(2)}`
            : "Shipping: Not available"
    );
        const validShipping =
      shippingFee !== null &&
      shippingFee !== undefined &&
      Number.isFinite(Number(shippingFee));

    const validPrice = Number.isFinite(price);

    const estimatedTotal = price + Number(shippingFee);

    addTextElement(
      item,
      "span",
      "estimated-total",
      validPrice && validShipping
        ? `Estimated delivered cost: $${estimatedTotal.toFixed(2)}`
        : "Estimated delivered cost: Unavailable"
    );

    if (listing.product_url) {
      try {
        const productUrl = new URL(listing.product_url, window.location.origin);
        if (productUrl.protocol === "http:" || productUrl.protocol === "https:") {
          const link = addTextElement(info, "a", "product-link", "View product page");
          link.href = productUrl.href;
          link.target = "_blank";
          link.rel = "noopener noreferrer";
        }
      } catch (error) {
        // Ignore invalid URLs; only backend-provided, valid product links are shown.
      }
    }
  }
}

async function openKitDetails(kit, card) {
  if (kit.id === undefined || kit.id === null) return;
  selectedCard = card;
  results.hidden = true;
  detailPanel.hidden = false;
  detailContent.replaceChildren();
  detailMessage.textContent = "Loading kit details…";
  detailClose.focus();
  detailPanel.scrollIntoView({ behavior: "smooth", block: "start" });

  const currentRequest = ++detailRequestNumber;
  try {
    const response = await fetch(`/gunpla/${encodeURIComponent(kit.id)}`);
    if (!response.ok) throw new Error("Kit details request failed");
    const details = await response.json();
    if (currentRequest !== detailRequestNumber) return;
    renderKitDetails(details);
    detailMessage.textContent = "";
  } catch (error) {
    if (currentRequest !== detailRequestNumber) return;
    detailContent.replaceChildren();
    detailMessage.textContent = "Could not load details for this kit. Please try again.";
  }
}

detailClose.addEventListener("click", () => {
  detailRequestNumber += 1;
  detailPanel.hidden = true;
  results.hidden = false;
  if (selectedCard) selectedCard.focus();
});

async function loadKits() {
  const currentRequest = ++requestNumber;
  const params = new URLSearchParams();
  const name = searchInput.value.trim();
  if (name) params.set("name", name);
  if (selectedCategory) params.set("category", selectedCategory);

  message.textContent = "Loading kits…";
  count.textContent = "";

  try {
    const response = await fetch(`/search?${params.toString()}`);
    if (!response.ok) throw new Error("Kit search failed");
    const kits = await response.json();
    if (currentRequest !== requestNumber) return;
    renderKits(kits);
    message.textContent = "";
  } catch (error) {
    if (currentRequest !== requestNumber) return;
    grid.replaceChildren();
    message.textContent = "Could not load kits. Make sure the database is running, then refresh the page.";
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  loadKits();
});

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    selectedCategory = button.dataset.category;
    filterButtons.forEach((item) => {
      const active = item === button;
      item.classList.toggle("is-active", active);
      item.setAttribute("aria-pressed", String(active));
    });
    loadKits();
  });
});

loadKits();
