    function loadInfo() {	  
    }

	var temperature_style = {

        chart: {
            type: 'gauge',
			backgroundColor: $("body").css("background-color"),
            plotBorderWidth: 0,
            plotShadow: false
        },

		credits: {
			enabled: false
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
        },

        series: [{
            name: 'Temperature',
            data: [1],
            tooltip: {
                valueSuffix: 'C'
            }
        }]

    }
	
	
    /**
     * Get the current time
     */
    function getNow() {
        var now = new Date();

        return {
            hours: now.getHours() + now.getMinutes() / 60,
            minutes: now.getMinutes() * 12 / 60 + now.getSeconds() * 12 / 3600,
            seconds: now.getSeconds() * 12 / 60
        };
    }
	
    function btn1() {
        $.get("/hello",function( response ) {
    	    console.log( response ); // server response
	    });
    }
  
    /**
     * Clear div elements
     */  
    function clearDiv(div) {
	    console.log(div);
	    $(div).empty();  
    }