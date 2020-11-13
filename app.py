import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,PATCH,DELETE,OPTIONS')
        return response
    
    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        try:
            all_movies=Movie.query.order_by(Movie.id).all()
            movies = []
            for movie in all_movies:
                if movie.title == None:
                    abort(404)
                movies.append( movie.format() )
                print(movie)
           

            return jsonify({
            'success':True,
            'movies': movies
            })
        except:
            abort(400)


    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        try:
            print("YES")
            all_actors= Actor.query.order_by(Actor.id).all()
            actors = []
            for actor in all_actors:
                if actor.name == None:
                    abort(404)
                actors.append( actor.format() )
                print(actor)
           
            return jsonify({
            'success':True,
            'actors': actors
            })
        except:
            abort(400)
    
    @app.route('/movies/<int:movie_id>' , methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        print("YES1")
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie == None:
                print("YES movie is none", movie.title)
                abort(404)
            movie.delete()
            
            
            return jsonify({
                'success':True
               
                })
        except:
            abort(422)
            
    
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        try:
            print("YES")
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if actor == None:
                print("YES actor is none", actor.name)
                abort(404)
            actor.delete()
            
            
            return jsonify({
                'success':True
            
                })
        except:
            abort(422)
            
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(payload):
        try:
            body = request.get_json(force=True)
        except:
            abort(400)

        new_title = body.get('title', None)
        new_releaseDate = body.get('releaseDate', None)


        try:
            if new_title is None:
                abort(400)
            movie = Movie(title = new_title, releaseDate = new_releaseDate )
            movie.insert()
            

            return jsonify({
            'success': True,
            'created': movie.id
            })
        except:
            abort(422)
           
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(payload):
        print("HELLO")
        try:
            body = request.get_json(force=True)
        except:
            abort(400)

        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender',None)
        print("name is ",new_name)

        try:
            if new_name is None:
                abort(400)
            actor = Actor( name = new_name, age = new_age, gender = new_gender)
            actor.insert()
            

            return jsonify({
            'success': True,
            'created': actor.id
            })
        except:
            abort(422)
            
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, actor_id):
        print("HELLO")
        try:
            body = request.get_json(force=True)
        except:
            abort(400)
          
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        print(actor.id)
        if actor == None:
            abort(404)
        
        new_name = body.get('name', None)

        try:
            actor.name = new_name
            actor.update()
            

            return jsonify({
            'success': True,
            'updated': actor.id
            })
        except:
            abort(422)
    
            
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):
        print("HELLO")
        try:
            body = request.get_json(force=True)
        except:
            abort(400)
            
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie == None:
            abort(404)
        
        new_title = body.get('title', None)

        try:
            movie.title = new_title
            movie.update()
            

            return jsonify({
            'success': True,
            'updated': movie.id
            })
        except:
            abort(422)
            
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "Bad Request" }),400

    @app.errorhandler(403)
    def method_not_allowed(error):
        return jsonify({"success": False, "error": 405, "message": "Forbidden" }),403
        
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "error": 404, "message": "Not Found" }),404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"success": False, "error": 405, "message": "this method is not allowed" }),405
        
    

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({"success": False, "error": 422, "message": "unprocessable entity" }),422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"success": False, "error": 500, "message": "internal server error" }),500
    
    
    @app.errorhandler(AuthError)
    def authentification_failed(AuthError):
        return jsonify({
        "success": False,
        "error": AuthError.status_code,
        "message": AuthError.error['description']
                    }), AuthError.status_code
                    
    return app
    

 
APP = create_app()


        
        

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
