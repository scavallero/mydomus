/**
 * Highcharts Linear-Gauge series plugin
 */
(function (H) {
    H.seriesType('lineargauge', 'column', null, {
        setVisible: function () {
            H.seriesTypes.column.prototype.setVisible.apply(this, arguments);
            if (this.markLine) {
                this.markLine[this.visible ? 'show' : 'hide']();
            }
        },
        drawPoints: function () {
            // Draw the Column like always
            H.seriesTypes.column.prototype.drawPoints.apply(this, arguments);

            // Add a Marker
            var series = this,
                chart = this.chart,
                inverted = chart.inverted,
                xAxis = this.xAxis,
                yAxis = this.yAxis,
                point = this.points[0], // we know there is only 1 point
                markLine = this.markLine,
                ani = markLine ? 'animate' : 'attr';

            // Hide column
            point.graphic.hide();

            if (!markLine) {
                var path = inverted ? ['M', 0, 0, 'L', -5, -5, 'L', 5, -5, 'L', 0, 0, 'L', 0, 0 + xAxis.len] : ['M', 0, 0, 'L', -5, -5, 'L', -5, 5, 'L', 0, 0, 'L', xAxis.len, 0];
                markLine = this.markLine = chart.renderer.path(path)
                    .attr({
                        'fill': series.color,
                        'stroke': series.color,
                        'stroke-width': 1
                    }).add();
            }
            markLine[ani]({
                translateX: inverted ? xAxis.left + yAxis.translate(point.y) : xAxis.left,
                translateY: inverted ? xAxis.top : yAxis.top + yAxis.len -  yAxis.translate(point.y)
            });
        }
    });
}(Highcharts));

/***** Theme ****/
    
Highcharts.setOptions({
	global: {
		useUTC: false
	},
	credits: {
		enabled: false
	}
});

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

/**** Styles ****/
    
linear_gauge_style = {
	chart: {
		type: 'lineargauge',
		//inverted: false
	},
	exporting:{enabled:false},
	title: {
		text: ''
	},
	xAxis: {
		lineColor: '#C0C0C0',
		labels: {
			enabled: false
		},
		tickLength: 0
	},
	yAxis: {
		/*min: 0,
		max: 120,
		tickLength: 5,
		tickWidth: 1,
		tickColor: '#C0C0C0',
		gridLineColor: '#C0C0C0',
		gridLineWidth: 1,
		minorTickInterval: 5,
		minorTickWidth: 1,
		minorTickLength: 5,
		minorGridLineWidth: 0,*/
		min: 0,
		max: 120,
		
		minorTickWidth: 1,
		minorTickLength: 10,
		minorTickPosition: 'inside',
		minorTickColor: '#666',

		tickPixelInterval: 30,
		tickWidth: 2,
		tickPosition: 'inside',
		tickLength: 10,
		tickColor: '#666',
		
		title: {
			text: 'Chart title'
		},
		labels: {
			format: '{value}'
		},
		plotBands: [{
			from: 0,
			to: 60,
			color: '#55BF3B' // green
		}, {
			from:60,
			to: 80,
			color: '#DDDF0D' // yellow
		}, {
			from: 80,
			to: 120,
			color: '#DF5353' // red
		}]
	},
	legend: {
		enabled: false
	}
}

gauge_style = {

	chart: {
		type: 'gauge',
		backgroundColor: null,
		plotBorderWidth: 0,
		plotShadow: false
	},
	exporting:{enabled:false},
	title: {
		text: 'Chart title'
	},
	pane: {
		startAngle: -150,
		endAngle: 150,
		background: [{
			backgroundColor: {
				linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
				stops: [
					[0, '#FFF'],
					[1, '#333']
				]
			},
			borderWidth: 0,
			outerRadius: '109%'
		}, {
			backgroundColor: {
				linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
				stops: [
					[0, '#333'],
					[1, '#FFF']
				]
			},
			borderWidth: 1,
			outerRadius: '107%'
		}, {
			// default background
		}, {
			backgroundColor: '#DDD',
			borderWidth: 0,
			outerRadius: '105%',
			innerRadius: '103%'
		}]
	},

	// the value axis
	yAxis: {
		min: 0,
		max: 120,

		minorTickInterval: 'auto',
		minorTickWidth: 1,
		minorTickLength: 10,
		minorTickPosition: 'inside',
		minorTickColor: '#666',

		tickPixelInterval: 30,
		tickWidth: 2,
		tickPosition: 'inside',
		tickLength: 10,
		tickColor: '#666',
		labels: {
			step: 2,
			rotation: 'auto'
		},
		title: {
			text: 'C'
		},
		plotBands: [{
			from: 0,
			to: 60,
			color: '#55BF3B' // green
		}, {
			from:60,
			to: 80,
			color: '#DDDF0D' // yellow
		}, {
			from: 80,
			to: 120,
			color: '#DF5353' // red
		}]
	}
}

graph_history_style = {
	chart: {
		zoomType: 'x'
	},
	title: {
		text: 'Measure variation by day'
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
			text: null
		}
	},
	tooltip: {
		crosshairs: true,
		shared: true,
		valueSuffix: ' '
	},
	legend: {
		enabled: false
	}
}



graph_style = {
	chart: {
		zoomType: 'x'
	},
	title: {
		text: 'Daily Values'
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
	}
}
