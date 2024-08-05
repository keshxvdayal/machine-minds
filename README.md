<div align="center">

<!-- https://coolors.co/gradient-palette/f72585-066da5?number=3 -->

[![GitHub stars](https://img.shields.io/github/stars/keshxvdayal/machine-minds?color=F72585&labelColor=302D41&style=for-the-badge)](https://github.com/keshxvdayal/machine-minds)
[![GitHub last commit](https://img.shields.io/github/last-commit/keshxvdayal/machine-minds?color=7F4995&labelColor=302D41&style=for-the-badge)](https://github.com/keshxvdayal/machine-minds)
[![GitHub issues](https://img.shields.io/github/issues/keshxvdayal/machine-minds?color=066DA5&labelColor=302D41&style=for-the-badge)](https://github.com/keshxvdayal/machine-minds)


https://github.com/keshxvdayal/machine-minds/raw/main/assets/recording.mp4
<!-- https://user-images.githubusercontent.com/79649185/182558272-255becc8-1dcc-45b5-99ef-22e0596cf490.mp4 -->

</div>




<br><hr><br>



# Introduction
- Designed an **attractive game-based learning platform** for machine learning concepts
- Developed **engaging quizzes** to test the user's knowledge
- Developed **interactive visualizations** to help users understand the role of the hyperparamters
- Provided **guides with a human touch** for various machine learning concepts
- Implemented a **forum** for users to ask questions and get help from the community
- Integrated a **Google OAuth** to simplify and streamline the login process

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
(Common)
- `/` - Home page
- `/dashboard` - Dashboard for the user
(Playground)
- `/playground` - Page for choosing basic or advanced levels
- `/basic` - All the basic levels
- `/basic/level<int>` - A specific basic level
- `/advanced` - All the advanced levels
- `/advanced/level<int>` - A specific advanced level
(Forum)
- `/forum` - Home page of the forum
- `/forum/<postid>` - A specific post
- `/forum/submit` - Page for creating a new post
(Guides)
- `/guides` - All the guides
- `/guides/<guideid>` - A specific guide



<table>
    <tr>
        <td rowspan=2>Common</td>
    </tr>
    <tr>
        <td>`/`</td>
        <td>Home page</td>
    </tr>
    <tr>
        <td>`/dashboard`</td>
        <td>Dashboard for the user</td>
    </tr>
    <tr>
        <td rowspan=2>Playground</td>
    </tr>
    <tr>
        <td>`/playground`</td>
        <td>Page for choosing basic or advanced levels</td>
    </tr>
    <tr>
        <td>`/basic`</td>
        <td>All the basic levels</td>
    </tr>
    <tr>
        <td>`/basic/level<int>`</td>
        <td>A specific basic level</td>
    </tr>
    <tr>
        <td>`/advanced`</td>
        <td>All the advanced levels</td>
    </tr>
    <tr>
        <td>`/advanced/level<int>`</td>
        <td>A specific advanced level</td>
    </tr>
    <tr>
        <td rowspan=2>Forum</td>
    </tr>
    <tr>
        <td>`/forum`</td>
        <td>Home page of the forum</td>
    </tr>
    <tr>
        <td>`/forum/<postid>`</td>
        <td>A specific post</td>
    </tr>
    <tr>
        <td>`/forum/submit`</td>
        <td>Page for creating a new post</td>
    </tr>
    <tr>
        <td rowspan=2>Guides</td>
    </tr>
    <tr>
        <td>`/guides`</td>
        <td>All the guides</td>
    </tr>
    <tr>
        <td>`/guides/<guideid>`</td>
        <td>A specific guide</td>
    </tr>
</table>



<br><hr><br>



# Running the website

If you want to run the wesbite locally, follow the steps below:

<br>

First of all, ensure that [git](https://git-scm.com/downloads) and [python](https://www.python.org/downloads/) are installed on your system. Then run the following commands:

```bash
git clone https://github.com/keshxvdayal/machine-minds
cd machine-minds/src
pip install -r requirements.txt
python main.py
```

And voila, the website should be up and running on `http://127.0.0.1:5001`

