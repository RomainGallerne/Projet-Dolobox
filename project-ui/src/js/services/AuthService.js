import RequestHandler from "./RequestHandler.js";
/**
 * Service pour gérer l'authentification
 * @class AuthService
 *
 * @property {string} API_URL URL de l'API
 * @property {object} headers En-têtes de la requête
 *
 * @method send Envoie une requête HTTP
 * @method getLoggedInUser Récupère l'utilisateur connecté
 * @method login Connecte un utilisateur
 * @method getCookie Récupère un cookie
 * @method setCookie Définit un cookie
 */
export default class AuthService {
  API_URL = "https://eriospainapi.onrender.com";

  constructor() {
    if (AuthService.instance) {
      return AuthService.instance;
    }
    this.headers = {
      "Content-Type": "application/json",
    };
    this.requestHandler = new RequestHandler();
    AuthService.instance = this;
  }

  /**
   * Récupère l'utilisateur connecté grâce au token stocké dans un cookie
   * @returns {array} [status, data]
   */
  async getLoggedInUser() {
    const url = `${this.API_URL}/api/user`;
    const method = "GET";
    const token = this.getCookie("token");
    const headers = {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    };

    return this.requestHandler.send(url, method, headers);
  }
  /**
   * Connecte un utilisateur
   * @param {string} username Nom d'utilisateur
   * @param {string} password Mot de passe
   * @returns {array} [status, data]
   */
  async login(username, password) {
    const url = `${this.API_URL}/api/login`;
    const method = "POST";

    const body = JSON.stringify({ username: username, password: password });
    const response = await this.requestHandler.send(
      url,
      method,
      this.headers,
      body
    );
    const token = response[1]["accessToken"];
    this.setCookie("token", token, 1); // Mettez le token dans un cookie expirant dans 7 jours

    return response;
  }
  async logout() {
    this.setCookie("token", "", 0);
  }
  /**
   *
   * @param {string} name clef du cookie
   * @returns {string} valeur du cookie
   */
  getCookie(name) {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      const [cookieName, cookieValue] = cookie.split("=");
      if (cookieName.trim() === name) {
        return cookieValue;
      }
    }
    return null;
  }
  /**
   * Définit un cookie dans le navigateur
   * @param {string} name clef du cookie
   * @param {string} value valeur du cookie
   * @param {number} hours durée de vie du cookie en heures
   */
  setCookie(name, value, hours) {
    let expires = "";
    if (hours) {
      const date = new Date();
      date.setTime(date.getTime() + hours * 60 * 60 * 1000);
      expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
  }
}
