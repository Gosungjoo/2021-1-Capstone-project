let serverdata;

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
        

        
       /* for(var i = 0; i < commentframe.length-1; i++ ){
          commentframe[i].remove();
          if (commentframe[commentframe.length].getAttribute('id')=="comments"){
            clearTimeout(timerId);
          }
        }*/
      
      


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
      setCell(data[0],data[1],data[2],data[3],data[4]);
  
  }

//<iframe width="560" height="315" src="http://www.youtube.com/embed/jNAK7QL5JjI"  frameborder="0">이 브라우저는 iframe을 지원하지 않습니다</iframe></p>
function iniCell(){
    var zCell = '<div id = timeLine> <div id = "timeLineheader" style =" width:150pt;height=50pt; " >   <div id = "timeimage" style="  float: left; width:50pt;height=50pt;"> img </div><div id = rightwindows> <div id = "timename"> name </div>  <div id = "timecomments"> comments </div><div id = "timeLike"> Like </div> </div> </div></div>'
    $(document.getElementsByClassName("style-scope ytd-watch-flexy")[10]).append(zCell);
    
}


function setCell(imgUrl,name,comment,like,time){
    document.getElementById("timeimage").innerHTML = "<a  target = blank><img src=" +imgUrl+ " width='50' height='50'>";
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

// 드래그 가능한 요소 생성

access();
iniCell();
$(document.getElementById("timeLine")).draggable();
$(document.getElementById("frame")).draggable();





