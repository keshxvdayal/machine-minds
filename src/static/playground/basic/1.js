const LEVEL = 1
const CORRECT = ['b','c','a','d','a']

let curr_active_ques = 1
let total_ques = 5
let ques
let ans
let answers = {}


function onclick_button(q_no) {
	curr_active_ques = q_no
	// Display the div with id " q{number}", abd hide the rest
	for (let i = 1; i <= total_ques; i++) {
		ques = document.getElementById(`q${i}`)
		ans = document.getElementById(`a${i}`)
		ques.style.display = "none"
		ans.style.display = "none"
	}
	ques = document.getElementById(`q${q_no}`)
	ans = document.getElementById(`a${q_no}`)
	ques.style.display = "block"
	ans.style.display = "block"
}

function onclick_option(opt) {
	answers[curr_active_ques] = opt
	console.log(answers)

	// Turn elem with id "<q><ans>" into class=selected, and remove that class from all other answers of that question
	let option = document.getElementById(`${curr_active_ques}a`)
	option.classList.remove("selected")
	option = document.getElementById(`${curr_active_ques}b`)
	option.classList.remove("selected")
	option = document.getElementById(`${curr_active_ques}c`)
	option.classList.remove("selected")
	option = document.getElementById(`${curr_active_ques}d`)
	option.classList.remove("selected")

	option = document.getElementById(`${curr_active_ques}${opt}`)
	option.classList.add("selected")
}

function onclick_submit() {
	let score = 0;
	for (let i = 1; i <= total_ques; i++) {
		if (answers[i] === CORRECT[i - 1]) {
			score += 1
		}
	}
	
	fetch(`/api/submit-basic-level`, {
		method: "POST",
		body: JSON.stringify({
			level: LEVEL,
			answers: answers,
			score: score
		}),
		headers: { "Content-Type": "application/json" },
	})
	.then(response => response.json())
	.then(data => {})

	alert(`You got ${score} questions right!`)
}

onclick_button(curr_active_ques)

