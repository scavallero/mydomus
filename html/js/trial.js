/**
 * Get the current time
 */
 
function doAll() {

    doTheme();
    
    $.post("gateway.php",{"url": "/get/sensor/config"},function(response){
        var jsonresp = JSON.parse(response);
        var groups = jsonresp['value'];
        jQuery.each(groups, function(item, val) {
            jQuery.each(val['Peripherials'], function(sensorname, val) {
                var html='';
                html += '<div data-role="collapsible">';
                html +=   '<h4>'+sensorname+'</h4>';
                html +=   '<div class="ui-grid-a ui-responsive">'
                html +=     '<div class="ui-block-a">';
                html +=       '<div id="gauge_'+sensorname+'">';
                html +=       '</div>';
                html +=     '</div>';
                html +=     '<div class="ui-block-b">';
                html +=       '<div id="graph_'+sensorname+'">';
                html +=       '</div>';
                html +=     '</div>';
                html +=   '</div>';
                html += '</div>';
                $("#sensorlist").append(html).collapsibleset('refresh');;
                
                var chart1 = Highcharts.chart('gauge_'+sensorname,temperature_style,function (chart) {
                    if (!chart.renderer.forExport) {
                        setInterval(function () {
                            if(chart.series) { // Prevent calls on false redraw
                                var point = chart.series[0].points[0];
                                $.post("gateway.php",{"url": "/get/sensor/"+sensorname},function(response){
                                var newVal = JSON.parse(response);
                                point.update(newVal['value']); 
                                });
                            }
                        }, 3000);
                    }
                });
    
                var data = [1,100,74,5,23,7,33,60,80,90,45,23,1];
                var graph1 = Highcharts.chart('graph_'+sensorname, {
                    chart: {
                        zoomType: 'x'
                    },
                    credits: {
                        enabled: false
                    },
                    title: {
                        text: 'CPU Temperature'
                    },
                    subtitle: {
                        text: document.ontouchstart === undefined ?
                                'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
                    },
                    xAxis: {
                        type: 'datetime'
                    },
                    yAxis: {
                        title: {
                            text: 'Temperature'
                        }
                    },
                    legend: {
                        enabled: false
                    },
                    plotOptions: {
                        area: {
                            fillColor: {
                                linearGradient: {
                                    x1: 0,
                                    y1: 0,
                                    x2: 0,
                                    y2: 1
                                },
                                stops: [
                                    [0, Highcharts.getOptions().colors[0]],
                                    [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                                ]
                            },
                            marker: {
                                radius: 2
                            },
                            lineWidth: 1,
                            states: {
                                hover: {
                                    lineWidth: 1
                                }
                            },
                            threshold: null
                        }
                    },

                    series: [{
                        type: 'area',
                        name: 'Temp',
                        data: data
                    }]
                });
                console.log(sensorname);
            });
        });  
    });
}

function doTheme() {
    Highcharts.theme = {
       colors: ['#f45b5b', '#8085e9', '#8d4654', '#7798BF', '#aaeeee', '#ff0066', '#eeaaee',
          '#55BF3B', '#DF5353', '#7798BF', '#aaeeee'],
       chart: {
          backgroundColor: null,
          style: {
             fontFamily: 'Signika, serif'
          }
       },
       title: {
          style: {
             color: 'black',
             fontSize: '16px',
             fontWeight: 'bold'
          }
       },
       subtitle: {
          style: {
             color: 'black'
          }
       },
       tooltip: {
          borderWidth: 0
       },
       legend: {
          itemStyle: {
             fontWeight: 'bold',
             fontSize: '13px'
          }
       },
       xAxis: {
          labels: {
             style: {
                color: '#6e6e70'
             }
          }
       },
       yAxis: {
          labels: {
             style: {
                color: '#6e6e70'
             }
          }
       },
       plotOptions: {
          series: {
             shadow: true
          },
          candlestick: {
             lineColor: '#404048'
          },
          map: {
             shadow: false
          }
       },

       // Highstock specific
       navigator: {
          xAxis: {
             gridLineColor: '#D0D0D8'
          }
       },
       rangeSelector: {
          buttonTheme: {
             fill: 'white',
             stroke: '#C0C0C8',
             'stroke-width': 1,
             states: {
                select: {
                   fill: '#D0D0D8'
                }
             }
          }
       },
       scrollbar: {
          trackBorderColor: '#C0C0C8'
       },

       // General
       background2: '#E0E0E8'

    };

    // Apply the theme
    Highcharts.setOptions(Highcharts.theme);
}