let timeline_data;
let comments_data;
let comments_start;
let comments_end;
let comments_length;


var ontimeline = 1;
var oncomment = 1;
var ordertype = "relevance"; //  time


// resizable용 css파일
$('head').append('<link rel="stylesheet" href="https://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">');

// request 부분
function requestComments(){
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
          comments_data = res.data;
          index = 0;
          

          if(typeof(comments_data) == 'string'){
              if(comments_data == 'kids'){
                  alert("유아 영상은 댓글이 제한되어 있습니다.");
              }
              if(comments_data == 'no commenet'){
                  alert("해당 영상은 댓글이 제한되어 있습니다.");
              }if(comments_data == 'not enough'){
                  alert("해당 영상은 댓글이 부족합니다.");
              }if(comments_data == 'no timeline'){
                  alert("해당 영상은 타임라인을 언급한 댓글이 존재하지 않습니다.");
              }
              
  
          }
          else{
            comments_length = comments_data.length;
            comments_start = 0;
            comments_end = 0;
            if(comments_length > 11){
            comments_end = 10;
            load_comments();
              

            }
            else{
              comments_end = comments_length-1;
              load_comments();


            }

          }
          
          //let timerId = setInterval(() => compare(), 200);
  
          
        }
      });
      
}
  

function requestTimelines(){
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
        timeline_data = res.one;
        if(typeof(timeline_data) == 'string'){
            if(timeline_data == 'kids'){
                alert("유아 영상은 댓글이 제한되어 있습니다.");
            }
            if(timeline_data == 'no comment'){
                alert("해당 영상은 댓글이 제한되어 있습니다.");
            }if(timeline_data == 'not enough'){
                alert("해당 영상은 댓글이 부족합니다.");
            }if(timeline_data == 'no timeline'){
                alert("해당 영상은 타임라인을 언급한 댓글이 존재하지 않습니다.");
            }
        }
        else{


        }
        let timerId = setInterval(() => time_compare(), 200);

        
      }
    });
    
}



function CurrentTime(){  // 현재 동영상의 재생시간

  var htmlVideoPlayer= document.getElementsByTagName('video')[0];
  return htmlVideoPlayer.currentTime;

}




function time_compare(){ // 해당시간에 존재하는 타임라인 찾아서 5초 띄우고 제거

  if(ontimeline == 1){
  var nowtime = CurrentTime()
  var k = timeline_data.length;
    for(var i = 0 ; i < k; i++ ){
        var timeSum = 0;
        var ser = timeline_data[i]
        var timeArray = ser[4].split(':');  // 00:00:00 or 00:00 or 0:00;
        if(timeArray.length == 3 ){
          timeSum += parseInt(timeArray[0])*3600;
          timeSum += parseInt(timeArray[1])*60;
          timeSum += parseInt(timeArray[2]);




        }
        else if(timeArray.length == 2){

          timeSum += parseInt(timeArray[0])*60;
          timeSum += parseInt(timeArray[1]);



        }
        if(timeSum == nowtime){
          timeLine_distribute(ser);

            ontimeline = false;
            setTimeout(function(){
            clearCell();
            ontimeline = true;
            }, 5000);
            break;
        }
   
    }
  }
}



function timeLine_distribute(data){
  //String[]  = data.split(",");
      setTimeCell(data[0],data[1],data[2],data[3],data[4]);
  
  }


function setTimeCell(imgUrl,name,comment,like,time){
    document.getElementById("timeimage").innerHTML = "<a  target = blank><img src=" +imgUrl+ " width='50' height='50' bother-radius:'50%'>";
    document.getElementById("timename").innerHTML = "<a  target = blank> &nbsp&nbsp&nbsp<b>      " +name+ "</b> ";
    document.getElementById("timecomments").innerHTML = "<a  target = blank> &nbsp&nbsp&nbsp<b>" +comment+ "</b> ";
    document.getElementById("timeLike").innerHTML = "<a  target = blank> &nbsp&nbsp&nbsp<b> like is = " +like+ "</b> ";

}




function timeCell(){
    var zCell = '<div id = "timeLine" style ="position:absolute; left:50pt ;top:150;background-color: rgba(200, 200, 200, 0.4);opacity:1.0"> <div id = "timeLineheader" style =" width:150pt;height=50pt; " >   <div id = "timeimage" style="  float: left; width:50pt;height=50pt;"> img </div><div id = rightwindows> <div id = "timename"> name </div>  <div id = "timecomments"> comments </div><div id = "timeLike"> Like </div> </div> </div></div>'
    $(document.getElementById("columns")).append(zCell);
}



function clearCell(){
    document.getElementById("timeimage").innerHTML = "";
    document.getElementById("timename").innerHTML = "";
    document.getElementById("timecomments").innerHTML = "";
    document.getElementById("timeLike").innerHTML = "";
 
}



function commentCell(){
  var zCell = '<div id = "commentsScroll" , style="width:100%; height:200px;margin-top:20px;background-color: rgba(200, 200, 200, 0.4);opacity:1.0;"><div id = "warp" style ="width:100%; height:100%; overflow:auto; overflow-x:hidden;" > 왜? <table id="tg"><thead><tr><td class="tg-baqh">   </td><td class="tg-baqh">   </td></tr></thead></table></div></div>';
  $(document.getElementsByClassName("style-scope ytd-watch-flexy")[11]).append(zCell);
}






function comment_distribute(data){
  //String[]  = data.split(",");
      addRow(data[2],data[0],data[1],data[5],data[3],data[4],data[6]);
  
  }

  
function load_comments(){
  for(var i = comments_start ; i < comments_end ; i++ ){
    comment_distribute(comments_data[i]);
  }
  return end;
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
  








var bar = '<input type="range" value="0" min="0" max="100" id = "range"></input>';
var bar2 = '<span id="value"></span>';
var bar3 = '<span id="outputVar"></span>';
$(document.getElementsByClassName("ytp-left-controls")).append(bar);
$(document.getElementsByClassName("ytp-left-controls")).append(bar2);
$(document.getElementsByClassName("ytp-left-controls")).append(bar3);

var slider = document.getElementById("range");
var output = document.getElementById("value");
var outputVarNo = document.getElementById("outputVar");
function update(){
   output.innerHTML = slider.value;
   $("#commentsScroll").css('opacity', slider.value/100);
   $("#timeLine").css('opacity', slider.value/100);
  };
slider.addEventListener('input', update);









timeCell();
commentCell();
requestTimelines();
requestComments();
clearCell();
drag_resize();
update();


function comments_setting(){
  if(comments_end != comments_length-1){}

  if(comments_end + 10 <comments_length){
    comments_end += 10;
  }
  else{
    comments_end = comments_length-1;
  }


}




function drag_resize(){
  $("#commentsScroll").mCustomScrollbar({
    mouseWheel:{ scrollAmount: 300 },
    callbacks:{
      onTotalScroll:function(){
        alert("Scrolled to end of content."); // 여기에 추가하자공
        comments_setting();
        load_comments();
      }
  }
  });
  $(document.getElementById("timeLine")).draggable({}
    
  );
  $(document.getElementById("commentsScroll")).draggable();
  $( "#commentsScroll" ).resizable({
    alsoResize:'timeLineheader',
    //커질때 애니메이션 발생 
    animate :  true,
    animateDuration: 100,
    animateEasing:"swing",
    //비율유지
    //마우스 hover 아닐때 핸들러 숨기기
    autoHide: true,
    //minHeight, maxHeight, minWidth, maxWidth 최소,최대 크기지정 
  });
  $('#timeLine').resizable({
    //함께 커질영역 
    alsoResize:'timeLineheader',
  
    animate :  true,
    animateDuration: 100,
    animateEasing:"swing",
    //비율유지
    //마우스 hover 아닐때 핸들러 숨기기
    autoHide: true,
    //minHeight, maxHeight, minWidth, maxWidth 최소,최대 크기지정 
  });
  hideXscroll();
}




function hideXscroll(){
$("#warp").css('overflow-x', "hidden");
}


function hideTimeline(){
  $('#timeline').hide();
}

function hideComments(){
  $('#commentsScroll').hide();
}


function showTimeline(){
  $('#timeline').show();
}

function showComments(){
  $('#commentsScroll').show();
}


//$(document.getElementsById("content-text"));


