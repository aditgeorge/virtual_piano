document.addEventListener("keydown", 
    function (event){
    if( event.target.nodeName == "INPUT" || event.target.nodeName == "TEXTAREA" ) return;
    if( event.target.isContentEditable ) return;

    let kcode= String.fromCharCode(event.which);
    if (kcode == "Z" || kcode == "X" ||kcode == "C" ||kcode == "V" ||kcode == "B" ||kcode == "N" ||kcode == "M")
    {
      a=a+kcode;
      document.getElementById('output').value=a;
      console.log("The '", kcode, "' key is pressed.");
      playKey(kcode);
    }
    });

