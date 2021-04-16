let myImage = document.querySelector('img');

myImage.onclick = function() {
    let mySrc = myImage.getAttribute('src');
    if(mySrc === 'images/bonobono.png') {
      myImage.setAttribute ('src','images/bonoicon.png');

      $.ajax({
        url: `http://127.0.0.1:8000/ch/comment`,
        method: 'POST',
        async : true,
        data : JSON.stringify({ "comments" : "www.youtube.com/watch?v=Cba_0j-v-CQ",}),
        dataType :'json',
        
        error: function (request) {
          alert(JSON.parse(request));
      },
      success: function (res) {
          alert(" Done !"+ JSON.parse(res));
      }
    });
        

    } else {
      myImage.setAttribute ('src','images/bonobono.png');

    }
}


router.get('/test', function(req, res, next){

  console.log('test');

  res.send('hello world');

})

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
  