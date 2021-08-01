const url_base = "/"
const height = 300

const colorMap = [
    "rgba(31, 119, 180, 0.8)",
    "rgba(255, 127, 14, 0.8)",
    "rgba(44, 160, 44, 0.8)",
    "rgba(214, 39, 40, 0.8)",
    "rgba(148, 103, 189, 0.8)",
    "rgba(140, 86, 75, 0.8)",
    "rgba(227, 119, 194, 0.8)",
    "rgba(127, 127, 127, 0.8)",
    "rgba(188, 189, 34, 0.8)",
    "rgba(23, 190, 207, 0.8)",
    "rgba(31, 119, 180, 0.8)",
    "rgba(255, 127, 14, 0.8)",
    "rgba(44, 160, 44, 0.8)",
    "rgba(214, 39, 40, 0.8)",
    "rgba(148, 103, 189, 0.8)",
    "rgba(140, 86, 75, 0.8)",
    "rgba(227, 119, 194, 0.8)",
    "rgba(127, 127, 127, 0.8)",
    "rgba(188, 189, 34, 0.8)",
    "rgba(23, 190, 207, 0.8)",
    "rgba(31, 119, 180, 0.8)",
    "rgba(255, 127, 14, 0.8)",
    "rgba(44, 160, 44, 0.8)",
    "rgba(214, 39, 40, 0.8)",
    "rgba(148, 103, 189, 0.8)",
    "rgba(140, 86, 75, 0.8)",
    "rgba(227, 119, 194, 0.8)",
    "rgba(127, 127, 127, 0.8)",
    "rgba(188, 189, 34, 0.8)",
    "rgba(23, 190, 207, 0.8)",
    "rgba(31, 119, 180, 0.8)",
    "rgba(255, 127, 14, 0.8)",
    "rgba(44, 160, 44, 0.8)",
    "rgba(214, 39, 40, 0.8)",
    "rgba(148, 103, 189, 0.8)",
    "magenta",
    "rgba(227, 119, 194, 0.8)",
    "rgba(127, 127, 127, 0.8)",
    "rgba(188, 189, 34, 0.8)",
    "rgba(23, 190, 207, 0.8)",
    "rgba(31, 119, 180, 0.8)",
    "rgba(255, 127, 14, 0.8)",
    "rgba(44, 160, 44, 0.8)",
    "rgba(214, 39, 40, 0.8)",
    "rgba(148, 103, 189, 0.8)",
    "rgba(140, 86, 75, 0.8)",
    "rgba(227, 119, 194, 0.8)",
    "rgba(127, 127, 127, 0.8)"
];

const hourMap = [
    "0:00", "1:00", "2:00", "3:00", "4:00", "5:00", "6:00",
    "7:00", "8:00", "9:00", "10:00", "11:00", "12:00", "13:00",
    "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00",
    "21:00", "22:00", "23:00"
];

const plotly_selector_options = {
    buttons: [{
        step: 'hour',
        stepmode: 'backward',
        count: 24,
        label: '1d'
    }, {
        step: 'hour',
        stepmode: 'backward',
        count: 168,
        label: '1w'
    }, {
        step: 'all'
    }]
};

const plotly_layout = {
    autosize: true,
    xaxis: {
        rangeselector: plotly_selector_options,
        rangeslider: {}
    },
    yaxis: {
        fixedrange: true
    },
    legend: {
        xanchor: 'center',
        yanchor: 'top',
        y: -0.5,
        x: 0.5,
        orientation: 'h'
    },
    margin: {
        l: 50,
        r: 50,
        b: 50,
        t: 50,
        pad: 4
    }
};

const plotly_option = {
    scrollZoom: true, //lets us scroll to zoom in and out - works
    showLink: false, //removes the link to edit on plotly - works
    modeBarButtonsToRemove: ['sendDataToCloud', 'hoverCompareCartesian'],
    displaylogo: false, //this is working
    displayModeBar: true, //this one does work
    doubleClick: 'reset+autoscale'
};

let chart_title = false;
let chart_title_style = false;

const color_map = {
    'primary': 'rgb(26, 179, 148)',
    'success': 'rgb(28, 132, 198)',
    'info': 'rgb(35, 198, 200)',
    'warning': 'rgb(247, 165, 74)',
    'danger': 'rgb(237, 85, 101)'
}
/*
    @param data_src: drawing data
    @param visual: visual method (hourly etc)
    @param canvas_id: id for target element
    @param title: drawing title
    @param title_style: style of the drawing title
 */
function draw(data_src, visual, canvas_id, title, title_style, url){
    chart_title = title;
    chart_title_style = title_style;
    //chart_style[canvas_id] = title_style;

    if(visual === 'hourly_data'){
        draw_hourly(data_src, canvas_id, url)
        var title = "Hourly Time-series Data";
        build_title(title, canvas_id);
        return
    }

}

function draw_hourly(setting, canvas_id, url){
    var canvas = $("#" + canvas_id)
    canvas.find(".empty-spinner").show()
    var height = canvas.find(".empty-spinner").outerHeight();
    canvas.find(".empty-spinner").css("padding-top", (height / 2 - 11) + 'px')
    $.ajax({
        type:'GET',
        url: url,
        data: {
            //we need to have some sort of access to the data
            setting: JSON.stringify(setting),
        },
        success: function(data){
            if(data['status'] === 'success'){
                var visual = setting['visual'];
                var keys = setting['keys'];
                if(visual !== 'line' && visual !=='scatter' && visual !== 'scatter_3d'
                && visual !== 'table' && keys.length > 1){
                    visual = 'line';
                }
                if(visual === 'scatter_3d'){
                    if(keys.length === 3){
                        draw_scatter_3d_chart(data, canvas_id)
                    }else{
                        visual = 'line';
                    }
                }
                if(visual === 'heat_map'){
                    draw_heatmap_chart(data, canvas_id)
                }else if(visual === '3d_plot'){
                    draw_3d_surface_chart(data, canvas_id)
                }else if(visual === 'distribution'){
                    draw_distribution_chart(data, canvas_id)
                }else if(visual === 'multiline'){
                    draw_multi_line_chart(data, canvas_id)
                }
            }
        }
    })
}

function draw_multi_line_chart(data, canvas_id){
    var lineData = JSON.parse(data['data']);
    console.log(lineData)
    var keys = data['keys']

    var xData = []
    var yData = []
    var dataLeng = lineData.length;

    for(var i=0; i<dataLeng; i++){
        var line = lineData[i];
        for(var k=0; k<keys.length; k++){
            if(typeof xData[k] === 'undefined'){
                xData[k] = []
            }
            if(typeof yData[k] === 'undefined'){
                yData[k] = []
            }
            xData[k].push(line['DateTime'])
            yData[k].push(line[keys[k]])
        }
    }

    //create results
    for(i=0; i<keys.length; i++){
        var result = {
            x: xData[i],
            y: yData[i],
            type: 'scatter',
            mode: 'lines',
            line: {
                color: colorMap[i],
                width: 2,
            }
        };
        var result2 = {
            x: [xData[i][0], xData[i][xData[i].length-1]],
            y: [yData[i][0], yData[i][yData[i].length-1]],
            type: 'scatter',
            mode: 'markers',
            marker:{
                color: colorMap[i],
                size: 12
            }
        };
        data.push(result, result2);
    }
    var layout = {
        showlegend: false,
        height: 600,
        width: 600,
        xaxis: {
            showline: true,
            showgrid: false,
            showticklabels: true,
            linecolor: 'rgb(204,204,204)',
            linewidth: 2,
            autotick: false,
            ticks: 'outside',
            tickcolor: 'rgb(204,204,204)',
            tickwidth: 2,
            ticklen: 5,
            tickfont: {
                family: 'Arial',
                size: 12,
                color: 'rgb(82,82,82)'
            }
        },
        yaxis: {
            showgrid: false,
            zeroline: false,
            showline: false,
            showticklabels: false
        },
        margin:{
            autoexpand: false,
            l: 100,
            r: 20,
            t: 100
        },
        annotations: [
            {
                
            }
        ]
    }


}

function draw_distribution_chart(data, canvas_id){
    var allData = JSON.parse(data['data']['data']);
    console.log(allData)
    var key = data['keys']

    var dataList=[]
    $.each(allData, function(i,v){
       dataList.push(v[key])
    });

    var min = data['data']['min']
    var max = data['data']['max']

    var trace={
        x: dataList,
        type: 'histogram',
        opacity: 0.5,
        marker: {
            color: 'green',
        },
        xbins:{
            start: min,
            size: 0.5,
            end: max
        }
    };

    var chart_data = [trace];
    var layout = {
        barmod: "overlay",
        autosize: true,
        yaxis: {
            fixedrange: true
        },
        margin: {
            l: 50,
            r: 50,
            b: 50,
            t: 50,
            pad: 4
        }
    };

    var id="hourly_data_dis_" + (new Date().getTime());
    var canvas = $("<div>").attr("id", id);
    $("#" + canvas_id).html("");
    $("#" + canvas_id).css("padding-left","0px").append(canvas);

    Plotly.newPlot(id, chart_data, layout, plotly_option);
    resize_plotly_chart(canvas_id, id);

}

function draw_scatter_3d_chart(data, canvas_id){
    var scatters = JSON.parse(data['data']);
    var keys = data['keys'];
    // besides keys, the data should also have a list of datetime
    var dataLeng = scatters.length
    var d1=[], d2=[], d3=[]
    for(var i=0; i<dataLeng; i++){
        var scatter = scatters[i]
        //process time
        var scattertime = scatter['DateTime']
        var check = new Date(scattertime);
        //does time really matters in 3d scatter plot?
        d1.push(parseFloat(scatter[keys[0]]))
        d2.push(parseFloat(scatter[keys[1]]))
        d3.push(parseFloat(scatter[keys[2]]))
    }

    var trace = {
        type: 'scatter3d',
        mode: 'markers',
        marker: {
            size: 4,
            symbol: 'circle',
            line: {
                color: 'rgba(255,255,255)',
                width: 0.5
            },
            color: colorMap[3]
        },
        x: d1,
        y: d2,
        z: d3
    };

    var scatter_data = {}
    scatter_data['trace'] = [trace];
    scatter_data['title_1'] = keys[0];
    scatter_data['title_2'] = keys[1];
    scatter_data['title_3'] = keys[2];

    var id = "hourly_data_3d_scatter_" + (new Date().getTime());
    var canvas = $("<div>").attr("id", id).attr("class", "scatter_3d_chart");
    $("#" + canvas_id).html("");
    $("#" + canvas_id).css("padding-left", "0px").append(canvas);

    var style = chart_title_style;
    var layout = {
        autosize: true,
        scene:{
            xaxis: {title: style && style['x_title']? style['x_title']: scatter_data['title_1']},
            yaxis: {title: style && style['y_title']? style['y_title']: scatter_data['title_2']},
            zaxis: {title: scatter_data['title_3']},
        },
        margin:{
            l: 50,
            r: 50,
            b: 50,
            t: 50,
            pad: 4
        }
    };
    //chart_data[id] = scatter_data
    Plotly.newPlot(id, scatter_data['trace'], layout, plotly_option)
    resize_plotly_chart(canvas_id, id)
}

function draw_heatmap_chart(data, canvas_id){
    var surface = JSON.parse(data['data']);
    var key = data['keys'];

    var hm_data = []
    hm_data.push(plotly_prepHeatmap(surface, key, 'heatmap'));

    var id="hourly_data_3d_surface_" + (new Date().getTime());
    var canvas = $("<div>").attr("id", id).attr("class","heatmap_chart");
    $("#" + canvas_id).html("");
    $("#" + canvas_id).css("padding-left","0px").append(canvas)

    var width = $("#" + id).css('width');
    width = parseFloat(width.substring(0, width.length-2))

    var style = chart_title_style;
    var layout = {
        autosize: true,
        width: width,
        yaxis: {
            fixedrange: true
        },
        xaxis: {
            fixedrange: true
        },
        scene:{
            xaxis: {title: style && style['x_title']? style['x_title']: 'Dates'},
            yaxis: {title: style && style['y_title']? style['y_title']: 'Hours'},
            zaxis: {title: 'Value'},
        },
        margin: {
            l: 50,
            r: 50,
            b: 100,
            t: 50,
            pad: 4
        }
    };
    chart_data[id] = hm_data;
    Plotly.newPlot(id, hm_data, layout, plotly_option)

    resize_plotly_chart(canvas_id, id);
}

function draw_3d_surface_chart(data, canvas_id){
    var surface = JSON.parse(data['data']);
    var key = data['keys'];

    var surface_data = [];
    surface_data.push(plotly_prepHeatmap(surface, key, 'surface'))

    var id="hourly_data_3d_surface_" + (new Date().getTime());
    var canvas = $("<div>").attr("id", id).attr("class", "surface_3d_chart");
    $("#" + canvas_id).html("");
    $("#" + canvas_id).css("padding-left", "0px").append(canvas);

    var width = $("#" + id).css('width');
    width = parseFloat(width.substring(0, width.length - 2));

    var style = chart_title_style;
    var layout = {
        autosize: true,
        width: width,
        scene: {
            xaxis: {title: style && style['x_title'] ? style['x_title'] : 'Dates'},
            yaxis: {title: style && style['y_title'] ? style['y_title'] : 'Hours'},
            zaxis: {title: 'Value'},
        },
        margin: {
            l: 50,
            r: 50,
            b: 50,
            t: 50,
            pad: 4
        }
    };
    chart_data[id] = surface_data;
    Plotly.newPlot(id, surface_data, layout, plotly_options);

    resize_plotly_chart(canvas_id, id);
}

/*
UNFINISHED - Need a more solid understanding on the data before
implement heat map
 */
function plotly_prepHeatmap(rawData, key, type){
    var firstData = new Date(rawData[0]['DateTime'])
    var year = firstData.getFullYear();
    var from = new Date(year-1, 11, 31);

    var days = [];
    var values = [];

    for(var i=0; i<rawData.length; i++){
        var hourlyObj = rawData[i];
        var time = hourlyObj['DateTime']
        var check = new Date(time)
        //date hour started from index 0
        var hour_min = time.split(":")
        var hour = parseInt(time.substring(time.indexOf('T')+1, time.indexOf(':')));
        if(typeof values[hour] === 'undefined'){
            values[hour] = []
        }

        var value = parseFloat(hourlyObj[key]);
        values[hour].push(value);

        //year count wrap-around
        if((+check - +from) >= 864000){
            var dayStr = (check.getMonth() + 1) + "/" + check.getDate() + "/" + check.getFullYear();
            days.push(dayStr);
            from = check
        }
    }
    var text = [];
    for(var h=0; h<hourMap.length; h++){
        var tooltip = []
        for(var d=0; d<days.length; d++){
            tooltip.push(days[d] + " " + hourMap[h] + "<br>Value: " + fixed_2(values[h][d]))
        }
        text.push(tooltip)
    }

    var trace = {
        type: type,
        colorscale: 'Viridis',
        name: key,
        x: days,
        y: hourMap,
        z: values,
        text: text,
        hoverinfo: 'text',
        zsmooth: 'best'
    };
    return trace;
}

function resize_plotly_chart(canvas_id, chart_id){
    var height = $("#" + canvas_id).outerHeight();
    $("#" + canvas_id).find(".svg_container").css("height", height+'px');
    Plotly.plots.resize(chart_id)
}

function build_title(title, canvas_id){
    if(chart_title){
        title=chart_title;
    }
}

function fixed_2(num){
    return parseFloat(parseInt(num * 100)) / 100;
}