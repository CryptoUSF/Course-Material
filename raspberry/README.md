Raspberry Pi
============

Raspberry Pi Hardware
---------------------

The required Raspberry Pi components are described here: <http://rpi.cs.usfca.edu/2017-fall>

I'd recommend a [metal case](https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Delectronics&field-keywords=Eleduino+Raspberry+Aluminum+Metal+Case) for the Pi.

##Setting up Kali Linux on Raspberry Pi
Kali LInux images are avaialble from:
<https://www.offensive-security.com/kali-linux-arm-images/>

After downloading the image, you should check the SHA256Sum of the downloaded 'xz' file.

    $ shasum -a 256 kali-2017.2-rpi3-nexmon.img.xz
    341a942010a34d1c11ffed97a0695c4f5b5033387228d48955aa03d027f00474

When setting up Kali Linux on Raspberry Pi, there are some slight differences from installing Raspbian. Detailed instructions are available [here](https://docs.kali.org/kali-on-arm/install-kali-linux-arm-raspberry-pi).

The Kali Linux ARM image is packaged as a .xz extension file. If you are using a
Mac, you may need to download a 3rd party tool like the
[Unarchiver](https://theunarchiver.com/) to extract the image or use brew to
download the "xzcat" command line tool which is already available on Linux
platforms. The same goes for Windows users, download a 3rd party tool for
decompression of files.

Once you have extracted the .img file of Kali. On Mac and Linux, you can use the
"dd" command or use Etcher if you are not comfortable with the command line.
Depending on the type of SD card, it can take a while to copy the image to your
SD card. On Windows, you can use Etcher as well.

Once you have successfully copied the Kali image to the SD card, you may insert
it into the Raspberry Pi and boot up the Pi. Connect the Pi to an external
display. Kali only takes up about 6GB of the SD card. Most of you will have an
SD card of 8GB, 16GB or 32GB. To fully maximize the space available, you must
resize the Kali image. There are a couple of ways to do this. You can use the
"resize2fs" command line tool or use gparted to resize. gparted is a GUI
application which you can download by running "apt install gparted".

You will need to perform other stuff like setting up ssh for headless
connectivity.

### Change default root password

Change the default root password:

    root@kali:~# passwd
    Enter new UNIX password: 
    Retype new UNIX password: 
    passwd: password updated successfully

### Create a standard user account
The Kali distribution does not create a standard user account. One of the first things that needs to be done is to create a standard user account (cs486 in this example):

    root@kali:~# useradd -m cs486

The -m option creates the user's home directory.

Create a password for the user: 

    root@kali:~# passwd cs486
    Enter new UNIX password: 
    Retype new UNIX password: 
    passwd: password updated successfully

Add the user to the sudo group (to install software etc): 

    root@kali:~# usermod -a -G sudo cs486

The -a indicates add and -G gives the group name.

Change the default shell for the newly added user:

    root@kali:~# chsh -s /bin/bash cs486

### Regenerate SSH Keys

Delete old ssh host keys: 
  
    root@kali:/etc/ssh# rm -v /etc/ssh/ssh_host_*
    removed '/etc/ssh/ssh_host_ecdsa_key'
    removed '/etc/ssh/ssh_host_ecdsa_key.pub'
    removed '/etc/ssh/ssh_host_ed25519_key'
    removed '/etc/ssh/ssh_host_ed25519_key.pub'
    removed '/etc/ssh/ssh_host_rsa_key'
    removed '/etc/ssh/ssh_host_rsa_key.pub'
 
 Now create a new set of keys on your SSHD server, enter:

    root@kali:/etc/ssh# dpkg-reconfigure openssh-server
    Creating SSH2 RSA key; this may take some time ...
    2048 SHA256:Z4SSbdtK+IBenKkEqgPwVo6MFO90qCTuypd/sIT5EvQ root@kali (RSA)
    Creating SSH2 ECDSA key; this may take some time ...
    256 SHA256:KzAGc/dsWGQ00KMPEGGkzXaua970mhpk205XWkeE2mw root@kali (ECDSA)
    Creating SSH2 ED25519 key; this may take some time ...
    256 SHA256:hqVavgnXDZwDTnTMFl/or1chk6JuE/vba2ZTYXjBRLA root@kali (ED25519)

Restart the SSH server:

    root@kali:~# /etc/init.d/ssh restart
    [ ok ] Restarting ssh (via systemctl): ssh.service.

Update know ~/.ssh/known_hosts file on the on any system that has already connected to this server to prevent errors like:

	fish:$ ssh cs486@192.168.1.89
	@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
	@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
	@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
	IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
	Someone could be eavesdropping on you right now (man-in-the-middle attack)!
	It is also possible that a host key has just been changed.
	The fingerprint for the ECDSA key sent by the remote host is
	SHA256:KzAGc/dsWGQ00KMPEGGkzXaua970mhpk205XWkeE2mw.
	Please contact your system administrator.
	Add correct host key in /Users/paul/.ssh/known_hosts to get rid of this message.
	Offending ECDSA key in /Users/paul/.ssh/known_hosts:7
	ECDSA host key for 192.168.1.89 has changed and you have requested strict checking.
	Host key verification failed.
	http://www.r00tsec.com/2013/04/howto-installing-kali-in-raspberry-pi.html

This problem can be fixed by editing the ~.sss/know\_hosts file to remove the recorded key for the Kali SSH server.  This will be on the machine you are using as an SSH client. This and the prior changes will not disconnect an existing session. If there are no other important host keys in the know_hosts file, this error may also be prevented by deleting the known hosts file:

    $rm ~/.ssh/known_hosts

Logout and log-in again as the standard user.


### Resize the SD Partitions - 'gparted'

If you plan on running the full Kali distribution you must resize the partition. When initially installed, the partition is configured for only 8G of SD card storage. Run the 'gparted' application from the UI: Applications/System/Gparted
    
### Update/Upgrade the Installation

    cs486@kali:~$ sudo apt-get update
    cs486@kali:~$ sudo apt-get -y dist-upgrade
    cs486@kali:~$ sudo apt-get -y autoremove
    cs486@kali:~$ sudo apt-get clean
    cs486@kali:~$ sudo reboot

### Enable Wireshark usage for non-root user

The OS prevents Wireshark from accessing network interfaces unless the capabilities are modified.

    $ sudo groupadd wireshark
    $ sudo usermod -a -G wireshark <$USER>
    $ sudo newgrp wireless
    $ sudo reboot
    
### Backing up an SD using a Macintosh

Insert SD card and find the correct drive number:

    $diskutil list

Using the identified drive number (replacing <x> below):

    $sudo dd of=/dev/rdisk<x> bs=5m of=~/Desktop/raspberrypi.dmg 
    
### Restoring a SD card from a .dmg using a Macintosh

Put target SD card in carrier and connect to Mac. List the mounted drives and identify the newly mounted SD card:

    $diskutil list

Identify the correct drive and use this number in the commanline operations below:
    
    $diskutil unmountDisk /dev/disk<x>
    $sudo newfs_msdos -F 16 /dev/disk<x>
    $sudo dd if=~/Desktop/sd_image.dmg of=/dev/rdisk<x> bs=5m

[Reference](https://computers.tutsplus.com/articles/how-to-clone-raspberry-pi-sd-cards-using-the-command-line-in-os-x--mac-59911)

### Install VNC (not complete ...)

To remotely access the graphical user interfaces you may want to install VNC:

    $sudo apt-get install tightvncserver

Run 'tightvncserver' to set password:

    $tightvncserver
    
    
 ... more ... tbd
 <http://blog.cudmore.io/post/2015/04/29/vnc-on-raspberry/>
 
 Install Autocutsel package to enable cut&paste between client and server:

    $sudo apt-get install autocutsel
    

 
     #!/bin/sh

    xrdb $HOME/.Xresources
    xsetroot -solid grey
    autocutsel -fork
    #x-terminal-emulator -geometry 80x24+10+10 -ls -title "$VNCDESKTOP Desktop" &
    #x-window-manager &
      # Fix to make GNOME work
    export XKL_XMODMAP_DISABLE=1
    /etc/X11/Xsession
    


https://www.jeffgeerling.com/blog/2017/mount-raspberry-pi-sd-card-on-mac-read-only-osxfuse-and-ext4fuse





<http://blog.sevagas.com/?VNC-to-access-Kali-Linux-on-Raspberry-Pi>
<http://blog.sevagas.com/?Linux-filesystem-security-scans>
<http://blog.sevagas.com/?Rogue-WiFi-Access-point>