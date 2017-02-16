function initCompare(){
	var se= $("#stage");
	var pe = $("#prod");
	var prod_top = $("#prod .zstop .zstopblock").html();	
	var stage_top = $("#stage .zstop .zstopblock").html();
	var prod_newTop = $("#prod .zstop .zstopblock").prop("outHTML");	
	var stage_newTtop = $("#stage .zstop .zstopblock").prop("outHTML");
	var prod_zsdataStyle = $("#prod .zsdata").attr("style");
	var stage_zsdataStyle = $("#stage .zsdata").attr("style");
	var zsdataStyle = "height: 1500px";
	$("#prod .zstop").remove();	
	$("#stage .zstop").remove();
	if (! $("#prod .zsblock").children().is(".zsh1")) 
	{
		$("#prod .zsblock").prepend(prod_top);
	}
	if (! $("#stage .zsblock").children().is(".zsh1")) 
	{
		$("#stage .zsblock").prepend(stage_top);
	}
	$("#stage .zsdatapad").removeAttr("style");
	$("#prod .zsdatapad").removeAttr("style");
	$("#stage .zsdata").attr("style",stage_zsdataStyle.replace(/height:(.*?)px;/,zsdataStyle));
	$("#prod .zsdata").attr("style",prod_zsdataStyle.replace(/height:(.*?)px;/,zsdataStyle));	
	console.log("stage/prod:"+se.tagName+"/"+pe.tagName);
	$(se).find("script").each(function(){$(this).remove();});
	$(pe).find("script").each(function(){$(this).remove();});
	$(se).find("a").each(function(){$(this).attr("href","");});
	$(pe).find("a").each(function(){$(this).attr("href","");});
	compareNodes(se,pe);
}	
function compareNodes(ss,pp){	
  var sameFlag = true;
  if($(ss).size()>0 && $(pp).size()>0){
    var s1 = $(ss).children(); 
    var p1 = $(pp).children();
    console.log($(s1).size() +"---"+ $(p1).size()) ;
    var step = $(s1).size() >= $(p1).size() ? $(s1).size() : $(p1).size();
    for(var i = 0 ; i < step; i++){
      var cs = s1[i];
      var cp = p1[i];
      if(cs && cp) {
        if (cs.isEqualNode(cp)) {   
          cp.style.color="black";
          cs.style.color="black";
          console.log("same:"+step+"/"+i+"--"+cs.tagName+"/"+cp.tagName);          
          continue;
        }
        if (! cs.isEqualNode(cp) && $(cs).children().size()>0 && $(cp).children().size()>0){
          sameFlag = false; 
          var csNode = getNodeInfo(cs);
          var cpNode = getNodeInfo(cp);         
          if (csNode != cpNode) {
            cp.style.color="red";
            cs.style.color="red";
            console.log("diff parent:"+step+"/"+i+"--"+csNode+"/"+cpNode);
          }
           compareNodes(cs, cp);
        }
        if (! cs.isEqualNode(cp) && $(cs).children().size()==0 && $(cp).children().size()==0) {
          sameFlag = false;
          cp.style.color="red";
          cs.style.color="red";
          console.log("text diff:"+step+"/"+i+"--"+$(cs).text()+"/"+$(cp).text());
        }
        if (! cs.isEqualNode(cp) && $(cs).children().size()==0 && $(cp).children().size()>0) {
          sameFlag = false;
          cp.style.color="red";	
          $(cp).find("a").each(function(){this.style.color="red";});
          console.log("d_prod diff:"+step+"/"+i+"--"+cs.tagName+"/"+cp.tagName);
        }
        if (! cs.isEqualNode(cp) && $(cs).children().size()>0 && $(cp).children().size()==0) {
          sameFlag = false;
          cs.style.color="red";		
          $(cs).find("a").each(function(){this.style.color="red";});
          console.log("d_stage diff:"+step+"/"+i+"--"+cs.tagName+"/"+cp.tagName);
        }
      }	
      if( ! cs) {
        sameFlag = false;
        cp.style.color="red";
        $(cp).find("a").each(function(){this.style.color="red";});
        console.log("prod diff:"+step+"/"+i+"-- /"+cp.tagName);
      }
      if( ! cp) {
        sameFlag = false;
        cs.style.color="red";
        $(cs).find("a").each(function(){this.style.color="red";});
        console.log("stage diff:"+step+"/"+i+"--"+cs.tagName+"/");
      }			
      
    } 
     return sameFlag;
  }else{
    console.log("target element don't exist!");
    return false;
  }
}

function getNodeInfo(node){
	var nodeAll= $(node).html();
	if($(node).children().size()==0) return nodeAll;
	if($(node).children().size()>0) {		
		$(node).children().each(function(){
			nodeAll=nodeAll.replace($(this).html(),"");
		});
    return nodeAll;
	}
}