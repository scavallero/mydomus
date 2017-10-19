

SevenSegment = function(id,options) {
    
    this.id = id;
    
    this.options = $.extend({
        "leftDigit":1,
        "rightDigit":0,
        "leftLabelDigit":0,
        "rightLabelDigit":0,
        "background":"#000000",
        "onColor":"#00ff00",
        "offColor":"#002200"
    },options);
    
    this.totaldigit = this.options.leftDigit+this.options.rightDigit+this.options.leftLabelDigit+this.options.rightLabelDigit;
    
    var width = 100.0/this.totaldigit;
    var height = 100;
    var html = "";
    
    var ic4026 = [[1,1,1,1,1,1,0,1],
                  [0,1,1,0,0,0,0,1],
                  [1,1,0,1,1,0,1,1],
                  [1,1,1,1,0,0,1,1],
                  [0,1,1,0,0,1,1,1],
                  [1,0,1,1,0,1,1,0],
                  [1,0,1,1,1,1,1,0],
                  [1,1,1,0,0,0,0,0],
                  [1,1,1,1,1,1,1,0],
                  [1,1,1,1,0,1,1,0]];
    
    var html_start = '<div style="display: inline-block; height: '+height+'%; width: '+width+'%; background-color:'+this.options.background+';">';
    html_start += '<svg viewBox="-5 -5 65 85" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" focusable="false">';
    html_start += '    <defs>';
    html_start += '        <polyline id="hseg" points="11 0, 37 0, 42 5, 37 10, 11 10, 6 5"></polyline>';
    html_start += '        <polyline id="vseg" points="0 11, 5 6, 10 11, 10 34, 5 39, 0 39"></polyline>';
    html_start += '    </defs>';
    
    var html_end = '</svg></div>';
    
    draw_segment = function(digit,point) {
        
        digit = typeof digit !== 'undefined' ? digit : 0;
        point = typeof point !== 'undefined' ? point : false;
        
        var color = [this.options.offColor,this.options.onColor];
        
        var txt = '<!-- A --> <use xlink:href="#hseg" x="0" y="0" style="fill: '+color[ic4026[digit][0]]+';"></use>'
        txt +=    '<!-- B --> <use xlink:href="#vseg" x="-48" y="0" transform="scale(-1,1)" style="fill: '+color[ic4026[digit][1]]+';"></use>'
        txt +=    '<!-- C --> <use xlink:href="#vseg" x="-48" y="-80" transform="scale(-1,-1)" style="fill: '+color[ic4026[digit][2]]+';"></use>'
        txt +=    '<!-- D --> <use xlink:href="#hseg" x="0" y="70" style="fill: '+color[ic4026[digit][3]]+';"></use>'
        txt +=    '<!-- E --> <use xlink:href="#vseg" x="0" y="-80" transform="scale(1,-1)" style="fill: '+color[ic4026[digit][4]]+';"></use>'
        txt +=    '<!-- F --> <use xlink:href="#vseg" x="0" y="0" style="fill: '+color[ic4026[digit][5]]+';"></use>'
        txt +=    '<!-- G --> <use xlink:href="#hseg" x="0" y="35" style="fill: '+color[ic4026[digit][6]]+';"></use>'
        if (point) txt +=    '<!-- P --> <circle cx="52" cy="75" r="5" style="fill: '+color[1]+';"></circle>'
        
        return txt;
    }
    
    draw_degree = function(){
        
        var color = [this.options.background,this.options.onColor];
        var txt = '<circle cx="20" cy="10" r="10" style="fill: '+color[1]+';"></circle>'
        txt += '<circle cx="20" cy="10" r="5" style="fill: '+color[0]+';"></circle>'
        
        return txt;
    }
    
    draw_glyphicon = function(x,y,code,color,fsize){
        
        var txt = '<text x="'+x+'" y="'+y+'" class="glyphicon" style="font-size: '+fsize+'; fill: '+color+';">'+code+'</text>'
        return txt;
    }
    
    
    draw_digit = function(digit,point) {
        var html = html_start;
        html += draw_segment(digit,point);
        html += html_end;
        
        return html;
    }
    
    draw_label = function(opt) {
        var html = html_start;
        if (opt.indexOf("degree") >= 0)
            html+=draw_degree();
        if (opt.indexOf("flame") >= 0)
            html+=draw_glyphicon(10,35,'&#xe104;','#ff0000',36);
        if (opt.indexOf("off") >= 0)
            html+=draw_glyphicon(10,80,'&#xe017;',this.options.onColor,36);
        if (opt.indexOf("auto") >= 0)
            html+=draw_glyphicon(5,75,'AUTO','#00ff00',16);
        if (opt.indexOf("heat") >= 0)
            html+=draw_glyphicon(5,50,'HEAT','#ff0000',16);
        
        html += html_end;
        
        return html;
    }
    
    /* ************************************* 
    
       value = floating value printed on display
       opt.leftLabel = [] array of leftLabel
       opt.rightLabel = [] array of leftLabel
       
       ************************************* */
    this.draw = function(value,opt){

        options = $.extend({
            "leftLabel" : [],
            "rightLabel" : []
        },opt);
        
        var ndigit = this.options.leftDigit+this.options.rightDigit
        
        Number.prototype.pad = function(size,decimal) {
            var v = this;
            for (i=0;i<decimal;i++) v = v * 10;
            var s = String(v);
            while (s.length < (size || 2)) {s = "0" + s;}
            return s;
        }
    
        value_pad = parseFloat(value).pad(ndigit,this.options.rightDigit);
        
        var html = "";
        for (i=0;i<this.options.leftLabelDigit;i++)
            html += draw_label(options.leftLabel);
        for (i=0;i<ndigit;i++) {
            if (i == (this.options.leftDigit-1) && this.options.rightDigit > 0) {
                html += draw_digit(value_pad.substring(i,i+1),true);
            }
            else
                html += draw_digit(value_pad.substring(i,i+1),false);
        }
        for (i=0;i<this.options.rightLabelDigit;i++)
            html += draw_label(options.rightLabel);
        $('#'+this.id).html(html);
    };    
    
    return this;
};

WeThermo = function(id) {
    
    var html = '<div style="background-color: #000000;">';
            html += '    <br>';
            html += '    <div id="_'+id+'"></div>';
            html += '    <br>';
            html += '    <div align="center">';
            html += '        <button type="button" class="btn btn-success">Auto</button>';
            html += '        <button type="button" class="btn btn-danger">Heat</button>';
            html += '        <button type="button" class="btn btn-primary">Off</button>';
            html += '    </div>';
            html += '    <br>';
            html += '</div>';
    $('#'+id).html(html);
    
    this.display = SevenSegment('_'+id,{
        "leftDigit":2,
        "rightDigit":1,
        "leftLabelDigit":1,
        "rightLabelDigit":1,
        "onColor":"#0000ff",
        "offColor":"#000022"
    });
    
    this.show = function(value) {
        console.log(value);
        this.display.draw(value,{
                "rightLabel":["degree","auto","heat"],
                "leftLabel":["flame","off"]
        });
    };
    
    return this;
};