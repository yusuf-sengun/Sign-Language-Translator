<h1>Sign Language Translator </h1>

<h2>Project Description</h2>

The main purpose of project is translating sign-language to letters. In accordance with this purpose we deice a   <a href="https://www.kaggle.com/datamunge/sign-language-mnist" target="_blank">dataset</a> and we trained a <a href="" target="_blank">CNN-Model</a> with the dataset. You can find the <a href="" target="_blank">summary</a> of the model. We proceed the image that come from camera thanks to <a href="https://opencv.org/">openCV</a> and we predicted with CNN-Model. We take advantage of <a href="https://pypi.org/project/PyQt5/" target="_blank">PyQT5</a> to provide a graphical user inetrafce to user.

<h3>Project Features</h3>
<p>Sign-Language Translator</p>
<p>Education of Sign-Language</p>

<h3>Versions</h3>
<p>Current Project version : v0.8.0</p>
<p>Current model version : v0.3.0</p>
<p>Python version : v3.9.2</p>

<h2>Installation</h2>

<h2> How To ? </h2>

First of all you need to start project from Home.py. When you start the program a user graphical user interface pop up, In this interface there are two main and one assistan feature;<br>
<h3>1-)Sign-Language Translator</h3>
<p>The application translate the sign-language to letters that user show specified area. There are some features that established in this window as follows;</p>
<h4>1.1-)Did you mean</h4>
<p>After translation process is done, User can click "did you mean" button to list all of words that similar to predicted word.User can seelct any words that she/he wants and thanks to this feature we avoid wrong translation</p>
<h4>1.2-)Direct select to letter</h4>
<p>While translating letters user can directly select a letter from list without waiting for prediction time</p>
<h3>2-)Education</h3>
<p>The application also provide an educition system to gain ability about Sign-Language.In this mode first of all user selects a letter that want to train, after selection an image appers this image reprents selected letter in terms of Sign-Language</p>
<h3>3-)Dataset</h3>
<p>User can see the letters in terms of Sing-Language, This window does not close untill user close thanks to that, user can access data while tranlating some letters</p>
