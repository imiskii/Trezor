# Trezor

## Motivation

I created this project to brush up on my python knowledge, use encryption and hashing, create a user interface using python Kivy and Kivy MD.
The idea was to create an application that works as a safe for documents.

## What it does ?

This project contains an application that acts as a safe that store files, documents/programs/... . The application authenticates the user and at the same time encrypts all content located in the ```Safe``` folder.

There are two versions here:

1. It's a version of the app that uses a Firebase account for authentication. The encryption key is stored in the database on Firebase. This key is used for data encryption. So, in order to be able to open the safe, it is necessary to have an Internet connection.

2. This version of the application uses the user password for authentication, which is hardcoded in the program (for now) and the path to the file with the encryption key. This file must be in ```.key``` format. The idea was to store this file on a portable medium such as a USB stick or SD card.



## How you can use it ?

* __Consider using version 1.:__ First, you need to create a project on [Google Firebase](https://firebase.google.com). In this project, create a database in this way:

![img1](https://user-images.githubusercontent.com/93945176/217561143-395e1576-bf9a-42d6-b5ce-e9591ef487b0.png)

You can modify the names as you like, but it will need to be changed in the code afterwards. The value of your key does not need to be set. The first time you run it, the key will be generated and uploaded to the database. The last thing you have to do is to add to your project on Firebase the option of authentication using email and password and create an account with which you will log in. This account must have access to the database you created. It must be able to read and write to the database.

* __Consider using version 2.:__ For now, the password is set to ```password```. If you want to change it, you can use the ```Trezor_ver2/src/tmp.py``` script, replace the password you want in the ```password``` variable and run the script. A hash for this password will be generated for you. Subsequently, insert this password in the ```Trezor_ver2/src/backend.py``` file into the ```self.password``` variable in the ```SafeLock``` class.


## Dependencies

* python 3 (3.10.6)
* cryptography.fernet
* pyrebase - version 3.0.27 
* urllib
* kivy - version 2.1.0
* kivymd - version 1.1.1


## Screen Shots

### Version 1

![img2](https://user-images.githubusercontent.com/93945176/217567617-50c761d0-1114-4d60-b16f-1b4ac272b9eb.png)

### Version 2

![img3](https://user-images.githubusercontent.com/93945176/217567630-59f1da7b-5413-4298-adf7-121bc85455c1.png)

## Disclaimer

As a still learning student, I cannot judge how safe this application is for storing sensitive documents. The project is intended more as a means for learning, creating new applications and improving programming skills. This application cannot be considered safe and intended to protect sensitive documents.
