let check = document.getElementByid(".check");

let text = check.innerText(".text");
console.log(text);

let regex = /^[1-9]{1}[0-9]{9}$/;

check.addEventListener("click",()=>{
	if(number.value ==""){
		text.innerText = "Please Enter Your Phone Number";
		text.style.color = "#fff";
	}
	else if(number.value.match(regex)){
		text.innerText = "Congrats! You Enter A Valid Phone Number";
		text.style.color = "rgba(4,125,9,1)";
	}
	else
		{
		text.innerText = "Oops! Your Phone Number Is Invalid";
		text.style.color = "#da3400";
		}
});