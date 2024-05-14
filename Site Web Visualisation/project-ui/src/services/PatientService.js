import AuthService from "./AuthService.js";
import RequestHandler from "./RequestHandler.js";
/**
 * Service pour gérer les patients
 * @class PatientService
 * @singleton
 *
 * @property {string} API_URL URL de l'API
 * @property {object} headers En-têtes de la requête
 * @property {object} authService Service d'authentification
 * @property {object} requestHandler Service pour envoyer des requêtes HTTP
 *
 * @method getPatients Récupère la liste des patients
 * @method getPatient Récupère un patient
 * @method getPainRecords Récupère les enregistrements de douleur d'un patient
 */
export default class PatientService {
  API_URL = "https://eriospainapi.onrender.com";

  constructor() {
    if (PatientService.instance) {
      return PatientService.instance;
    }
    this.headers = {
      "Content-Type": "application/json",
    };
    this.authService = new AuthService();
    this.requestHandler = new RequestHandler();
    PatientService.instance = this;
  }
  /**
   * Récupère la liste des patients
   * @returns {array} [status, data]
   */
  async getPatients() {
    const url = `${this.API_URL}/api/patients`;
    const method = "GET";
    const token = this.authService.getCookie("token");
    const headers = {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    };

    return await this.requestHandler.send(url, method, headers);
  }
  /**
   * Récupère un patient
   * @param {number} id Patient ID
   * @returns {array} [status, data]
   */
  async getPainRecords(id) {
    const url = `${this.API_URL}/api/patient/${id}/streams`;
    const method = "GET";
    const token = this.authService.getCookie("token");
    const headers = {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    };

    return await this.requestHandler.send(url, method, headers);
  }
}
