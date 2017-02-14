var base_fn = function(ticks,i) {
    return ticks.append("svg:image")
        .attr("xlink:href","/static/img/link.png")
        .attr("width", 18)
        .attr("height",18)
        .attr("x", -margin.left + 5 + (i*20))
        .attr("y", -9);
}

var icon_fns = {"link" : function(ticks, i) {
    var k = ticks[0][0].baseURI.split("/").reverse()[2];
      base_fn(ticks,i)
        .attr("xlink:href","/static/img/link.png")
        .attr("class", "linkIcon icon")
        .on("click", function(d) { window.location.href = "/topic_explorer/doc/" + k + "/" + encodeURIComponent(d);});
  },
  "ver" : function(ticks, i) {
      //var propuesta = ticks[0][i].__data__;
      console.log(ticks);
      base_fn(ticks,i)
        .attr("xlink:href","/static/img/document.png")
        .attr("class", "verIcon icon")
        .on("click", function(d) { window.open("/topic_explorer/see_topic/"+d+"/",'_blank');});
  },
 "ap" : function(ticks, i) {
      base_fn(ticks,i)
        .attr("data-doc-id", function (d) {return d})
        .attr("xlink:href","/static/ap.jpg")
        .attr("class", "apIcon icon")
        .attr("onclick", function(d) { return (d) ? "fulltext.popover(this)" : ""; });
  },
 "fulltext" : function(ticks, i) {
      base_fn(ticks,i)
        .attr("data-doc-id", function (d) {return d})
        .attr("xlink:href","/static/icon-book.png")
        .attr("class", "fulltextIcon icon")
        .attr("onclick", function(d) { return (d) ? "fulltext.popover(this)" : ""; });
  },
 "htrc" : function(ticks, i) {
      base_fn(ticks,i)
        .attr("xlink:href","/static/htrc.png")
        .attr("class", "htrcIcon icon")
        .attr("data-htrc-id", function(d) { return d; })
        .attr("onclick", function(d) { return (d) ? "htrc.popover(this)" : ""; });
  },
 "inpho" : function(ticks, i) { 
      base_fn(ticks,i)
        .attr("xlink:href","/static/topic_explorer/inpho.png")
        .attr("class", "inphoIcon icon")
        .on("click", function(d) { window.open("https://inpho.cogs.indiana.edu/entity?redirect=True&sep=" + d, "_blank");});
   },
 "sep" : function(ticks, i) {
      base_fn(ticks,i)
        .attr("xlink:href","/static/topic_explorer/sep.png")
        .attr("class", "sepIcon icon")
        .on("click", function(d) { window.open("http://plato.stanford.edu/entires/" + d, "_blank");});
   }
};

String.prototype.format = String.prototype.f = function() {
    var s = this,
        i = arguments.length;

    while (i--) {
        s = s.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
    }
    return s;
};

var icon_tooltips = {
    "link" : 'Click para enfocar el Modelado de Tópicos en este documento.',
    "ver" : 'Click para ver este documento.',
    "ap" : 'Click for the full-text.',
    "fulltext" : 'Click for the full-text.',
    "htrc" : 'Click for the HathiTrust Details.',
    "inpho" : 'Click to see more information<br /> at the InPhO Project.',
    "sep" : 'Click for the SEP article.'
    };
