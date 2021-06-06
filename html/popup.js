let myImage = document.querySelector('img');
let serverdata;
var scribeindex;

let com = $('#com');

com.click(function(){
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id, {comment: "0"}, function(response) {
    });
  });
}
);


let tim = $('#time');


tim.click(function(){
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id, {time: "0"}, function(response) {
    });
  });
}
);




let cup = $('#korea');
let tea = $('#kcolor');

cup.click( function(){
  
  if(tea.text()=="끔"){
  $('#kcolor').text("켬");
  $('#kcolor').css('color',"red");


  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id, {korean: "1"}, function(response) {
    });
  });



  }




  else if(tea.text()=="켬"){
  $('#kcolor').text("끔");
  $('#kcolor').css('color',"gray")

  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id, {korean: "0"}, function(response) {
    });
  });




}
});

let yoong = $('#spam');
let jung = $('#scolor');

yoong.click( function(){
  
  if(jung.text()=="끔"){
  $('#scolor').text("켬");
  $('#scolor').css('color',"red");
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id, {spam: "1"}, function(response) {
    });
  });

  
  }
  
  
  
  else if(jung.text()=="켬"){
  $('#scolor').text("끔");
  $('#scolor').css('color',"gray")
  
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id, {spam: "0"}, function(response) {
    });
  });


}
});

let rcmd = $('#subsc');
let menual = $('#readme');

menual.click( function(){
  window.open("https://github.com/Gosungjoo/2021-1-Capstone-project");
  
});


let sibal =$('#subscribe');
let qudtls = $('#forsubsc');
let goback = $('#among');

sibal.hide();

rcmd.click ( function() {
  
      qudtls.hide();
      sibal.show();
      
      let taburl;
      getCurrentTabUrl(function(youtubeurl,callback) {
        //alert(youtubeurl.substr(8,));    
        renderURL(youtubeurl);
        
        
        
        $.ajax({
          url: 'http://127.0.0.1:8000/ch/comment',
          method: 'POST',
          async : true,
          data : JSON.stringify({ "comments" : youtubeurl.substr(8,),}),
          dataType :'json',
  
          error: function (request) {
            alert("Open The Tab watching Youtube");
        },
        success: function (res) {
          serverdata = res.datas;
          scribeindex = 0;
          load_subscribe(10);
        }
      });
      
      
      });

        

  
    });

goback.click( function(){
  sibal.hide();
  qudtls.show();
  
});






function load_subscribe(c){

    for(var i = 0 ; i < c ; i++ ){
    if(serverdata.length == scribeindex){
      scribeindex = -1;
      //alert("no more exist data!");
    }
    else{
    line_distibute(serverdata[scribeindex]);
    scribeindex++;
  }
 
  }
}




function line_distibute(data){
  //String[]  = data.split(",");
      addRow(data[0],data[1],data[2],data[3]);
  
  }




function getCurrentTabUrl(callback) {

  var queryInfo = {

    active: true,

    currentWindow: true

  };


  chrome.tabs.query(queryInfo, function(tabs) {

    var tab = tabs[0];

    var url = tab.url;

    callback(url);

  });

}


function renderURL(statusText) {

  /*document.getElementById('urls').textContent = statusText;
*/
  //alert(statusText);


}




document.addEventListener('DOMContentLoaded', function() {

  var link = document.getElementById('subscribe');
 
 link.addEventListener("scroll", function(){
   var scroll_top = $(this).scrollTop(); //스크롤바의 상단위치
   var scroll_H = $(this).height(); //스크롤바를 갖는 div의 높이
   var contentH = $(document.getElementById('tg')).height(); //문서 전체 내용을 갖는 div의 높이
     $(".top").text(scroll_top);
      $(".H").text(scroll_H);
      $(".CH").text(contentH);
   if(scroll_top + scroll_H +1 >= contentH) { // 스크롤바가 아래 쪽에 위치할 때
       if(scribeindex != '-1'){
         load_subscribe(10)
       }
       
   }
});
});


// subscribe table insert

function addRow(LinkSource,name,imgUrl,rank) {
  // table element 찾기
  const Link = "https://youtube.com/channel/" + LinkSource;
  const table = document.getElementById('tg');
  
  // 새 행(Row) 추가 (테이블 중간에)
  const newRow = table.insertRow(-1);
  
  // 새 행(Row)에 Cell 추가
  const newCell1 = newRow.insertCell(0);
  const newCell2 = newRow.insertCell(1);
  //const newCell3 = newRow.insertCell(2);
  
  // Cell에 텍스트 추가
  newCell1.innerHTML = "<a href=" +Link+ " target = blank><img src=" +imgUrl+ " width='50' height='50'>";
  newCell2.innerHTML = "<a href=" +Link+ " target = blank> &nbsp&nbsp&nbsp<b>" +name+ "</b> ";
  //newCell3.innerHTML = rank;
}


