function selected_reload(testName) {
	
	let selectedElement = document.getElementById(testName);
		
	// console.log("classList: ", selectedElement.classList);
	if(selectedElement.classList.contains("bg-green-500")) {
		selectedElement.classList.replace("bg-green-500", "bg-purple-500");
	} else {
		selectedElement.classList.replace("bg-purple-500", "bg-green-500");
	}
}

eel.expose(get_pictures);
function get_pictures(pictures) {
	
	// console.log("pictures: ", pictures);
	pictures.forEach( pictureName => {
		let card = document.createElement("div");
		card.className = 
		"h-32 bg-green-500 mt-5 mx-5 rounded transition duration-500 hover:bg-indigo-600 transform hover:-translate-y-1 hover:scale-110 flex flex-row";
		card.id = pictureName;
		
		let picture = document.createElement("img");
		picture.src = "pictures/" + pictureName;
		picture.className = "object-scale-down w-1/3 ml-3 my-3";
		card.appendChild(picture);
		
		let textDiv = document.createElement("div");
		textDiv.appendChild(document.createTextNode(pictureName));
		textDiv.className = "";
		
		card.appendChild(textDiv);
		card.addEventListener("click", () => selected_reload(pictureName));
		document.getElementById("cardsList").appendChild(card);
	});
}

function start() {
	
	let picturesElement = document.getElementsByClassName("bg-purple-500");
	let pictures = [];
	for( let p of picturesElement ) {
		pictures.push(p.children[1].textContent);
	}
	eel.start(pictures);
}