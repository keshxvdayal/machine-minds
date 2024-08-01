var tl = new TimelineLite, 
    chars = new SplitText("#quote", {type:"words,chars"}).chars; 

TweenLite.set("#quote", {perspective:200});

tl.staggerFrom(chars, 0.1, { bottom: 30, opacity:0, scale: 1.5, rotationY: -25,  ease:Power3.easeOut}, 0.03);

document.getElementById("bubble").onclick = function() {
  tl.restart();
}




