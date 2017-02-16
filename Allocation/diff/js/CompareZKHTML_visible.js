function initCompare(){
	var se = $("#stage");
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
//	console.log("stage/prod:"+se.tagName+"/"+pe.tagName);
	$(se).find("script").each(function(){$(this).remove();});
	$(pe).find("script").each(function(){$(this).remove();});
	$(se).find("a").each(function(){$(this).attr("href","");});
	$(pe).find("a").each(function(){$(this).attr("href","");});
	compareNodes(se,pe);	
	$("#stage option[style$='brown;']").parent().attr("style","background: brown");
	$("#prod option[style$='brown;']").parent().attr("style","background: brown");
}
	
function compareNodes(ss,pp){	
  var color_same = "black";
  var color_diff = "brown";
  var background_diff = "brown";
  var sameFlag = true;
  if($(ss).size()>0 && $(pp).size()>0){
    var s1 = $(ss).children("*:visible"); 
    var p1 = $(pp).children("*:visible");
	//   console.log($(s1).size() +"---"+ $(p1).size()) ;
    var step = $(s1).size() >= $(p1).size() ? $(s1).size() : $(p1).size();
    for(var i = 0 ; i < step; i++){
      var cs = s1[i];
      var cp = p1[i];
      if(cs && cp) {
       if (cs.isEqualNode(cp)) {   
          cp.style.color=color_same;
          cs.style.color=color_same;
//          console.log("same:"+step+"/"+i+"--"+cs.tagName+"/"+cp.tagName);          
          continue;
        } 
        if (! cs.isEqualNode(cp) && $(cs).children("*:visible").size()>0 && $(cp).children("*:visible").size()>0){
          sameFlag = false; 
          var csNode = getNodeInfo(cs);
          var cpNode = getNodeInfo(cp);         
          if (csNode != cpNode) {
            cp.style.color=color_diff;
            cs.style.color=color_diff;
  //          console.log("diff parent:"+step+"/"+i+"--"+csNode+"/"+cpNode);
			console.log("node diff: stage/prod"+"--"+csNode+"/"+cpNode);
          }
           compareNodes(cs, cp);
        }
        if (! cs.isEqualNode(cp) && $(cs).children("*:visible").size()==0 && $(cp).children("*:visible").size()==0) {
          sameFlag = false;
 //         cp.style.color=color_diff;
 //         cs.style.color=color_diff;
//          console.log("text diff:"+step+"/"+i+"--"+$(cs).text()+"/"+$(cp).text());
		  var csNode = getNodeInfo(cs);
          var cpNode = getNodeInfo(cp);         
          if (csNode != cpNode) {
            cp.style.color=color_diff;
            cs.style.color=color_diff;
            console.log("node diff: stage/prod"+"--"+csNode+"/"+cpNode);
          }	
		 
        }
        if (! cs.isEqualNode(cp) && $(cs).children("*:visible").size()==0 && $(cp).children("*:visible").size()>0) {
          sameFlag = false;
          var csNode = getNodeInfo(cs);
          var cpNode = getNodeInfo(cp);         
          if (csNode != cpNode) {
            cp.style.color=color_diff;
            cs.style.color=color_diff;
            console.log("node diff: stage/prod"+"--"+csNode+"/"+cpNode);
          }	
//        $(cp).find("a").each(function(){this.style.color=color_diff;});
		  $(cp).find("*").each(function(){this.style.color=color_diff;});
          console.log("stage:no / prod:diff:"+"--"+ $(cs).html()+"/"+ $(cp).html());
        }
        if (! cs.isEqualNode(cp) && $(cs).children("*:visible").size()>0 && $(cp).children("*:visible").size()==0) {
          sameFlag = false;
          var csNode = getNodeInfo(cs);
          var cpNode = getNodeInfo(cp);         
          if (csNode != cpNode) {
            cp.style.color=color_diff;
            cs.style.color=color_diff;
            console.log("node diff: stage/prod"+"--"+csNode+"/"+cpNode);
          }	
//        $(cs).find("a").each(function(){this.style.color=color_diff;});
		  $(cs).find("*").each(function(){this.style.color=color_diff;});
          console.log("stage:diff / prod:no:"+"--"+$(cs).html()+"/"+$(cp).html());
        }
      }	
      if( ! cs) {
        sameFlag = false;
        cp.style.color=color_diff;
        $(cp).find("*:visible").each(function(){this.style.color=color_diff;});
        console.log("outerHTML stage:no / prod:diff:"+"--"+$(cs).prop("outerHTML")+"/"+$(cp).prop("outerHTML"));
      }
      if( ! cp) {
        sameFlag = false;
        cs.style.color=color_diff;
        $(cs).find("*:visible").each(function(){this.style.color=color_diff;});
        console.log("outerHTML stage:diff / prod:no:"+"--"+$(cs).prop("outerHTML")+"/"+$(cp).prop("outerHTML"));
      }			
      
    } 
     return sameFlag;
  }else{
    console.log("target element don't exist!");
    return false;
  }
}

function getNodeInfo(node){
	var nodeAll= $(node).prop("outerHTML");
	if($(node).children().size()>0) {		
		$(node).children().each(function(){
			nodeAll=nodeAll.replace($(this).prop("outerHTML"),"");
		});   
	}
	return nodeAll;
}