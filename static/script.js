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
            title: "Mode Standard",
            text: "Escriu quin tipus de viatge vols fer. Pots indicar origen, dates, durada, clima, activitats i pressupost aproximat.",
            example: "Exemple: Vull marxar 5 dies des de Barcelona, amb natura, bon menjar i vols barats."
        },
        mood: {
            title: "Mode Mood",
            text: "Afegeix imatges que representin el mood del teu viatge. La IA podrà interpretar l’estil visual i proposar destins similars.",
            example: "Exemple: puja una imatge de muntanya, una cafeteria acollidora i una ciutat amb llums de nit."
        },
        budget: {
            title: "Mode Pressupost",
            text: "Escriu el teu pressupost total i què vols incloure: vols, hotel, menjar, transport o activitats.",
            example: "Exemple: Tinc 1200€ per vol, hotel i menjar. Vull saber on puc anar i quants dies."
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
                promptInput.placeholder = "Ex: Vull fer un viatge de 5 dies amb natura i bon menjar des de Barcelona.";
            } else {
                promptInput.placeholder = "Ex: Tinc 1200€ per vol, hotel i menjar. On puc anar?";
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

        if (!container) {
            return;
        }

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

        if (currentMode === "budget") {
            searchForm.action = "/budget-results";
        } else {
            searchForm.action = "/search";
        }

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
});