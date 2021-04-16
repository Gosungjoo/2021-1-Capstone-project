$(document).ready(function(){


  $('#getUrl').click(function(){

      getCurrentTabUrl(function(url) {

           renderURL(url);

       });
       sendURL(url);

  })

});



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


function renderURL(statusText,) {

document.getElementById('urls').textContent = statusText;

}


function sendURL(youtubeURL){
  $.ajax({
      url : '127.0.0.1:8000/ch/list',
      method : 'POST',
      data:JSON.stringify({
          url : URLs
    })
  });
  alert("전송");
  getData(sendUser);
  alert("수신");
  
}



function getData(){
$.ajax({

  url : 'https://127.0.0.1:8000/',

  success:function(data){

    alert(data);
    sendUser(data);
  }
  
})
}

function sendUser(user){
  $.ajax({
      url : '127.0.0.1:8000/ch/list',
      method : 'POST',
      data:JSON.stringify({
          url : URLs
    })
  });
}


chrome.alert("전송");

