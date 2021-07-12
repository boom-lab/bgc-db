let data;

const var_translation = {
    "TEMP":"Temperature (°C)",
    "PRES":"Pressure (dbar)",
    "PSAL": "Practical Salinity",
    "DOXY":"Dissolved Oxygen (μmol/kg)",
    "CHLA":"Chlorophyll a (mg/m<sup>3</sup>)",
    "BBP700":"Particle backscattering at 700 nm (m<sup>-1</sup>)",
    "PH_IN_SITU_TOTAL":"pH total scale",
    "NITRATE":"Nitrate (μmol/kg)",
    "CDOM":"Coloured dissolved organic matter (ppb)"
}

function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}

function create_plot(response, var_selected){
    //Remove plots
    let plots_container = document.getElementById('plots');
    removeAllChildNodes(plots_container);

    //Each float, seperate plots
    for (let deployment in response){
        let dp = response[deployment] //original data
        let data = []; //data for plotly

        //Continuous data series, each profile
        if (dp['x'] != null){ // if no continuous data (nitrate)
            for ( let i = 0 ; i < dp['x'].length ; i++ ) {
                const result = {
                    x: dp['x'][i],
                    y: dp['y'][i],
                    type: 'scatter',
                    mode: 'lines',
                    hovertemplate: `X: %{x}<br>PRES: %{y:.0f}`,
                    marker: {
                        'color': dp['continuous_colors'][i],
                    },
                    name:`Profile: ${dp['CYCLE_ID'][i]}<br>${dp['TIME_START_PROFILE'][i]}`
                };
                data.push(result);
            }
        }

        //Discrete data series, each profile
        for ( let i = 0 ; i < dp['dis_x'].length ; i++ ) {
            const result = {
                x: dp['dis_x'][i],
                y: dp['dis_y'][i],
                type: 'scatter',
                mode: 'markers',
                marker: {
                    'color': dp['continuous_colors'][i],
                },
                hovertemplate: `X: %{x}<br>PRES: %{y:.0f}`,
                name:`Profile: ${dp['CYCLE_ID'][i]}<br>${dp['TIME_START_PROFILE'][i]}<br>${i}`
            };
            data.push(result);
        }

        const layout = {
            xaxis: {
                title: var_translation[var_selected],
                linecolor: 'black',
                linewidth: 1,
                mirror: true,
                zeroline: false,
            },
            yaxis:{title:"Pressure",
                linewidth:1,
                linecolor:'black',
                mirror: true,
                range: [2000,0]
            },
            showlegend: false,
            height: 750,
            plot_bgcolor:"#EDEDED",
            margin: {'t': 30, 'l':60,'r':30,'b':40}
        }

        
        let plot_div = document.createElement("div");
        plot_div.id = deployment;
        plot_div.className = "cohort_plot"
        
        plots_container.appendChild(plot_div);
        $('#plots').show();
        Plotly.newPlot(plot_div, data, layout);  
        
    }
}
function slider_update(start, end){

    var plotDivs = document.getElementsByClassName("cohort_plot");
    //For each plot
    for (let plot of plotDivs){

        let days = data[plot.id]['DAY'];
        days = days.concat(days);
        let indexes = days.map((elm, idx) => elm <= start | elm >= end ? idx : '').filter(String);

        //turn all traces on
        var update_vis = {
            visible:'true'
        }
        Plotly.restyle(plot, update_vis)

        //turn off traces
        if (indexes.length > 0){
            var update = {
                visible:'legendonly'
            }
            Plotly.restyle(plot, update, indexes)
        }

    }
}

//Create plot, update if year or var selected
function update(year_selected, var_selected){
    fetch(`ajax/cohort_data?year_selected=${year_selected}&var_selected=${var_selected}`)
        .then(response => response.json())
        .then(function(fetched_data){
            data = fetched_data
            create_plot(fetched_data, var_selected);
            $('.spinner-border').hide();
        })
}

//Initial load
let var_selected = $("#var_selector").val();
let year_selected = $("#year_selector").val();
update(year_selected, var_selected, 1, 365)

//Change with var selection
$("#var_selector").change(function (e) {
    e.preventDefault();
    //Unhide loading spinner
    $('#plots').hide();
    $('.spinner-border').show();
    //get selectors
    let var_selected = $("#var_selector").val();
    let year_selected = $("#year_selector").val();
    let slider_vals = document.getElementById('slider').noUiSlider.get();
    //update plot
    update(year_selected, var_selected, slider_vals[0], slider_vals[1])
})

//Change with year selection
$("#year_selector").change(function (e) {
    e.preventDefault();
    //Unhide loading spinner
    $('#graph').hide();
    $('.spinner-border').show();
    //get selectors
    let var_selected = $("#var_selector").val();
    let year_selected = $("#year_selector").val();
    let slider_vals = document.getElementById('slider').noUiSlider.get();
    //update plot
    update(year_selected, var_selected, slider_vals[0], slider_vals[1])
})

var range_all_sliders = {
    'min': [     1 ],
    'max': [ 365 ]
};

function month_formatter(value) {
    value = Math.round(value)
    let month = value
    if (value==1){
        month='Jan';
    }
    if (value==60){
        month='Mar';
    }
    if (value==121){
        month='May';
    }
    if (value==182){
        month='Jul';
    }
    if (value==244){
        month='Sep';
    }
    if (value==305){
        month='Nov';
    }
    if (value==365){
        month='Jan';
    }
    return month
}

function dateFromDay(day){
    let year_selected = document.getElementById("#year_selector");
    var date = new Date(year_selected, 0); // initialize a date in `year-01-01`
    let datef = new Date(date.setDate(day));
    let dayofmonth = datef.getDate();
    let month = datef.getMonth()+1;
    return `${month}/${dayofmonth}`;
  }

//Create slider
var slider = document.getElementById('slider');

noUiSlider.create(slider, {
    start: [1, 365],
    connect: true,
    step: 1,
    tooltips:[
        {
            to: dateFromDay,
            from: function (value) {return Number(value.replace(',-', ''));}
        },
        {
            to: dateFromDay,
            from: function (value) {return Number(value.replace(',-', ''));}
        }
    ],
    range: {
        'min': 1,
        'max': 365
    },
    range: range_all_sliders,
    pips: {
        mode: 'values',
        values: [1, 60,121,182,244,305,365],
        density: 8,
        stepped: true,
        format: {
            to: month_formatter,
            // 'from' the formatted value.
            // Receives a string, should return a number.
            from: function (value) {
                return Number(value.replace(',-', ''));
            }
        }
    }
});


//Slider change
slider.noUiSlider.on('change', function (values, handle) {
    //update plot
    slider_update(values[0], values[1])
});