let myImage = document.querySelector('img');

myImage.onclick = function() {
    let mySrc = myImage.getAttribute('src');
    if(mySrc === 'images/bonobono.png') {
      myImage.setAttribute ('src','images/bonoicon.png');
    } else {
      myImage.setAttribute ('src','images/bonobono.png');
    }
}
