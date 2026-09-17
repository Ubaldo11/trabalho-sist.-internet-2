const searchForm = document.getElementById("searchForm");

const nomeInput = document.getElementById("nome");
const cargoInput = document.getElementById("cargo");
const ufInput = document.getElementById("uf");
const orgaoInput = document.getElementById("orgao");

const similarCheckbox = document.getElementById("similarCheckbox");
const limitContainer = document.getElementById("limitContainer");
const limitInput = document.getElementById("limit");

const searchButton = document.getElementById("searchButton");
const clearButton = document.getElementById("clearButton");

const loading = document.getElementById("loading");
const resultsSection = document.getElementById("resultsSection");
const resultsList = document.getElementById("resultsList");
const resultsCount = document.getElementById("resultsCount");
const pagination = document.getElementById("pagination");
const messageArea = document.getElementById("messageArea");

const state = {
page: 1,
limit: 20,
total: 0,
results: [],
filters: {}
};

/* ================================
EVENTOS
================================ */

searchForm.addEventListener("submit", function (event) {

```
event.preventDefault();

state.page = 1;

performSearch();
```

});

clearButton.addEventListener("click", clearSearch);

similarCheckbox.addEventListener("change", function () {

```
limitContainer.classList.toggle(
    "hidden",
    !similarCheckbox.checked
);
```

});

/* ================================
BUSCA
================================ */

async function performSearch() {

```
clearMessage();

const filters = getFilters();


if (!hasValidSearch(filters)) {
    showMessage(
        "Informe pelo menos um critério para realizar a pesquisa.",
        "warning"
    );

    return;
}


state.filters = filters;

setLoading(true);


try {

    const response = await searchServers({
        ...filters,
        page: state.page,
        limit: state.limit
    });


    const normalized = normalizeResponse(response);


    state.results = normalized.results;
    state.total = normalized.total;


    renderResults();

} catch (error) {

    state.results = [];
    state.total = 0;

    resultsSection.classList.add("hidden");

    showMessage(
        error.message ||
        "Não foi possível realizar a consulta.",
        "error"
    );

} finally {

    setLoading(false);

}
```

}

/* ================================
FILTROS
================================ */

function getFilters() {

```
const nome = nomeInput.value.trim();
const cargo = cargoInput.value.trim();
const uf = ufInput.value.trim();
const orgao = orgaoInput.value.trim();


const filters = {};


if (similarCheckbox.checked && nome) {

    filters.similar = nome;

} else if (nome) {

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


return filters;
```

}

function hasValidSearch(filters) {

```
return Object.keys(filters).length > 0;
```

}

/* ================================
RESPOSTA DA API
================================ */

function normalizeResponse(response) {

```
/*
 * Aceita diferentes nomes de propriedades para
 * facilitar a integração com o backend da equipe.
 *
 * O formato definitivo deve ser combinado com
 * os desenvolvedores do backend.
 */


let results =
    response.dados ??
    response.data ??
    response.resultados ??
    response.results ??
    [];


if (!Array.isArray(results)) {

    if (
        results &&
        typeof results === "object"
    ) {
        results = [results];
    } else {
        results = [];
    }

}


const total =
    Number(
        response.total ??
        response.total_resultados ??
        response.count ??
        results.length
    ) || 0;


return {
    results,
    total
};
```

}

/* ================================
RESULTADOS
================================ */

function renderResults() {

```
resultsList.innerHTML = "";
pagination.innerHTML = "";


if (state.results.length === 0) {

    resultsSection.classList.remove("hidden");

    resultsCount.textContent = "0 resultados";


    resultsList.innerHTML = `
        <div class="message message-info">
            Nenhum servidor foi encontrado com os critérios informados.
        </div>
    `;

    return;
}


resultsSection.classList.remove("hidden");


resultsCount.textContent =
    `${formatNumber(state.total)} ${
        state.total === 1
            ? "resultado"
            : "resultados"
    }`;


state.results.forEach(server => {

    resultsList.appendChild(
        createResultCard(server)
    );

});


renderPagination();
```

}

/**

* Cria o card visual de um servidor.
  */
  function createResultCard(server) {

  const card = document.createElement("article");

  card.className = "result-card";

  const name =
  getValue(
  server,
  [
  "nome",
  "Nome",
  "name",
  "NOME"
  ]
  ) || "Nome não informado";

  const cargo =
  getValue(
  server,
  [
  "cargo",
  "Cargo",
  "profissao",
  "profissão",
  "PROFISSAO",
  "PROFISSÃO"
  ]
  ) || "Cargo não informado";

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
  "órgão",
  "orgao_instituicao",
  "instituicao",
  "instituição",
  "ORGAO"
  ]
  ) || "Não informado";

  const iniciais = getInitials(name);

  card.innerHTML = ` <div class="result-main">

  ```
       <div class="result-avatar">
           ${escapeHtml(iniciais)}
       </div>

       <div class="result-content">

           <div class="result-name">
               ${escapeHtml(String(name))}
           </div>

           <div class="result-cargo">
               ${escapeHtml(String(cargo))}
           </div>

           <div class="result-details">

               <span class="result-detail">
                   <strong>UF:</strong>
                   ${escapeHtml(String(uf))}
               </span>

               <span class="result-detail">
                   <strong>Órgão:</strong>
                   ${escapeHtml(String(orgao))}
               </span>

           </div>

       </div>

   </div>
  ```

  `;

  return card;
  }

/* ================================
PAGINAÇÃO
================================ */

function renderPagination() {

```
pagination.innerHTML = "";


const totalPages =
    Math.ceil(state.total / state.limit);


if (totalPages <= 1) {
    return;
}


const previousButton =
    createPaginationButton(
        "←",
        state.page === 1,
        function () {
            goToPage(state.page - 1);
        }
    );


pagination.appendChild(previousButton);


const pages = getPageNumbers(
    state.page,
    totalPages
);


pages.forEach(page => {

    if (page === "...") {

        const span =
            document.createElement("span");

        span.className = "pagination-info";
        span.textContent = "...";

        pagination.appendChild(span);

        return;
    }


    const button =
        createPaginationButton(
            String(page),
            false,
            function () {
                goToPage(page);
            }
        );


    if (page === state.page) {
        button.classList.add("active");
    }


    pagination.appendChild(button);

});


const nextButton =
    createPaginationButton(
        "→",
        state.page === totalPages,
        function () {
            goToPage(state.page + 1);
        }
    );


pagination.appendChild(nextButton);
```

}

function createPaginationButton(
text,
disabled,
onClick
) {

```
const button =
    document.createElement("button");

button.type = "button";

button.textContent = text;

button.disabled = disabled;

button.addEventListener(
    "click",
    onClick
);

return button;
```

}

function getPageNumbers(current, total) {

```
if (total <= 7) {

    return Array.from(
        { length: total },
        (_, index) => index + 1
    );

}


const pages = [];


pages.push(1);


if (current > 4) {
    pages.push("...");
}


const start =
    Math.max(2, current - 1);

const end =
    Math.min(total - 1, current + 1);


for (let page = start; page <= end; page++) {
    pages.push(page);
}


if (current < total - 3) {
    pages.push("...");
}


pages.push(total);


return pages;
```

}

function goToPage(page) {

```
if (page < 1) {
    return;
}


state.page = page;

performSearch();


window.scrollTo({
    top: resultsSection.offsetTop - 30,
    behavior: "smooth"
});
```

}

/* ================================
LOADING
================================ */

function setLoading(active) {

```
loading.classList.toggle(
    "hidden",
    !active
);


searchButton.disabled = active;


if (active) {

    searchButton.innerHTML = `
        <span class="spinner"></span>
        Pesquisando...
    `;

} else {

    searchButton.innerHTML = `
        <span class="button-icon">⌕</span>
        Pesquisar
    `;

}
```

}

/* ================================
MENSAGENS
================================ */

function showMessage(
message,
type = "info"
) {

```
messageArea.className =
    `message-area`;


const div =
    document.createElement("div");

div.className =
    `message message-${type}`;

div.textContent = message;


messageArea.appendChild(div);
```

}

function clearMessage() {

```
messageArea.innerHTML = "";

messageArea.className =
    "message-area hidden";
```

}

/* ================================
LIMPAR
================================ */

function clearSearch() {

```
searchForm.reset();

state.page = 1;
state.total = 0;
state.results = [];
state.filters = {};

limitContainer.classList.add("hidden");

resultsSection.classList.add("hidden");

clearMessage();

resultsList.innerHTML = "";
pagination.innerHTML = "";
```

}

/* ================================
UTILITÁRIOS
================================ */

function getValue(object, keys) {

```
for (const key of keys) {

    if (
        Object.prototype.hasOwnProperty.call(
            object,
            key
        )
    ) {

        const value = object[key];

        if (
            value !== null &&
            value !== undefined &&
            String(value).trim() !== ""
        ) {
            return value;
        }

    }

}


return null;
```

}

function getInitials(name) {

```
const words =
    String(name)
        .trim()
        .split(/\s+/)
        .filter(Boolean);


if (words.length === 0) {
    return "?";
}


if (words.length === 1) {

    return words[0]
        .substring(0, 2)
        .toUpperCase();

}


return (
    words[0][0] +
    words[words.length - 1][0]
).toUpperCase();
```

}

function formatNumber(number) {

```
return new Intl.NumberFormat(
    "pt-BR"
).format(number);
```

}

/**

* Impede que dados vindos da API sejam
* interpretados como HTML.
*
* Isso é importante para evitar XSS.
  */
  function escapeHtml(value) {

  return String(value)
  .replaceAll("&", "&")
  .replaceAll("<", "<")
  .replaceAll(">", ">")
  .replaceAll('"', """)
  .replaceAll("'", "'");

}
