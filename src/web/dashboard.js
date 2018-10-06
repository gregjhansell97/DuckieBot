//Key Listener

var wbutton = document.getElementById('w');
var abutton = document.getElementById('a');
var sbutton = document.getElementById('s');
var dbutton = document.getElementById('d');

window.addEventListener('keydown', function (e) {
 	var key = e.keyCode ? e.keyCode : e.which;
	//W key
	if (key == 87) {
		wbutton.style.backgroundColor = 'blue';
	} 
   //A key: rotate wheel -45 degrees
   if (key == 65) {
   	abutton.style.backgroundColor = 'blue';
   }
   //S key
   if (key == 83) {
   	sbutton.style.backgroundColor = 'blue';
   }
   //D key: rotate wheel 45 degrees
   if (key == 68) {
   	dbutton.style.backgroundColor = 'blue';
   }
})
window.addEventListener('keyup', function (e) {
 	var key = e.keyCode ? e.keyCode : e.which;
	//W key
	if (key == 87) {
		wbutton.style.backgroundColor = 'purple';
	} 
   //A key: rotate wheel -45 degrees
   if (key == 65) {
   	abutton.style.backgroundColor = 'purple';
   }
   //S key
   if (key == 83) {
   	sbutton.style.backgroundColor = 'purple';
   }
   //D key: rotate wheel 45 degrees
   if (key == 68) {
   	dbutton.style.backgroundColor = 'purple';
   }           
})