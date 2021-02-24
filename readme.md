### Casting Agency Project
This is the capstone project for Full-Stack Udacity Nanodegree.The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. There are three roles in the Casting Agency and each role has different permissions.
#### Roles:
	Casting Assistant
		Can view actors and movies
	Casting Director
		All permissions a Casting Assistant has and…
		Add or delete an actor from the database
		Modify actors or movies
	Executive Producer
		All permissions a Casting Director has and…
		Add or delete a movie from the database
		
Heroku link: https://git.heroku.com/casting-agency-undf.git
#### Endpoints
GET '/movies'
	returns all the movies in the database, and a success value.
example:
curl  -H 'Accept: application/json' -H "Authorization: Bearer token" http://127.0.0.1:5000/movies
 output:

{"movies":[{"id":3,"releaseDate":"Wed, 11 Nov 2020 20:16:47 GMT","title":"Purple Panther"},{"id":4,"releaseDate":"Thu, 01 Jan 2009 00:00:00 GMT","title":"Twilight"},{"id":6,"releaseDate":"Fri, 01 Jan 9999 00:00:00 GMT","title":"Movie2"},{"id":7,"releaseDate":"Fri, 01 Jan 9999 00:00:00 GMT","title":"Movie3"},{"id":8,"releaseDate":"Fri, 01 Jan 9999 00:00:00 GMT","title":"Movie4"},{"id":9,"releaseDate":"Thu, 01 Jan 2009 00:00:00 GMT","title":"Twilight"},{"id":10,"releaseDate":"Thu, 01 Jan 2009 00:00:00 GMT","title":"Twilight"}],"success":true}

GET '/actors'
	returns all the actors in the database, and a success value.
example:
curl  -H 'Accept: application/json' -H "Authorization: Bearer token" http://127.0.0.1:5000/actors
 output:
 
 {"actors":[{"age":30,"gender":"female","id":3,"name":"Beyonce"},{"age":20,"gender":"male","id":4,"name":"John"},{"age":16,"gender":male,"id":6,"name":"Zack"},{"age":20,"gender":"male","id":8,"name":"Joe"},{"age":20,"gender":"male","id":9,"name":"Jack"}],"success":true}
 
 DELETE '/movies/move_id'
 	deletes the movie with the specified id, returns a success value which equals true when deletion succeeds.
 	
 example:
 
 curl -X DELETE -H 'Accept: application/json' -H "Authorization: Bearer token" http://127.0.0.1:5000/movies/5

 output:
 { "success": true }
 
 DELETE '/actors/actor_id'
 	deletes the actor with the specified id, returns a success value which equals true when deletion succeeds.
 	
 example:
 
 curl -X DELETE -H 'Accept: application/json' -H "Authorization: Bearer token" http://127.0.0.1:5000/actors/5

 output:
 { "success": true }
 
 POST '/movies'
 	Creates a new movie in the database. Returns success value and the ID of the newly created movie.
 example:
 	curl -d '{"title":"Purple Panther","releaseDate":"2020-11-11 20:16:47.987959"}' -H "Content-Type: application/json" -H 'Accept: application/json' -H "Authorization: Bearer token" -X POST http://127.0.0.1:5000/movies
 	
 output:
 	{"created":1,"success":true}
POST '/actors'
	Creates a new actor in the database. Returns success value and the ID of the newly created actor.
example:

curl -d '{"name":"Suzan","gender":"female", "age" : "21" }' -H "Content-Type: application/json" -H 'Accept: application/json' -H "Authorization: Bearer token" -X POST http://127.0.0.1:5000/actors

Output:

{"created":1,"success":true}

PATCH '/movies/movie_id'
     endpoin to update a specific movie's title. Returns success value and updated movie id,
example:
 	curl -d '{"title":"Purple Panther" }' -H "Content-Type: application/json" -H 'Accept: application/json' -H "Authorization: Bearer token" -X POST http://127.0.0.1:5000/movies/1
 	
 output:
 	{"updated":1,"success":true}
 	
 	
PATCH '/actors/actor_id'
     endpoin to update a specific actor's name. Returns success value and updated actor id,
example:
 	curl -d '{"name":"New Name" }' -H "Content-Type: application/json" -H 'Accept: application/json' -H "Authorization: Bearer token" -X POST http://127.0.0.1:5000/actors/1
 	
 output:
 	{"updated":1,"success":true}


