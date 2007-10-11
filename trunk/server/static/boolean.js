// utility function to get an element by id
function get(name){
	return document.getElementById(name);
}

// this toggles between none and block
function toggle(name){
	var elem = get(name)
	if (elem) {
		if (elem.style.display=="none"){
			elem.style.display="block"
		} else {
			elem.style.display="none"
		}
	}
}

function change( name, state){
	var elem = get(name)
	if ( elem ) {
		elem.style.display=state
	}
}

function show( name ){
	change( name, 'block')
}

function hide( name ){
	change( name, 'none')
}

// utility function to get the length of on object 
function len(obj){
	return obj.length
}

function main(){
	menu = get('method')
	if ( menu.selectedIndex == 2 ) {
		show( 'time' )		
	} else {
		hide( 'time' )
	}
}


