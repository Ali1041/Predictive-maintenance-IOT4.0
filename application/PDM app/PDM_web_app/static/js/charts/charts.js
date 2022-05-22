
  const sensorOne = JSON.parse(document.getElementById('sensor_one').textContent);
  const sensorTwo = JSON.parse(document.getElementById('sensor_two').textContent);
  let oneDataX = []
  let oneDataY = []
  let labels = []
  let twoDataX = []
  let twoDataY = []
  sensorOne.map((item, index) => {
      // if (index === 21000){ break;}
      oneDataX.push(item.x_axis);
      oneDataY.push(item.y_axis);
      twoDataX.push(sensorTwo[index].x_axis);
      twoDataY.push(sensorTwo[index].x_axis);
      labels.push(index);
  });
  let selectCanvas = document.getElementById('vibrationChartOneX').getContext('2d')
  new Chart(selectCanvas, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    data:oneDataX,
                    backgroundColor:'white',
                    fill:true,
                    borderColor:'rgb(173,216,230)',
                    borderWidth:1,
                    label:'',
                }]
            },
            options: {
                legend:{
                    display:false
                },
                elements: {
                    point:{
                        radius: 0
                    }
                },
                scales: {
                    x: {
                        display:false
                    }
                }
            },

        });

  selectCanvas = document.getElementById('vibrationChartOneY').getContext('2d')
  new Chart(selectCanvas, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    data:oneDataY,
                    label:'',
                    backgroundColor:'white',
                    fill:true,
                    borderColor:'rgb(173,216,230)',
                    borderWidth:1
                }]
            },
            options: {
                elements: {
                    point:{
                        radius: 0
                    }
                },
                tooltips: {enabled: false},
                hover: {mode: null},
                scales: {
                    x: {
                        display:false
                    }
                }
            },

        });

  selectCanvas = document.getElementById('vibrationChartTwoX').getContext('2d')
   new Chart(selectCanvas, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    data:twoDataX,
                    label:'',
                    backgroundColor:'white',
                    fill:true,
                    borderColor:'rgb(173,216,230)',
                    borderWidth:1
                }]
            },
            options: {
                elements: {
                    point:{
                        radius: 0
                    }
                },
                tooltips: {enabled: false},
                hover: {mode: null},
                scales: {
                    x: {
                        display:false
                    }
                }
            },

        });

  selectCanvas = document.getElementById('vibrationChartTwoY').getContext('2d')
  new Chart(selectCanvas, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    data:twoDataY,
                    label:'',
                    backgroundColor:'white',
                    fill:true,
                    borderColor:'rgb(173,216,230)',
                    borderWidth:1
                }]
            },
            options: {
                elements: {
                    point:{
                        radius: 0
                    }
                },
                tooltips: {enabled: false},
                hover: {mode: null},
                scales: {
                    x: {
                        display:false
                    }
                }
            },

        });