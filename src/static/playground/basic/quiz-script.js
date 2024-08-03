const LEVEL = 1

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
	fetch(`/api/submit-basic-level/level${LEVEL}`, {
		method: "POST",
		body: JSON.stringify(answers),
		headers: { "Content-Type": "application/json" },
	})
		.then(response => response.json())
		.then(data => {
			alert(`You got ${data.score} questions right!`)
		})
}

onclick_button(curr_active_ques)

