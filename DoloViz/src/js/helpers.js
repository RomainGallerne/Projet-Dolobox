import AuthService from "./services/AuthService.js";
import PatientService from "./services/PatientService.js";

export async function Connexion(identifiant, motdepasse) {
  const authService = new AuthService();
  try {
    const response = await authService.login(identifiant, motdepasse);
    if (response[0] != 200) {
      return false;
    }

    return true;
  } catch (error) {
    return false;
  }
}

export async function Patients() {
  const patientService = new PatientService();
  try {
    const response = await patientService.getPatients();
    if (response[0] != 200) {
      return false;
    }
    return response;
  } catch (error) {
    console.error(error);
    return false;
  }
}

export async function Douleur(id) {
  try {
    const patientService = new PatientService();
    const response = await patientService.getPainRecords(id);
    if (response[0] != 200) {
      return false;
    }
    return response;
  } catch (error) {
    console.error(error);
    return false;
  }
}
