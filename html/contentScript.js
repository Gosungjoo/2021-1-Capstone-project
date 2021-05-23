let timelinedata;
let commentsdata;
var index;
$(function() {
  var url = document.location.href;
  //alert(url);
  var iframe = $("<iframe>", {
    "id": "frame",
    "src": url,
    "width": "100%",
    "height": "500px"
  });
  var body = $(document.getElementById("secondary")).prepend(iframe);
  body.find("#frame").contents()
  .find("body").html(a);


  
  $(iframe).on('load',function() {
    

    
        const idocument = $('#frame').get(0).contentDocument;



        removeFrame("masthead-container",idocument)
        removeFrame("player",idocument)
        removeFrame("panels",idocument);
        removeFrame("chat-template",idocument);
        removeFrame("playlist",idocument);
        removeFrame("info",idocument);
        removeFrame("meta",idocument);
        removeFrame("related",idocument);
        

        

      
      


  } );

  function removeFrame(name, idocument){
    let timerId = setTimeout(function tick() {
      try{
        const player  = idocument.getElementById(name);
        player.remove();
        clearTimeout(timerId);
      }
      catch(error){
      }
      timerId = setTimeout(tick, 100); // (*)
    }, 500);

  }


});
function getComments(){
  //image객체가 생성되어 속성들을 추가할수 있음
     // image.src = chrome.extension.getURL(images/button(letf).png);
      //alert(document.getElementsByClassName("ytp-time-current").value);
      var link = document.location.href;
      
      
      $.ajax({
          url: 'http://127.0.0.1:8000/sd/daet',
          method: 'POST',
          async : true,
          data : JSON.stringify({ "comments" : link.substr(8,),}),
          dataType :'json',
  
          error: function (request) {
            
            alert("연결에 오류가 있습니다.");
        },
        success: function (res) {
          alert(res.data);
          commentsdata = res.data;
          index = 0;
          load_comments(10);

          if(typeof(serverdata) == 'string'){
              if(serverdata == 'kids'){
                  alert("유아 영상은 댓글이 제한되어 있습니다.");
              }
              if(serverdata == 'no commenet'){
                  alert("해당 영상은 댓글이 제한되어 있습니다.");
              }if(serverdata == 'not enough'){
                  alert("해당 영상은 댓글이 부족합니다.");
              }if(serverdata == 'no timeline'){
                  alert("해당 영상은 타임라인을 언급한 댓글이 존재하지 않습니다.");
              }
              
  
          }
          else{
  
  
          }
          
          //let timerId = setInterval(() => compare(), 200);
  
          
        }
      });
      
  }
  

function access(){
//image객체가 생성되어 속성들을 추가할수 있음
   // image.src = chrome.extension.getURL(images/button(letf).png);
    //alert(document.getElementsByClassName("ytp-time-current").value);
    var link = document.location.href;
    
    
    $.ajax({
        url: 'http://127.0.0.1:8000/tl/comment',
        method: 'POST',
        async : true,
        data : JSON.stringify({ "comments" : link.substr(8,),}),
        dataType :'json',

        error: function (request) {
          
         // alert("연결에 오류가 있습니다.");
      },
      success: function (res) {
        alert(res.one);
        serverdata = res.one;
        if(typeof(serverdata) == 'string'){
            if(serverdata == 'kids'){
                alert("유아 영상은 댓글이 제한되어 있습니다.");
            }
            if(serverdata == 'no comment'){
                alert("해당 영상은 댓글이 제한되어 있습니다.");
            }if(serverdata == 'not enough'){
                alert("해당 영상은 댓글이 부족합니다.");
            }if(serverdata == 'no timeline'){
                alert("해당 영상은 타임라인을 언급한 댓글이 존재하지 않습니다.");
            }
        }
        else{


        }
        let timerId = setInterval(() => compare(), 200);

        
      }
    });
    
}





function compare(){
    var items = document.getElementsByClassName("ytp-time-current");
    var time = items.item(0).innerHTML;
    var k = serverdata.length;
    for(var i = 0 ; i < k; i++ ){
        var ser = serverdata[i]
        if(ser[4] == items.item(0).innerHTML){
            line_distibute(ser);
            break;
        }
   
    }
}



function line_distibute(data){
  //String[]  = data.split(",");
      setTimeCell(data[0],data[1],data[2],data[3],data[4]);
  
  }

//<iframe width="560" height="315" src="http://www.youtube.com/embed/jNAK7QL5JjI"  frameborder="0">이 브라우저는 iframe을 지원하지 않습니다</iframe></p>
function timeCell(){
    var zCell = '<div id = "timeLine" style ="position:absolute; left:50pt ;top:150;background-color: rgba(200, 200, 200, 0.4);"> <div id = "timeLineheader" style =" width:150pt;height=50pt; " >   <div id = "timeimage" style="  float: left; width:50pt;height=50pt;"> img </div><div id = rightwindows> <div id = "timename"> name </div>  <div id = "timecomments"> comments </div><div id = "timeLike"> Like </div> </div> </div></div>'
    $(document.getElementById("columns")).append(zCell);
}

function commentCell(){
  var zCell = '<div id = "commentsScroll" , style="width:100%; height:200px;margin-top:20px;backgroud-color:gray;opacity:0.95;overflow:auto;"><div id = "warp" ><table id="tg"><thead><tr><td class="tg-baqh">   </td><td class="tg-baqh">   </td></tr></thead></table></div></div>';
  $(document.getElementsByClassName("style-scope ytd-watch-flexy")[11]).append(zCell);
}


function setTimeCell(imgUrl,name,comment,like,time){
    document.getElementById("timeimage").innerHTML = "<a  target = blank><img src=" +imgUrl+ " width='50' height='50' bother-radius:'50%'>";
    document.getElementById("timename").innerHTML = "<a  target = blank> &nbsp&nbsp&nbsp<b>      " +name+ "</b> ";
    document.getElementById("timecomments").innerHTML = "<a  target = blank> &nbsp&nbsp&nbsp<b>" +comment+ "</b> ";
    document.getElementById("timeLike").innerHTML = "<a  target = blank> &nbsp&nbsp&nbsp<b> like is = " +like+ "</b> ";

}


function clearCell(){
    document.getElementById("timeimage").innerHTML = "";
    document.getElementById("timename").innerHTML = "";
    document.getElementById("timecomments").innerHTML = "";
    document.getElementById("timeLike").innerHTML = "";
 
}




function line_distibute_com(data){
  //String[]  = data.split(",");
      addRow(data[2],data[0],data[1],data[5],data[3],data[4],data[6]);
  
  }

document.addEventListener('DOMContentLoaded', function() {

  var link = document.getElementById('commentsScroll');
  alert("sibal");
 link.addEventListener("scroll", function(){
   var scroll_top = $(this).scrollTop(); //스크롤바의 상단위치
   var scroll_H = $(this).height(); //스크롤바를 갖는 div의 높이
   var contentH = $(document.getElementById('tg')).height(); //문서 전체 내용을 갖는 div의 높이
     $(".top").text(scroll_top);
      $(".H").text(scroll_H);
      $(".CH").text(contentH);
   if(scroll_top + scroll_H +1 >= contentH) { // 스크롤바가 아래 쪽에 위치할 때
       if(scribeindex != '-1'){
         load_comments(10);
       }
       
   }
});
});

function load_comments(c){

  for(var i = 0 ; i < c ; i++ ){
  if(commentsdata.length == index){
    index = -1;
    alert("no more exist data!");
  }
  else{
  line_distibute_com(commentsdata[index]);
  index++;
}

}
}




function addRow(LinkSource,imgUrl,name,upload,comment,like,replie) {
  // table element 찾기
  const Link = LinkSource;
  const table = document.getElementById('tg');
  
  // 새 행(Row) 추가 (테이블 중간에)
  const newRow1 = table.insertRow(-1);
  
  // 새 행(Row)에 Cell 추가
  const newCell1 = newRow1.insertCell(0); // img
  const newCell2 = newRow1.insertCell(1); // name
  const newCell3 = newRow1.insertCell(2); // date
  const tempCell0 = newRow1.insertCell(3);

  const newRow2 = table.insertRow(-1);
  const newCell4 = newRow2.insertCell(0); // comment
  const newCell5 = newRow2.insertCell(1);
  const newCell6 = newRow2.insertCell(2); // replie
 
  //const newRow3 = table.insertRow(-1); // like 
  
  // Cell에 텍스트 추가
  newCell4.innerHTML = "<a href=" +Link+  "target = blank><img src=" +imgUrl+ " width='50'; height='50' >";
  newCell2.innerHTML = "<a href=" +Link +  "target = blank> &nbsp&nbsp&nbsp<b>" +name+ "</b></a>" + "&nbsp&nbsp&nbsp"+ upload;
 // newCell3.innerHTML = ;
  newCell5.innerHTML = comment;
  newCell6.innerHTML = like;
  document.querySelector('img').style.mborderRadius="50%";
  
  //newCell6.innerHTML = "replie";
  
  //newCell3.innerHTML = rank;
}

var bar = '<input type="range" value="0" min="0" max="100"></input>';


$(document.getElementsByClassName("ytp-left-controls")).append(bar);

timeCell();
commentCell();
access();
getComments();
clearCell();
//LoadCommentCell();
$(document.getElementById("timeLine")).draggable();
$(document.getElementById("commentsScroll")).draggable();

$('timeLine').resizable({
  //함께 커질영역 
  alsoResize:'timeLineheader',
  //커질때 애니메이션 발생 
  animate :  true,
  animateDuration: 300,
  animateEasing:"swing",
  //비율유지
  aspectRatio: true,
  //마우스 hover 아닐때 핸들러 숨기기
  autoHide: true,
  //minHeight, maxHeight, minWidth, maxWidth 최소,최대 크기지정 
});



//$(document.getElementsById("content-text"));



