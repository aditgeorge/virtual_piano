document.addEventListener("keydown", 
    function (event){
    if( event.target.id == "songnamein") return;

    let kcode= String.fromCharCode(event.which);
    if (kcode == "A" || kcode == "S" ||kcode == "D" ||kcode == "F" ||kcode == "G" ||kcode == "H" ||kcode == "J" ||kcode == "W" ||kcode == "E" ||kcode == "T" ||kcode == "Y" ||kcode == "U" || kcode == "Z" || kcode == "X" ||kcode == "C" ||kcode == "V" ||kcode == "B" ||kcode == "N" ||kcode == "M")
    {
      a=a+kcode;
      document.getElementById('output').value=a;
      console.log("The '", kcode, "' key is pressed.");
      playKey(kcode);
    }
    });