
let a="";

let clrbtn = document.querySelector('#clr');
let savebtn = document.querySelector('#save');
let playbtn = document.querySelector('#play');

let audio2 = [];
function playtext(song){
  a=song;
  console.log(a);
  console.log("Playtext Button Pressed");
  for (var i=0; i<a.length; i++){
    audio2[i] = document.createElement("AUDIO");
    audio2[i].src = "http://widit.knu.ac.kr/~adit/proj/player/Tune/" + a[i] + ".mp3";
  }
  playkey2(0,a.length);

}

function playKey(k){
        let audio = document.createElement("AUDIO");
        audio.src = "http://widit.knu.ac.kr/~adit/proj/player/Tune/" + k + ".mp3";
        audio.play();
        console.log("Function playKey(", k, ") is called");
}

function playkey2(k,maxk) {
  audio2[k].play();
  console.log("Audio ", k , "played");
  audio2[k].addEventListener('ended', function(e){
    var j=k+1;
    if (j<maxk) {
      playkey2(j,maxk);
    }
  });
}

// Event Listner for the Play Button
document.getElementById('play').addEventListener('click', ()=>{
  console.log("Play Button Pressed");
  for (var i=0; i<a.length; i++){
    audio2[i] = document.createElement("AUDIO");
    audio2[i].src = "http://widit.knu.ac.kr/~adit/proj/player/Tune/" + a[i] + ".mp3";
  }
  playkey2(0,a.length);
});



// Event Listner for the Clear Button
clrbtn.addEventListener('click', ()=>{
    a="";
    document.getElementById('output').value=a;
    console.log("Clear Pressed");
});
