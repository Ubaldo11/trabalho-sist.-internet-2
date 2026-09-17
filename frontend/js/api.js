/*

* Comunicação com a API Flask.
*
* O endereço "/api" funciona quando o frontend e a API
* estiverem publicados no mesmo domínio através do Docker.
*
* Caso o backend esteja em outro endereço durante o
* desenvolvimento, altere API_BASE_URL.
  */

const API_BASE_URL = "/api";

const API_TIMEOUT = 10000;

/**

* Executa uma requisição GET para a API.
*
* @param {string} endpoint
* @param {Object} params
* @returns {Promise<Object>}
  */
  async function apiGet(endpoint, params = {}) {

  const queryString = new URLSearchParams();

  Object.entries(params).forEach(([key, value]) => {

  ```
   if (
       value !== undefined &&
       value !== null &&
       String(value).trim() !== ""
   ) {
       queryString.append(key, value);
   }
  ```

  });

  const query = queryString.toString();

  const url = query
  ? `${API_BASE_URL}${endpoint}?${query}`
  : `${API_BASE_URL}${endpoint}`;

  const controller = new AbortController();

  const timeout = setTimeout(() => {
  controller.abort();
  }, API_TIMEOUT);

  try {

  ```
   const response = await fetch(url, {
       method: "GET",

       headers: {
           "Accept": "application/json"
       },

       signal: controller.signal
   });


   clearTimeout(timeout);


   let data;

   try {
       data = await response.json();
   } catch {
       data = {};
   }


   if (!response.ok) {

       const message =
           data.message ||
           data.error ||
           `Erro HTTP ${response.status}.`;

       throw new Error(message);
   }


   return data;
  ```

  } catch (error) {

  ```
   clearTimeout(timeout);


   if (error.name === "AbortError") {
       throw new Error(
           "A consulta excedeu o tempo limite. Tente novamente."
       );
   }


   if (error instanceof TypeError) {
       throw new Error(
           "Não foi possível conectar ao servidor da API."
       );
   }


   throw error;
  ```

  }
  }

/**

* Consulta servidores.
*
* @param {Object} filters
* @returns {Promise<Object>}
  */
  async function searchServers(filters) {

  return await apiGet("/servidores", filters);
  }
