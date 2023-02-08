# Trezor

## Motivation

I created this project to brush up on my python knowledge, use encryption and hashing, create a user interface using python Kivy and Kivy MD.
The idea was to create an application that works as a safe for documents.

## What it does ?

This project contains an application that acts as a safe that store files, documents/programs/... . The application authenticates the user and at the same time encrypts all content located in the ```Safe``` folder.

There are two versions here:

1. It's a version of the app that uses a Firebase account for authentication. The encryption key is stored in the database on Firebase. This key is used for data encryption. So, in order to be able to open the safe, it is necessary to have an Internet connection.

2. This version of the application uses the user password for authentication, which is hardcoded in the program (for now) and the path to the file with the encryption key. This file must be in ```.key``` format. The idea was to store this file on a portable medium such as a USB stick or SD card.



## How can it be used ?

* __Consider using version 1.:__ First, you need to create a project on [Google Firebase](https://firebase.google.com). In this project, create a database in this way:

![obr1](https://user-images.githubusercontent.com/93945176/217557355-00761ab3-da40-44ab-851f-f22c42fb800d.png)


* __Consider using version 2.:__


## Disclaimer

As a still learning student, I cannot judge how safe this application is for storing sensitive documents. The project is intended more as a means for learning, creating new applications and improving programming skills. This application cannot be considered safe and intended to protect sensitive documents.
