document.addEventListener("DOMContentLoaded", () => {
    const modeButtons = document.querySelectorAll(".mode-btn");
    const modeInput = document.getElementById("modeInput");
    const textPromptArea = document.getElementById("textPromptArea");
    const imagePromptArea = document.getElementById("imagePromptArea");
    const promptInput = document.getElementById("promptInput");
    const helpTitle = document.getElementById("helpTitle");
    const helpText = document.getElementById("helpText");
    const helpExample = document.getElementById("helpExample");
    const searchForm = document.getElementById("searchForm");
    const responseBox = document.getElementById("responseBox");
    const imageInput = document.getElementById("imageInput");

    let selectedImages = [];

    const helpContent = {
        standard: {
            title: "Standard Mode",
            text: "Describe the type of trip you would like to take. You can include origin, dates, duration, climate, activities and an estimated budget.",
            example: "Example: I want to travel for 5 days from Barcelona, with nature, good food and affordable flights."
        },
        mood: {
            title: "Mood Mode",
            text: "Upload images that represent the atmosphere of your ideal trip. The AI will interpret the visual style and suggest similar destinations.",
            example: "Example: upload an image of mountains, a cosy café and a city with night lights."
        },
        budget: {
            title: "Budget Mode",
            text: "Enter your total budget and what you want to include, such as flights, accommodation, food, transport or activities.",
            example: "Example: I have €1200 for flights, accommodation and food. Where can I go and for how many days?"
        }
    };

    modeButtons.forEach(button => {
        button.addEventListener("click", () => {
            const mode = button.dataset.mode;

            modeButtons.forEach(btn => btn.classList.remove("active"));
            button.classList.add("active");

            modeInput.value = mode;
            updateMode(mode);
        });
    });

    function updateMode(mode) {
        const content = helpContent[mode];

        helpTitle.textContent = content.title;
        helpText.textContent = content.text;
        helpExample.textContent = content.example;

        responseBox.classList.add("hidden");

        if (mode === "mood") {
            textPromptArea.classList.add("hidden");
            imagePromptArea.classList.remove("hidden");
            promptInput.removeAttribute("required");
        } else {
            imagePromptArea.classList.add("hidden");
            textPromptArea.classList.remove("hidden");
            promptInput.setAttribute("required", "required");

            selectedImages = [];

            if (imageInput) {
                imageInput.value = "";
            }

            const preview = document.getElementById("imagePreview");

            if (preview) {
                preview.innerHTML = "";
            }

            if (mode === "standard") {
                promptInput.placeholder = "Example: I want a 5-day trip from Barcelona with nature and good food.";
            } else {
                promptInput.placeholder = "Example: I have €1200 for flights, accommodation and food. Where can I go?";
            }
        }
    }

    if (imageInput) {
        imageInput.addEventListener("change", event => {
            const files = Array.from(event.target.files);

            files.forEach(file => {
                selectedImages.push(file);
            });

            renderImagePreview();
        });
    }

    function renderImagePreview() {
        const container = document.getElementById("imagePreview");

        if (!container) return;

        container.innerHTML = "";

        selectedImages.forEach((file, index) => {
            const div = document.createElement("div");
            div.classList.add("img-preview");

            const img = document.createElement("img");
            const url = URL.createObjectURL(file);

            img.src = url;
            img.onload = () => URL.revokeObjectURL(url);

            const btn = document.createElement("button");
            btn.type = "button";
            btn.innerText = "✕";

            btn.addEventListener("click", () => {
                selectedImages.splice(index, 1);
                renderImagePreview();
            });

            div.appendChild(img);
            div.appendChild(btn);
            container.appendChild(div);
        });
    }

    searchForm.addEventListener("submit", () => {
        const currentMode = modeInput.value;

        searchForm.action = currentMode === "budget" ? "/budget-results" : "/search";
        searchForm.method = "POST";
        searchForm.enctype = "multipart/form-data";

        if (currentMode === "mood" && selectedImages.length > 0 && imageInput) {
            const dataTransfer = new DataTransfer();

            selectedImages.forEach(file => {
                dataTransfer.items.add(file);
            });

            imageInput.files = dataTransfer.files;
        }
    });

    function getCart() {
        return JSON.parse(sessionStorage.getItem("travelCart")) || [];
    }

    function renderCart() {
        const cart = getCart();
        const cartItems = document.getElementById("cartItems");
        const cartTotal = document.getElementById("cartTotal");

        if (!cartItems || !cartTotal) return;

        if (cart.length === 0) {
            cartItems.innerHTML = "<p>Your basket is empty.</p>";
            cartTotal.textContent = "Total: €0";
            return;
        }

        let total = 0;

        cartItems.innerHTML = cart.map((trip, index) => {
            total += trip.total;

            return `
                <div class="cart-item">
                    <div style="
                        display:flex;
                        justify-content:space-between;
                        align-items:center;
                        gap:10px;
                    ">
                        <strong>${trip.city}, ${trip.country}</strong>

                        <button
                            onclick="removeCartItem(${index})"
                            style="
                                border:none;
                                background:#ef4444;
                                color:white;
                                width:24px;
                                height:24px;
                                border-radius:50%;
                                cursor:pointer;
                                font-weight:bold;
                                font-size:14px;
                            "
                        >
                            ×
                        </button>
                    </div>

                    <ul>
                        ${trip.items.map(item => `
                            <li>${item.name} — €${item.price}</li>
                        `).join("")}
                    </ul>

                    <p><strong>€${trip.total}</strong></p>
                </div>
            `;
        }).join("");

        cartTotal.textContent = "Total: €" + total;
    }

    window.removeCartItem = function(index) {
        const cart = getCart();

        cart.splice(index, 1);

        sessionStorage.setItem("travelCart", JSON.stringify(cart));

        renderCart();
    };

    renderCart();
});

// Function to Open/Close Menu
function toggleMenu() {
    const menu = document.getElementById('side-menu');
    const overlay = document.getElementById('overlay');
    
    menu.classList.toggle('active');
    overlay.classList.toggle('active');

    // Prevent scrolling when menu is open
    if (menu.classList.contains('active')) {
        document.body.style.overflow = 'hidden';
    } else {
        document.body.style.overflow = 'auto';
    }
}

// LOADING SCREEN LOGIC (New independent block)
document.getElementById('searchForm').addEventListener('submit', function() {
    // Mostramos la pantalla de carga justo cuando se hace el envío
    document.getElementById('loading-screen').style.display = 'flex';
});