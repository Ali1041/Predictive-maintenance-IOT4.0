const featuresOneX = JSON.parse(document.getElementById('features_one_x').textContent);
const featuresOneY = JSON.parse(document.getElementById('features_one_y').textContent);
const featuresTwoX = JSON.parse(document.getElementById('features_two_x').textContent);
const featuresTwoY = JSON.parse(document.getElementById('features_two_y').textContent);
let mean = {
    one_x:[],
    one_y:[],
    two_x:[],
    two_y:[],
}
let std = {
    one_x:[],
    one_y:[],
    two_x:[],
    two_y:[],
}
let crest = {
    one_x:[],
    one_y:[],
    two_x:[],
    two_y:[],
}
let clearance = {
    one_x:[],
    one_y:[],
    two_x:[],
    two_y:[],
}
let kurtosis = {
    one_x:[],
    one_y:[],
    two_x:[],
    two_y:[],
}
let skewness = {
    one_x:[],
    one_y:[],
    two_x:[],
    two_y:[],
}
let impulse = {
    one_x:[],
    one_y:[],
    two_x:[],
    two_y:[],
}
let shape = {
    one_x:[],
    one_y:[],
    two_x:[],
    two_y:[],
}
let labelsMean = []

function pushValues(objName, index, attribute){
    objName.one_x.push(featuresOneX[index][attribute])
    objName.one_y.push(featuresOneY[index][attribute])
    objName.two_x.push(featuresTwoX[index][attribute])
    objName.two_y.push(featuresTwoY[index][attribute])
}

featuresOneX.map((item, index)=>{
    pushValues(mean, index, 'mean')
    pushValues(std, index, 'std')
    pushValues(crest, index, 'crest')
    pushValues(clearance, index, 'clearance')
    pushValues(kurtosis, index, 'kurtosis')
    pushValues(skewness, index, 'skewness')
    pushValues(impulse, index, 'impulse')
    pushValues(shape, index, 'shape')
    labelsMean.push(index)
});
function makeGraphs(idName, value, index) {
    const mapping = {
        1:'one_x',
        2:'one_y',
        3:'two_x',
        4:'two_y'
    }
    const attribute = mapping[index]
    let canvas = document.getElementById(idName).getContext('2d')
    new Chart(canvas, {
        type: 'line',
        data: {
            labels: labelsMean,
            datasets: [{
                data: value[attribute],
                label:'',
                backgroundColor:'rgb(173,216,230)',
                    fill:true,
                    borderColor:'rgb(199,216,230)',
                    borderWidth:1,
            }]
        },
        options: {
            elements: {
                point: {
                    radius: 0
                }
            },
            scales: {
                x: {
                    display: false
                }
            }
        },

    });
}

for (let i=1;i<5;i++){
    makeGraphs(`mean-${i}`,mean, i)
    makeGraphs(`std-${i}`,std, i)
    makeGraphs(`clear-${i}`,clearance, i)
    makeGraphs(`crest-${i}`,crest, i)
    makeGraphs(`kur-${i}`,kurtosis, i)
    makeGraphs(`shape-${i}`,shape, i)
    makeGraphs(`impulse-${i}`,impulse, i)
    makeGraphs(`skew-${i}`,skewness, i)
}

function applyFeatureFilter(e){
    const val = e.target.value
    const mean = document.getElementById('mean');
    const crest = document.getElementById('crest');
    const skew = document.getElementById('skew');
    const std = document.getElementById('std');
    const clear = document.getElementById('clear');
    const kur = document.getElementById('kur');
    const impulse = document.getElementById('impulse');
    const shape = document.getElementById('shape');
    for (let i=0;i<=3;i++){
        mean.children[i].style.display = 'none';
        crest.children[i].style.display = 'none';
        skew.children[i].style.display = 'none';
        std.children[i].style.display = 'none';
        clear.children[i].style.display = 'none';
        impulse.children[i].style.display = 'none';
        kur.children[i].style.display = 'none';
        shape.children[i].style.display = 'none';
    };
        mean.children[val].style.display = 'block';
        crest.children[val].style.display = 'block';
        skew.children[val].style.display = 'block';
        std.children[val].style.display = 'block';
        clear.children[val].style.display = 'block';
        impulse.children[val].style.display = 'block';
        kur.children[val].style.display = 'block';
        shape.children[val].style.display = 'block';
}
