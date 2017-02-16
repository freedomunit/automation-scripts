function initCompare(){
	var se= $("#stage");
	var pe = $("#prod");
	console.log("stage/prod:"+se.tagName+"/"+pe.tagName);
	$(se).find("script").each(function(){$(this).remove();});
	$(pe).find("script").each(function(){$(this).remove();});
	$(se).find("*").each(function(){$(this).attr("href","");});
	$(pe).find("*").each(function(){$(this).attr("href","");});
	compareNodes(se,pe);
}	
function compareNodes(ss,pp){	
  var sameFlag = true;
  if($(ss).size()>0 && $(pp).size()>0){
    var s1 = $(ss).children(); 
    var p1 = $(pp).children();
 //   console.log($(s1).size() +"---"+ $(p1).size()) ;
    var step = $(s1).size() >= $(p1).size() ? $(s1).size() : $(p1).size();
    for(var i = 0 ; i < step; i++){
      var cs = s1[i];
      var cp = p1[i];
      if(cs && cp) {
        if (cs.isEqualNode(cp)) {   
          cp.style.color="black";
          cs.style.color="black";
    //      console.log("same:"+step+"/"+i+"--"+cs.tagName+"/"+cp.tagName);          
          continue;
        }
        if (! cs.isEqualNode(cp) && $(cs).children().size()>0 && $(cp).children().size()>0){
          sameFlag = false; 
          var csNode = getNodeInfo(cs);
          var cpNode = getNodeInfo(cp);         
          if (csNode != cpNode) {
            cp.style.color="red";
            cs.style.color="red";
            console.log("diff parent node:"+"--"+csNode+"/"+cpNode);
          }
           compareNodes(cs, cp);
        }
        if (! cs.isEqualNode(cp) && $(cs).children().size()==0 && $(cp).children().size()==0) {
          sameFlag = false;
          cp.style.color="red";
          cs.style.color="red";
          console.log("diff node:"+"--"+$(cs).prop("outerHTML")+"/"+$(cp).prop("outerHTML"));
        }
        if (! cs.isEqualNode(cp) && $(cs).children().size()==0 && $(cp).children().size()>0) {
          sameFlag = false;
          var csNode = getNodeInfo(cs);
          var cpNode = getNodeInfo(cp);         
          if (csNode != cpNode) {
            cp.style.color="red";
            cs.style.color="red";
			console.log("diff parent:"+step+"/"+i+"--"+csNode+"/"+cpNode);
          }
          $(cp).find("*").each(function(){this.style.color="red";});
          console.log("prod_childNodes diff:"+step+"/"+i+"--"+$(cs).html()+"/"+$(cp).html());
        }
        if (! cs.isEqualNode(cp) && $(cs).children().size()>0 && $(cp).children().size()==0) {
          sameFlag = false;
		  var csNode = getNodeInfo(cs);
          var cpNode = getNodeInfo(cp);         
          if (csNode != cpNode) {
            cp.style.color="red";
            cs.style.color="red";
			console.log("diff parent:"+step+"/"+i+"--"+csNode+"/"+cpNode);
          }
          cs.style.color="red";		
          $(cs).find("a").each(function(){this.style.color="red";});
          console.log("stage_childNodes diff:"+step+"/"+i+"--"+$(cs).html()+"/"+$(cp).html());
        }
      }	
      if( ! cs) {
        sameFlag = false;
        cp.style.color="red";
        $(cp).find("a").each(function(){this.style.color="red";});
        console.log("prod diff:"+step+"/"+i+"-- /"+$(cp).prop("outerHTML"));
      }
      if( ! cp) {
        sameFlag = false;
        cs.style.color="red";
        $(cs).find("a").each(function(){this.style.color="red";});
        console.log("stage diff:"+step+"/"+i+"--"+$(cs).prop("outerHTML")+"/");
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
//	if($(node).children().size()==0) return nodeAll;
	if($(node).children().size()>0) {		
		$(node).children().each(function(){
			nodeAll=nodeAll.replace($(this).html(),"");
		});
    return nodeAll;
	}
}
