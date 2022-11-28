const lts = {
timer : null,
setTimer : 10,
setCaut : 5,
setStop : 10,

//start traffic lights
init : () => {
	lts.timer = setInterval(lts.tickGrn, 1000);
	greenL = document.querySelector('#green').style.opacity = 0;
	yellowL = document.querySelector('#yellow').style.opacity = 0;
	redL = document.querySelector('#red').style.opacity = 0;
},

//green light timer
tickGrn : () => {
count = lts.setTimer;

if(count > 0) {
	greenL = document.querySelector('#green').style.opacity = 1;
	display = document.querySelector('#trfTimer');
	display.textContent = 'go';
	gTxt = document.querySelector('#grnTxt');
	gTxt.textContent = count;
	lts.setTimer--;
} else {
	greenL = document.querySelector('#green').style.opacity = 0;
	gTxt.textContent = "";
	clear = clearInterval(lts.tickGrn);
	lts.tickCaut();
	}
},

//yellow light timer
tickCaut : () => {
count = lts.setCaut;

if(count > 0) {
	yellowL = document.querySelector('#yellow').style.opacity = 1;
	display = document.querySelector('#trfTimer');
	display.textContent = 'caution';

	gTxt = document.querySelector('#ylwTxt');
	gTxt.textContent = count;
	lts.setCaut--;
} else {
	yellowL = document.querySelector('#yellow').style.opacity = 0;
	gTxt.textContent = "";
	clear = clearInterval(lts.tickCaut);
	lts.tickStop();
	}
},

//red light timer
tickStop : () => {
count = lts.setStop;

if(count > 0) {
	redL = document.querySelector('#red').style.opacity = 1;
	display = document.querySelector('#trfTimer');
	display.textContent = 'stop';

	gTxt = document.querySelector('#redTxt');
	gTxt.textContent = count;
	lts.setStop--;
} else {
	gTxt.textContent = "";
	clear = clearInterval(lts.tickStop);
	//restore the timers
	redL = document.querySelector('#red').style.opacity = 0;
	lts.setTimer = 10;
	lts.setCaut = 5;
	lts.setStop = 10;
	//restart traffic lights
	lts.tickGrn();
	}
},


};

window.addEventListener('load', lts.init);
