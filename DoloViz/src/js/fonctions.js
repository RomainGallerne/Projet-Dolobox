import { Patients, Douleur } from "./helpers.js";
import { myChart } from "./accueil.js";

// Fonction pour charger la liste des patients
export function LoadPatients(patients) {
  //var patientList = document.getElementById('patientList');
  // Ajouter chaque patient à la liste
  patients.forEach(function (patient) {
    var patientItem = document.createElement("div");
    patientItem.classList.add("patient-item");
    patientItem.textContent =
      patient.IPP + " - " + patient.prenom + " " + patient.nom;
    patientItem.addEventListener("click", async function () {
      showPatientDetails(patient);
      var patientPain_API = await Douleur(patient.id);
      var pain = [];
      for (let enregistement of patientPain_API[1].data) {
        pain.push({
          x: enregistement.evaluation_date,
          y: enregistement.level,
        });
      }

      updateChart(pain);
    });
    patientList.appendChild(patientItem);
  });
}

let width, height, gradient;

// Chargement de la liste des patients
export async function loadList() {
  var patientList_APIreturn = await Patients();
  var patientList = patientList_APIreturn[1].data.patients;

  LoadPatients(patientList);
}
/**
 * Met à jour le graphique de visualisation à partir des nouvelles donnés
 */

export function updateChart(dataPain) {
  myChart.data.datasets[0].data = dataPain;
  myChart.data.datasets[0].backgroundColor = function () {
    const { ctx, chartArea } = myChart;
    return getGradient_light(ctx, chartArea);
  };
  myChart.data.datasets[0].fill = true;
  myChart.update();
}
export function getGradient_light(ctx, chartArea) {
  const chartWidth = chartArea.right - chartArea.left;
  const chartHeight = chartArea.bottom - chartArea.top;
  if (!gradient || width !== chartWidth || height !== chartHeight) {
    // Create the gradient because this is either the first render
    // or the size of the chart has changed
    width = chartWidth;
    height = chartHeight;
    gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
    gradient.addColorStop(1.0, "#FF9999"); // Rouge clair
    gradient.addColorStop(0.5, "#FFCC66"); // Jaune clair
    gradient.addColorStop(0.0, "#99FF99"); // Vert clair
  }

  return gradient;
}

// Fonction pour afficher les détails du patient sélectionné
export function showPatientDetails(patient) {
  // Afficher les détails du patient sélectionné dans la div 'patientDetails'
  var patientDetailsDiv = document.getElementById("patientDetails");
  patientDetailsDiv.innerHTML = `
      <h2>Détails du patient</h2>
      <p><strong>ID :</strong> ${patient.id}</p>
      <p><strong>IPP :</strong> ${patient.IPP}</p>
      <p><strong>Prénom :</strong> ${patient.prenom}</p>
      <p><strong>Nom :</strong> ${patient.nom}</p>
      <p><strong>Date de Naissance :</strong> ${patient.dateNaissance}</p>
      <!-- Ajouter d'autres détails du patient ici -->
  `;
}
