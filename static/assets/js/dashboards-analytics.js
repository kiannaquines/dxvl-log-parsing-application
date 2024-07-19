'use strict';

(function () {
  let cardColor, headingColor, axisColor, shadeColor, borderColor;

  cardColor = config.colors.cardColor;
  headingColor = config.colors.headingColor;
  axisColor = config.colors.axisColor;
  borderColor = config.colors.borderColor;



  var Weeklyoptions = {
    series: [
      {
        name: 'This Week Aired Advertisements',
        data: [31, 40, 28, 51, 42, 109, 100]
      },
      {
        name: 'Last Week Aired Advertisements',
        data: [31, 15, 12, 56, 46, 42, 21]
      }
    ],
    chart: {
      height: 350,
      type: 'area',
      fontFamily: 'Public Sans, Arial, sans-serif',
    },
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 1,
        opacityFrom: 0.7,
        opacityTo: 0.9,
        stops: [0, 100]
      }
    },
    dataLabels: {
      enabled: false,
    },
    stroke: {
      curve: 'smooth'
    },
    xaxis: {
      type: 'datetime',
      categories: ["2018-09-19T00:00:00.000Z", "2018-09-19T01:30:00.000Z", "2018-09-19T02:30:00.000Z", "2018-09-19T03:30:00.000Z", "2018-09-19T04:30:00.000Z", "2018-09-19T05:30:00.000Z", "2018-09-19T06:30:00.000Z"],
      labels: {
        style: {
          fontSize: '13px',
          colors: '#95A2AF'
        }
      }
    },
    yaxis: {
      labels: {
        style: {
          fontSize: '13px',
          colors: '#95A2AF'
        }
      }
    },
    tooltip: {
      shared: true,
      intersect: false,
      onDatasetHover: {
        highlightDataSeries: false,
      },
      x: {
        format: 'dd/MM/yy HH:mm'
      },
    },
    colors: [config.colors.warning,config.colors.primary],
    grid:{
      show: true,
      strokeDashArray: 5,
    }
  };

  var WeeklyComparison = new ApexCharts(document.querySelector("#WeeklyComparisonAiredAdvertisements"), Weeklyoptions);
  WeeklyComparison.render();

})();
