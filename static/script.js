var max = 100; //User changable. Changes the max size of attendance
function barWobble(element, height, speed) {
    //If user clicks/adjusts too fast, stop previous animation, and start new one.
    $(element).stop().animate({height: height+"%"}, speed, 'easeOutElastic');
}
function updateAttendance() { //Allows for multiple containers. Make sure input[name] = div.bar[id]
    var level = $("#"+this.name+" .level"),
        value = parseInt(this.value) || 0; //If parseInt returns NaN, use 0
    //Make sure value is within our boundaries (if <0, set to 0, if >max, set to max)
    value = value < 0 ? 0 : value > max ? max : value;
    this.value = value; //If user put an invalid number, push it back into the element
    value /= max / 100; //Normalize the height to percentage (same as value/max * 100)
    if( value !== 100 ) { //Switch between full and not full
        level.toggleClass('low', value < 50); //Toggle class for low.
        level.toggleClass('med', value >= 50); //Toggle class for med.
    } else //Remove all classes
        level.removeClass('low med');
    barWobble( level, value, 700 ); //Do the wobble
}
$(document).ready(function () {
    //Bind change and keyup on the inputs.
    $('input[type="number"]').bind( 'change keyup', updateAttendance ).attr('max',max);
});
