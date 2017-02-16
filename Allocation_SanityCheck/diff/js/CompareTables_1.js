function compareTables(){
	$(".nav").each(function(){$(this).hide()});
	var sCriteria = $("#stage").find(".black");
	var pCriteria = $("#prod").find(".black");
	if(sCriteria.text() != pCriteria.text()) {
		sCriteria.css("background-color","red");		
		pCriteria.css("background-color","red");
	}
	var sTime = $("#stage").find("div")[1];
	var pTime = $("#prod").find("div")[1];
	if(sTime.innerHTML != pTime.innerHTML) {
		sTime.style.background="red";		
		pTime.style.background="red";
	}	
    var t1 = document.getElementsByClassName("table3")[0];   //document.getElementById("stage"); 
    var t2 = document.getElementsByClassName("table3")[1];   //document.getElementById("prod"); 
    var sRowCount = t1.rows.length;
    var pRowCount = t2.rows.length;
    var minRows = (sRowCount >=  pRowCount ? pRowCount : sRowCount);
  	var maxRows = (sRowCount >=  pRowCount ? sRowCount : pRowCount);
  	console.log( "stage row count/"+sRowCount +"---prod row count/"+pRowCount+"   min/max rows---"+minRows+"/"+maxRows);
    for(var i=0; i<maxRows; i++){    	
    	if (i< minRows) {
    		if(t1.rows[i].innerHTML == t2.rows[i].innerHTML){     			
    			countinue;
    		}else {    		
    			t2.rows[i].style.backgroundColor = '#F00';
		        t1.rows[i].style.backgroundColor = '#F00';	 			
	    		var sCellCount = t1.rows[i].cells.length
	   			var pCellCount = t2.rows[i].cells.length    		
	    		var maxCells = (sCellCount >= pCellCount ? sCellCount : pCellCount);
	   			var minCells = (sCellCount >= pCellCount ? pCellCount : sCellCount);
	   			console.log( i +"row cellsCount stage/prod: "+minCells+"/"+maxCells);
		        for(var p=0; p<maxCells; p++){		        	
		             if(p< minCells && t1.rows[i].cells[p].innerHTML == t2.rows[i].cells[p].innerHTML){	             	
		      	        t2.rows[i].cells[p].style.backgroundColor = '#FFF';
		                t1.rows[i].cells[p].style.backgroundColor = '#FFF';
		                console.log("row/col: "+i+"/"+p+ "---stage:"+t1.rows[i].cells[p].innerHTML+"/prod:"+t2.rows[i].cells[p].innerHTML);	
		            }
		             if(p >= minCells && t1.rows[i].cells.length > minCells && t2.rows[i].cells.length == minCells){			              
		                 t1.rows[i].cells[p].style.backgroundColor = '#F00';
		                 console.log("row/col: "+i+"/"+p+"---stage:" +t1.rows[i].cells[p].innerHTML);	
		            }
		             if(p >= minCells && t1.rows[i].cells.length == minCells && t2.rows[i].cells.length > minCells){			              
		                 t2.rows[i].cells[p].style.backgroundColor = '#F00';
		                 console.log("row/col: "+i+"/"+p+"---prod:" + t2.rows[i].cells[p].innerHTML);	
		            }
				}							            
	        }	
	  		         
    	}	
	  	if (i >= minRows && sRowCount == minRows && pRowCount > minRows ) {
	  		 t2.rows[i].style.backgroundColor = '#F00';		
	  		 console.log( i+"prod/"+maxRows);   			        
	  	}	
	  	if (i >= minRows && sRowCount > minRows && pRowCount == minRows ) {
	  		 t1.rows[i].style.backgroundColor = '#F00';		   	
	  		 console.log( i+"stage/"+maxRows);		        
	  	}		   
    }
}
