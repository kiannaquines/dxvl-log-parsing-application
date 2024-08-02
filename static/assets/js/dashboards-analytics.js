'use strict';

(function () {
  let cardColor, headingColor, axisColor, shadeColor, borderColor;

  cardColor = config.colors.cardColor;
  headingColor = config.colors.headingColor;
  axisColor = config.colors.axisColor;
  borderColor = config.colors.borderColor;

  fetch('/dashboard/advertisement/daily/logs')
  .then( response => response.json())
  .then( jsonData => {

    var current_year = jsonData[0].year;
    var daily_logs = jsonData[0].logs;

    var currentYearDataY = daily_logs.map(item => item.daily_count);
    var currentYearDataX = daily_logs.map(item => item.date_only_aired);

    var Weeklyoptions = {
      series: [
        {
          name: `${current_year} DXVL Aired Advertisements`,
          data: currentYearDataY,
        }
      ],
      chart: {
        height: 360,
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
        categories: currentYearDataX,
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
          format: 'dd/MM/yy'
        },
      },
      colors: [config.colors.primary],
      grid:{
        show: true,
        strokeDashArray: 5,
      }
    };

    var WeeklyComparison = new ApexCharts(document.querySelector("#WeeklyComparisonAiredAdvertisements"), Weeklyoptions);
    WeeklyComparison.render();
  })

})();
