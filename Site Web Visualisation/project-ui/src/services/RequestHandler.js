/**
 * @class RequestHandler
 * @singleton
 *
 * @method send Envoie une requête HTTP
 */
export default class RequestHandler {
  constructor() {
    if (RequestHandler.instance) {
      return RequestHandler.instance;
    }
    RequestHandler.instance = this;
  }

  /**
   *
   * @param {string} url URL de l'endpoint
   * @param {string} method methode de la requête GET, POST, PUT, DELETE, UPDATE
   * @param {object} headers En-têtes de la requête
   * @param {object} body Corps de la requête
   * @returns {array} [status, data]
   */
  async send(url, method, headers, body) {
    var requestOptions = {
      method: method,
      headers: headers,
      redirect: "manual",
    };
    if (method != "GET") {
      requestOptions.body = body;
    }

    const response = await fetch(url, requestOptions);
    const data = await response.json();

    return [response.status, data];
  }
}
