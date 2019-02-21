var chips
var deal
var check

function playFx() {
    chips = new Audio();
    chips.src = "/media/audio/poker-chips.mp3";
    chips.volume = 0.5;
    deal = new Audio();
    deal.src = "/media/audio/deal-cards.mp3";
    deal.volume = 0.5;
    check = new Audio();
    check.src = "/media/audio/check.mp3";
    check.volume = 0.5;
}

window.addEventListener('load', playFx);

window.onload = function(){
    document.getElementById("chips").onclick = function(){
        chips.play();
    };
    
    document.getElementById("deal").onclick = function(){
        deal.play();
    };
        
    document.getElementById("check").onclick = function(){
        check.play();
    };
};
