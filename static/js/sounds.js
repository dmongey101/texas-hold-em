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

$(document).on('click','#chips',function() {
    chips.play();
}); 

$(document).on('click','#deal',function() {
    deal.play();
}); 

$(document).on('click','#check',function() {
    check.play();
}); 

