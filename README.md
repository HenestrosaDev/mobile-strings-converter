<div id="top"></div>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![CC0-1.0 license][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">Android strings converter</h3>

  <p align="center">
    A Python package that converts Android strings.xml file to any file type supported by the package. 
    <br />
    <a href="https://github.com/HenestrosaConH/android-strings-converter/issues">Report Bug</a> · <a href="https://github.com/HenestrosaConH/android-strings-converter/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
   <summary>Table of Contents</summary>
   <ol>
      <li>
         <a href="#about-the-project">About The Project</a>
         <ul>
            <li><a href="#project-structure">Project Structure</a></li>
            <li><a href="#built-with">Built With</a></li>
         </ul>
      </li>
      <li><a href="#getting-started">Getting Started</a></li>
      <li><a href="#usage">Usage</a></li>
      <li><a href="#contributing">Contributing</a></li>
      <li><a href="#license">License</a></li>
      <li><a href="#contact">Contact</a></li>
      <li><a href="#acknowledgments">Acknowledgments</a></li>
   </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

In the first execution, the script asks the user to select a folder to store the xkcds vignettes (in a folder called `xkcd-vignettes`) and explanations (`xkcd-explanations`).
Once that's done, the script will start to download all existing xkcds. On successive runs of the script, it will check if there are any new xkcds available for download.

<!-- PROJECT STRUCTURE -->

### Project Structure

Directories:

- `data`: Contains the `xkcd-path.txt`, which stores the path where the xkcds are being stored.
- `src`:  Contains the source code files.

Besides those directories, there are also these two files in the root (apart from the .gitignore, README.md and LICENSE):

- `requirements.txt`: Lists the names and versions of each package used to build this project. To install the requirements, execute `pip install -r requirements.txt`.

<!-- BUILT WITH -->

### Built With

- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [httpx](https://www.python-httpx.org/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

If you want to execute the program:
- Go to [releases](https://github.com/HenestrosaConH/android-strings-converter/releases) and download the latest one.

If you want to open the code:
- Clone the project with the `git clone https://github.com/HenestrosaConH/android-strings-converter.git` command and then open it with your favourite IDE (mine is [PyCharm](https://www.jetbrains.com/pycharm/)).

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE -->

## Usage



<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag `enhancement`.
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the Creative Commons 1.0 License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

<a href="https://www.linkedin.com/in/henestrosaconh/" target="blank"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
<a href="mailto:henestrosaconh@gmail.com" target="_blank"><img alt="Gmail" src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" /></a>

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

I've made use of the following resources to make this project:

- [Best-README-Template](https://github.com/othneildrew/Best-README-Template/)
- [Img Shields](https://shields.io)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/HenestrosaConH/android-strings-converter.svg?style=for-the-badge
[contributors-url]: https://github.com/HenestrosaConH/android-strings-converter/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/HenestrosaConH/android-strings-converter.svg?style=for-the-badge
[forks-url]: https://github.com/HenestrosaConH/android-strings-converter/network/members
[stars-shield]: https://img.shields.io/github/stars/HenestrosaConH/android-strings-converter.svg?style=for-the-badge
[stars-url]: https://github.com/HenestrosaConH/android-strings-converter/stargazers
[issues-shield]: https://img.shields.io/github/issues/HenestrosaConH/android-strings-converter.svg?style=for-the-badge
[issues-url]: https://github.com/HenestrosaConH/android-strings-converter/issues
[license-shield]: https://img.shields.io/github/license/HenestrosaConH/android-strings-converter.svg?style=for-the-badge
[license-url]: https://github.com/HenestrosaConH/android-strings-converter/blob/master/LICENSE.txt
[linkedin-url]: https://linkedin.com/in/henestrosaconh
