var expected_styleYear = "2016";
var expected_styleSeason = "Autumn";
var timeRange = "Shop";
var startDate = new Date();
var endDate = new Date();
startDate.setFullYear(2016,05,19);
endDate.setFullYear(2016,06,10);
var timeRangeCol=$(".zstopblock").children("div:eq(0)").children("div:contains("+timeRange+")").index();
var styleYearCol=$(".zstopblock").children("div:eq(1)").children("div:contains('Style Year')").index();
var styleSeasonCol=$(".zstopblock").children("div:eq(1)").children("div:contains('Style Season')").index();
var styleSeasonCol=$(".zstopblock").children("div:eq(1)").children("div:contains('Style Season')").index();
var jobTicketCol=$(".zstopblock").children("div:eq(1)").children("div:contains('Job Ticket #')").index();
var statusCol=$(".zstopblock").children("div:eq(1)").children("div:contains('Status')").index();
var poPrepackCol,poQtyOrderedCol,poOpenStockCol,receiverPrepackCol,receiverQtyCol,receiverOpenStockCol,receiverBalanceCol;
var allocatedPrepackCol,allocatedQtyCol,allocatedOpenStockCol,reservedOpenStockCol,reservedQtyCol,reservedPrepackCol;
$(".zstopblock").children("div:eq(1)").children("div:contains('Prepack')").each(function(){
    if(($(".zstopblock").children("div:eq(0)").children("div:eq("+$(this).index()+")").text())== 'PO'){
        poPrepackCol=$(this).index();        
    } 
    if(($(".zstopblock").children("div:eq(0)").children("div:eq("+$(this).index()+")").text())== 'Receiver'){
        receiverPrepackCol=$(this).index();       
    } 
    if(($(".zstopblock").children("div:eq(0)").children("div:eq("+$(this).index()+")").text())== 'Qty Allocated'){
        allocatedPrepackCol=$(this).index();        
    }
    if(($(".zstopblock").children("div:eq(0)").children("div:eq("+$(this).index()+")").text())== 'Qty Reserved'){
        reservedPrepackCol=$(this).index();       
    }  
});
$(".zstopblock").children("div:eq(1)").children("div:contains('Stock')").each(function(){
    if(($(".zstopblock").children("div:eq(0)").children("div:eq("+$(this).index()+")").text())== 'PO Open'){
        poOpenStockCol=$(this).index();        
    } 
    if(($(".zstopblock").children("div:eq(0)").children("div:eq("+$(this).index()+")").text())== 'Receiver'){
        receiverOpenStockCol=$(this).index();       
    } 
    if(($(".zstopblock").children("div:eq(0)").children("div:eq("+$(this).index()+")").text())== 'Qty Allocated'){
        allocatedOpenStockCol=$(this).index();        
    }
    if(($(".zstopblock").children("div:eq(0)").children("div:eq("+$(this).index()+")").text())== 'Qty Reserved'){
        reservedOpenStockCol=$(this).index();       
    }  
});
$(".zstopblock").children("div:eq(0)").children("div:contains('Qty')").each(function(){
    if(($(".zstopblock").children("div:eq(1)").children("div:eq("+$(this).index()+")").text())== 'Ordered'){
        poQtyOrderedCol=$(this).index();        
    } 
    if(($(".zstopblock").children("div:eq(1)").children("div:eq("+$(this).index()+")").text())== 'Allocated'){
        allocatedQtyCol=$(this).index();        
    }
    if(($(".zstopblock").children("div:eq(1)").children("div:eq("+$(this).index()+")").text())== 'Reserved'){
        reservedQtyCol=$(this).index();       
    }  
});
$(".zstopblock").children("div:eq(0)").children("div:contains('Receiver')").each(function(){
    if(($(".zstopblock").children("div:eq(1)").children("div:eq("+$(this).index()+")").text())== 'Qty'){
        receiverQtyCol=$(this).index();        
    } 
    if(($(".zstopblock").children("div:eq(1)").children("div:eq("+$(this).index()+")").text())== 'Balance'){
        receiverBalanceCol=$(this).index();        
    }
});
var errorInfo = new Array();
var n=0;
$(".zsblock").children("div").each(function(){
  var row = $(".zslefthead .zsleftcell:eq("+$(this).index()+")").text();
  var error = "Row-"+row+" wrong: ";
  var current_timeRange = $(this).children("div:eq("+timeRangeCol+")").text().split("/");   
  var currentDate= new Date();
  currentDate.setFullYear(current_timeRange[2],current_timeRange[0],current_timeRange[1]);
  var current_jobTicket = $(this).children("div:eq("+jobTicketCol+")").text();  
  var current_status = $(this).children("div:eq("+status+")").text();  
  var current_receiverQty=$(this).children("div:eq("+receiverQtyCol+")").text();
  var current_allocatedQty=$(this).children("div:eq("+allocatedQtyCol+")").text();
  var current_poQty=$(this).children("div:eq("+poQtyOrderedCol+")").text();
  var current_reservedQty=$(this).children("div:eq("+reservedQtyCol+")").text();  
  var current_poPrepack= $(this).children("div:eq("+poPrepackCol+")").text();  
  var current_receiverPrepack=$(this).children("div:eq("+receiverPrepackCol+")").text();  
  var current_allocatedPrepack=$(this).children("div:eq("+allocatedPrepackCol+")").text();  
  var current_reservedPrepack=$(this).children("div:eq("+reservedPrepackCol+")").text(); 
  if (parseInt(row)>2 ){
    if($(this).children("div:eq("+styleYearCol+")").text() != expected_styleYear){
      error +="StyleYear,"
    }
    if($(this).children("div:eq("+styleSeasonCol+")").text() != expected_styleSeason){
      error +="StyleSeason,"
    }  
    if(currentDate < startDate || currentDate > endDate ){
         error +=timeRange+" Date,"
    }
    if((!current_jobTicket && current_status) ||(current_jobTicket && current_status != 'R') ){
         error +="Status,"
    }
    if(!current_poPrepack){
      if(current_poQty != $(this).children("div:eq("+poOpenStockCol+")").text()){
          error +="PO Open Stock,"
      }
    }
    if(!current_receiverPrepack){
      if( current_receiverQty != $(this).children("div:eq("+receiverOpenStockCol+")").text()){
          error +="Receiver Open Stock,"
      }
      if( !current_poPrepack && (parseInt(current_poQty)-parseInt(current_receiverQty)) != parseInt($(this).children("div:eq("+receiverBalanceCol+")").text())){
          error +="Receiver Balance,"
      }

    }
    if(!current_allocatedPrepack){
      if(current_allocatedQty != $(this).children("div:eq("+allocatedOpenStockCol+")").text()){
          error +="Qty Allocated Open Stock,"
      }
    }
    if(!current_reservedPrepack){
      if(current_reservedQty != $(this).children("div:eq("+reservedOpenStockCol+")").text()){
          error +="Qty Reserved Open Stock,"
      }
      if(!current_receiverPrepack && !current_allocatedPrepack && parseInt(current_reservedQty) != (parseInt(current_receiverQty) - parseInt(current_allocatedQty))){
          error +="Qty Reserved,"
      }
    }
    if (error != "Row-"+row+" wrong: "){  
      errorInfo[n] = error.substring(0, error.length-1);    
      n++;
    }
  } 
});
return errorInfo;
