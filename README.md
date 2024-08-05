<div align="center">

<!-- https://coolors.co/gradient-palette/f72585-066da5?number=3 -->

[![GitHub stars](https://img.shields.io/github/stars/keshxvdayal/machine-minds?color=F72585&labelColor=302D41&style=for-the-badge)](https://github.com/keshxvdayal/machine-minds)
[![GitHub last commit](https://img.shields.io/github/last-commit/keshxvdayal/machine-minds?color=7F4995&labelColor=302D41&style=for-the-badge)](https://github.com/keshxvdayal/machine-minds)
[![GitHub issues](https://img.shields.io/github/issues/keshxvdayal/machine-minds?color=066DA5&labelColor=302D41&style=for-the-badge)](https://github.com/keshxvdayal/machine-minds)




https://github.com/user-attachments/assets/4996afbf-ca61-4a05-ac33-c60859f9cf44

<!-- https://github.com/keshxvdayal/machine-minds/raw/main/assets/recording.mp4 -->
<!-- https://user-images.githubusercontent.com/79649185/182558272-255becc8-1dcc-45b5-99ef-22e0596cf490.mp4 -->

</div>




<br><hr><br>



# Introduction
- Designed an **attractive game-based learning platform** for machine learning concepts
- Developed **engaging quizzes** to test the user's knowledge
- Developed **interactive visualizations** to help users understand the role of the hyperparamters
- Provided **guides with a human touch** for various machine learning concepts
- Implemented a **forum** for users to ask questions and get help from the community
- Integrated **Google OAuth** to simplify and streamline the login process

<br>

### Techstack
- Python
- Flask
- Scikit-learn
- SQLite3
- Matplotlib
- HTML+CSS+JS

<br>

### Endpoints
| URL Path                 | Description                        |
|--------------------------|------------------------------------|
| `/`                      | Home page                          |
| `/dashboard`             | Dashboard for the user             |
| `/playground`            | Page for choosing basic or advanced levels |
| `/basic`                 | All the basic levels               |
| `/basic/level<int>`      | A specific basic level             |
| `/advanced`              | All the advanced levels            |
| `/advanced/level<int>`   | A specific advanced level          |
| `/forum`                 | Home page of the forum             |
| `/forum/<postid>`        | A specific post                    |
| `/forum/submit`          | Page for creating a new post       |
| `/guides`                | All the guides                     |
| `/guides/<guideid>`      | A specific guide                   |




<br><hr><br>



# Running the website

If you want to run the wesbite locally, follow the steps below:

<br>

First of all, ensure that [git](https://git-scm.com/downloads) and [python](https://www.python.org/downloads/) are installed on your system. Then run the following commands:

```bash
git clone https://github.com/keshxvdayal/machine-minds
cd machine-minds/src
pip install -r requirements.txt
python app.py
```

And voila, the website should be up and running on `http://127.0.0.1:5001`

