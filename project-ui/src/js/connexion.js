import { Connexion } from "./helpers.js";
//Gestion du bouton d'authentification
document
  .getElementById("connexion")
  .addEventListener("click", async function (event) {
    var identifiant = document.getElementById("identifiant").value;
    var motdepasse = document.getElementById("motdepasse").value;
    var connected = await Connexion(identifiant, motdepasse);
    if (connected) {
      document.location.href = "accueil.html";
    } else {
      var denied = document.getElementById("denied");
      denied.innerHTML = "identifiants rejetés";
    }
  });
