var se= $("#stage");
var pe = $("#prod");
compareNodes(se,pe);
function compareNodes(ss,pp){	
  var sameFlag = true;
  if($(ss).size()>0 && $(pp).size()>0){
    var s1 = $(ss).children(); 
    var p1 = $(pp).children();
    console.log($(s1).size() +"---"+ $(p1).size())    
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
          console.log("d_prod diff:"+step+"/"+i);
        }
        if (! cs.isEqualNode(cp) && $(cs).children().size()>0 && $(cp).children().size()==0) {
          sameFlag = false;
          cs.style.color="red";		
          console.log("d_stage diff:"+step+"/"+i);
        }
      }	
      if( ! cs) {
        sameFlag = false;
        cp.style.color="red";
        console.log("prod diff:"+step+"/"+i);
      }
      if( ! cp) {
        sameFlag = false;
        cs.style.color="red";
        console.log("stage diff:"+step+"/"+i);
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
