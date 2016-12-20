# Checkpoint-1
[![Coverage Status](https://coveralls.io/repos/github/andela-gochieng/Checkpoint-1/badge.svg?branch=develop&update=2)](https://coveralls.io/github/andela-gochieng/Checkpoint-1?branch=develop)
[![Code Climate](https://codeclimate.com/repos/5836fc96b211081579003726/badges/f052d6d199ff57cd1dd1/gpa.svg)](https://codeclimate.com/repos/5836fc96b211081579003726/feed)
[![Build Status](https://travis-ci.org/andela-gochieng/Checkpoint-1.svg?branch=develop&update=1)](https://travis-ci.org/andela-gochieng/Checkpoint-1)
[![Code Health](https://landscape.io/github/andela-gochieng/Checkpoint-1/develop/landscape.svg?style=flat&update=1)](https://landscape.io/github/andela-gochieng/Checkpoint-1/master)
[![Issue Count](https://codeclimate.com/repos/5836fc96b211081579003726/badges/f052d6d199ff57cd1dd1/issue_count.svg)](https://codeclimate.com/repos/5836fc96b211081579003726/feed)
[![Test Coverage](https://codeclimate.com/repos/5836fc96b211081579003726/badges/f052d6d199ff57cd1dd1/coverage.svg)](https://codeclimate.com/repos/5836fc96b211081579003726/coverage)
## Amity - Automated Space Allocation System
Amity is a system that automates the allocation of rooms in a facility. It is especially modelled for the Andela fellowship. It keeps track of all the rooms available and the occupants therin. The created rooms can either be offices which hold a maximum of 6 people or livingspaces which hold only 4 people. The people added are either fellows or staff and are placed in rooms automatically after addition. It allows for the:
* Creation of rooms
* Addition of people
* Reallocation of people from one room to the other
* Printing of the current allocations
* Printing of occupants of a particular room
* Saving the data to a database and retrieving it.

### Getting started
Clone this repo from Github to your local machine:
```
git clone https://github.com/andela-gochieng/checkpoint-1
```
cd into the checkpoint-1 folder
```
cd checkpoint-1
```
Create a virtual environment

Install the dependencies
```
pip install -r requirements.txt
```
Run the program in interactive mode
```
python app.py -i
```
### Usage
```
1. create_room <room_type> <room_name>..
```
Allows for the creation of one or multiple rooms of the same type. The room type is limited to either office or livingspace.
Example:
```
create_room livingspace Yellow Orange red
```
```
2. add_person <firstname> <surname> <designation> [<wants_accommodation>]
```
Adds people to the system one at a time who are then automatically allocated office, and livingspaces if need be. The designation is restricted to either fellow or staff. The wants_accomodation field is optional and only fellows are eligible to fill this field.
Examples:
```
add_person Sophie Wahiga fellow Y
add_person Darcy Rasanga staff
```
```
3. print_unallocated [filename]
```
Displays the names of the people who have not been placed into rooms yet. If the optional field filename is specified, the information is printed on the desired file.
Examples:
```
print_unallocated
print_unallocated sample.txt
```
```
4. print_allocations [filename] 
```
Displays the current allocations on the screen. These are all the current rooms and their corresponding occupants. The filename field is optional and if given, the allocations are printed to the specified file.
Examples:
```
print_allocations
print_allocations sample.txt
```
```
5. reallocate <person_identifier> <room_name>
```
Moves a person from one room to another. Requires the person_identifier(which is displayed when print_allocations is run) and the new room name. This can also be used to allocated space to a person who was previously unallocated.
Example:
```
reallocate ST01 Pink
```
```
6. save_state [--db=sqlite_database]
```
Stores the data to a database for retrieval when the app is next launched. The db field is optional and if not given the data ia saved to a default database file named latest_working.db
Example:
```
save_state 
save_state --db sample.db
```
```
7. load_state <load_file>
```
Retrieves the stored data from the database. The load_file specifies the database file from which to retrieve the data.
Example:
```
load_state sample.db
```
### Tests
To run the tests without coverage details
```
nosetests
```
To run the tests with coverage details
```
nosetests --with-coverage
```
