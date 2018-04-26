var easycam;
var count;
var size;
var pad;
var step;

var data;

function setup(){
 
	pixelDensity(1);

	var canvas = createCanvas(windowWidth, windowHeight, WEBGL);
	
  	
	setAttributes('antialias', true);
	easycam = new Dw.EasyCam(this._renderer, {distance : 500}); 
	easycam.setRotationConstraint(true, true, false);


	data = new Array();
	count = 16;
	size = 20;
	pad = 2;
	step = size + pad;

	for (var i = 0; i < count; i++) {
		data.push([]);
		for (var j = 0; j < count; j++) {
			data[i][j] = random(100);
		}
	}

	colorMode(HSB, 1);
}

function draw(){

	background(0, 0, 0.1);
	noStroke();
	
	normalMaterial(250);

	// gotta point exactly at the middle -> 1 less pad in width
	
	push();
	translate(-step * count / 2, -step * count / 2, 0);
	for (var i = 0; i < count; i++) {
		for (var j = 0; j < count; j++) {
			fill(color(j / count, 1, (i + 1) / count));
			h = data[i][j];
			translate(0, 0, h / 2)
			box(size, size, h);
			translate(0, step, -h / 2);
		}
		translate(step, -step * count, 0);
	}
	pop();
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
  easycam.setViewport([0, 0, windowWidth, windowHeight]);
}