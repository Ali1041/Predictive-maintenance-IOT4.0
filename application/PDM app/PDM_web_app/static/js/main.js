
const vibrationData = JSON.parse(document.getElementById('sensor_one').textContent)
let canvasV = document.getElementById('salesOverview').getContext('2d');

let labelsV = []
let dataV = []

vibrationData.map((item, index)=>{
    dataV.push(item.x_axis);
    labelsV.push(index)
})
let chart = new Chart(canvasV, {
            type: 'line',
            data: {
                labels: labelsV,
                datasets: [{
                    label:'',
                    data:dataV,
                    backgroundColor:'white',
                    fill:true,
                    borderColor:'rgb(173,216,230)',
                    borderWidth:1,
                }]
            },
            options: {
                elements: {
                    point:{
                        radius: 0
                    }
                },
                scales: {
                    y: {
                        max:1
                    },
                    x:{
                        min:0,
                        max:10000,
                        ticks:{
                            stepSize:1000
                        }
                    }
                }
            },

        });