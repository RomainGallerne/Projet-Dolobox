import AuthService from "./services/AuthService.js";
import PatientService from "./services/PatientService.js";

(async function () {
  const authService = new AuthService();
  const patientService = new PatientService();
  try {
    let response = await authService.login("MorganDev", "123");
    console.log(response);

    response = await patientService.getPatients();
    console.log(response);

    response = await patientService.getPainRecords(6);
    console.log(response);
    response = await authService.getLoggedInUser();
    console.log(response);
  } catch (error) {
    console.error(error);
  }
})();
