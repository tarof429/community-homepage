# Community Homepage

## Introduction

This is a community homepage similar to those found on websites like https://www.paloaltoonline.com. It has a special focus on a community calendar where users can browse for local events. Below is a description of the initial requirements and progression of code development.

<img src="community_homepage.png" />

## Description

The community homepage app manages events with the following fields:

- title
- date
- time
- description
- location

Data will be stored in SQLite and displayed in a table. Users will be able to perform basic CRUD actions. 

At this point, I'd like to introduce testing for models and utility functions. This can alleviate some of the manual effort to ensure the application's functionality as additional features are added.

Once the app is working, I'd like to address some of the limitations. As more events are added to the database, users will want to be able to search for events. Also I'd like to limit the number of events shown to the user. These problems can be solved by implementing a data table. There is actually a Javascript library called dataTables.js that will be used to implement this. Since I am only adding a Javascript library, I don't expect any tests to break.

At this point, I might want to introduce another field: category. I'm not sure whether this would be an enum or just a text field. The goal is to see whether adding this field can make it easier to search for events, such as events that don't have a keyword in the title. 

Next, I'd like to migrate the database from SQLite to a database running in a docker container. Some things to consider are: what database to use and whether to continue using SQLite for testing/development. Again we don't expect any tests to break.

Finally the app will be migrated to a docker container, making it possible to run in any environment easily. 

