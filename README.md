# LabMap

## What is it?

LabMap is a web application that shows current timetable and computer usage in MIM UW laboratories. It allows students to find a perfect spot for individual studying in between classes or an active machine to use as a remote host when working from home.

![](https://i.imgur.com/N7PRCbf.png)

## API interface

### Timetable

#### URL structure: 
`students.mimuw.edu.pl/~tm385898/labmap/api/timetable/{room_number}`
#### Example:
`students.mimuw.edu.pl/~tm385898/labmap/api/timetable/2041`

```javascript
{
  "monday": [
    {
      
      "start_time": "8:30",
      "end_time": "10:00",
      "course_type": "LAB",
      "group": "gr.1",
      "course_name": "Ciekawe zajęcia informatyczne",
      "teachers": "Jan Przykładowy"
    },
    ...
  ],
  ...
}
```


### Computers

#### URL structure: 
`students.mimuw.edu.pl/~tm385898/labmap/api/computers/{room_number}`
#### Example:
`students.mimuw.edu.pl/~tm385898/labmap/api/computers/3045`

```javascript
[
  {
    "id": "violet00",
    "room": 3045,
    "state": "linux",
    "user": null
  },
  ...
]
```
