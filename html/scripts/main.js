let myImage = document.querySelector('img');

myImage.onclick = function() {
    let mySrc = myImage.getAttribute('src');
    if(mySrc === 'images/bonobono.png') {
      myImage.setAttribute ('src','images/bonoicon.png');

      $.ajax({
        url: `http://127.0.0.1:8000/ch/comment`,
        method: 'GET',
        async : true,
        data : { comments : "yourudsfa.com/",},
        dataType : 'json',
        
        success : function (res) {
          alert("hi");
            // 서번단에서 HTML을 반환해서 기존 페이지를 깜빡임없이 새로 고친다.
            document.querySelector("#appendHtml").innerHTML = res;


        },
        error: function (xhr) {
            alert("fail");
        }
    });
        

    } else {
      myImage.setAttribute ('src','images/bonobono.png');

    }
}
