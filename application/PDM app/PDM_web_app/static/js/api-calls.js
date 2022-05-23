

function applyFilter(e){
    const value = e.target.value
    const vibrationCharts = document.getElementById('vibrationCharts');
    const fftCharts = document.getElementById('fftCharts');
    const envelopeCharts = document.getElementById('envelopeCharts');
    const features = document.getElementById('features');
    for (let i=0;i<=3;i++){
        vibrationCharts.children[i].style.display = 'none';
        fftCharts.children[i].style.display = 'none';
        envelopeCharts.children[i].style.display = 'none';
        features.children[i].style.display = 'none';
    }
    vibrationCharts.children[value].style.display = 'block';
    fftCharts.children[value].style.display = 'block';
    envelopeCharts.children[value].style.display = 'block';
    features.children[value].style.display = 'block';
}


fetch('http://127.0.0.1:8000/fft-api/')
    .then((response) => {
            return response.json()
        })
    .then((data) => {
    let oneFFTX = [];
    let labelsFFT = [];
      let oneFFTY = [];
      let twoFFTX = [];
      let twoFFTY = [];
        data.y_1_x_val.map((item, index) => {
        oneFFTX.push(item);
        labelsFFT.push(index);
        oneFFTY.push(data.y_1_y_val[index]);
        twoFFTX.push(data.y_2_x_val[index]);
        twoFFTY.push(data.y_2_y_val[index]);
    });
    let selectCanvas = document.getElementById('fftOverview-1').getContext('2d');
    let chart = new Chart(selectCanvas, {
            type: 'line',
            data: {
                labels: labelsFFT,
                datasets: [{
                    label:'',
                    data:oneFFTX,
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

    selectCanvas = document.getElementById('fftOverview-2').getContext('2d')
    new Chart(selectCanvas, {
            type: 'line',
            data: {
                labels: labelsFFT,
                datasets: [{
                    data:oneFFTY,
                    backgroundColor:'white',
                    fill:true,
                    borderColor:'rgb(173,216,230)',
                    borderWidth:1,
                    label:'',
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

    selectCanvas = document.getElementById('fftOverview-3').getContext('2d')
    new Chart(selectCanvas, {
            type: 'line',
            data: {
                labels: labelsFFT,
                datasets: [{
                    data:twoFFTX,
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

    selectCanvas = document.getElementById('fftOverview-4').getContext('2d')
    new Chart(selectCanvas, {
            type: 'line',
            data: {
                labels: labelsFFT,
                datasets: [{
                    data:twoFFTY,
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

});

fetch('http://127.0.0.1:8000/envelope-api/')
    .then((response) => {
            return response.json();
        })
    .then((data) => {
        console.log(data)

        let oneX = [];
        let labelsFFT = [];
        let oneY = [];
        let twoX = [];
        let twoY = [];
    data.y_one_x.map((item, index) => {
        oneX.push(item);
        labelsFFT.push(index);
        oneY.push(data.y_one_y[index]);
        twoX.push(data.y_one_y[index]);
        twoY.push(data.y_one_y[index]);
    });
    let selectCanvas1 = document.getElementById('envelope-1').getContext('2d');
        new Chart(selectCanvas1, {
            type: 'line',
            data: {
                labels: labelsFFT,
                datasets: [{
                    data:oneX,
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
            },

        });

        selectCanvas2 = document.getElementById('envelope-2').getContext('2d');
        new Chart(selectCanvas2, {
            type: 'line',
            data: {
                labels: labelsFFT,
                datasets: [{
                    data:oneY,
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
            },

        });

        selectCanvas3 = document.getElementById('envelope-3').getContext('2d');
        new Chart(selectCanvas3, {
            type: 'line',
            data: {
                labels: labelsFFT,
                datasets: [{
                    data:twoX,
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
            },

        });

        selectCanvas4 = document.getElementById('envelope-4').getContext('2d');
        new Chart(selectCanvas4, {
            type: 'line',
            data: {
                labels: labelsFFT,
                datasets: [{
                    data:twoY,
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
            },

        });

});




