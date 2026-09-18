"use strict";

/* =========================================================
   SERVIDORES FEDERAIS - FRONTEND
   ========================================================= */


/* =========================================================
   ELEMENTOS
   ========================================================= */

const form = document.getElementById("searchForm");

const nomeInput = document.getElementById("nome");
const cargoInput = document.getElementById("cargo");
const ufInput = document.getElementById("uf");
const orgaoInput = document.getElementById("orgao");

const similarCheckbox =
    document.getElementById("similarCheckbox");

const limitContainer =
    document.getElementById("limitContainer");

const limitInput =
    document.getElementById("limit");

const searchButton =
    document.getElementById("searchButton");

const clearButton =
    document.getElementById("clearButton");

const loading =
    document.getElementById("loading");

const resultsSection =
    document.getElementById("resultsSection");

const resultsList =
    document.getElementById("resultsList");

const resultsCount =
    document.getElementById("resultsCount");

const pagination =
    document.getElementById("pagination");

const messageArea =
    document.getElementById("messageArea");


/* =========================================================
   ESTADO
   ========================================================= */

const state = {
    page: 1,
    limit: 10,
    total: 0,
    results: [],
    filters: {}
};


/* =========================================================
   INICIALIZAÇÃO
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    form.addEventListener("submit", handleSearch);

    clearButton.addEventListener("click", clearSearch);

    similarCheckbox.addEventListener(
        "change",
        handleSimilarChange
    );

});


/* =========================================================
   PESQUISA
   ========================================================= */

async function handleSearch(event) {

    event.preventDefault();

    state.page = 1;

    state.limit = Number(limitInput.value) || 10;

    state.filters = getFilters();

    await performSearch();

}


/* =========================================================
   FILTROS
   ========================================================= */

function getFilters() {

    const filters = {};

    const nome = nomeInput.value.trim();
    const cargo = cargoInput.value.trim();
    const uf = ufInput.value.trim();
    const orgao = orgaoInput.value.trim();

    if (nome) {
        filters.nome = nome;
    }

    if (cargo) {
        filters.cargo = cargo;
    }

    if (uf) {
        filters.uf = uf;
    }

    if (orgao) {
        filters.orgao = orgao;
    }

    if (similarCheckbox.checked && nome) {
        filters.similar = true;
    }

    filters.limit = state.limit;
    filters.page = state.page;

    return filters;
}


/* =========================================================
   REQUISIÇÃO À API
   ========================================================= */

async function performSearch() {

    setLoading(true);
    clearMessage();

    try {

        const params = new URLSearchParams();

        Object.entries(state.filters).forEach(
            ([key, value]) => {

                if (
                    value !== undefined &&
                    value !== null &&
                    value !== ""
                ) {
                    params.set(key, value);
                }

            }
        );

        const controller =
            new AbortController();

        const timeout =
            setTimeout(
                () => controller.abort(),
                10000
            );

        const response = await fetch(
            `/api/servidores?${params.toString()}`,
            {
                method: "GET",
                headers: {
                    "Accept": "application/json"
                },
                signal: controller.signal
            }
        );

        clearTimeout(timeout);

        const data =
            await parseResponse(response);

        const normalized =
            normalizeResponse(data);

        state.results =
            normalized.results;

        state.total =
            normalized.total;

        renderResults();

    }

    catch (error) {

        console.error(
            "Erro na consulta:",
            error
        );

        state.results = [];
        state.total = 0;

        resultsSection.classList.add("hidden");

        if (error.name === "AbortError") {

            showMessage(
                "A consulta demorou demais para responder. Tente novamente.",
                "error"
            );

        }
        else {

            showMessage(
                error.message ||
                "Não foi possível realizar a consulta.",
                "error"
            );

        }

    }

    finally {

        setLoading(false);

    }
}


/* =========================================================
   RESPOSTA HTTP
   ========================================================= */

async function parseResponse(response) {

    let data;

    try {

        data = await response.json();

    }
    catch {

        throw new Error(
            "A API retornou uma resposta inválida."
        );

    }

    if (!response.ok) {

        const message =
            data?.message ||
            data?.error ||
            `Erro HTTP ${response.status}.`;

        throw new Error(message);
    }

    return data;
}


/* =========================================================
   NORMALIZAÇÃO DA API
   ========================================================= */

function normalizeResponse(data) {

    let results = [];

    if (Array.isArray(data)) {
        results = data;
    }
    else if (Array.isArray(data.results)) {
        results = data.results;
    }
    else if (Array.isArray(data.data)) {
        results = data.data;
    }
    else if (Array.isArray(data.items)) {
        results = data.items;
    }
    else if (Array.isArray(data.servidores)) {
        results = data.servidores;
    }

    const total =
        Number(
            data.total ??
            data.count ??
            results.length
        ) || 0;

    return {
        results,
        total
    };
}


/* =========================================================
   RESULTADOS
   ========================================================= */

function renderResults() {

    resultsList.innerHTML = "";
    pagination.innerHTML = "";

    resultsSection.classList.remove("hidden");

    resultsCount.textContent =
        `${formatNumber(state.total)} ${
            state.total === 1
                ? "resultado"
                : "resultados"
        }`;

    if (state.results.length === 0) {

        resultsList.innerHTML = `
            <div class="result-card">
                <div class="result-name">
                    Nenhum servidor encontrado
                </div>

                <div class="result-value">
                    Não foram encontrados registros para
                    os critérios informados.
                </div>
            </div>
        `;

        return;
    }

    state.results.forEach(
        (server) => {

            resultsList.appendChild(
                createResultCard(server)
            );

        }
    );

    renderPagination();

}


/* =========================================================
   CARD
   ========================================================= */

function createResultCard(server) {

    const card =
        document.createElement("article");

    card.className = "result-card";

    const name =
        getValue(
            server,
            [
                "nome",
                "Nome",
                "name"
            ]
        ) || "Nome não informado";

    const cargo =
        getValue(
            server,
            [
                "cargo",
                "Cargo",
                "cargo_nome",
                "profissao",
                "Profissão"
            ]
        ) || "Não informado";

    const uf =
        getValue(
            server,
            [
                "uf",
                "UF",
                "estado",
                "Estado"
            ]
        ) || "Não informado";

    const orgao =
        getValue(
            server,
            [
                "orgao",
                "Órgão",
                "orgao_nome",
                "orgao_exercicio"
            ]
        ) || "Não informado";

    card.innerHTML = `
        <div class="result-name">
            ${escapeHtml(name)}
        </div>

        <div class="result-grid">

            <div class="result-item">
                <span class="result-label">
                    Cargo / Profissão
                </span>

                <span class="result-value">
                    ${escapeHtml(cargo)}
                </span>
            </div>

            <div class="result-item">
                <span class="result-label">
                    Estado
                </span>

                <span class="result-value">
                    ${escapeHtml(uf)}
                </span>
            </div>

            <div class="result-item">
                <span class="result-label">
                    Órgão
                </span>

                <span class="result-value">
                    ${escapeHtml(orgao)}
                </span>
            </div>

        </div>
    `;

    return card;
}


/* =========================================================
   PAGINAÇÃO
   ========================================================= */

function renderPagination() {

    const totalPages =
        Math.ceil(
            state.total / state.limit
        );

    if (totalPages <= 1) {
        return;
    }

    const previous =
        createPageButton(
            "‹",
            state.page - 1,
            state.page === 1
        );

    pagination.appendChild(previous);

    const start =
        Math.max(
            1,
            state.page - 2
        );

    const end =
        Math.min(
            totalPages,
            state.page + 2
        );

    for (
        let page = start;
        page <= end;
        page++
    ) {

        const button =
            createPageButton(
                String(page),
                page,
                false
            );

        if (page === state.page) {
            button.classList.add("active");
        }

        pagination.appendChild(button);
    }

    const next =
        createPageButton(
            "›",
            state.page + 1,
            state.page === totalPages
        );

    pagination.appendChild(next);

    const info =
        document.createElement("span");

    info.className = "page-info";

    info.textContent =
        `Página ${state.page} de ${totalPages}`;

    pagination.appendChild(info);
}


function createPageButton(
    text,
    page,
    disabled
) {

    const button =
        document.createElement("button");

    button.type = "button";
    button.className = "page-button";

    button.textContent = text;

    button.disabled = disabled;

    button.addEventListener(
        "click",
        async () => {

            state.page = page;

            state.filters =
                getFilters();

            await performSearch();

            window.scrollTo({
                top:
                    resultsSection.offsetTop - 25,
                behavior: "smooth"
            });

        }
    );

    return button;
}


/* =========================================================
   SIMILARIDADE
   ========================================================= */

function handleSimilarChange() {

    const enabled =
        similarCheckbox.checked;

    limitContainer.classList.toggle(
        "hidden",
        !enabled
    );

}


/* =========================================================
   LIMPAR
   ========================================================= */

function clearSearch(event) {

    if (event) {
        event.preventDefault();
    }

    /*
     * Cancela qualquer estado anterior.
     */

    state.page = 1;
    state.limit = 10;
    state.total = 0;
    state.results = [];
    state.filters = {};

    /*
     * Limpa os campos.
     */

    nomeInput.value = "";
    cargoInput.value = "";
    ufInput.value = "";
    orgaoInput.value = "";

    similarCheckbox.checked = false;
    limitInput.value = "10";

    /*
     * Restaura a interface.
     */

    limitContainer.classList.add("hidden");

    resultsSection.classList.add("hidden");

    loading.classList.add("hidden");

    resultsList.innerHTML = "";

    pagination.innerHTML = "";

    resultsCount.textContent =
        "0 resultados";

    clearMessage();

    searchButton.disabled = false;
    clearButton.disabled = false;

    searchButton.innerHTML =
        `<span class="button-icon">⌕</span> Pesquisar`;

    /*
     * Coloca o cursor novamente no nome.
     */

    nomeInput.focus();

}


/* =========================================================
   LOADING
   ========================================================= */

function setLoading(active) {

    loading.classList.toggle(
        "hidden",
        !active
    );

    searchButton.disabled = active;

    /*
     * O botão Limpar continua disponível
     * mesmo durante a consulta.
     */

    clearButton.disabled = false;

    if (active) {

        searchButton.innerHTML =
            `<span class="spinner"></span> Pesquisando...`;

    }
    else {

        searchButton.innerHTML =
            `<span class="button-icon">⌕</span> Pesquisar`;

    }

}


/* =========================================================
   MENSAGENS
   ========================================================= */

function showMessage(
    message,
    type = "info"
) {

    messageArea.textContent = message;

    messageArea.className =
        `message ${type}`;

}


function clearMessage() {

    messageArea.textContent = "";

    messageArea.className =
        "message hidden";

}


/* =========================================================
   UTILITÁRIOS
   ========================================================= */

function getValue(
    object,
    keys
) {

    for (const key of keys) {

        if (
            object &&
            object[key] !== undefined &&
            object[key] !== null &&
            String(object[key]).trim() !== ""
        ) {

            return String(object[key]);

        }

    }

    return "";
}


function formatNumber(number) {

    return new Intl.NumberFormat(
        "pt-BR"
    ).format(number);

}


function escapeHtml(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");

}