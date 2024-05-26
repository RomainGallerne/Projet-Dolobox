import AuthService from "./services/AuthService.js";
import { loadList } from "./fonctions.js";

var data = {
  datasets: [
    {
      label: "Douleur enregistrée",
      data: [],
      backgroundColor: function (context) {
        const chart = context.chart;
        const { ctx, chartArea } = chart;

        if (!chartArea) {
          // This case happens on initial chart load
          return;
        }
        return getGradient_light(ctx, chartArea);
      },
      borderColor: "#1470c7",
      borderWidth: 1,
      fill: true,
      tension: 0.1,
    },
  ],
};
/**
 * Définition des Charts
 */

var ctx = document.getElementById("myChart").getContext("2d");
var myChart = new Chart(ctx, {
  type: "line",
  data: {
    datasets: [
      {
        data: [],
        fill: false,
      },
    ],
  },
  options: {
    plugins: {
      legend: {
        display: false,
      },
    },
    scales: {
      x: {
        type: "time",
        adapter: "chartjs-adapter-date-fns",
        time: {
          unit: "day",
          displayFormats: {
            hour: "HH",
            day: "HH:mm.ss - dd MMM",
          },
        },
        ticks: {
          source: "data",
          display: true,
        },
      },
      y: {
        ticks: {
          display: false,
        },
        border: {
          display: false,
        },
        beginAtZero: true
      },
    },
    responsive: true,
  },
});
export { myChart };
const ctx2 = document.getElementById("mySecondChart");
new Chart(ctx2, {
  type: "line",
  data: {
    datasets: [
      {
        data: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        fill: false,
      },
    ],
  },
  options: {
    maintainAspectRatio: false,
    layout: {
      padding: {
        bottom: 36,
      },
    },
    plugins: {
      legend: {
        display: false,
      },
    },
    scales: {
      x: {
        ticks: {
          display: false,
        },
        gridLines: {
          display: false,
        },
      },
      y: {
        afterFit: (c) => {
          c.width = 40;
        },
      },
    },
  },
});
const authService = new AuthService();

const token = authService.getCookie("token");
if (!token) {
  window.location.href = "/src/html/connexion.html";
}

loadList();
