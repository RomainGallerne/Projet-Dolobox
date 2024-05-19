import AuthService from "./services/AuthService.js";
import PatientService from "./services/PatientService.js";

export async function Connexion(identifiant, motdepasse) {
  const authService = new AuthService();
  try {
    let response1 = await authService.login(identifiant, motdepasse);
    if(response1[0] == 401 || response1[0] == 404){return false;}
    else{console.log(response1);}

    let response4 = await authService.getLoggedInUser();
    if(response4[0] == 401 || response4[0] == 404){return false;}
    else{console.log(response4);}

    return true;
  } catch (error) {
    console.error(error);
    return false;
  }
}

export async function Patients(){
  const patientService = new PatientService();
  try {
    let response = await patientService.getPatients();
    if(response[0] == 401 || response[0] == 404 || response[0] == 500){return false;}
    return response;
  } catch (error) {
    console.error(error);
  }
}

export async function Douleur(id){
  try {
    const patientService = new PatientService();
    let response = await patientService.getPainRecords(id);
      if(response[0] == 401 || response[0] == 404 || response[0] == 500){return false;}
      return response;
    } catch (error) {
      console.error(error);
    }
}