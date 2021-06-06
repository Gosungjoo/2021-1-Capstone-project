let timeline_data;
let comments_data;
let comments_start;
let comments_end;
let comments_length;


var ontimeline = 1;
var oncomment = 1;
var korean = 0;
var spam = 0;
var ordertype = "time"; //  time




chrome.runtime.onMessage.addListener(function (response, sendResponse) {
  if(response.spam == 1){
    spam = 1;
    //alert("스팸1");
    updateSetting();
  }
  else if(response.spam == 0){
    spam = 0;
    
    updateSetting();
    //alert("스팸0");
  }
  else if(response.korean == 1){
    korean = 1;
    
    updateSetting();
    //alert("1");
  }
  else if(response.korean == 0){
    korean = 0;
    
    updateSetting();
    //alert("0");
  }
  else if(response.time == 0){
    if(ontimeline == 0){
      ontimeline =1 ;
    }
    else{
      ontimeline =0;
    }
    updateSetting();

  }
  
  else if(response.comment == 0){
    if( oncomment== 0){
      oncomment =1 ;
    }
    else{
      oncomment =0;
    }
    updateSetting();
  }


});

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
          data : JSON.stringify({ "comments" : link.substr(8,),"korean" : korean, "spam" : spam , "type" : ordertype}, ),
          dataType :'json',
  
          error: function (request) {
            
            alert("연결에 오류가 있습니다.");
        },
        success: function (res) {
          //alert(res.data);
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
        //alert(res.one);
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
            }, 10000);
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
    var zCell = '<div id = "timeLine" style ="position:absolute; left:50pt ;top:150;background-color: rgba(255, 255, 255, 1.0);opacity:1.0"> <div id = "timeLineheader" style =" width:150pt;height=50pt; " >   <div id = "timeimage" style="  float: left; width:50pt;height=50pt;"> img </div><div id = rightwindows> <div id = "timename"> name </div>  <div id = "timecomments"> comments </div><div id = "timeLike"> Like </div> </div> </div></div>'
    $(document.getElementById("columns")).append(zCell);
}



function clearCell(){
    document.getElementById("timeimage").innerHTML = "";
    document.getElementById("timename").innerHTML = "";
    document.getElementById("timecomments").innerHTML = "";
    document.getElementById("timeLike").innerHTML = "";
 
}



function commentCell(){

  var zCell = '<div id = "commentsScroll" , style="position:absolute; left:50pt ;top:150; width:30%; height:200px;background-color: rgba(255, 255, 255, 1.0);opacity:1.0;"><div id = "warp" style ="width:100%; height:80%; overflow:auto; overflow-x:hidden;" >  <table id="tg"><thead><tr><td class="tg-baqh">   </td><td class="tg-baqh">   </td></tr></thead></table></div></div>';
  $(document.getElementById("columns")).append(zCell);
  //$(document.getElementsByClassName("style-scope ytd-watch-flexy")[11]).append(zCell);
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
    
  var thumb = chrome.runtime.getURL('images/thumb.png');

    // table element 찾기
    const Link = LinkSource;
    const table = document.getElementById('tg');
    
    // 새 행(Row) 추가 (테이블 중간에)
    const newRow1 = table.insertRow(-1);
    
    // 새 행(Row)에 Cell 추가
    const newCell1 = newRow1.insertCell(0); // img
    const newCell2 = newRow1.insertCell(1); // name
    const newCell3 = newRow1.insertCell(2); // date
    const newCell4 = newRow1.insertCell(3);
  
    const newRow2 = table.insertRow(-1);
    const newCell5 = newRow2.insertCell(0); // comment
    const newCell6 = newRow2.insertCell(1);
    const newCell7 = newRow2.insertCell(2); //
    const newCell8 = newRow2.insertCell(3);
   
    //const newRow3 = table.insertRow(-1); // like 
    
    let cssValue = 'font size="2em" ;color = "gray"';
    // Cell에 텍스트 추가
    newCell1.innerHTML = "<a href=" +Link+  "target = blank><img src=" +imgUrl+ " width='25'; height='25' top = '25' id = 'gd'>";
    newCell2.innerHTML = "  <b sytle  = " + cssValue+"> &nbsp&nbsp&nbsp" +name+ "</b>" + "&nbsp&nbsp&nbsp"+ upload +"&nbsp&nbsp&nbsp like &nbsp"+like;
    //newCell3.innerHTML = "<span>&nbsp &nbsp </span>";
    //newCell4.innerHTML = "<span>"+like+"</span>";
    newCell6.innerHTML = comment;
    //newCell6.innerHTML = like;
    //$('#gd').style.mborderRadius="50%";
    //document.getElementById("someImage").src = thumb;

    //newCell6.innerHTML = "replie";
    
    //newCell3.innerHTML = rank;
  }
  
 
function updateSetting(){

  if(ontimeline == 1){
    $('#iconT').css('color','white');
  }
  else{
    $('#iconT').css('color','gray');
  }
  if(oncomment == 1){
    $('#iconC').css('color','white');
  }
  else{
    $('#iconC').css('color','gray');
  }
  if(korean == 1){
    $('#iconK').css('color','white');
  }
  else{
    $('#iconK').css('color','gray');
  }
  if(spam == 1){
    $('#iconS').css('color','white');
  }
  else{
    $('#iconS').css('color','gray');
  }
  if(ontimeline == 0){
    hideTimeline();
    $('#iconT').css('color','gray');
  }

  if(oncomment == 0){
    hideComments();
    $('#iconC').css('color','gray');
  }
  if(ontimeline == 1){
    showTimeline();
    $('#iconT').css('color','white');
  }

  if(oncomment == 1){
    showComments();
    $('#iconC').css('color','white');
  }




}






var bar = '<input type="range" value="0" min="0" max="100" id = "range"></input>';
var bar2 = '<span id="value"></span>';
var bar3 = '<span id="outputVar"> &nbsp;</span>';
var barTime = '<span id="iconT"> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;Time &nbsp;</span>';
var barComment = '<span id="iconC">Commnet &nbsp;</span>';
var barFkorean = '<span id="iconK">Korean &nbsp;</span>';
var barFspan = '<span id="iconS">Spam &nbsp;</span>';


$(document.getElementsByClassName("ytp-left-controls")).append(bar);
$(document.getElementsByClassName("ytp-left-controls")).append(bar2);
$(document.getElementsByClassName("ytp-left-controls")).append(barTime);
$(document.getElementsByClassName("ytp-left-controls")).append(barComment);

$(document.getElementsByClassName("ytp-left-controls")).append(barFkorean);
$(document.getElementsByClassName("ytp-left-controls")).append(barFspan);



updateSetting()
var slider = document.getElementById("range");
var output = document.getElementById("value");
var outputVarNo = document.getElementById("outputVar");
function update(){
   output.innerHTML = slider.value/100;
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
  if(comments_end != comments_length-1){

  if(comments_end + 10 <comments_length){
    comments_end += 10;
  }
  else{
    comments_end = comments_length-1;
  }
}
else{
  alert("end!");}

}




function drag_resize(){
  $("#warp").mCustomScrollbar({
    theme:"dark",
    mouseWheel:{ scrollAmount: 500 },
    callbacks:{
      onTotalScroll:function(){
        alert("loading");
        // alert("Scrolled to end of content."); // 여기에 추가하자공
        comments_setting();
        load_comments();
        

      },
      whileScrolling:function(){
        $("#warp").css("height","80%");
        $('#warp').mCustomScrollbar("scrollTo","bottom",{
          scrollInertia:1000
      });    
    
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
  $('#timeLine').hide();
}

function hideComments(){
  $('#commentsScroll').hide();
}


function showTimeline(){
  $('#timeLine').show();
}

function showComments(){
  $('#commentsScroll').show();
}


//$(document.getElementsById("content-text"));


