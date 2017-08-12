    function loadInfo() {	  
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