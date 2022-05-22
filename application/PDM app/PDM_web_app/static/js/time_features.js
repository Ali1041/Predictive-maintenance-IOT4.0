const features = JSON.parse(document.getElementById('features_x').textContent);
let mean = []
let std = []
let crest = []
let clearance = []
let kurtosis = []
let skewness = []
let impulse = []
let shape = []
let labelsMean = []
features.map((item, index)=>{
    mean.push(item.mean)
    std.push(item.std);
    crest.push(item.crest)
    clearance.push(item.clearance)
    kurtosis.push(item.kurtosis)
    skewness.push(item.skewness)
    impulse.push(item.impulse)
    shape.push(item.shape)
    labelsMean.push(index)
});
console.log(mean, shape)
  let canvas = document.getElementById('mean').getContext('2d')
  new Chart(canvas, {
            type: 'line',
            data: {
                labels: labelsMean,
                datasets: [{
                    data:mean,
                }]
            },
            options: {
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


canvas = document.getElementById('std').getContext('2d')
  new Chart(canvas, {
            type: 'line',
            data: {
                labels: labelsMean,
                datasets: [{
                    data:std,
                }]
            },
            options: {
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

canvas = document.getElementById('crest').getContext('2d')
  new Chart(canvas, {
            type: 'line',
            data: {
                labels: labelsMean,
                datasets: [{
                    data:crest,
                }]
            },
            options: {
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

canvas = document.getElementById('clear').getContext('2d')
  new Chart(canvas, {
            type: 'line',
            data: {
                labels: labelsMean,
                datasets: [{
                    data:clearance,
                }]
            },
            options: {
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

canvas = document.getElementById('kur').getContext('2d')
  new Chart(canvas, {
            type: 'line',
            data: {
                labels: labelsMean,
                datasets: [{
                    data:kurtosis,
                }]
            },
            options: {
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


canvas = document.getElementById('skew').getContext('2d')
  new Chart(canvas, {
            type: 'line',
            data: {
                labels: labelsMean,
                datasets: [{
                    data:skewness,
                }]
            },
            options: {
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


canvas = document.getElementById('impulse').getContext('2d')
  new Chart(canvas, {
            type: 'line',
            data: {
                labels: labelsMean,
                datasets: [{
                    data:impulse,
                }]
            },
            options: {
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


canvas = document.getElementById('shape').getContext('2d')
  new Chart(canvas, {
            type: 'line',
            data: {
                labels: labelsMean,
                datasets: [{
                    data:shape,
                }]
            },
            options: {
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