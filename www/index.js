var map;
var myData;
var mapNotCreated = true;
function load() {
	//Runs when the html page is loaded
    var notCalled = true;
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if(notCalled){
			insert(xhttp.responseText);
			notCalled = false;
		}
		console.log("onreadystatechange was called but not run");
	};
	xhttp.open("GET", "people.json", true);
	xhttp.send();

}

function loadInterval(){
	load();
}

function insert(data){
	// alert(notCalled);
	//Inserts info to html page
	data = JSON.parse(data);
	myData = data;
	console.log(Object.keys(data.people));
	// document.getElementById('tableid').insertAdjacentHTML("beforeend","<tbody>");
	var insertString = "";
	for(var i=0;i<Object.keys(data.people).length;i++){
		// alert(data.people[i].name);
		//for adding th +"<td>"++"</td>"+
		// 
		var index = Object.keys(data.people)[i];
		
		if(data.people[index].notsafe == "true"){
			console.log(data.people[index].name + ".notSafe is"+data.people[index].notSafe);
			insertString += "<tr><td>"+ (i+1) +"</td>"+
			"<td>"+data.people[index].name+"</td>"+
			"<td>"+data.people[index].age+"</td>"+
			"<td>"+data.people[index].homeaddr+"</td>"+
			"<td>"+data.people[index].bloodtype+"</td>"+
			// "<td>"+"Lat:"+data.people[index].lat+" Long:"+data.people[index].long+"</td>"+
			"<td><button type='button' onclick='geocode("+data.people[index].lat+","+data.people[index].long+','+i+");' class='btn btn-secondary'>"+"Lat:"+data.people[index].lat+" Long:"+data.people[index].long+"</button></td>"+
			"<td>"+new Date(data.people[index].timestamp*1000)+"</td>"+
			"<td>"+data.people[index].specneeds+"</td>"+
			"<td>"+data.people[index].other+"</td>"+
			"</tr>";
		}else{
			console.log(data.people[index].name + ".notsafe is "+data.people[index].notsafe);
		}
	}
	document.getElementById('tableid').insertAdjacentHTML("beforeend",insertString);
	sort();
	// document.getElementById('tableid').insertAdjacentHTML("beforeend","</tbody>");
	
}
function sort(){
	$('#tableid').DataTable( {
        "order": [[ 3, "desc" ]]
    } );
    window.scrollTo(0,0);
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function moveEverythingRight(amt){
	let children = document.getElementsByTagName("*");
	for(var i = 0; i < children.length; i++){
		children[i].style.left += amt;
	}
}

function danger(){
	alert("DANGER!!!");
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		console.log("Sent");
	};
	xhttp.open("GET", "shitgroundisshakingbruh", true);
	xhttp.send();
}

function createGeoCode(lat,long){
	var platform = new H.service.Platform({
	  'app_id': '8QZRPks2FC5AiCn1C6ON',
	  'app_code': 'B9SV9d5o-I0jtq8P8b2_Xg',
	  "useHTTPS":'true'
	});
	// Obtain the default map types from the platform object:
	var defaultLayers = platform.createDefaultLayers();
	// Instantiate (and display) a map object:
	map = new H.Map(
	  document.getElementById('mapContainer'),
	  defaultLayers.normal.map,
	  {
	    zoom: 10,
	    center: { lat: lat, lng: long }
	  });
	  
	var behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(map));
	var ui = H.ui.UI.createDefault(map, defaultLayers)
}
function geocode(lat,long,id){
	if(mapNotCreated){
		document.getElementById("mapContainer").style.width = "300px";
		document.getElementById("mapContainer").style.height = "300px";
		createGeoCode(lat,long);
		mapNotCreated= false;
	}
	var newMarker = new H.map.Marker({lat:lat, lng:long});
	map.addObject(newMarker);
	map.setCenter({lat:lat, lng:long});
	map.setZoom(10);
	var index = Object.keys(myData.people)[id];
	document.getElementById("mapTxt").innerHTML = myData.people[index].name;
	document.getElementById("mapTxt").style.marginLeft = "auto";
	document.getElementById("mapTxt").style.marginRight = "auto";
	document.getElementById("mapContainer").style.border = "thick solid #4a505b";
	document.getElementById("mapOf").scrollIntoView();
}