var data = {
  datasets: [
    {
      label: 'Douleur enregistrée',
      data: [],
      backgroundColor: function(context) {
        const chart = context.chart;
        const {ctx, chartArea} = chart;

        if (!chartArea) {
          // This case happens on initial chart load
          return;
        }
        return getGradient_light(ctx, chartArea);
      },
      borderColor: "#1470c7",
      borderWidth: 1,
      fill: true,
      tension: 0.1
    }
  ]
};

// Fonction pour charger la liste des patients
function LoadPatients(patients) {
  //var patientList = document.getElementById('patientList');
  console.log(patients);
  // Ajouter chaque patient à la liste
  patients.forEach(function(patient) {
      var patientItem = document.createElement('div');
      patientItem.classList.add('patient-item');
      patientItem.textContent = patient.IPP + " - " + patient.prenom + " " + patient.nom;
      patientItem.addEventListener('click', async function() {
          showPatientDetails(patient);
          var patientPain_API = await window.Douleur(patient.id);
          var pain = [];
          for(let enregistement of patientPain_API[1].data){
            console.log(enregistement)
            pain.push({
              "x": enregistement.evaluation_date,
              "y": (enregistement.level/4095.0)*10.0
            });
          }
          
          console.log(pain);
          updateChart(pain);
      });
      patientList.appendChild(patientItem);
  });
}

let width, height, gradient;

function getGradient_light(ctx, chartArea) {
  const chartWidth = chartArea.right - chartArea.left;
  const chartHeight = chartArea.bottom - chartArea.top;
  if (!gradient || width !== chartWidth || height !== chartHeight) {
    // Create the gradient because this is either the first render
    // or the size of the chart has changed
    width = chartWidth;
    height = chartHeight;
    gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
    gradient.addColorStop(1.0, "#FF9999");  // Rouge clair
    gradient.addColorStop(0.5, "#FFCC66");  // Jaune clair
    gradient.addColorStop(0.0, "#99FF99");  // Vert clair
  }

  return gradient;
}

// Fonction pour afficher les détails du patient sélectionné
function showPatientDetails(patient) {
  // Afficher les détails du patient sélectionné dans la div 'patientDetails'
  var patientDetailsDiv = document.getElementById('patientDetails');
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

function getCookie(name) {
  const cookies = document.cookie.split(";");
  for (let cookie of cookies) {
    const [cookieName, cookieValue] = cookie.split("=");
    if (cookieName.trim() === name) {
      return cookieValue;
    }
  }
  return null;
}