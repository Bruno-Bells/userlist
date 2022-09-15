[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/bruno-odinukweze-023a48198/)


## TECHNICAL ACCESSMENT SOLUTION

<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="http://localhost:5000/api/docs/" target="_blank">
    <img src="https://img.freepik.com/free-vector/gradient-api-illustration_23-2149368725.jpg?w=1060&t=st=1663195122~exp=1663195722~hmac=3a7503a684c20cde6aef60d2c9ee282c3d605702dfd44dd2d0459ad3daceecea" alt="Logo" width="180" height="150">
  </a>

  <h3 align="center">Users API</h3>

  <p align="center">
    This repo contains an API code base.
    <br />
    <a href="http://localhost:5000/api/docs/" target="_blank"><strong>Explore the API docs »</strong></a>
    <br />
    <br />
 
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Tech Stack</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation/Setup Instruction</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project is an API endpoint that get a list of Users from a database.

### Features:
* Pagination support
* Filtration support
* Cache-Control (client and server-side)

This project is a solution to a technical challenge and is built as per the requirements/problem statement which can be found <a href="https://gist.github.com/scabbiaza/82e9069cfa71c4d7aa9d9539a794a1db" target="_blank">HERE</a>.



Use this url to <a href="#readme-top">View Live Demo</a>

<!-- <p align="right">(<a href="#readme-top">back to top</a>)</p> -->



### Built With

Below is a list of technologies used to build the project.

* ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
* ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
* ![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
* ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
* ![Heroku](https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white)
* ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
* ![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)
* ![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
* ![GitLab](https://img.shields.io/badge/gitlab-%23181717.svg?style=for-the-badge&logo=gitlab&logoColor=white)




<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

These is a necessary software that you need to install on your OS in order to run this project locally.
* Docker


### Installation

_Below is a list of instructions in other to install the project locally._

1. `Clone this repo and CD into the root directory`

2. `create a .env file in the project root and add you environment variables. look at` [.env.example](./.env.example) `to see the specification sample for this project`

   _setup commands. Run the following commands at the root of the project to spin it up_

2. ```
   docker-compose up --build
   ```
   
3. ```
   docker exec -it project_website_1 bash 
   ```
   `project_website_1 is the name of the image in this case`
   
4. ```
   pip install --editable .
   ```
   `type exit and hit enter to exit the bash and enter the following command:`
5. ```
   docker-compose exec website project add all
   ```
6. `open your web browser and enter the following url`
   ```
   http://localhost:5000/api/docs/
   ```
   `Hurrey! the API is up!`
   

<!-- USAGE EXAMPLES -->
## Usage

_To play around with the API, please visit to the [Documentation](http://localhost:5000/api/docs/) _


<!-- LICENSE -->
## License

[![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](./LICENSE)


<!-- CONTACT -->
## Contact

Bruno Odinukweze - [LinkedIn](https://www.linkedin.com/in/bruno-odinukweze-023a48198/)


<p align="right">(<a href="#readme-top">back to top</a>)</p>


