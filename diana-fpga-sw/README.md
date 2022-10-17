<div id="top"></div>

<!-- PROJECT TITLE -->
<br />
<div align="center">
  <h3 align="center">diana-fpga-sw</h3>

  <p align="center">
    Python software and script to execute on the ARM core of the FPGA and on the host PC
    <br />
    <a href="https://github.com/dianaKUL/diana-fpga-sw"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/dianaKUL/diana-fpga-sw/issues">Report Bug</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About

The repository contains the Python software and scripts to be executed on the ARM core of the FPGA and on the host PC.

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

First, please clone the repository:
```sh
git clone git@github.com:dianaKUL/diana-fpga-sw.git
```
After that we highly advise to setup a dedicate `RSA key` to connect to the Zedboard through `ssh` from any ESAT machine.
First create an SSH keypair on your esat machine:
```sh
ssh-keygen -f ~/.ssh/zedb-diana-key
```
For a complete setup, we suggest to create a dedicated gateway in the ssh config file located under `~/.ssh/config`. Below an example:
```ssh-config
Host zedb-diana
        User root
        HostName 10.88.18.167
        Port 22
        IdentityFile ~/.ssh/zedb-diana-key
```
Then login to the zedboard with the password provided by one of your colleagues
```sh
ssh zedb-diana
```
Append the contents of your public key (e.g. `~/.ssh/zedb-diana-key.pub` to the `authorized_keys` file on the zedboard.

### Prerequisites

The host scripts need pyvisa API nad pyvisa-py drivers to control the instrumentation in the lab. We highly suggest to create a dedicated conda environment.
* pyvisa
  ```sh
  conda create --name "pyvisa"
  conda activate pyvisa
  conda install mako
  conda install -c conda-forge pyvisa-py
  ```

### Installation
1. Clone the repo
   ```sh
   git clone git@github.com:dianaKUL/diana-fpga-sw.git
   ```
2. Install the <a href="#prerequisites">Prerequisites</a>

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

# Manual use

Open 4 different terminals. They will be used for:
- `Host PC` script
- `FPGA` python script
- `openocd` connection
- `gdb` program

First run the host PC script `host_scripts/boot-diana-man.py` and follow the instruction on the script.

Note: to automatically run the gdb program use the `-x <gdb-script>` option

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

If you want to modify base scripts or libraries please follow this procedure:

1. Create your Feature Branch (`git checkout -b <user>/AmazingFeature`)
2. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
3. Push to the Branch (`git push origin <user>/AmazingFeature`)
4. Make sure your Feature is stable
5. Merge to main (`git checkout main` + `git merge <user>/AmazingFeature`)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Giuseppe Sarda - Giuseppe.Sarda@imec.be

Project Link: [https://github.com/dianaKUL](https://github.com/dianaKUL)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Grazie mamma!

<p align="right">(<a href="#top">back to top</a>)</p>
