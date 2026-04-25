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

        if (mode === "standard") {
            promptInput.placeholder = "Ex: Vull fer un viatge de 5 dies amb natura i bon menjar des de Barcelona.";
        } else {
            promptInput.placeholder = "Ex: Tinc 1200€ per vol, hotel i menjar. On puc anar?";
        }
    }
}

searchForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const currentMode = modeInput.value;

    if (currentMode === "budget") {
        searchForm.action = "/budget-results";
        searchForm.method = "POST";
        searchForm.submit();
        return;
    }

    const formData = new FormData(searchForm);

    const response = await fetch("/search", {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    responseBox.classList.remove("hidden");
    responseBox.innerHTML = `
        <h3>Resposta temporal</h3>
        <p><strong>Mode:</strong> ${data.mode}</p>
        <p>${data.message}</p>
        ${data.prompt ? `<p><strong>Prompt:</strong> ${data.prompt}</p>` : ""}
    `;
});

searchForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const prompt = document.getElementById("promptInput").value;
    
    // Guardem el prompt temporalment per mostrar-lo al xat de la següent pàgina
    localStorage.setItem('lastPrompt', prompt);
    
    // Redirigim a la pàgina de resultats
    window.location.href = "/results";
});